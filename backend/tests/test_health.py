"""
Test health check endpoint.

A simple test to verify the API server is running and responding to requests.
"""

import pytest


def test_health_endpoint(client):
    """
    Test that /health endpoint returns 200 OK with expected response.
    
    This test:
    1. Makes GET request to /health
    2. Verifies response status is 200
    3. Checks response contains required fields
    """
    response = client.get("/health")
    
    # Verify status code
    assert response.status_code == 200
    
    # Verify response content
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "zombie-api-backend"
    assert "version" in data
    
    print("✅ Health check test passed!")


def test_health_endpoint_response_format(client):
    """Test that health endpoint returns proper JSON format."""
    response = client.get("/health")
    
    # Should be JSON
    assert response.headers["content-type"] == "application/json"
    
    # Should have these fields
    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data
    assert "service" in data
    assert "version" in data
