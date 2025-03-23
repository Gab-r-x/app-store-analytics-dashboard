from celery import Celery
from config import settings
from processor.processor import process_apps
import logging

# Celery configuration
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.process_data"],
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle", "json"],
)

# Logging configuration
logging.basicConfig(
    filename="logs/process_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@celery_app.task(name="tasks.process_data.run_data_processing", queue="data_processor")
def run_data_processing():
    """Celery task to run full app data processing pipeline."""
    logging.info("🚀 Starting task: run_data_processing")
    process_apps()
    logging.info("🏁 Task finished: run_data_processing")
