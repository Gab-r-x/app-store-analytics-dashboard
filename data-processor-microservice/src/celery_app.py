from celery import Celery
import os
from config import settings

def make_celery():
    return Celery(
        "tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=["tasks.process_data", 
                 "tasks.generate_labels", 
                 "tasks.cluster_analysis_task"],
        task_serializer="pickle",
        result_serializer="pickle",
        accept_content=["pickle", "json"],
    )
