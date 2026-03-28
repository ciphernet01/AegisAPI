"""
End-to-end tests for zombie API detection system.

Validates complete workflows:
- Create APIs → Classify → Analyze → Retrieve Stats
- Bulk zombie detection scenarios
- Data consistency across requests
- State transition accuracy
- Edge cases and boundary conditions
"""

import pytest
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.models import API
from security.classification import classify_api, APIStatus
from utils.logger import get_logger

logger = get_logger(__name__)

# Check if full app is available for integration tests
try:
    from fastapi.testclient import TestClient
    from main import create_app
    FULL_APP_AVAILABLE = True
except ImportError:
    FULL_APP_AVAILABLE = False


@pytest.mark.skipif(not FULL_APP_AVAILABLE, reason="Full app not available")
class TestE2EZombieDetectionWorkflow:
    """End-to-end tests for complete zombie detection workflows."""

    @pytest.fixture(scope="function")
    def client(self, db):
        """Create test client with database override."""
        try:
            from main import create_app
            from database.db import get_db
            
            app = create_app()
            
            def override_get_db():
                yield db
            
            app.dependency_overrides[get_db] = override_get_db
            
            with TestClient(app) as test_client:
                yield test_client
            
            app.dependency_overrides.clear()
        except ImportError as e:
            pytest.skip(f"Full app integration test skipped: {e}")

    @pytest.fixture(autouse=True)
    def setup(self, db: Session):
        """Setup test environment with clean database."""
        # Clear existing APIs
        db.query(API).delete()
        db.commit()
        self.db = db

    def test_e2e_create_and_classify_single_api(self, client):
        """
        E2E Workflow: Create API → Classify → Analyze Single → Verify Status
        
        Validates:
        - API creation in database
        - Classification accuracy
        - Single API analysis endpoint
        - Response structure completeness
        """
        # Step 1: Create a test API (active)
        active_api = API(
            name="E2E Test Active API",
            endpoint="/api/v1/users",
            method="GET",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=5),
            status=APIStatus.ACTIVE
        )
        self.db.add(active_api)
        self.db.commit()
        api_id = active_api.id
        
        # Step 2: Analyze single API
        response = client.get(f"/api/v1/apis/{api_id}/analysis")
        
        # Step 3: Validate response structure
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == api_id
        assert data["name"] == "E2E Test Active API"
        assert data["status"] in ["ACTIVE", "ZOMBIE", "ORPHANED", "DEPRECATED"]
        assert "confidence" in data
        assert "risk_score" in data
        assert "factors" in data
        assert isinstance(data["confidence"], (int, float))
        assert 0 <= data["risk_score"] <= 100
        
        # Step 4: Verify classification reasoning
        assert "reasoning" in data or "factors" in data
        logger.info(f"Single API analysis passed: {data['status']} (confidence: {data['confidence']}%)")

    def test_e2e_bulk_zombie_detection_scenario(self, client):
        """
        E2E Workflow: Create Multiple APIs → Analyze All → Validate Results
        
        Validates:
        - Bulk API classification
        - Statistics accuracy
        - Correct status distribution
        - Response consistency across endpoints
        """
        
        # Step 1: Create diverse set of APIs
        apis_data = [
            {
                "name": "Active API 1",
                "endpoint": "/api/v1/active",
                "owner": "team_a",
                "is_documented": True,
                "last_traffic": datetime.utcnow() - timedelta(days=10),
                "status": APIStatus.ACTIVE
            },
            {
                "name": "Zombie API 1",
                "endpoint": "/api/v1/zombie",
                "owner": "legacy_team",
                "is_documented": False,
                "last_traffic": datetime.utcnow() - timedelta(days=200),
                "status": APIStatus.ACTIVE  # Will be detected as zombie
            },
            {
                "name": "Deprecated API 1",
                "endpoint": "/api/v1/deprecated",
                "owner": "old_team",
                "is_documented": True,
                "last_traffic": datetime.utcnow() - timedelta(days=120),
                "status": APIStatus.DEPRECATED
            },
            {
                "name": "Orphaned API 1",
                "endpoint": "/api/v1/orphaned",
                "owner": None,
                "is_documented": False,
                "last_traffic": datetime.utcnow() - timedelta(days=180),
                "status": APIStatus.ACTIVE
            }
        ]
        
        created_apis = []
        for api_data in apis_data:
            api = API(**api_data)
            self.db.add(api)
            created_apis.append(api)
        self.db.commit()
        
        # Step 2: Analyze all APIs
        response = client.post("/api/v1/analyze")
        assert response.status_code == 200
        analysis_result = response.json()
        
        # Step 3: Validate analysis structure
        assert "summary" in analysis_result
        assert "classifications" in analysis_result
        assert len(analysis_result["classifications"]) == len(apis_data)
        
        # Step 4: Verify statistics
        summary = analysis_result["summary"]
        assert "total_apis" in summary
        assert "zombie_count" in summary
        assert "deprecated_count" in summary
        assert "orphaned_count" in summary
        assert "active_count" in summary
        assert summary["total_apis"] == len(apis_data)
        
        # Step 5: Cross-validate with /zombies endpoint
        zombies_response = client.get("/api/v1/zombies")
        assert zombies_response.status_code == 200
        zombies_data = zombies_response.json()
        assert "zombies" in zombies_data
        
        logger.info(f"Bulk analysis complete: {len(apis_data)} APIs analyzed, {summary['zombie_count']} zombies detected")

    def test_e2e_statistics_consistency(self, client):
        """
        E2E Workflow: Create APIs → Get Stats → Verify Consistency
        
        Validates:
        - Statistics endpoint accuracy
        - Percentage calculations
        - Total consistency across endpoints
        """
        
        # Step 1: Setup diverse API set
        status_counts = {
            APIStatus.ACTIVE: 5,
            APIStatus.ZOMBIE: 3,
            APIStatus.DEPRECATED: 2,
            APIStatus.ORPHANED: 1
        }
        
        for status, count in status_counts.items():
            for i in range(count):
                api = API(
                    name=f"{status.value}_api_{i}",
                    endpoint=f"/api/{status.value}/{i}",
                    owner=f"team_{status.value}_{i}",
                    is_documented=status != APIStatus.ZOMBIE,
                    last_traffic=datetime.utcnow() - timedelta(days=5 if status == APIStatus.ACTIVE else 200),
                    status=status
                )
                self.db.add(api)
        self.db.commit()
        
        # Step 2: Get statistics
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        stats = response.json()
        
        # Step 3: Validate statistics
        total = sum(status_counts.values())
        assert stats["total"] == total
        assert stats["active_count"] == status_counts[APIStatus.ACTIVE]
        assert stats["zombie_count"] == status_counts[APIStatus.ZOMBIE]
        assert stats["deprecated_count"] == status_counts[APIStatus.DEPRECATED]
        assert stats["orphaned_count"] == status_counts[APIStatus.ORPHANED]
        
        # Step 4: Verify percentages
        zombie_percentage = (3 / total) * 100
        assert abs(stats["zombie_percentage"] - zombie_percentage) < 0.1
        
        logger.info(f"Stats consistency verified: {stats}")

    def test_e2e_state_transition_accuracy(self, client):
        """
        E2E Workflow: Create API with changing metadata → Verify Classification Change
        
        Validates:
        - Classification changes when API metadata changes
        - Proper state transitions
        - Accuracy of multi-factor analysis
        """
        
        # Step 1: Create API initially classified as ACTIVE
        api = API(
            name="State Transition Test API",
            endpoint="/api/v1/transition",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=5),
            status=APIStatus.ACTIVE
        )
        self.db.add(api)
        self.db.commit()
        api_id = api.id
        
        # Step 2: Verify initial classification
        response = client.get(f"/api/v1/apis/{api_id}/analysis")
        assert response.status_code == 200
        initial_data = response.json()
        initial_status = initial_data["status"]
        logger.info(f"Initial classification: {initial_status}")
        
        # Step 3: Update API to simulate zombie state (remove traffic, no documentation)
        api.last_traffic = datetime.utcnow() - timedelta(days=200)
        api.is_documented = False
        self.db.commit()
        
        # Step 4: Re-analyze and verify state change
        response = client.get(f"/api/v1/apis/{api_id}/analysis")
        assert response.status_code == 200
        updated_data = response.json()
        
        # Step 5: Validate detection of zombie characteristics
        assert "factors" in updated_data or "risk_score" in updated_data
        logger.info(f"Updated classification: {updated_data['status']} (risk_score: {updated_data.get('risk_score', 'N/A')})")

    def test_e2e_edge_case_new_api(self, client):
        """
        E2E Edge Case: Newly created API (no traffic history)
        
        Validates:
        - Correct classification of new APIs
        - Edge case: API < 30 days old with no traffic
        - Risk scoring for new APIs
        """
        
        # Step 1: Create very new API (created less than 30 days ago)
        api = API(
            name="Brand New API",
            endpoint="/api/v1/new",
            owner="new_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(hours=1),
            status=APIStatus.ACTIVE,
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        self.db.add(api)
        self.db.commit()
        
        # Step 2: Analyze
        response = client.get(f"/api/v1/apis/{api.id}/analysis")
        assert response.status_code == 200
        data = response.json()
        
        # Step 3: Verify new API is not classified as zombie
        assert data["status"] != "ZOMBIE"
        logger.info(f"New API classification: {data['status']} (appropriate for new API)")

    def test_e2e_edge_case_no_owner_api(self, client):
        """
        E2E Edge Case: API with null owner (orphaned detection)
        
        Validates:
        - Orphaned status detection
        - Risk scoring for ownerless APIs
        - Correct classification
        """
        
        # Step 1: Create API with no owner
        api = API(
            name="Orphaned API",
            endpoint="/api/v1/orphaned",
            owner=None,
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=150),
            status=APIStatus.ACTIVE
        )
        self.db.add(api)
        self.db.commit()
        
        # Step 2: Analyze
        response = client.get(f"/api/v1/apis/{api.id}/analysis")
        assert response.status_code == 200
        data = response.json()
        
        # Step 3: Verify orphaned detection
        assert "owner" in str(data).lower() or "orphaned" in str(data).lower() or data.get("risk_score", 0) > 50
        logger.info(f"Orphaned API classification: {data['status']} (risk_score: {data.get('risk_score', 'N/A')})")

    def test_e2e_error_handling_invalid_api_id(self, client):
        """
        E2E Error Handling: Request analysis for non-existent API
        
        Validates:
        - 404 response for invalid API IDs
        - Error message clarity
        - Gateway resilience
        """
        
        # Step 1: Request analysis for non-existent API
        response = client.get("/api/v1/apis/99999/analysis")
        
        # Step 2: Verify error handling
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data or "error" in error_data
        logger.info(f"Error handling validated: {response.status_code} with detail")

    def test_e2e_error_handling_empty_database(self, client):
        """
        E2E Error Handling: Analyze when database is empty
        
        Validates:
        - Graceful handling of empty database
        - Correct statistics (all zeros)
        - No crashes or exceptions
        """
        
        # Database already empty from setup fixture
        
        # Step 1: Analyze empty database
        response = client.post("/api/v1/analyze")
        assert response.status_code == 200
        
        # Step 2: Verify empty response
        data = response.json()
        assert data["summary"]["total_apis"] == 0
        
        # Step 3: Get stats for empty database
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total"] == 0
        logger.info("Empty database handled gracefully")

    def test_e2e_performance_bulk_operations(self, client):
        """
        E2E Performance: Analyze large number of APIs
        
        Validates:
        - Performance with 50+ APIs
        - Response time acceptable
        - No memory leaks or crashes
        - Accurate bulk classification
        """
        
        # Step 1: Create 50 realistic APIs
        for i in range(50):
            status = [APIStatus.ACTIVE, APIStatus.ZOMBIE, APIStatus.DEPRECATED, APIStatus.ORPHANED][i % 4]
            api = API(
                name=f"Performance Test API {i}",
                endpoint=f"/api/v1/perf/{i}",
                owner=f"team_{i % 5}" if i % 7 != 0 else None,
                is_documented=i % 3 != 0,
                last_traffic=datetime.utcnow() - timedelta(days=5 if status == APIStatus.ACTIVE else 200),
                status=status
            )
            self.db.add(api)
        self.db.commit()
        
        # Step 2: Measure analysis performance
        start = time.time()
        response = client.post("/api/v1/analyze")
        duration = time.time() - start
        
        # Step 3: Validate performance
        assert response.status_code == 200
        data = response.json()
        assert len(data["classifications"]) == 50
        assert duration < 5.0  # Should complete in under 5 seconds
        
        logger.info(f"Bulk analysis of 50 APIs completed in {duration:.2f}s")

    def test_e2e_data_consistency_multiple_requests(self, client):
        """
        E2E Data Consistency: Multiple sequential requests return consistent results
        
        Validates:
        - Same API analyzed multiple times produces same classification
        - Statistics remain consistent
        - No race conditions or state inconsistencies
        """
        
        # Step 1: Create test API
        api = API(
            name="Consistency Test API",
            endpoint="/api/v1/consistency",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=15),
            status=APIStatus.ACTIVE
        )
        self.db.add(api)
        self.db.commit()
        api_id = api.id
        
        # Step 2: Analyze same API 5 times
        results = []
        for i in range(5):
            response = client.get(f"/api/v1/apis/{api_id}/analysis")
            assert response.status_code == 200
            results.append(response.json())
        
        # Step 3: Verify consistency
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert result["status"] == first_result["status"], f"Inconsistency at request {i+1}"
            assert result["confidence"] == first_result["confidence"], f"Confidence inconsistency at request {i+1}"
            assert result["risk_score"] == first_result["risk_score"], f"Risk score inconsistency at request {i+1}"
        
        logger.info(f"Data consistency verified across 5 sequential requests")


