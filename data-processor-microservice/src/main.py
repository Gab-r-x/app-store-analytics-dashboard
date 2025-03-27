import logging
from config import settings

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Data transformation microservice is starting...")

    logging.info(f"Mongo URI: {settings.MONGO_URI}")
    logging.info(f"Postgres URI: {settings.POSTGRES_URI}")
    logging.info("✅ Settings loaded successfully.")

if __name__ == "__main__":
    main()
