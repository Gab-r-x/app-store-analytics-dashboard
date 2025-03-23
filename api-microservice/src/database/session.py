# src/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dynaconf import settings

# Create synchronous engine (for compatibility if needed)
sync_engine = create_engine(settings.POSTGRES_URI, echo=False)

# Create async engine for FastAPI
async_engine = create_async_engine(settings.POSTGRES_URI.replace("postgresql://", "postgresql+asyncpg://"), echo=False)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependency for route handlers
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
