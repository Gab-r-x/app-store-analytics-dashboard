from celery import Celery
from pymongo import MongoClient
import logging

# Celery configuration
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@rabbitmq//",
    backend="mongodb://mongo:27017/scraper_results"
)

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client["scraper_db"]

# Logging configuration
logging.basicConfig(
    filename="logs/mongo_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@celery_app.task
def save_categories_to_mongo(categories):
    """Saves categories to MongoDB."""
    if categories:
        db.categories.insert_many([{"name": cat[0], "url": cat[1]} for cat in categories])
        logging.info(f"✅ {len(categories)} categories saved to MongoDB.")


@celery_app.task
def save_apps_to_mongo(apps):
    """Saves apps to MongoDB."""
    if apps:
        db.raw_apps.insert_many(
            [
                {
                    "category": app[0],
                    "list_type": app[1],
                    "rank": app[2],
                    "name": app[3],
                    "developer": app[4],
                    "url": app[5],
                }
                for app in apps
            ]
        )
        logging.info(f"✅ {len(apps)} apps saved to MongoDB.")


@celery_app.task
def save_app_details_to_mongo(app_details):
    """Saves app details to MongoDB."""
    if app_details:
        db.app_details.insert_many(app_details)
        logging.info(f"✅ {len(app_details)} app details saved to MongoDB.")
