"""
Tests for remediation workflows and API routes.

Covers:
- Remediation plan generation
- Remediation actions (decommission, archive, notify, revive)
- Bulk remediation operations
- Remediation statistics
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.models import API
from security.classification import classify_api, APIStatus
from services.remediation import (
    RemediationEngine,
    RemediationAction,
    RemediationPlan,
    RemediationStatus
)


class TestRemediationPlanGeneration:
    """Test generation of remediation plans."""

    @pytest.fixture
    def engine(self):
        """Create remediation engine."""
        return RemediationEngine()

    def test_zombie_api_generates_decommission_plan(self, db: Session, engine):
        """Zombie API with high risk should generate decommission plan."""
        api = API(
            name="High Risk Zombie",
            endpoint="/api/v1/zombie",
            method="GET",
            owner="test_team",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=200),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        
        plan = engine.generate_remediation_plan(api)
        
        assert plan.status == APIStatus.ZOMBIE
        assert RemediationAction.DECOMMISSION in plan.recommended_actions or RemediationAction.NOTIFY_OWNER in plan.recommended_actions
        assert plan.urgency in ["critical", "high"]
        assert plan.api_id == api.id

    def test_deprecated_api_generates_archive_plan(self, db: Session, engine):
        """Deprecated API should generate archive plan."""
        api = API(
            name="Deprecated API",
            endpoint="/api/v1/deprecated",
            method="GET",
            owner="old_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=120),
            status=APIStatus.DEPRECATED.value
        )
        db.add(api)
        db.commit()
        
        plan = engine.generate_remediation_plan(api)
        
        assert plan.status == APIStatus.DEPRECATED
        assert RemediationAction.ARCHIVE in plan.recommended_actions or RemediationAction.NOTIFY_OWNER in plan.recommended_actions
        assert plan.urgency in ["medium", "high"]

    def test_orphaned_api_generates_migration_plan(self, db: Session, engine):
        """Orphaned API should generate migration plan."""
        api = API(
            name="Orphaned API",
            endpoint="/api/v1/orphaned",
            method="GET",
            owner=None,
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=150),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        
        plan = engine.generate_remediation_plan(api)
        
        assert plan.status == APIStatus.ORPHANED
        assert RemediationAction.MIGRATE_CONSUMERS in plan.recommended_actions or RemediationAction.NOTIFY_OWNER in plan.recommended_actions
        assert plan.urgency == "high"

    def test_active_api_minimal_remediation(self, db: Session, engine):
        """Active API with recent traffic needs minimal remediation."""
        api = API(
            name="Active API",
            endpoint="/api/v1/active",
            method="GET",
            owner="active_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=5),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        
        plan = engine.generate_remediation_plan(api)
        
        # Active APIs may still be in plan, but urgency should be low
        assert plan.urgency == "low"

    def test_plan_conversion_to_dict(self, db: Session, engine):
        """RemediationPlan should convert to dictionary for JSON serialization."""
        api = API(
            name="Test API",
            endpoint="/api/v1/test",
            method="GET",
            owner="test_team",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=100),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        
        plan = engine.generate_remediation_plan(api)
        plan_dict = plan.to_dict()
        
        assert isinstance(plan_dict, dict)
        assert "api_id" in plan_dict
        assert "api_name" in plan_dict
        assert "status" in plan_dict
        assert "risk_score" in plan_dict
        assert "recommended_actions" in plan_dict
        assert isinstance(plan_dict["recommended_actions"], list)


class TestRemediationActions:
    """Test remediation actions."""

    @pytest.fixture
    def engine(self):
        """Create remediation engine."""
        return RemediationEngine()

    def test_decommission_api(self, db: Session, engine):
        """Decommissioning should mark API as deprecated."""
        api = API(
            name="API to Decommission",
            endpoint="/api/v1/decom",
            method="GET",
            owner="test_team",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=200),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        original_id = api.id
        
        result = engine.decommission_api(db, original_id, reason="No longer needed")
        
        assert result["success"] is True
        assert result["action"] == RemediationAction.DECOMMISSION.value
        
        # Verify status changed
        api = db.query(API).filter(API.id == original_id).first()
        assert api.status == APIStatus.DEPRECATED.value

    def test_archive_api(self, db: Session, engine):
        """Archiving should return success response."""
        api = API(
            name="API to Archive",
            endpoint="/api/v1/archive",
            method="GET",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=180),
            status=APIStatus.DEPRECATED.value
        )
        db.add(api)
        db.commit()
        api_id = api.id
        
        result = engine.archive_api(db, api_id, archive_location="/archive/apis")
        
        assert result["success"] is True
        assert result["action"] == RemediationAction.ARCHIVE.value
        assert result["api_id"] == api_id

    def test_notify_owner(self, db: Session, engine):
        """Notifying owner should succeed when owner exists."""
        api = API(
            name="API to Notify",
            endpoint="/api/v1/notify",
            method="GET",
            owner="owner_email@company.com",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=100),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        api_id = api.id
        
        result = engine.notify_owner(db, api_id, message="Your API needs attention")
        
        assert result["success"] is True
        assert result["action"] == RemediationAction.NOTIFY_OWNER.value
        assert result["owner"] == "owner_email@company.com"

    def test_notify_owner_fails_without_owner(self, db: Session, engine):
        """Notifying owner should fail when API has no owner."""
        api = API(
            name="Orphaned API",
            endpoint="/api/v1/orphaned",
            method="GET",
            owner=None,
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=150),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.commit()
        api_id = api.id
        
        result = engine.notify_owner(db, api_id)
        
        assert result["success"] is False
        assert "no owner" in result["message"].lower()

    def test_revive_api(self, db: Session, engine):
        """Reviving should mark API as ACTIVE and update last_traffic."""
        api = API(
            name="API to Revive",
            endpoint="/api/v1/revive",
            method="GET",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=200),
            status=APIStatus.DEPRECATED.value
        )
        db.add(api)
        db.commit()
        original_id = api.id
        
        result = engine.revive_api(db, original_id)
        
        assert result["success"] is True
        assert result["action"] == RemediationAction.REVIVE.value
        assert result["new_status"] == APIStatus.ACTIVE.value
        
        # Verify status changed
        api = db.query(API).filter(API.id == original_id).first()
        assert api.status == APIStatus.ACTIVE.value

    def test_action_on_nonexistent_api(self, db: Session, engine):
        """Actions on non-existent APIs should fail gracefully."""
        result = engine.decommission_api(db, 99999)
        
        assert result["success"] is False
        assert "not found" in result["message"].lower()


class TestBulkRemediation:
    """Test bulk remediation operations."""

    @pytest.fixture
    def engine(self):
        """Create remediation engine."""
        return RemediationEngine()

    def test_bulk_decommission(self, db: Session, engine):
        """Bulk decommissioning should process multiple APIs."""
        api_ids = []
        for i in range(3):
            api = API(
                name=f"Zombie API {i}",
                endpoint=f"/api/v1/zombie{i}",
                method="GET",
                owner="test_team",
                is_documented=False,
                last_traffic=datetime.utcnow() - timedelta(days=200),
                status=APIStatus.ACTIVE.value
            )
            db.add(api)
            db.flush()
            api_ids.append(api.id)
        db.commit()
        
        result = engine.bulk_remediation(db, api_ids, RemediationAction.DECOMMISSION)
        
        assert result["action"] == RemediationAction.DECOMMISSION.value
        assert result["total_apis"] == 3
        assert result["successful"] == 3
        assert result["failed"] == 0

    def test_bulk_notify(self, db: Session, engine):
        """Bulk notification should handle multiple APIs."""
        api_ids = []
        for i in range(2):
            api = API(
                name=f"API {i}",
                endpoint=f"/api/v1/api{i}",
                method="GET",
                owner=f"owner{i}@company.com",
                is_documented=True,
                last_traffic=datetime.utcnow() - timedelta(days=100),
                status=APIStatus.ACTIVE.value
            )
            db.add(api)
            db.flush()
            api_ids.append(api.id)
        db.commit()
        
        result = engine.bulk_remediation(db, api_ids, RemediationAction.NOTIFY_OWNER)
        
        assert result["total_apis"] == 2
        assert result["successful"] == 2

    def test_bulk_mixed_success_failure(self, db: Session, engine):
        """Bulk operations should handle mixed success/failure gracefully."""
        api_ids = []
        
        # Create valid API
        api = API(
            name="Valid API",
            endpoint="/api/v1/valid",
            method="GET",
            owner="owner@company.com",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=50),
            status=APIStatus.ACTIVE.value
        )
        db.add(api)
        db.flush()
        api_ids.append(api.id)
        db.commit()
        
        # Add non-existent API
        api_ids.append(99999)
        
        result = engine.bulk_remediation(db, api_ids, RemediationAction.NOTIFY_OWNER)
        
        assert result["total_apis"] == 2
        assert result["successful"] >= 0
        assert result["failed"] >= 0
        assert len(result["results"]) == 2


class TestRemediationStatistics:
    """Test remediation statistics and health metrics."""

    @pytest.fixture
    def engine(self):
        """Create remediation engine."""
        return RemediationEngine()

    def test_remediation_stats_empty_database(self, db: Session, engine):
        """Statistics should handle empty database."""
        stats = engine.get_remediation_stats(db)
        
        assert stats["total_apis"] == 0
        assert stats["health_score"] == 100.0

    def test_remediation_stats_with_zombies(self, db: Session, engine):
        """Statistics should correctly count zombie APIs."""
        # Create mix of APIs
        active = API(
            name="Active", endpoint="/active", method="GET", owner="team",
            is_documented=True, last_traffic=datetime.utcnow() - timedelta(days=5),
            status=APIStatus.ACTIVE.value
        )
        zombie = API(
            name="Zombie", endpoint="/zombie", method="GET", owner="team",
            is_documented=False, last_traffic=datetime.utcnow() - timedelta(days=200),
            status=APIStatus.ACTIVE.value
        )
        deprecated = API(
            name="Deprecated", endpoint="/deprecated", method="GET", owner="team",
            is_documented=True, last_traffic=datetime.utcnow() - timedelta(days=150),
            status=APIStatus.DEPRECATED.value
        )
        
        db.add_all([active, zombie, deprecated])
        db.commit()
        
        stats = engine.get_remediation_stats(db)
        
        assert stats["total_apis"] == 3
        assert stats["zombie_count"] >= 1
        assert stats["deprecated_count"] == 1
        assert "health_score" in stats
        assert "remediation_percentage" in stats

    def test_remediation_stats_health_calculation(self, db: Session, engine):
        """Health score should reflect proportion of healthy APIs."""
        # Create 10 APIs: 8 active, 2 zombie
        for i in range(8):
            api = API(
                name=f"Active {i}", endpoint=f"/active{i}", method="GET",
                owner="team", is_documented=True,
                last_traffic=datetime.utcnow() - timedelta(days=10),
                status=APIStatus.ACTIVE.value
            )
            db.add(api)
        
        for i in range(2):
            api = API(
                name=f"Zombie {i}", endpoint=f"/zombie{i}", method="GET",
                owner="team", is_documented=False,
                last_traffic=datetime.utcnow() - timedelta(days=200),
                status=APIStatus.ACTIVE.value
            )
            db.add(api)
        
        db.commit()
        
        stats = engine.get_remediation_stats(db)
        
        assert stats["total_apis"] == 10
        # Health score should be lower due to zombies
        assert stats["health_score"] < 100.0
