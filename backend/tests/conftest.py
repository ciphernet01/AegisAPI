"""
Pytest configuration and shared test fixtures.

Fixtures are reusable test setups used by multiple tests.

Example:
    @pytest.fixture
    def client():
        # Setup
        yield test_client
        # Cleanup
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Lazy imports to allow tests that don't need the full app to run
# from main import create_app

# Create test database (in-memory SQLite for speed)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Database fixture - creates tables before test, drops after."""
    # Try to create tables if Base is available, otherwise skip
    try:
        from database.db import Base
        Base.metadata.create_all(bind=engine)
        yield TestingSessionLocal()
        Base.metadata.drop_all(bind=engine)
    except ImportError:
        # If database can't be imported, just yield a session without table setup
        db_session = TestingSessionLocal()
        yield db_session
        db_session.close()


@pytest.fixture(scope="function")
def client(db):
    """Test client fixture."""
    try:
        from fastapi.testclient import TestClient
        from main import create_app
        from database.db import get_db
        
        app = create_app()
        app.dependency_overrides[get_db] = override_get_db
        
        with TestClient(app) as test_client:
            yield test_client
        
        app.dependency_overrides.clear()
    except ImportError as e:
        # Client fixture requires fastapi and main app
        raise ImportError(f"client fixture requires full app setup: {e}")


