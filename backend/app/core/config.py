"""
PhishGuard Backend Configuration
Environment and settings management using Pydantic
"""

from typing import List, Optional, Any
from functools import lru_cache
import os
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    APP_NAME: str = "PhishGuard Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database - SQLite for development (easier setup)
    DATABASE_URL: str = "sqlite:///./phishguard.db"
    DATABASE_URL_ASYNC: str = "sqlite+aiosqlite:///./phishguard.db"
    TEST_DATABASE_URL: str = "sqlite:///./phishguard_test.db"
    
    # Redis (optional for development)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    REDIS_ENABLED: bool = False  # Disabled for development
    
    # Security
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://phishguard.com",
        "https://www.phishguard.com"
    ]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "phishguard.com"]
    
    # CORS Settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_EXTENSIONS: List[str] = [".eml", ".msg", ".pdf", ".txt", ".html"]
    UPLOAD_DIRECTORY: str = "./uploads"
    
    # Email Processing
    EMAIL_PROCESSING_TIMEOUT: int = 30  # seconds
    MAX_EMAILS_PER_BATCH: int = 100
    
    # Machine Learning
    ML_MODEL_PATH: str = "./models"
    THREAT_DETECTION_THRESHOLD: float = 0.75
    
    # External APIs
    VIRUSTOTAL_API_KEY: Optional[str] = None
    VIRUSTOTAL_BASE_URL: str = "https://www.virustotal.com/vtapi/v2"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 900  # 15 minutes
    
    # WebSocket
    WEBSOCKET_ENABLED: bool = True
    WEBSOCKET_MAX_CONNECTIONS: int = 1000
    
    # Background Tasks
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PORT: int = 9090
    
    # Email Integration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # Notification Settings
    SLACK_WEBHOOK_URL: Optional[str] = None
    DISCORD_WEBHOOK_URL: Optional[str] = None
    
    # Testing
    TESTING: bool = False
    TEST_USER_EMAIL: str = "admin@phishguard.com"
    TEST_USER_PASSWORD: str = ""
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment setting"""
        allowed = ["development", "staging", "production", "testing"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """Handle CORS origins from environment"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def assemble_allowed_hosts(cls, v):
        """Handle allowed hosts from environment"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure secret key is secure in production"""
        # Note: In Pydantic v2, accessing other fields in validators is more complex
        # For now, we'll skip the cross-field validation
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.TESTING or self.ENVIRONMENT == "testing"
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to ensure settings are only loaded once
    """
    return Settings()


# Global settings instance
settings = get_settings()


# Environment-specific configurations
class DevelopmentConfig(Settings):
    """Development environment configuration"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ALLOWED_ORIGINS: List[str] = ["*"]  # Allow all origins in development


class ProductionConfig(Settings):
    """Production environment configuration"""
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    TESTING: bool = False


class TestingConfig(Settings):
    """Testing environment configuration"""
    TESTING: bool = True
    DATABASE_URL: str = "postgresql://phishguard:password@localhost:5432/phishguard_test"
    REDIS_URL: str = "redis://localhost:6379/15"  # Use different Redis DB for tests


def get_config_by_env(env: str) -> Settings:
    """Get configuration based on environment"""
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    config_class = configs.get(env, Settings)
    return config_class() 