from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
import logging

from src.models.app_model import App
from src.models.app_cluster import AppCluster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_total_downloads_per_category(session: AsyncSession):
    try:
        stmt = (
            select(App.category, func.sum(App.monthly_downloads_estimate))
            .where(App.active == True)
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
        .where(App.active == True)
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
        .where(App.active == True)
        .group_by(App.category)
        .order_by(func.sum(App.monthly_revenue_estimate).desc())
    )
    result = await session.execute(stmt)
    return [{"category": row[0], "mrr_per_download": row[1]} for row in result.all() if row[0]]


async def get_cluster_points(session: AsyncSession):
    try:
        stmt = (
            select(
                AppCluster.app_id,
                AppCluster.cluster,
                AppCluster.x,
                AppCluster.y,
                App.name,
                App.rank,
                App.category,
                App.list_type
            )
            .join(App, AppCluster.app_id == App.id)
        )
        result = await session.execute(stmt)
        return [
            {
                "app_id": row.app_id,
                "cluster": row.cluster,
                "x": row.x,
                "y": row.y,
                "name": row.name,
                "rank": row.rank,
                "category": row.category,
                "list_type": row.list_type
            }
            for row in result.fetchall()
        ]
    except Exception as e:
        logger.error("❌ Failed to fetch cluster points", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch cluster points")
