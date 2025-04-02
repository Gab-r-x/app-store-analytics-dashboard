from src.celery_app import make_celery
from src.database.postgres_connection import AsyncSessionLocal
from src.database.models import App
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import logging
import openai
from config import settings

celery_app = make_celery()
openai.api_key = settings.OPENAI_API_KEY

logger = logging.getLogger(__name__)

BATCH_SIZE = 10
SLEEP_BETWEEN_BATCHES = 2  # seconds

async def fetch_unlabeled_apps(session: AsyncSession, limit: int = 50):
    stmt = select(App).where(App.labels == None).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

def build_prompt(app: App) -> str:
    return (
        f"App Name: {app.name}\n"
        f"Subtitle: {app.subtitle}\n"
        f"Description: {app.description}\n"
        "\nBased on the information above, generate 5 descriptive labels (keywords or categories) for this app. Return as a comma-separated list."
    )

async def generate_label_for_app(app: App) -> list[str]:
    prompt = build_prompt(app)
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        return [label.strip() for label in content.split(",") if label.strip()]
    except Exception as e:
        logger.error(f"OpenAI error for app {app.id}: {e}")
        return []

@celery_app.task(name="tasks.generate_labels.generate_app_labels")
def generate_app_labels():
    async def process():
        async with AsyncSessionLocal() as session:
            while True:
                apps = await fetch_unlabeled_apps(session)
                if not apps:
                    logger.info("✅ No more unlabeled apps.")
                    break

                for i in range(0, len(apps), BATCH_SIZE):
                    batch = apps[i:i + BATCH_SIZE]
                    tasks = [generate_label_for_app(app) for app in batch]
                    labels_list = await asyncio.gather(*tasks)

                    for app, labels in zip(batch, labels_list):
                        app.labels = labels

                    await session.commit()
                    logger.info(f"📝 Labeled {len(batch)} apps.")
                    await asyncio.sleep(SLEEP_BETWEEN_BATCHES)

    asyncio.run(process())
