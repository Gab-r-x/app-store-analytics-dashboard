import logging
from celery import Celery
from database.get_mongo import get_mongo_connection, get_mongo_collection
from config import settings


# Celery configuration
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# MongoDB connection
db = get_mongo_connection()

# Logging configuration
logging.basicConfig(
    filename="logs/mongo_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@celery_app.task(queue="app_details")
def save_categories_to_mongo(categories):
    """Saves categories to MongoDB only if they don't already exist."""
    if not categories:
        logging.error("❌ No categories to save. Scraping may have failed.")
        return

    try:
        formatted_categories = [{"name": cat[0], "url": cat[1]} for cat in categories if isinstance(cat, tuple) and len(cat) == 2]
        if not formatted_categories:
            logging.error("❌ No valid categories found to save.")
            return

        collection = get_mongo_collection("categories")
        inserted_count = 0

        for cat in formatted_categories:
            exists = collection.find_one({"name": cat["name"]})
            if not exists:
                collection.insert_one(cat)
                inserted_count += 1

        logging.info(f"✅ {inserted_count} new categories saved to MongoDB.")
    except Exception as e:
        logging.error(f"❌ Error saving categories to MongoDB: {e}")
        raise


@celery_app.task(queue="app_details")
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


@celery_app.task(ignore_result=True, queue="app_details")
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

# def save_sensor_metrics_to_mongo(metrics: list):
#     """Saves Sensor Tower metrics to a MongoDB collection."""
#     if metrics:
#         db.sensor_tower_metrics.insert_many(metrics)
#         logging.info(f"📥 Inserted {len(metrics)} documents into sensor_tower_metrics.")
#     else:
#         logging.warning("⚠️ No metrics to insert into sensor_tower_metrics.")

def save_sensor_metrics_to_mongo(data: dict):
    """Saves a single Sensor Tower metric document to MongoDB."""
    if not data:
        logging.warning("⚠️ No data to insert into sensor_tower_metrics.")
        return

    try:
        db.sensor_tower_metrics.insert_one(data)
        logging.info(f"📥 Inserted metric for Apple ID: {data.get('apple_id')}")
    except Exception as e:
        logging.error(f"❌ Failed to insert metric for Apple ID: {data.get('apple_id')} - Error: {e}")
