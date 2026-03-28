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
