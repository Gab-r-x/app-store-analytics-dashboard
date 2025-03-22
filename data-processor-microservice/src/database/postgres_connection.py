from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dynaconf import settings
import logging

Base = declarative_base()

def get_postgres_session():
    try:
        engine = create_engine(settings.POSTGRES_URI)
        Session = sessionmaker(bind=engine)
        logging.info("✅ Connected to PostgreSQL.")
        return Session(), engine
    except Exception as e:
        logging.error(f"❌ Failed to connect to PostgreSQL: {e}")
        raise
