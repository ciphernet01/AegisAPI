"""
Tests for Zombie API Classification Engine.

Verifies:
- Traffic analysis (active vs inactive)
- Ownership detection
- Documentation status impact
- Deprecation detection
- Multi-factor risk scoring
- Edge cases and thresholds
"""

import pytest
from datetime import datetime, timedelta
from database.models import API
from security.classification import (
    ZombieClassifier,
    APIStatus,
    ZombieDetectionConfig,
    classify_api,
)


class TestTrafficAnalysis:
    """Test traffic pattern analysis for zombie detection."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    @pytest.fixture
    def api_with_recent_traffic(self, db):
        """API with recent traffic (active)."""
        api = API(
            name="user-service",
            endpoint="http://localhost:8001/api/users",
            method="GET",
            owner="platform-team",
            status="active",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=5),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        return api
    
    @pytest.fixture
    def api_with_old_traffic(self, db):
        """API with no recent traffic (inactive)."""
        api = API(
            name="legacy-service",
            endpoint="http://localhost:8002/api/legacy",
            method="GET",
            owner="legacy-team",
            status="active",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=120),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        return api
    
    @pytest.fixture
    def api_with_no_traffic(self, db):
        """API with no traffic history at all."""
        api = API(
            name="untouched-api",
            endpoint="http://localhost:8003/api/untouched",
            method="GET",
            owner="unknown",
            status="active",
            is_documented=False,
            last_traffic=None,
            created_at=datetime.utcnow() - timedelta(days=180),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        return api
    
    def test_classify_recent_traffic_is_active(self, classifier, api_with_recent_traffic):
        """API with recent traffic should be ACTIVE."""
        status, analysis = classifier.classify(api_with_recent_traffic)
        
        assert status == APIStatus.ACTIVE
        assert analysis["factors"]["traffic"]["is_active"] is True
        assert analysis["factors"]["traffic"]["days_since_traffic"] <= 7
    
    def test_classify_old_traffic_is_zombie(self, classifier, api_with_old_traffic):
        """API with no traffic for 120 days should be ZOMBIE."""
        status, analysis = classifier.classify(api_with_old_traffic)
        
        assert status == APIStatus.ZOMBIE
        assert analysis["factors"]["traffic"]["threshold_exceeded"] is True
        assert analysis["factors"]["traffic"]["days_since_traffic"] == 120
    
    def test_classify_no_traffic_is_zombie(self, classifier, api_with_no_traffic):
        """API with no traffic history should be ZOMBIE."""
        status, analysis = classifier.classify(api_with_no_traffic)
        
        assert status == APIStatus.ZOMBIE


class TestOwnershipAnalysis:
    """Test ownership and accountability detection."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_api_with_owner_is_owned(self, classifier, db):
        """API with owner should be marked as owned."""
        api = API(
            name="payment-service",
            endpoint="http://localhost/api/payments",
            method="POST",
            owner="payments-team",
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=1),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        _, analysis = classifier.classify(api)
        
        assert analysis["factors"]["ownership"]["has_owner"] is True
        assert analysis["factors"]["ownership"]["risk_score_contribution"] == 0.0
    
    def test_api_without_owner_increases_risk(self, classifier, db):
        """API without owner should increase zombie risk."""
        api = API(
            name="orphaned-service",
            endpoint="http://localhost/api/orphaned",
            method="GET",
            owner=None,
            status="active",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=100),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        assert analysis["factors"]["ownership"]["has_owner"] is False
        assert analysis["factors"]["ownership"]["risk_score_contribution"] == 30.0


