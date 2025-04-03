from processor.processor import process_apps, process_sensor_tower_metrics
from celery_app import make_celery
import logging

celery_app = make_celery()

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
    logging.info("✅ Finished processing apps. Triggering label generation...")
    celery_app.send_task("tasks.generate_labels.generate_app_labels", queue="data_processor")
    logging.info("🏁 Task finished: run_data_processing")

@celery_app.task(name="tasks.process_data.run_sensor_metrics_processing", queue="data_processor")
def run_sensor_metrics_processing():
    """Celery task to process Sensor Tower metrics into PostgreSQL."""
    logging.info("🚀 Starting task: run_sensor_metrics_processing")
    process_sensor_tower_metrics()
    logging.info("🏁 Task finished: run_sensor_metrics_processing")