@pytest.fixture(scope="function")
def sample_apis(db):
    """Sample API data fixture - creates 25 realistic test APIs."""
    from datetime import datetime, timedelta
    from database.models import API
    
    # Current timestamp for reference
    now = datetime.utcnow()
    
    # Sample API configurations
    api_configs = [
        # ACTIVE APIs (recent traffic, documented, owned)
        {"name": "user-service", "endpoint": "/api/v1/users", "method": "GET", "owner": "platform-team", "tech_stack": "Python/FastAPI", "is_documented": True, "last_traffic": now - timedelta(hours=2)},
        {"name": "orders-api", "endpoint": "/api/v1/orders", "method": "POST", "owner": "commerce-team", "tech_stack": "Node.js/Express", "is_documented": True, "last_traffic": now - timedelta(hours=1)},
        {"name": "payments-service", "endpoint": "/api/v1/payments", "method": "POST", "owner": "finance-team", "tech_stack": "Java/Spring", "is_documented": True, "last_traffic": now - timedelta(days=1)},
        {"name": "auth-gateway", "endpoint": "/api/v1/auth", "method": "POST", "owner": "security-team", "tech_stack": "Python/FastAPI", "is_documented": True, "last_traffic": now - timedelta(hours=6)},
        {"name": "notification-service", "endpoint": "/api/v1/notifications", "method": "POST", "owner": "backend-team", "tech_stack": "Node.js", "is_documented": True, "last_traffic": now - timedelta(days=1)},
        {"name": "analytics-api", "endpoint": "/api/v1/analytics", "method": "GET", "owner": "data-team", "tech_stack": "Python/Django", "is_documented": True, "last_traffic": now - timedelta(hours=3)},
        
        # DEPRECATED APIs (explicitly marked)
        {"name": "legacy-user-api", "endpoint": "/api/v1/legacy/users", "method": "GET", "owner": "platform-team", "tech_stack": "Python/Flask", "is_documented": True, "status": "deprecated", "last_traffic": now - timedelta(days=30)},
        {"name": "old-payment-gateway", "endpoint": "/api/v1/old/payment", "method": "POST", "owner": "finance-team", "tech_stack": "Java", "is_documented": False, "status": "deprecated", "last_traffic": now - timedelta(days=45)},
        {"name": "v1-auth-api", "endpoint": "/api/v1/authentication", "method": "POST", "owner": "security-team", "tech_stack": "Node.js", "is_documented": False, "status": "deprecated", "last_traffic": now - timedelta(days=60)},
        
        # ORPHANED APIs (no owner + no documentation)
        {"name": "mystery-api", "endpoint": "/api/v1/mystery", "method": "GET", "owner": None, "tech_stack": "Unknown", "is_documented": False, "last_traffic": now - timedelta(days=15)},
        {"name": "abandoned-service", "endpoint": "/api/v1/abandoned", "method": "POST", "owner": None, "tech_stack": None, "is_documented": False, "last_traffic": now - timedelta(days=25)},
        {"name": "orphaned-export", "endpoint": "/api/v1/export", "method": "GET", "owner": None, "tech_stack": "Unknown", "is_documented": False, "last_traffic": now - timedelta(days=40)},
        {"name": "lost-api", "endpoint": "/api/v1/lost", "method": "PUT", "owner": None, "tech_stack": None, "is_documented": False, "last_traffic": now - timedelta(days=50)},
        
        # ZOMBIE APIs (no traffic > 90 days)
        {"name": "inactive-reports", "endpoint": "/api/v1/reports", "method": "GET", "owner": "analytics-team", "tech_stack": "Python", "is_documented": True, "last_traffic": now - timedelta(days=100)},
        {"name": "dormant-batch", "endpoint": "/api/v1/batch-jobs", "method": "POST", "owner": "backend-team", "tech_stack": "Java", "is_documented": True, "last_traffic": now - timedelta(days=120)},
        {"name": "unused-webhook", "endpoint": "/api/v1/webhooks", "method": "POST", "owner": "integration-team", "tech_stack": "Node.js", "is_documented": False, "last_traffic": now - timedelta(days=150)},
        {"name": "stale-import", "endpoint": "/api/v1/import", "method": "POST", "owner": None, "tech_stack": "Unknown", "is_documented": False, "last_traffic": now - timedelta(days=180)},
        {"name": "cold-storage-api", "endpoint": "/api/v1/archive", "method": "GET", "owner": "storage-team", "tech_stack": "Python", "is_documented": False, "last_traffic": now - timedelta(days=200)},
        
        # Mixed risk APIs (need multi-factor analysis)
        {"name": "documented-but-inactive", "endpoint": "/api/v1/docs-inactive", "method": "GET", "owner": "docs-team", "tech_stack": "Python", "is_documented": True, "last_traffic": now - timedelta(days=110)},
        {"name": "owned-but-undocumented", "endpoint": "/api/v1/owned-no-docs", "method": "POST", "owner": "dev-team", "tech_stack": "Node.js", "is_documented": False, "last_traffic": now - timedelta(days=20)},
        {"name": "new-api-no-traffic", "endpoint": "/api/v1/new-service", "method": "GET", "owner": "platform-team", "tech_stack": "Go", "is_documented": True, "last_traffic": None},
        {"name": "recently-updated", "endpoint": "/api/v1/updated", "method": "POST", "owner": "backend-team", "tech_stack": "Python/FastAPI", "is_documented": True, "last_traffic": now - timedelta(minutes=30)},
        {"name": "low-traffic-api", "endpoint": "/api/v1/low-volume", "method": "GET", "owner": "shared-team", "tech_stack": "Java", "is_documented": False, "last_traffic": now - timedelta(days=5)},
        {"name": "maintenance-mode", "endpoint": "/api/v1/maintenance", "method": "GET", "owner": "ops-team", "tech_stack": "Unknown", "is_documented": False, "last_traffic": now - timedelta(days=70)},
        {"name": "edge-system", "endpoint": "/api/v1/edge", "method": "POST", "owner": "platform-team", "tech_stack": "Rust", "is_documented": True, "last_traffic": now - timedelta(hours=12)},
    ]
    
    # Create API objects and add to database
    apis = []
    for config in api_configs:
        api = API(
            name=config["name"],
            endpoint=config["endpoint"],
            method=config["method"],
            owner=config.get("owner"),
            tech_stack=config.get("tech_stack"),
            status=config.get("status", "active"),
            is_documented=config.get("is_documented", False),
            last_traffic=config.get("last_traffic"),
            created_at=config.get("created_at", now - timedelta(days=180))
        )
        db.add(api)
        apis.append(api)
    
    db.commit()
    
    # Refresh to get IDs
    for api in apis:
        db.refresh(api)
    
    return apis
