# src/test_processor.py

from src.processor.processor import process_apps
from src.database.mongo_connection import get_mongo_client
from src.database.postgres_connection import get_postgres_session
import logging

def test_pipeline():
    logging.basicConfig(level=logging.INFO)
    logging.info("🧪 Running test: processor.process_apps()")
    
    try:
        process_apps()
        logging.info("✅ Test finished without errors.")
    except Exception as e:
        logging.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_pipeline()
