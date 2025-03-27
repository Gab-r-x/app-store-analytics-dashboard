# src/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.config import settings

Base = declarative_base()

# (Opcional) Engine síncrono, só se for realmente necessário em alguma parte do código:
sync_engine = create_engine(settings.POSTGRES_URI, echo=False)

# Monta a URI para o dialeto async do psycopg,
# adicionando sslmode=disable ao final (caso queira desabilitar SSL).
# Se preferir habilitar, mude para "?sslmode=require" ou similar.
DATABASE_URL_PSY = (
    settings.POSTGRES_URI
    .replace("postgresql://", "postgresql+psycopg://")
    + "?sslmode=disable"
)

# Cria o engine assíncrono com psycopg
async_engine = create_async_engine(
    DATABASE_URL_PSY,
    echo=False,
    connect_args={"ssl": None},  # ou ssl=False, se quiser garantir desativação do SSL
)

# Cria a factory de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency para injetar a sessão nos endpoints FastAPI
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
