from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, text, Float, cast
from src.models.app_model import App
from fastapi import HTTPException
from typing import List, Optional
from src.schemas.app_schema import AppSchema
from src.core.config import settings

async def get_apps_paginated(
    session: AsyncSession,
    skip: int = 0,
    limit: int = settings.PAGE_SIZE,
    category: Optional[str] = None,
    label: Optional[str] = None,
    has_in_app_purchases: Optional[bool] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    downloads_min: Optional[float] = None,
    downloads_max: Optional[float] = None,
    revenue_min: Optional[float] = None,
    revenue_max: Optional[float] = None,
    screenshots_min: Optional[int] = None,
    rating_min: Optional[float] = None,
    list_type: Optional[str] = None,
) -> List[AppSchema]:
    filters = []

    if category:
        filters.append(App.category == category)
    if label:
        filters.append(App.labels.any(label))
    if has_in_app_purchases is not None:
        filters.append(App.has_in_app_purchases == ("Yes" if has_in_app_purchases else "No"))
    if price_min is not None:
        filters.append(cast(func.nullif(func.replace(App.price, "$", ""), 'Free'), Float) >= price_min)
    if price_max is not None:
        filters.append(cast(func.nullif(func.replace(App.price, "$", ""), 'Free'), Float) <= price_max)
    if downloads_min is not None:
        filters.append(App.monthly_downloads_estimate >= downloads_min)
    if downloads_max is not None:
        filters.append(App.monthly_downloads_estimate <= downloads_max)
    if revenue_min is not None:
        filters.append(App.monthly_revenue_estimate >= revenue_min)
    if revenue_max is not None:
        filters.append(App.monthly_revenue_estimate <= revenue_max)
    if screenshots_min is not None:
        filters.append(App.num_screenshots >= screenshots_min)
    if rating_min is not None:
        rating_cast = cast(func.regexp_replace(App.rating_summary, '[^0-9.]', '', 'g'), Float)
        filters.append(rating_cast >= rating_min)
    if list_type:
        filters.append(App.list_type == list_type)

    stmt = select(App).where(and_(*filters)).offset(skip).limit(limit)
    result = await session.execute(stmt)
    apps = result.scalars().all()

    if not apps:
        raise HTTPException(status_code=404, detail="No apps found.")

    return [AppSchema.model_validate(app) for app in apps]


async def get_app_by_id(
    session: AsyncSession,
    apple_id: str,
) -> AppSchema:
    stmt = select(App).where(App.apple_id == apple_id)
    result = await session.execute(stmt)
    app = result.scalar_one_or_none()

    if not app:
        raise HTTPException(status_code=404, detail="App not found.")

    return AppSchema.model_validate(app)


async def get_all_categories(session: AsyncSession) -> List[str]:
    stmt = select(func.distinct(App.category)).where(App.category.isnot(None))
    result = await session.execute(stmt)
    return [row[0] for row in result.all() if row[0]]


async def get_all_labels(session: AsyncSession) -> List[str]:
    raw_sql = text("SELECT DISTINCT UNNEST(labels) FROM apps WHERE labels IS NOT NULL")
    result = await session.execute(raw_sql)
    return [row[0] for row in result.all() if row[0]]
