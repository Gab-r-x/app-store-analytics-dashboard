import logging
from celery_app import make_celery
from cluster_analysis.saturation_analyzis import run_saturation_analysis

celery_app = make_celery()
logger = logging.getLogger(__name__)

@celery_app.task(name="tasks.cluster_analysis.run_saturation_analysis", queue="data_processor")
def run_saturation_cluster_task(n_clusters: int = 8):
    """Celery task to perform saturation analysis using clustering."""
    logger.info(f"🚀 Starting clustering task with {n_clusters} clusters...")
    run_saturation_analysis(n_clusters=n_clusters)
    logger.info("🏁 Saturation cluster analysis task complete.")
