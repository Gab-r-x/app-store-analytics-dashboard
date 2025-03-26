from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.app_model import App


async def get_total_downloads_per_category(session: AsyncSession):
    stmt = (
        select(App.category, func.sum(App.monthly_downloads_estimate))
        .group_by(App.category)
        .order_by(func.sum(App.monthly_downloads_estimate).desc())
    )
    result = await session.execute(stmt)
    return [{"category": row[0], "downloads": row[1]} for row in result.all() if row[0]]


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
