"""
Mock Database Module - Returns sample data without requiring a real database.
"""

from typing import Optional
from sqlalchemy.orm import Session


class MockDB:
    """Mock database session that returns sample data."""
    pass


class MockAPI:
    """Mock API model."""
    def __init__(self, id, name, status="active", endpoint="/api/v1", risk_score=25.0):
        self.id = id
        self.name = name
        self.status = status
        self.endpoint = endpoint
        self.risk_score = risk_score
        self.last_used = "2024-03-15"
        self.documentation = "Available"
        self.owner = "API Team"


# Sample data
SAMPLE_APIS = [
    MockAPI(1, "User Authentication API", "active", "/auth", 15.0),
    MockAPI(2, "Payment Gateway API", "active", "/payments", 35.0),
    MockAPI(3, "Legacy Auth Service", "zombie", "/legacy-auth", 92.0),
    MockAPI(4, "Old Payment API", "deprecated", "/old-payments", 75.0),
    MockAPI(5, "Analytics API", "active", "/analytics", 28.0),
    MockAPI(6, "Notification Service", "zombie", "/notify", 88.0),
    MockAPI(7, "Reporting API", "deprecated", "/reports", 72.0),
    MockAPI(8, "Search Service", "active", "/search", 22.0),
    MockAPI(9, "Image Processing API", "zombie", "/images", 85.0),
    MockAPI(10, "Tagging Service", "active", "/tags", 32.0),
]


def get_mock_db() -> Session:
    """Return mock database session."""
    return MockDB()
