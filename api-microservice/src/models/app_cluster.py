from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AppCluster(Base):
    __tablename__ = "app_clusters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_id = Column(UUID(as_uuid=True), ForeignKey("apps.id", ondelete="CASCADE"), nullable=False, unique=True)

    cluster = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)  # 2D coordinate for visualization
    y = Column(Float, nullable=False)

    downloads = Column(Float, nullable=True)
    revenue = Column(Float, nullable=True)
