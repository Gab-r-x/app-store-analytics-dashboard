import os
import subprocess
from dynaconf import settings
import logging
from sqlalchemy import create_engine
from database.models import Base

def run_migrations():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_ini_path = os.path.join(project_root, "alembic.ini")

        subprocess.run(
            ["alembic", "-c", alembic_ini_path, "upgrade", "head"],
            check=True,
            cwd=project_root  # muda o diretório de trabalho para /app
        )
        logging.info("✅ Alembic migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed to apply migrations: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Data transformation microservice is starting...")

    logging.info(f"Mongo URI: {settings.MONGO_URI}")
    logging.info(f"Postgres URI: {settings.POSTGRES_URI}")
    logging.info("✅ Settings loaded successfully.")

    # Run migrations
    run_migrations()

if __name__ == "__main__":
    main()
