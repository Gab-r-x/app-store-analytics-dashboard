from datetime import date, datetime
from typing import List, Optional, Union
from uuid import UUID
from pydantic import BaseModel


class Review(BaseModel):
    rating: Optional[str]
    author: Optional[str]
    date: Optional[str]
    title: Optional[str]
    body: Optional[str]


class AppSchema(BaseModel):
    id: UUID
    apple_id: str
    name: Optional[str]
    subtitle: Optional[str]
    developer: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]

    # Ranking & Categorization
    rank: Optional[int]
    category_rank: Optional[str]
    category: Optional[str]
    list_type: Optional[str]

    # Monetization
    price: Optional[str]
    has_in_app_purchases: Optional[str]
    monthly_revenue_estimate: Optional[float]
    monthly_downloads_estimate: Optional[float]

    # Content
    description: Optional[str]
    screenshots: Optional[List[str]]
    num_screenshots: Optional[int]
    rating_summary: Optional[str]
    latest_version: Optional[str]
    latest_version_date: Optional[date]

    # Additional
    labels: Optional[List[str]]
    reviews: Optional[Union[str, List[Review]]]
    privacy_data: Optional[List[str]]
    general_info: Optional[dict]

    # Tracking
    last_seen: Optional[datetime]
    active: bool

    class Config:
        orm_mode = True
