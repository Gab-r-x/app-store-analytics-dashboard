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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = settings.BATCH_SIZE or 50

def process_apps():
    logger.info("🚀 Starting app processing pipeline")

    mongo_db = get_mongo_client()
    _, session = get_postgres_session()
    logger.info("🔌 Connected to MongoDB and PostgreSQL")

    raw_details = list(mongo_db.app_details.find({"Url": {"$exists": True}, "processed": {"$ne": True}}))
    logger.info(f"🧪 Found {len(raw_details)} unprocessed documents in app_details")

    details = {
        d["Url"].strip().lower(): d
        for d in raw_details
        if d.get("Url")
    }

    raw_apps = list(mongo_db.raw_apps.find())
    logger.info(f"📦 Loaded {len(raw_apps)} raw app entries")
    logger.info(f"📦 Loaded {len(details)} app details and {len(raw_apps)} raw app entries")

    seen_apple_ids = set()
    processed_count = 0
    skipped_count = 0

    for i in range(0, len(raw_apps), BATCH_SIZE):
        batch = raw_apps[i:i + BATCH_SIZE]
        logger.info(f"⚙️ Processing batch {i // BATCH_SIZE + 1} of {len(raw_apps) // BATCH_SIZE + 1}")

        for raw_app in batch:
            try:
                url = raw_app.get("url")
                if not url:
                    skipped_count += 1
                    continue

                normalized_url = url.strip().lower()
                detail = details.get(normalized_url)
                if not detail:
                    logger.debug(f"⛔ No detail found for URL: {url}")
                    skipped_count += 1
                    continue

                merged_app = {**detail, **raw_app}
                normalized = normalize_app_data(merged_app)
                transformed = transform_app_data(normalized)

                if not validate_app_data(transformed):
                    skipped_count += 1
                    logger.debug("⛔ Skipped invalid app data")
                    continue

                seen_apple_ids.add(transformed["apple_id"])

                stmt = insert(App).values(**transformed)
                update_dict = transformed.copy()
                update_dict["last_seen"] = datetime.utcnow()
                stmt = stmt.on_conflict_do_update(
                    index_elements=[App.apple_id],
                    set_=update_dict
                )

                session.execute(stmt)
                processed_count += 1
                logger.debug(f"✅ Upserted app: {transformed['apple_id']}")

                mongo_db.app_details.update_one({"_id": detail["_id"]}, {"$set": {"processed": True}})

            except Exception as e:
                logger.error(f"❌ Error processing app: {e}")
                session.rollback()
                skipped_count += 1

    logger.info("🧹 Deactivating apps not seen in this round...")
    deactivated_count = 0
    if seen_apple_ids:
        deactivated_count = session.query(App).filter(~App.apple_id.in_(seen_apple_ids)).count()
        session.query(App).filter(~App.apple_id.in_(seen_apple_ids)).update(
            {"active": False}, synchronize_session=False
        )

    session.commit()
    session.close()
    logger.info(f"🏁 Processing complete. Processed: {processed_count}, Skipped: {skipped_count}, Deactivated: {deactivated_count}")


def parse_estimate(value: str, is_revenue: bool = False) -> float:
    """Converts estimates like '80K', '$2M', '< $5k' into float values."""
    if not value:
        return 0.0

    value = value.replace("$", "").replace(",", "").strip().lower()

    if "<" in value:
        return 5000.0 if is_revenue else 0.0

    multiplier = 1
    if value.endswith("k"):
        multiplier = 1_000
        value = value[:-1]
    elif value.endswith("m"):
        multiplier = 1_000_000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except ValueError:
        return 0.0

def process_sensor_tower_metrics():
    logger.info("🚀 Starting Sensor Tower metrics update...")

    mongo_db = get_mongo_client()
    _, session = get_postgres_session()

    docs = list(mongo_db.sensor_tower_metrics.find({"processed": {"$ne": True}}))
    logger.info(f"📦 Found {len(docs)} unprocessed metrics")

    updated = 0
    skipped = 0

    for doc in docs:
        try:
            apple_id = doc.get("apple_id")
            if not apple_id:
                skipped += 1
                continue

            downloads = parse_estimate(doc.get("monthly_downloads_estimate", ""))
            revenue = parse_estimate(doc.get("monthly_revenue_estimate", ""), is_revenue=True)

            stmt = (
                insert(App)
                .values(
                    apple_id=apple_id,
                    monthly_downloads_estimate=downloads,
                    monthly_revenue_estimate=revenue,
                    last_seen=datetime.utcnow(),
                )
                .on_conflict_do_update(
                    index_elements=[App.apple_id],
                    set_={
                        "monthly_downloads_estimate": downloads,
                        "monthly_revenue_estimate": revenue,
                        "last_seen": datetime.utcnow(),
                    },
                )
            )

            session.execute(stmt)
            mongo_db.sensor_tower_metrics.update_one({"_id": doc["_id"]}, {"$set": {"processed": True}})
            updated += 1

        except Exception as e:
            logger.error(f"❌ Error updating app {doc.get('apple_id')}: {e}")
            session.rollback()
            skipped += 1

    session.commit()
    session.close()
    logger.info(f"✅ Metrics update complete. Updated: {updated}, Skipped: {skipped}")
