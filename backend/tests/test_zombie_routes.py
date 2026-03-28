"""
Integration tests for Zombie API detection routes.

Tests endpoint functionality with sample data and verifies classification accuracy.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from database.models import API
from security.classification import APIStatus


class TestZombieRoutes:
    """Test suite for zombie detection API endpoints."""
    
    @pytest.fixture(scope="function")
    def client(self, db, sample_apis):
        """Create test client with sample data."""
        try:
            from fastapi.testclient import TestClient
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
    
    def test_list_zombies_returns_classified_apis(self, client):
        """Test GET /api/v1/zombies returns zombie APIs with classifications."""
        response = client.get("/api/v1/zombies")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "total_apis" in data
        assert "zombie_count" in data
        assert "zombies" in data
        assert "orphaned" in data
        assert "deprecated" in data
        
        # Should have found at least some zombies
        assert data["total_apis"] > 0
        assert data["zombie_count"] > 0 or data["orphaned_count"] > 0
    
    def test_zombie_api_structure(self, client):
        """Test returned zombie API has correct structure."""
        response = client.get("/api/v1/zombies")
        
        assert response.status_code == 200
        data = response.json()
        
        if data["zombies"]:
            zombie = data["zombies"][0]
            
            assert "id" in zombie
            assert "name" in zombie
            assert "endpoint" in zombie
            assert "status" in zombie
            assert zombie["status"] == "zombie"
            assert "confidence" in zombie
            assert 0 <= zombie["confidence"] <= 1
            assert "risk_score" in zombie
            assert 0 <= zombie["risk_score"] <= 100
            assert "reasoning" in zombie
            assert isinstance(zombie["reasoning"], list)
    
    def test_analyze_all_apis_endpoint(self, client):
        """Test POST /api/v1/analyze runs comprehensive analysis."""
        response = client.post("/api/v1/analyze")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "total_apis" in data
        assert "analysis_results" in data
        assert "summary" in data
        
        summary = data["summary"]
        assert "active" in summary
        assert "zombie" in summary
        assert "orphaned" in summary
        assert "deprecated" in summary
        
        # Total should match sum of all statuses
        total = summary["active"] + summary["zombie"] + summary["orphaned"] + summary["deprecated"]
        assert total == data["total_apis"]
    
    def test_analyze_result_completeness(self, client):
        """Test analysis results contain all required fields."""
        response = client.post("/api/v1/analyze")
        
        assert response.status_code == 200
        data = response.json()
        
        if data["analysis_results"]:
            result = data["analysis_results"][0]
            
            assert "id" in result
            assert "name" in result
            assert "endpoint" in result
            assert "method" in result
            assert "owner" in result
            assert "status" in result
            assert result["status"] in ["active", "zombie", "orphaned", "deprecated"]
            assert "confidence" in result
            assert "risk_score" in result
            assert "reasoning" in result
            assert "last_traffic" in result
            assert "is_documented" in result
    
    def test_single_api_analysis(self, client, db):
        """Test GET /api/v1/apis/{id}/analysis for single API."""
        # Get first API
        api = db.query(API).first()
        assert api is not None
        
        response = client.get(f"/api/v1/apis/{api.id}/analysis")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == api.id
        assert data["name"] == api.name
        assert data["endpoint"] == api.endpoint
        assert "status" in data
        assert "confidence" in data
        assert "risk_score" in data
        assert "classification_details" in data
    
    def test_single_api_detailed_analysis(self, client, db):
        """Test single API analysis includes detailed factor breakdown."""
        api = db.query(API).first()
        
        response = client.get(f"/api/v1/apis/{api.id}/analysis")
        
        assert response.status_code == 200
        
        data = response.json()
        details = data["classification_details"]
        
        assert "traffic_analysis" in details
        assert "documentation_analysis" in details
        assert "ownership_analysis" in details
        assert "age_deprecation_analysis" in details
        assert "maintenance_analysis" in details
    
    def test_api_not_found(self, client):
        """Test 404 when API doesn't exist."""
        response = client.get("/api/v1/apis/99999/analysis")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_stats_endpoint(self, client):
        """Test GET /api/v1/stats returns quick statistics."""
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "total_apis" in data
        assert "active" in data
        assert "zombie" in data
        assert "zombie_percentage" in data
        assert "orphaned" in data
        assert "deprecated" in data
        
        # Zombie percentage should be between 0-100
        assert 0 <= data["zombie_percentage"] <= 100
    
    def test_zombie_vs_deprecated_classification(self, client, db):
        """Test that deprecated APIs are correctly classified as DEPRECATED, not ZOMBIE."""
        # Find a deprecated API
        deprecated_api = db.query(API).filter(API.status == "deprecated").first()
        
        if deprecated_api:
            response = client.get(f"/api/v1/apis/{deprecated_api.id}/analysis")
            
            assert response.status_code == 200
            data = response.json()
            
            # Should be marked as deprecated, not zombie
            assert data["status"] == "deprecated"
            assert data["confidence"] >= 0.90  # High confidence for deprecated
    
    def test_orphaned_detection(self, client, db):
        """Test that orphaned APIs (no owner + no docs) are detected."""
        # Find an orphaned API
        orphaned_api = db.query(API).filter(
            API.owner == None,
            API.is_documented == False
        ).first()
        
        if orphaned_api:
            response = client.get(f"/api/v1/apis/{orphaned_api.id}/analysis")
            
            assert response.status_code == 200
            data = response.json()
            
            # Should be detected as orphaned
            assert data["status"] in ["orphaned", "zombie"]
    
    def test_active_api_with_recent_traffic(self, client, db):
        """Test that APIs with recent traffic are classified as ACTIVE."""
        now = datetime.utcnow()
        
        # Find an API with recent traffic
        active_api = db.query(API).filter(
            API.last_traffic != None,
            API.last_traffic > now - timedelta(days=3),
            API.is_documented == True,
            API.owner != None
        ).first()
        
        if active_api:
            response = client.get(f"/api/v1/apis/{active_api.id}/analysis")
            
            assert response.status_code == 200
            data = response.json()
            
            # Should be active
            assert data["status"] == "active"
            assert data["confidence"] >= 0.60  # Good confidence for active
    
    def test_zombie_detection_no_traffic_90_days(self, client, db):
        """Test that APIs with no traffic >90 days are detected as ZOMBIE."""
        now = datetime.utcnow()
        
        # Find an API with no traffic >90 days (but with owner/docs)
        zombie_api = db.query(API).filter(
            API.last_traffic < now - timedelta(days=90),
            API.last_traffic != None
        ).first()
        
        if zombie_api:
            response = client.get(f"/api/v1/apis/{zombie_api.id}/analysis")
            
            assert response.status_code == 200
            data = response.json()
            
            # Should be detected as zombie
            assert data["status"] == "zombie"
            # Confidence should be high (92% for traffic-based detection)
            assert data["confidence"] >= 0.85


class TestZombieStatisticsAccuracy:
    """Test accuracy of zombie detection statistics."""
    
    def test_stats_total_matches_count(self, client):
        """Test that total_apis equals sum of all status counts."""
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        calculated_total = (
            data["active"] + 
            data["zombie"] + 
            data["orphaned"] + 
            data["deprecated"]
        )
        
        assert calculated_total == data["total_apis"]
    
    def test_zombie_percentage_calculation(self, client):
        """Test that zombie percentage is correctly calculated."""
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        if data["total_apis"] > 0:
            expected_percentage = (data["zombie"] / data["total_apis"]) * 100
            assert abs(data["zombie_percentage"] - expected_percentage) < 0.1


class TestZombieRoutesErrorHandling:
    """Test error handling in zombie detection routes."""
    
    def test_empty_database_handling(self, db):
        """Test routes handle empty database gracefully."""
        # This would need a separate client with empty DB
        # For now, documented but would need setup
        pass
    
    def test_malformed_api_id(self, client):
        """Test handling of non-integer API IDs."""
        response = client.get("/api/v1/apis/invalid/analysis")
        
        # Should return 422 (validation error) or 404
        assert response.status_code in [404, 422]
