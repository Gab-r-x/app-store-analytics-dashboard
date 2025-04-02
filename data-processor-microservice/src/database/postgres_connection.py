import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings

# Base class for ORM models
Base = declarative_base()

# ---------- Synchronous engine (used in cases like Alembic migrations) ----------

def get_postgres_session():
    """Create a synchronous SQLAlchemy session (if needed for sync operations)."""
    try:
        engine = create_engine(settings.POSTGRES_URI)
        Session = sessionmaker(bind=engine)
        logging.info("✅ Connected to PostgreSQL (sync engine).")
        return engine, Session()
    except Exception as e:
        logging.error(f"❌ Failed to connect to PostgreSQL: {e}")
        raise

# ---------- Asynchronous engine (used in most operations) ----------

# Transform sync URI to async URI (for psycopg + asyncpg compatibility)
DATABASE_URL_PSY = (
    settings.POSTGRES_URI
    .replace("postgresql+psycopg2://", "postgresql+psycopg://")  # ensure correct replacement
    + "?sslmode=disable"
)

# Create async engine with robust pooling config
async_engine = create_async_engine(
    DATABASE_URL_PSY,
    echo=False,
    connect_args={"ssl": None},
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=10,
    max_overflow=20,
)

# Factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency-style async session getter
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
