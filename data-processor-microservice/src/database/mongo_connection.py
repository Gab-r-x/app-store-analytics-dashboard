from pymongo import MongoClient
from config import settings
import logging

def get_mongo_client():
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        logging.info("✅ Connected to MongoDB.")
        return db
    except Exception as e:
        logging.error(f"❌ Failed to connect to MongoDB: {e}")
        raise
