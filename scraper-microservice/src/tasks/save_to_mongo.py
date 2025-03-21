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
try:
    client = MongoClient("mongodb://mongo:27017/")
    db = client["scraper_data"]
    logging.info("✅ Successfully connected to MongoDB.")
except Exception as e:
    logging.error(f"❌ Error connecting to MongoDB: {e}")
    raise

# Logging configuration
logging.basicConfig(
    filename="logs/mongo_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@celery_app.task
def save_categories_to_mongo(categories):
    """Saves categories to MongoDB."""
    if not categories:
        logging.error("❌ No categories to save. Scraping may have failed.")
        return

    try:
        formatted_categories = [{"name": cat[0], "url": cat[1]} for cat in categories if isinstance(cat, tuple) and len(cat) == 2]
        if not formatted_categories:
            logging.error("❌ No valid categories found to save.")
            return

        db.categories.insert_many(formatted_categories)
        logging.info(f"✅ {len(formatted_categories)} categories saved to MongoDB.")
    except Exception as e:
        logging.error(f"❌ Error saving categories to MongoDB: {e}")
        raise


@celery_app.task
def save_apps_to_mongo(apps):
    """Saves apps to MongoDB."""
    if not apps:
        logging.error("❌ No apps to save. Scraping may have failed.")
        return

    try:
        formatted_apps = [
            {
                "category": app.get("category"),
                "list_type": app.get("list_type"),
                "rank": app.get("rank"),
                "name": app.get("name"),
                "developer": app.get("developer"),
                "url": app.get("url"),
            }
            for app in apps if isinstance(app, dict)
        ]

        if not formatted_apps:
            logging.error("❌ No valid apps found to save.")
            return

        db.raw_apps.insert_many(formatted_apps)
        logging.info(f"✅ {len(formatted_apps)} apps saved to MongoDB.")
    except Exception as e:
        logging.error(f"❌ Error saving apps to MongoDB: {e}")
        raise


@celery_app.task(ignore_result=True)
def save_app_details_to_mongo(app_details):
    """Saves app details to MongoDB."""
    if not app_details:
        logging.error("❌ No app details to save. Scraping may have failed.")
        return

    try:
        if not all(isinstance(detail, dict) for detail in app_details):
            logging.error("❌ App details contain invalid data structure.")
            return

        # Remove _id to avoid conflicts before inserting
        for detail in app_details:
            detail.pop("_id", None)

        # Insert documents into MongoDB
        db.app_details.insert_many(app_details)

        logging.info(f"✅ {len(app_details)} app details saved to MongoDB.")

    except Exception as e:
        logging.error(f"❌ Error saving app details to MongoDB: {e}")
        raise
