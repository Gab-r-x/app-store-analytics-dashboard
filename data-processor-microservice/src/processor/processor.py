from database.mongo_connection import get_mongo_client
from database.postgres_connection import get_postgres_session
from processor.normalize import normalize_app_data
from processor.transform import transform_app_data
from processor.validator import validate_app_data
from database.models import App
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from dynaconf import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = settings.BATCH_SIZE or 50

def process_apps():
    logger.info("🚀 Starting app processing pipeline")

    # Connect to MongoDB and PostgreSQL
    mongo_client = get_mongo_client()
    mongo_db = mongo_client.scraper_data
    session = get_postgres_session()
    logger.info("🔌 Connected to MongoDB and PostgreSQL")

    # Fetch app details from MongoDB
    raw_apps = list(mongo_db.app_details.find())
    logger.info(f"📦 Loaded {len(raw_apps)} apps from MongoDB")

    seen_apple_ids = set()
    processed_count = 0
    skipped_count = 0

    for i in range(0, len(raw_apps), BATCH_SIZE):
        batch = raw_apps[i:i + BATCH_SIZE]
        logger.info(f"⚙️ Processing batch {i // BATCH_SIZE + 1} of {len(raw_apps) // BATCH_SIZE + 1}")

        for raw_app in batch:
            try:
                normalized = normalize_app_data(raw_app)
                if not validate_app_data(normalized):
                    skipped_count += 1
                    logger.debug("⛔ Skipped invalid app data")
                    continue

                transformed = transform_app_data(normalized)
                seen_apple_ids.add(transformed.apple_id)

                stmt = insert(App).values(**transformed.dict())
                update_dict = transformed.dict()
                update_dict["last_seen"] = datetime.utcnow()
                stmt = stmt.on_conflict_do_update(
                    index_elements=[App.apple_id],
                    set_=update_dict
                )

                session.execute(stmt)
                processed_count += 1
                logger.debug(f"✅ Upserted app: {transformed.apple_id}")

            except Exception as e:
                logger.error(f"❌ Error processing app: {e}")
                skipped_count += 1

    # Deactivate apps not seen in this round
    logger.info("🧹 Deactivating apps not seen in this round...")
    session.query(App).filter(~App.apple_id.in_(seen_apple_ids)).update({"active": False}, synchronize_session=False)

    session.commit()
    session.close()
    logger.info(f"🏁 Processing complete. Processed: {processed_count}, Skipped: {skipped_count}, Deactivated: {len(set(App.apple_id) - seen_apple_ids)}")
