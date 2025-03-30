from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.app_model import App
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_total_downloads_per_category(session: AsyncSession):
    try:
        stmt = (
            select(App.category, func.sum(App.monthly_downloads_estimate))
            .group_by(App.category)
            .order_by(func.sum(App.monthly_downloads_estimate).desc())
        )
        result = await session.execute(stmt)
        return [
            {"category": row[0], "downloads": row[1]}
            for row in result.all() if row[0]
        ]
    except Exception as e:
        logger.exception("Database query failed")
        raise HTTPException(status_code=500, detail="Failed to load download data")

async def get_total_revenue_per_category(session: AsyncSession):
    stmt = (
        select(App.category, func.sum(App.monthly_revenue_estimate))
        .group_by(App.category)
        .order_by(func.sum(App.monthly_revenue_estimate).desc())
    )
    result = await session.execute(stmt)
    return [{"category": row[0], "revenue": row[1]} for row in result.all() if row[0]]


async def get_mrr_per_download_per_category(session: AsyncSession):
    stmt = (
        select(
            App.category,
            (func.sum(App.monthly_revenue_estimate) / func.nullif(func.sum(App.monthly_downloads_estimate), 0)).label("mrr_download_ratio")
        )
        .group_by(App.category)
        .order_by(func.sum(App.monthly_revenue_estimate).desc())
    )
    result = await session.execute(stmt)
    return [{"category": row[0], "mrr_per_download": row[1]} for row in result.all() if row[0]]