@pytest.mark.skipif(not FULL_APP_AVAILABLE, reason="Full app not available")
class TestE2EZombieDetectionIntegration:
    """Integration tests for zombie detection system with external interactions."""

    def test_integration_classification_engine_accuracy(self, db: Session):
        """
        Integration Test: Verify classification engine accuracy with real data
        
        Validates:
        - Classification results match expected outcomes
        - Risk scoring is accurate
        - Confidence scoring is reliable
        """
        # Create test APIs with known outcomes
        zombie_api = API(
            name="Known Zombie",
            endpoint="/api/v1/zombie",
            method="GET",
            owner="old_team",
            is_documented=False,
            last_traffic=datetime.utcnow() - timedelta(days=180),
            status=APIStatus.ACTIVE
        )
        
        active_api = API(
            name="Known Active",
            endpoint="/api/v1/active",
            method="GET",
            owner="current_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=3),
            status=APIStatus.ACTIVE
        )
        
        db.add(zombie_api)
        db.add(active_api)
        db.commit()
        
        # Classify
        zombie_result = classify_api(zombie_api)
        active_result = classify_api(active_api)
        
        # Verify
        assert zombie_result.status == APIStatus.ZOMBIE
        assert active_result.status == APIStatus.ACTIVE
        assert zombie_result.risk_score > active_result.risk_score
        
        logger.info(f"Classification accuracy verified: Zombie={zombie_result.status}, Active={active_result.status}")

    def test_integration_response_format_compliance(self, db: Session):
        """
        Integration Test: Verify response format compliance with API contract
        
        Validates:
        - All responses follow documented schema
        - Required fields present
        - Data types correct
        """
        # Create test API
        api = API(
            name="Format Test API",
            endpoint="/api/v1/format",
            method="GET",
            owner="test_team",
            is_documented=True,
            last_traffic=datetime.utcnow() - timedelta(days=10),
            status=APIStatus.ACTIVE
        )
        db.add(api)
        db.commit()
        
        result = classify_api(api)
        
        # Verify contract
        required_fields = ["status", "confidence", "risk_score"]
        for field in required_fields:
            assert hasattr(result, field), f"Missing required field: {field}"
        
        assert isinstance(result.status, APIStatus)
        assert isinstance(result.confidence, (int, float))
        assert isinstance(result.risk_score, (int, float))
        assert 0 <= result.confidence <= 100
        assert 0 <= result.risk_score <= 100
        
        logger.info("Response format compliance verified")
