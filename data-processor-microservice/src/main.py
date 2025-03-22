from dynaconf import settings
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Data transformation microservice is starting...")

    # Placeholder: real logic will go in dedicated modules
    logging.info(f"Mongo URI: {settings.MONGO_URI}")
    logging.info(f"Postgres URI: {settings.POSTGRES_URI}")
    logging.info("✅ Settings loaded successfully.")

if __name__ == "__main__":
    main()