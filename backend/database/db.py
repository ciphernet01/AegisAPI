"""
Database connection setup using SQLAlchemy.

Handles:
- PostgreSQL connection
- Session management
- Connection pooling
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries if in debug mode
    poolclass=QueuePool,  # Connection pooling
    pool_size=10,  # Maintain 10 connections
    max_overflow=20,  # Allow up to 20 overflow connections
    pool_pre_ping=True,  # Test connection before using
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db() -> Session:
    """
    Dependency injection for database session.
    
    Usage in routes:
        @app.get("/apis")
        async def list_apis(db: Session = Depends(get_db)):
            return db.query(API).all()
    
    Yields:
        Session: SQLAlchemy session for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base class for all ORM models
from sqlalchemy.orm import declarative_base
Base = declarative_base()
