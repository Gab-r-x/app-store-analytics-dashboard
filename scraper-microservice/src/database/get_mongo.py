from pymongo import MongoClient
from config import settings
import logging

def get_mongo_connection():
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        logging.info("✅ Successfully connected to MongoDB.")
    except Exception as e:
        logging.error(f"❌ Error connecting to MongoDB: {e}")
        raise
    return db

def get_mongo_collection(collection_name: str):
    """Returns a MongoDB collection from the default database."""
    db = get_mongo_connection()
    return db[collection_name]
