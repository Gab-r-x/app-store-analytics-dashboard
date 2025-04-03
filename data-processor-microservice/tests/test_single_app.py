import logging
from datetime import datetime
from pymongo import MongoClient
from src.database.postgres_connection import get_postgres_session
from src.processor.normalize import normalize_app_data
from src.processor.transform import transform_app_data
from src.processor.validator import validate_app_data
from src.database.models import App
from sqlalchemy.dialects.postgresql import insert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_single_app():
    logger.info("🧪 Running test: single app upsert")

    # Setup
    mongo = MongoClient("mongodb://mongo:27017")
    db = mongo["scraper_data"]
    raw_app = db.raw_apps.find_one()
    app_detail = db.app_details.find_one({"Url": raw_app.get("url")})

    if not raw_app or not app_detail:
        logger.error("❌ No matching raw_app and app_detail found.")
        return

    merged = {**app_detail, **raw_app}
    normalized = normalize_app_data(merged)
    transformed = transform_app_data(normalized)

    if not validate_app_data(transformed):
        logger.warning("⚠️ App is invalid after validation. Skipping.")
        return

    # Insert in Postgres
    _, session = get_postgres_session()
    try:
        stmt = insert(App).values(**transformed)
        update_dict = transformed.copy()
        update_dict["last_seen"] = datetime.utcnow()
        stmt = stmt.on_conflict_do_update(
            index_elements=[App.apple_id],
            set_=update_dict
        )

        session.execute(stmt)
        session.commit()
        logger.info(f"✅ Successfully upserted app: {transformed['apple_id']}")

        # Mark as processed
        db.app_details.update_one({"_id": app_detail["_id"]}, {"$set": {"processed": True}})
    except Exception as e:
        logger.error(f"❌ Insert failed: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    test_single_app()
