from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

def get_mongo_collection(collection_name: str):
    """Returns a MongoDB collection from the default database."""
    return db[collection_name]
