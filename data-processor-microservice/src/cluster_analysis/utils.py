import time
import logging
from sqlalchemy import func
from sqlalchemy.future import select
from database.postgres_connection import AsyncSessionLocal
from celery_app import make_celery
from database.models import App

logger = logging.getLogger(__name__)
celery_app = make_celery()

async def has_apps_without_embedding() -> bool:
    """Check if there are apps with labels but not yet clustered."""
    async with AsyncSessionLocal() as session:
        stmt = select(func.count()).select_from(App).where(App.labels != None)
        result = await session.execute(stmt)
        total = result.scalar()
        return total > 0

def run_saturation_batch_loop(n_clusters: int = 50, delay_seconds: int = 10):
    """Run saturation analysis in batches, waiting for each task to complete before continuing."""
    import asyncio

    while True:
        logger.info("🔍 Checking for apps to embed...")
        if not asyncio.run(has_apps_without_embedding()):
            logger.info("✅ No more apps to process.")
            break

        logger.info("🚀 Dispatching saturation analysis task...")
        task = celery_app.send_task(
            "tasks.cluster_analysis.run_saturation_analysis",
            args=[n_clusters],
            queue="data_processor"
        )

        logger.info("⏳ Waiting for task to complete...")
        result = task.get(timeout=300)  # timeout 5 minutes
        logger.info(f"✅ Task finished. Result: {result}")

        logger.info(f"⏱️ Sleeping for {delay_seconds} seconds...")
        time.sleep(delay_seconds)