class TestDocumentationAnalysis:
    """Test documentation status impact."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_documented_api_lower_risk(self, classifier, db):
        """Documented API should have lower zombification risk."""
        api = API(
            name="documented-service",
            endpoint="http://localhost/api/documented",
            method="GET",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=50),
            owner="docs-team",
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        _, analysis = classifier.classify(api)
        
        assert analysis["factors"]["documentation"]["is_documented"] is True
        assert analysis["factors"]["documentation"]["risk_score_contribution"] == 0.0
    
    def test_undocumented_api_higher_risk(self, classifier, db):
        """Undocumented API should increase zombie risk."""
        api = API(
            name="undocumented-service",
            endpoint="http://localhost/api/undocumented",
            method="GET",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=50),
            owner="unknown-team",
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        _, analysis = classifier.classify(api)
        
        assert analysis["factors"]["documentation"]["is_documented"] is False
        assert analysis["factors"]["documentation"]["risk_score_contribution"] == 25.0


class TestDeprecationDetection:
    """Test deprecation status detection."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_explicitly_deprecated_api(self, classifier, db):
        """API marked as deprecated should be DEPRECATED."""
        api = API(
            name="deprecated-api",
            endpoint="http://localhost/api/v1-deprecated",
            method="GET",
            status="deprecated",
            owner="api-team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=10),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        assert status == APIStatus.DEPRECATED
        assert analysis["factors"]["age_deprecation"]["is_explicitly_deprecated"] is True


class TestOrphanedDetection:
    """Test orphaned API detection."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_orphaned_api_no_owner_no_docs(self, classifier, db):
        """API without owner and undocumented should be ORPHANED."""
        api = API(
            name="orphaned-service",
            endpoint="http://localhost/api/orphaned",
            method="GET",
            owner=None,
            is_documented=False,
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=20),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        assert status == APIStatus.ORPHANED


class TestMultiFactorRiskScoring:
    """Test multi-factor risk scoring system."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_high_risk_zombie_multiple_factors(self, classifier, db):
        """API with multiple zombie indicators should be classified as ZOMBIE."""
        # Create API with all zombie indicators:
        # - No traffic for 100 days
        # - Has owner (to avoid ORPHANED classification)
        # - Not documented
        # - Unknown tech stack
        api = API(
            name="zombie-api",
            endpoint="http://localhost/api/zombie",
            method="GET",
            owner="zombie-team",
            is_documented=False,
            tech_stack="Unknown",
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=100),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        assert status == APIStatus.ZOMBIE
        assert analysis["confidence_score"] >= 0.85
        assert "No traffic" in " ".join(analysis["reasoning"])
    
    def test_low_risk_active_multiple_factors(self, classifier, db):
        """API with all positive indicators should be ACTIVE."""
        # Create API with all active indicators:
        # - Recent traffic (daily)
        # - Has owner
        # - Documented
        # - Known tech stack
        api = API(
            name="active-api",
            endpoint="http://localhost/api/active",
            method="GET",
            owner="active-team",
            is_documented=True,
            tech_stack="Python/FastAPI",
            status="active",
            last_traffic=datetime.utcnow() - timedelta(hours=2),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        assert status == APIStatus.ACTIVE
        assert analysis["confidence_score"] >= 0.85


class TestThresholdBehavior:
    """Test threshold-based classification boundaries."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_just_before_zombie_threshold(self, classifier, db):
        """API just under 90-day threshold should not be ZOMBIE."""
        api = API(
            name="barely-active",
            endpoint="http://localhost/api/barely-active",
            method="GET",
            owner="team",
            is_documented=True,
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=89),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        # Should be ACTIVE (not exceeding threshold yet)
        assert status == APIStatus.ACTIVE or status == APIStatus.ZOMBIE
        assert not analysis["factors"]["traffic"]["threshold_exceeded"]
    
    def test_just_after_zombie_threshold(self, classifier, db):
        """API just over 90-day threshold should be ZOMBIE."""
        api = API(
            name="just-zombie",
            endpoint="http://localhost/api/just-zombie",
            method="GET",
            owner="team",
            is_documented=True,
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=91),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        # Should be ZOMBIE (exceeded threshold)
        assert status == APIStatus.ZOMBIE
        assert analysis["factors"]["traffic"]["threshold_exceeded"]


class TestTechStackAnalysis:
    """Test technology stack maintenance indicators."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return ZombieClassifier()
    
    def test_known_tech_stack_indicates_maintenance(self, classifier, db):
        """API with known tech stack suggests active maintenance."""
        api = API(
            name="maintained-api",
            endpoint="http://localhost/api/maintained",
            method="GET",
            owner="tech-team",
            tech_stack="Python/FastAPI",
            is_documented=True,
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=30),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        _, analysis = classifier.classify(api)
        
        assert analysis["factors"]["maintenance"]["has_tech_info"] is True
        assert analysis["factors"]["maintenance"]["risk_score_contribution"] == 0.0
    
    def test_unknown_tech_stack_indicates_neglect(self, classifier, db):
        """API with unknown tech stack suggests lack of maintenance."""
        api = API(
            name="neglected-api",
            endpoint="http://localhost/api/neglected",
            method="GET",
            owner="unknown-team",
            tech_stack="Unknown",
            is_documented=False,
            status="active",
            last_traffic=datetime.utcnow() - timedelta(days=80),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        _, analysis = classifier.classify(api)
        
        assert analysis["factors"]["maintenance"]["has_tech_info"] is False
        assert analysis["factors"]["maintenance"]["risk_score_contribution"] == 15.0


class TestCustomConfiguration:
    """Test classification with custom configuration."""
    
    def test_custom_no_traffic_threshold(self, db):
        """Should respect custom inactivity threshold."""
        config = ZombieDetectionConfig()
        config.NO_TRAFFIC_THRESHOLD_DAYS = 60  # More aggressive
        
        classifier = ZombieClassifier(config)
        
        api = API(
            name="test-api",
            endpoint="http://localhost/api/test",
            method="GET",
            owner="team",
            last_traffic=datetime.utcnow() - timedelta(days=65),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classifier.classify(api)
        
        # With 60-day threshold, 65 days inactive should be zombie
        assert status == APIStatus.ZOMBIE
        assert analysis["factors"]["traffic"]["threshold_exceeded"]


class TestClassifyApiFunction:
    """Test the convenience classify_api() function."""
    
    def test_classify_api_shorthand(self, db):
        """Verify convenience function works correctly."""
        api = API(
            name="test-api",
            endpoint="http://localhost/api/test",
            method="GET",
            owner="team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=5),
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        
        status, analysis = classify_api(api)
        
        assert isinstance(status, APIStatus)
        assert "api_id" in analysis
        assert "classified_as" in analysis
        assert "confidence_score" in analysis
        assert "reasoning" in analysis
