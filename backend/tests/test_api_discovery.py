"""
Tests for API Discovery endpoints.

Verifies:
- List APIs endpoint
- Get single API endpoint
- Search endpoint
- Statistics endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import create_app
from database.models import API
from datetime import datetime


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_api(db):
    """Create sample API in test database."""
    api = API(
        name="user-service",
        endpoint="http://localhost:8001/api/v1/users",
        method="GET",
        owner="platform-team",
        tech_stack="Python/FastAPI",
        status="active",
        risk_score=35.0,
        is_documented=True,
        created_at=datetime.utcnow(),
    )
    db.add(api)
    db.commit()
    db.refresh(api)
    return api


class TestAPIDiscovery:
    """Test API discovery endpoints."""
    
    def test_list_apis_empty(self, client):
        """
        Test listing APIs when none exist.
        
        Should return empty list with 200 OK.
        """
        response = client.get("/api/v1/apis")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total"] == 0
        assert data["data"] == []
    
    def test_list_apis_with_data(self, client, sample_api):
        """
        Test listing APIs with test data.
        
        Should return the sample API.
        """
        response = client.get("/api/v1/apis?limit=50&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total"] == 1
        assert len(data["data"]) == 1
        
        # Verify API details
        api = data["data"][0]
        assert api["name"] == "user-service"
        assert api["endpoint"] == "http://localhost:8001/api/v1/users"
        assert api["method"] == "GET"
        assert api["status"] == "active"
        assert api["risk_score"] == 35.0
    
    def test_list_apis_pagination(self, client):
        """
        Test pagination parameters.
        """
        # Default limit
        response = client.get("/api/v1/apis")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 50
        assert data["offset"] == 0
        
        # Custom limit
        response = client.get("/api/v1/apis?limit=100&offset=10")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 100
        assert data["offset"] == 10
    
    def test_get_api_by_id(self, client, sample_api):
        """
        Test getting single API by ID.
        """
        response = client.get(f"/api/v1/apis/{sample_api.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == sample_api.id
        assert data["data"]["name"] == "user-service"
    
    def test_get_api_not_found(self, client):
        """
        Test getting non-existent API.
        
        Should return 404.
        """
        response = client.get("/api/v1/apis/99999")
        assert response.status_code == 404
    
    def test_search_apis(self, client, sample_api):
        """
        Test searching APIs.
        """
        # Search by name
        response = client.get("/api/v1/apis/search?q=user-service")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["total"] == 1
        assert data["query"] == "user-service"
    
    def test_search_no_results(self, client):
        """
        Test search with no matches.
        """
        response = client.get("/api/v1/apis/search?q=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["data"] == []
    
    def test_get_statistics(self, client, sample_api):
        """
        Test API statistics endpoint.
        """
        response = client.get("/api/v1/apis/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        stats = data["data"]
        assert "total_apis" in stats
        assert "by_status" in stats
        assert "documented" in stats
        assert "undocumented" in stats
        
        # Verify counts
        assert stats["total_apis"] == 1
        assert stats["by_status"]["active"] == 1
        assert stats["documented"] == 1
        assert stats["undocumented"] == 0


class TestAPIModels:
    """Test API data model."""
    
    def test_api_creation(self, db):
        """Test creating an API record."""
        api = API(
            name="test-api",
            endpoint="http://localhost:8000/api",
            method="POST",
            owner="test-team",
            tech_stack="Node.js",
            status="active",
        )
        db.add(api)
        db.commit()
        
        # Verify
        retrieved = db.query(API).filter(API.name == "test-api").first()
        assert retrieved is not None
        assert retrieved.endpoint == "http://localhost:8000/api"
        assert retrieved.method == "POST"
    
    def test_api_status_values(self, db):
        """Test API status classification."""
        statuses = ["active", "deprecated", "orphaned", "zombie"]
        
        for i, status in enumerate(statuses):
            api = API(
                name=f"api-{status}",
                endpoint=f"http://localhost/{i}",
                status=status,
            )
            db.add(api)
        
        db.commit()
        
        # Verify each status
        for status in statuses:
            api = db.query(API).filter(API.status == status).first()
            assert api.status == status
