from celery_app import make_celery
from database.postgres_connection import AsyncSessionLocal
from database.models import App
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import logging
import json
import re
from config import settings
from openai import AsyncOpenAI

celery_app = make_celery()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

logger = logging.getLogger(__name__)

BATCH_SIZE = 10
SLEEP_BETWEEN_BATCHES = 2  # seconds


async def fetch_unlabeled_apps(session: AsyncSession, limit: int = 3000):
    logger.info(f"🔍 Fetching up to {limit} unlabeled apps from database...")
    try:
        stmt = select(App).where(App.labels == None).limit(limit)
        result = await session.execute(stmt)
        apps = result.scalars().all()
        logger.info(f"📦 Found {len(apps)} unlabeled apps.")
        return apps
    except Exception as e:
        logger.error(f"❌ Failed to fetch unlabeled apps: {e}")
        return []


def build_prompt(app: App) -> str:
    return (
        f"App Name: {app.name}\n"
        f"Subtitle: {app.subtitle}\n"
        f"Description: {app.description}\n"
        f"Category: {app.category}\n\n"
        "Based on the information above, generate exactly 5 descriptive labels (keywords or categories) for this app. "
        "Do NOT repeat the category as a label.\n\n"
        "Important: Return ONLY a valid JSON array of strings with 5 elements, no explanations or markdown.\n"
        "Example: [\"label one\", \"label two\", \"label three\", \"label four\", \"label five\"]"
    )


def extract_json_array(text: str) -> list[str] | None:
    """Extract and parse the first JSON array found in the text."""
    try:
        match = re.search(r"\[[^\[\]]+\]", text, re.DOTALL)
        if match:
            array = json.loads(match.group(0))
            if isinstance(array, list) and all(isinstance(i, str) for i in array):
                return array
    except Exception as e:
        logger.warning(f"⚠️ JSON extraction failed: {e}")
    return None


async def generate_label_for_app(app: App) -> list[str]:
    prompt = build_prompt(app)
    try:
        logger.info(f"🤖 Generating labels for app {app.id} - '{app.name}'")
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()
        labels = extract_json_array(content)
        if labels:
            logger.info(f"✅ Labels generated for app {app.id}: {labels}")
            return labels
        else:
            raise ValueError("No valid JSON array found in response.")
    except Exception as e:
        logger.warning(f"⚠️ Failed to generate labels for app {app.id}: {e}")
        return []


@celery_app.task(name="tasks.generate_labels.generate_app_labels", queue="data_processor")
def generate_app_labels():
    async def process():
        logger.info("🚀 [START] generate_app_labels")

        async with AsyncSessionLocal() as session:
            logger.info("🔌 Opened async session.")
            apps = await fetch_unlabeled_apps(session)

            if not apps:
                logger.info("✅ No unlabeled apps found. Exiting task.")
                return

            logger.info(f"📦 Starting to process {len(apps)} apps...")

            for i in range(0, len(apps), BATCH_SIZE):
                batch = apps[i:i + BATCH_SIZE]
                logger.info(f"⚙️ Processing batch {i//BATCH_SIZE + 1}: {len(batch)} apps")

                tasks = [generate_label_for_app(app) for app in batch]
                labels_list = await asyncio.gather(*tasks, return_exceptions=True)

                for app, labels in zip(batch, labels_list):
                    if isinstance(labels, Exception):
                        logger.warning(f"⚠️ Skipped app {app.id} due to error: {labels}")
                        continue
                    app.labels = labels

                await session.commit()
                logger.info(f"📝 Committed batch of {len(batch)} apps.")
                await asyncio.sleep(SLEEP_BETWEEN_BATCHES)

        logger.info("🎉 [END] Task generate_app_labels completed.")

    try:
        logger.info("⚙️ Running async label generation...")
        asyncio.run(process())
    except Exception as e:
        logger.error(f"❌ Uncaught error in label generation: {e}")
