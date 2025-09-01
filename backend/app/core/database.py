"""
PhishGuard Backend Database Configuration
SQLAlchemy with async support for PostgreSQL
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator, Generator
import structlog
from contextlib import asynccontextmanager

from app.core.config import settings

logger = structlog.get_logger()

# SQLAlchemy setup
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Detect database type and configure accordingly
is_sqlite = "sqlite" in settings.DATABASE_URL.lower()

if is_sqlite:
    # SQLite configuration
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async_engine = create_async_engine(
        settings.DATABASE_URL_ASYNC,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
    )
    
    async_engine = create_async_engine(
        settings.DATABASE_URL_ASYNC,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )

# Session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    """Create all database tables"""
    try:
        async with async_engine.begin() as conn:
            # Import all models to ensure they're registered
            from app.models import user, email, threat, organization  # noqa
            
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error("❌ Failed to create database tables", error=str(e))
        raise


async def drop_tables():
    """Drop all database tables (for testing)"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("🗑️ Database tables dropped successfully")
    except Exception as e:
        logger.error("❌ Failed to drop database tables", error=str(e))
        raise


# Dependency for getting async database session
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async database session dependency for FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Don't auto-commit, let the endpoint handle it
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


# Dependency for getting sync database session (for testing)
def get_sync_db() -> Generator[Session, None, None]:
    """
    Sync database session dependency
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error("Database session error", error=str(e))
        raise
    finally:
        session.close()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for async database sessions
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Don't auto-commit, let the caller handle it
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise


class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    async def health_check() -> bool:
        """Check database connectivity"""
        try:
            async with async_engine.begin() as conn:
                await conn.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return False
    
    @staticmethod
    async def get_stats() -> dict:
        """Get database statistics"""
        try:
            async with AsyncSessionLocal() as session:
                # Import models
                from app.models.user import User
                from app.models.email import Email
                from app.models.threat import Threat
                
                # Count records
                result = await session.execute(
                    "SELECT "
                    "(SELECT COUNT(*) FROM users) as user_count, "
                    "(SELECT COUNT(*) FROM emails) as email_count, "
                    "(SELECT COUNT(*) FROM threats) as threat_count"
                )
                stats = result.fetchone()
                
                return {
                    "users": stats.user_count if stats else 0,
                    "emails": stats.email_count if stats else 0,
                    "threats": stats.threat_count if stats else 0,
                    "status": "healthy"
                }
        except Exception as e:
            logger.error("Failed to get database stats", error=str(e))
            return {
                "users": 0,
                "emails": 0,
                "threats": 0,
                "status": "error",
                "error": str(e)
            }


# Test database configuration
def create_test_engine():
    """Create test database engine"""
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import create_async_engine
    
    test_engine = create_engine(
        settings.TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False} if "sqlite" in settings.TEST_DATABASE_URL else {},
        echo=False
    )
    
    test_async_engine = create_async_engine(
        settings.TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        poolclass=StaticPool,
        echo=False
    )
    
    return test_engine, test_async_engine


# Connection utilities
async def check_database_connection():
    """Verify database connection on startup"""
    try:
        async with async_engine.begin() as conn:
            result = await conn.execute("SELECT version();")
            version = result.scalar()
            logger.info("✅ Database connected successfully", version=version)
            return True
    except Exception as e:
        logger.error("❌ Database connection failed", error=str(e))
        return False


# Migration utilities
def run_migrations():
    """Run database migrations (to be used with Alembic)"""
    # This would typically use Alembic for migrations
    # For now, we'll create tables directly
    Base.metadata.create_all(bind=engine)


# Database initialization
async def init_database():
    """Initialize database with sample data if needed"""
    try:
        # Check if database is empty
        async with AsyncSessionLocal() as session:
            # Check for existing data
            from app.models.user import User
            result = await session.execute("SELECT COUNT(*) FROM users")
            user_count = result.scalar()
            
            if user_count == 0:
                logger.info("🔄 Initializing database with sample data...")
                await create_sample_data(session)
                await session.commit()
                logger.info("✅ Sample data created successfully")
            else:
                logger.info("📊 Database already contains data", user_count=user_count)
                
    except Exception as e:
        logger.error("❌ Failed to initialize database", error=str(e))
        raise


async def create_sample_data(session: AsyncSession):
    """Create sample data for development"""
    try:
        from app.models.user import User
        from app.models.organization import Organization
        from app.core.security import get_password_hash
        
        # Create default organization
        org = Organization(
            name="PhishGuard",
            domain="phishguard.com",
            is_active=True
        )
        session.add(org)
        await session.flush()  # Get the org ID
        
        # Create admin user
        admin_user = User(
            email=settings.TEST_USER_EMAIL,
            username="admin",
            hashed_password=get_password_hash(settings.TEST_USER_PASSWORD),
            full_name="Administrator",
            is_active=True,
            is_superuser=True,
            organization_id=org.id
        )
        session.add(admin_user)
        
        logger.info("👤 Created sample admin user", email=settings.TEST_USER_EMAIL)
        
    except Exception as e:
        logger.error("❌ Failed to create sample data", error=str(e))
        raise 