from pymongo import MongoClient
from config import settings
import logging

# Mongo connection
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Logging
logger = logging.getLogger(__name__)

def init_scrape_progress(categories: list):
    """Create or recreate category progress."""
    try:
        db.scrape_status.replace_one(
            {"_id": "category_progress"},
            {
                "_id": "category_progress",
                "remaining": categories,
                "completed": []
            },
            upsert=True
        )
        logger.info("✅ Initialized scrape progress for categories.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize scrape progress: {e}")

def mark_category_done(category_name: str) -> bool:
    try:
        doc = db.scrape_status.find_one({"_id": "category_progress"})
        if not doc:
            logger.warning("⚠️ scrape_status not initialized.")
            return False

        if category_name not in doc["completed"]:
            db.scrape_status.update_one(
                {"_id": "category_progress"},
                {
                    "$pull": {"remaining": category_name},
                    "$addToSet": {"completed": category_name}
                }
            )

        updated = db.scrape_status.find_one({"_id": "category_progress"})
        done = len(updated["remaining"]) == 0

        if done:
            logger.info("🎯 All categories scraped. Triggering Sensor Tower scraping.")
            from tasks.scrape import scrape_sensor_tower_data
            scrape_sensor_tower_data.delay()

        return done

    except Exception as e:
        logger.error(f"❌ Failed to mark category as done: {e}")
        return False
