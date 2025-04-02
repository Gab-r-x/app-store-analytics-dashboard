from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings
import logging

Base = declarative_base()

# Build the sync session for the data processor 
def get_postgres_session():
    try:
        engine = create_engine(settings.POSTGRES_URI)
        Session = sessionmaker(bind=engine)
        logging.info("✅ Connected to PostgreSQL.")
        return engine, Session()
    except Exception as e:
        logging.error(f"❌ Failed to connect to PostgreSQL: {e}")
        raise

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

# Dependency to inject session
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
