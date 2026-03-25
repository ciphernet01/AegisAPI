"""
Configuration management for the Zombie API Platform backend.
Loads settings from .env file and provides defaults.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Usage:
        from config import get_settings
        settings = get_settings()
        print(settings.database_url)
    """
    
    # ========== SERVER CONFIG ==========
    environment: str = "development"
    debug: bool = True
    port: int = 5000
    log_level: str = "INFO"
    
    # ========== DATABASE CONFIG ==========
    database_url: str = "postgresql://postgres:postgres@localhost:5432/zombie_api_db"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "zombie_api_db"
    
    # ========== AUTHENTICATION CONFIG ==========
    secret_key: str = "your-secret-key-change-this-for-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ========== CORS CONFIG ==========
    allowed_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # ========== EXTERNAL APIs ==========
    github_token: str = ""
    github_org: str = ""
    
    # ========== REDIS CONFIG ==========
    redis_url: str = "redis://localhost:6379"
    
    # ========== CELERY CONFIG ==========
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"
    
    # ========== SLACK CONFIG ==========
    slack_webhook_url: str = ""
    slack_enabled: bool = False
    
    # ========== SENTRY CONFIG ==========
    sentry_dsn: str = ""
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings instance (cached for performance).
    
    Returns:
        Settings: Application settings
    
    Usage:
        settings = get_settings()
    """
    return Settings()
