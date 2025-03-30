# src/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.config import settings

Base = declarative_base()

# Optional synchronous engine (only if needed somewhere in the code)
sync_engine = create_engine(settings.POSTGRES_URI, echo=False)

# Build the async URI for psycopg, adding sslmode=disable
# If you want SSL enabled, replace with "?sslmode=require" or similar
DATABASE_URL_PSY = (
    settings.POSTGRES_URI
    .replace("postgresql://", "postgresql+psycopg://")
    + "?sslmode=disable"
)

# Create the async engine with connection pooling and stability options
async_engine = create_async_engine(
    DATABASE_URL_PSY,
    echo=False,
    connect_args={"ssl": None},  # or ssl=False to explicitly disable SSL
    pool_pre_ping=True,          # checks connection before using it
    pool_recycle=1800,           # recycles connections every 30 minutes
    pool_size=10,                # max number of connections in the pool
    max_overflow=20,             # extra connections if pool is full
)

# Create the async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to inject session into FastAPI routes
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
