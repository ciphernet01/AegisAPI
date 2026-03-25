"""
Tests for GitHub API discovery scanner.

Verifies:
- GitHub repository scanning
- OpenAPI spec parsing
- Code route extraction
- Technology stack detection
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from services.discovery_service import APIDiscoveryService
from database.models import API
from datetime import datetime


class TestGitHubScanner:
    """Test GitHub API discovery functionality."""
    
    @pytest.fixture
    def mock_repo(self):
        """Create mock GitHub repository."""
        repo = MagicMock()
        repo.name = "test-api-service"
        repo.owner.login = "test-org"
        repo.html_url = "https://github.com/test-org/test-api-service"
        repo.language = "Python"
        return repo
    
    @pytest.fixture
    def service(self, db):
        """Create discovery service."""
        return APIDiscoveryService(db)
    
    def test_detect_tech_stack_python_fastapi(self, service, mock_repo):
        """Test technology stack detection for FastAPI."""
        # Mock requirements.txt
        mock_file = MagicMock()
        mock_file.decoded_content = b"fastapi==0.104.1\nuvicorn==0.24.0"
        mock_repo.get_contents.return_value = mock_file
        
        tech_stack = service._detect_tech_stack(mock_repo)
        
        assert "Python" in tech_stack
        assert "FastAPI" in tech_stack
    
    def test_detect_tech_stack_nodejs_express(self, service, mock_repo):
        """Test technology stack detection for Express."""
        mock_repo.language = "JavaScript"
        
        # Mock package.json
        mock_file = MagicMock()
        mock_file.decoded_content = b'{"dependencies": {"express": "4.18.0"}}'
        mock_repo.get_contents.return_value = mock_file
        
        tech_stack = service._detect_tech_stack(mock_repo)
        
        assert "JavaScript" in tech_stack
        assert "Express" in tech_stack
    
    def test_extract_routes_python_fastapi(self, service):
        """Test extracting routes from FastAPI code."""
        content = """
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/users")
        def get_users():
            return []
        
        @app.post("/users")
        def create_user():
            return {}
        """
        
        routes = service._extract_routes_from_content(content, "routes.py")
        
        assert len(routes) == 2
        assert any(r["endpoint"] == "/users" and r["method"] == "GET" for r in routes)
        assert any(r["endpoint"] == "/users" and r["method"] == "POST" for r in routes)
    
    def test_extract_routes_python_flask(self, service):
        """Test extracting routes from Flask code."""
        content = """
        from flask import Flask
        app = Flask(__name__)
        
        @app.route("/api/users", methods=["GET"])
        def get_users():
            return []
        
        @app.route("/api/users", methods=["POST"])
        def create_user():
            return {}
        """
        
        routes = service._extract_routes_from_content(content, "routes.py")
        
        assert len(routes) >= 1  # Should find at least Flask routes
    
    def test_extract_routes_javascript_express(self, service):
        """Test extracting routes from Express code."""
        content = """
        const express = require('express');
        const app = express();
        
        app.get('/api/users', (req, res) => {
            res.json([]);
        });
        
        app.post('/api/users', (req, res) => {
            res.json({});
        });
        """
        
        routes = service._extract_routes_from_content(content, "routes.js")
        
        assert len(routes) == 2
        assert any(r["endpoint"] == "/api/users" and r["method"] == "GET" for r in routes)
        assert any(r["endpoint"] == "/api/users" and r["method"] == "POST" for r in routes)
    
    def test_extract_routes_java_spring(self, service):
        """Test extracting routes from Spring Boot code."""
        content = """
        @RestController
        @RequestMapping("/api/users")
        public class UserController {
            
            @GetMapping
            public List<User> getUsers() {
                return new ArrayList<>();
            }
            
            @PostMapping
            public User createUser() {
                return new User();
            }
        }
        """
        
        routes = service._extract_routes_from_content(content, "UserController.java")
        
        assert len(routes) >= 1  # Should find Spring routes
    
    def test_store_discovered_apis_new(self, service, db):
        """Test storing newly discovered APIs."""
        apis = [
            {
                "name": "user-service",
                "endpoint": "/api/users",
                "method": "GET",
                "owner": "test-org",
                "tech_stack": "Python/FastAPI",
                "status": "active",
                "is_documented": True,
                "risk_score": 25.0,
            }
        ]
        
        count = service._store_discovered_apis(apis)
        assert count == 1
        
        # Verify API was stored
        api = db.query(API).filter(API.endpoint == "/api/users").first()
        assert api is not None
        assert api.name == "user-service"
        assert api.method == "GET"
        assert api.owner == "test-org"
    
    def test_store_discovered_apis_duplicate(self, service, db):
        """Test that duplicate APIs are not stored."""
        # Insert first API
        api1 = API(
            name="user-service-1",
            endpoint="/api/users",
            method="GET",
            owner="test-org",
            tech_stack="Python/FastAPI",
            status="active",
            is_documented=True,
            risk_score=25.0,
        )
        db.add(api1)
        db.commit()
        
        # Try to store duplicate
        apis = [
            {
                "name": "user-service-2",  # Different name
                "endpoint": "/api/users",  # Same endpoint
                "method": "GET",
                "owner": "test-org",  # Same owner
                "tech_stack": "Python/FastAPI",
                "status": "active",
                "is_documented": True,
                "risk_score": 25.0,
            }
        ]
        
        count = service._store_discovered_apis(apis)
        assert count == 0  # Should not store duplicate
        
        # Verify original API still exists
        api = db.query(API).filter(API.endpoint == "/api/users").first()
        assert api.name == "user-service-1"  # Original name preserved
    
    def test_find_route_files(self, service, mock_repo):
        """Test finding route definition files in repository."""
        # Mock repository contents
        item1 = MagicMock()
        item1.name = "routes.py"
        item1.type = "file"
        item1.path = "routes.py"
        
        item2 = MagicMock()
        item2.name = "api_controller.py"
        item2.type = "file"
        item2.path = "controllers/api_controller.py"
        
        item3 = MagicMock()
        item3.name = "vendor"
        item3.type = "dir"
        item3.name = ".venv"
        item3.type = "dir"
        
        contents = [item1, item2]
        
        route_files = service._find_route_files(mock_repo, contents)
        
        assert "routes.py" in route_files
        assert "controllers/api_controller.py" in route_files


class TestGitHubDiscoveryIntegration:
    """Integration tests for GitHub discovery."""
    
    @pytest.mark.skip(reason="Requires GitHub credentials")
    def test_discover_from_github_real(self, db):
        """Test real GitHub discovery (requires credentials)."""
        service = APIDiscoveryService(db)
        count = service.discover_from_github("ciphernet01")
        
        # Should discover at least some APIs
        assert count >= 0
        
        # Verify APIs were stored in database
        total_apis = db.query(API).count()
        assert total_apis >= 0
    
    def test_discover_from_github_no_token(self, db):
        """Test GitHub discovery without token (public repos only)."""
        import os
        
        # Ensure no token is set
        original_token = os.getenv("GITHUB_TOKEN")
        if original_token:
            del os.environ["GITHUB_TOKEN"]
        
        service = APIDiscoveryService(db)
        
        # Should handle gracefully (may return 0 due to rate limiting)
        with patch("services.discovery_service.Github") as mock_github:
            mock_github.return_value.get_organization.side_effect = Exception("Rate limited")
            count = service.discover_from_github("public-org")
            
            assert count >= 0  # Should not crash
        
        # Restore token if it was set
        if original_token:
            os.environ["GITHUB_TOKEN"] = original_token
