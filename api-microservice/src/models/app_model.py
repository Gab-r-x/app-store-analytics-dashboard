# src/models/app_model.py

import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, Integer, Boolean, Float, Date, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class App(Base):
    __tablename__ = "apps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apple_id = Column(String, unique=True, nullable=False)
    name = Column(String)
    subtitle = Column(String)
    developer = Column(String)
    url = Column(String)
    icon_url = Column(String)

    # Ranking & Categorization
    rank = Column(Integer)
    category_rank = Column(String)
    category = Column(String)
    list_type = Column(String)

    # Monetization
    price = Column(String)
    has_in_app_purchases = Column(String)
    monthly_revenue_estimate = Column(Float)
    monthly_downloads_estimate = Column(Float)

    # Content
    description = Column(String)
    screenshots = Column(ARRAY(String))
    num_screenshots = Column(Integer)
    rating_summary = Column(String)
    latest_version = Column(String)
    latest_version_date = Column(Date)

    # Additional
    labels = Column(ARRAY(String))
    reviews = Column(JSON)
    privacy_data = Column(ARRAY(String))
    general_info = Column(JSON)

    # Tracking
    last_seen = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Full Text Search
    search_vector = Column(TSVECTOR)
