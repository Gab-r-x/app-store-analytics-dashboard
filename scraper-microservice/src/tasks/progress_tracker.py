from pymongo import MongoClient
from config import settings
import logging

# Configurar conexão com o Mongo
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Logging (opcional)
logger = logging.getLogger(__name__)

def init_scrape_progress(categories: list):
    """Cria ou reinicia o status de progresso das categorias."""
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
    """Marca uma categoria como concluída e verifica se acabou."""
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
        return len(updated["remaining"]) == 0

    except Exception as e:
        logger.error(f"❌ Failed to mark category as done: {e}")
        return False
