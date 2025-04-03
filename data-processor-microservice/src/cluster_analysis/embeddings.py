import logging
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import App
from database.postgres_connection import AsyncSessionLocal
from config import settings
import openai

openai.api_key = settings.OPENAI_API_KEY
logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "text-embedding-ada-002"

def build_input_text(app: App) -> str:
    """Concatena informações relevantes para gerar um embedding significativo."""
    labels = ", ".join(app.labels or [])
    return f"{app.name or ''}. {app.subtitle or ''}. {app.description or ''}. Labels: {labels}"

async def fetch_apps_to_embed(session: AsyncSession, limit: int = 50):
    """Busca apps com labels e sem embedding ainda."""
    stmt = select(App).where(App.labels != None).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

async def generate_embedding_for_app(app: App) -> list[float] | None:
    try:
        input_text = build_input_text(app)
        response = await openai.Embedding.acreate(
            input=input_text,
            model=EMBEDDING_MODEL,
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        logger.warning(f"❌ Failed to generate embedding for {app.id}: {e}")
        return None

async def generate_all_embeddings():
    logger.info("🚀 Generating embeddings for labeled apps...")
    async with AsyncSessionLocal() as session:
        apps = await fetch_apps_to_embed(session)

        if not apps:
            logger.info("✅ No apps found for embedding generation.")
            return []

        logger.info(f"🧠 Generating embeddings for {len(apps)} apps...")
        result = []

        for app in apps:
            embedding = await generate_embedding_for_app(app)
            if embedding:
                result.append((app, embedding))

        logger.info(f"🎯 Finished generating {len(result)} embeddings.")
        return result
