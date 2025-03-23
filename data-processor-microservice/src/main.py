from dynaconf import settings
import logging
from sqlalchemy import create_engine
from database.models import Base

def create_tables_if_not_exist():
    try:
        engine = create_engine(settings.POSTGRES_URI)
        Base.metadata.create_all(engine)
        logging.info("✅ Tables created or already exist.")
    except Exception as e:
        logging.error(f"❌ Failed to create tables: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Data transformation microservice is starting...")

    # Log config
    logging.info(f"Mongo URI: {settings.MONGO_URI}")
    logging.info(f"Postgres URI: {settings.POSTGRES_URI}")
    logging.info("✅ Settings loaded successfully.")

    # Create tables if not exist
    create_tables_if_not_exist()

if __name__ == "__main__":
    main()
