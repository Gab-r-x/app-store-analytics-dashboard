from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_async_session
from src.services.analysis_service import (
    get_total_downloads_per_category,
    get_total_revenue_per_category,
    get_mrr_per_download_per_category,
)
from slowapi.extension import Limiter as LimiterExtension


limiter: LimiterExtension


router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/downloads")
@limiter.limit("20/minute")
async def analysis_downloads(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    return await get_total_downloads_per_category(session)


@router.get("/revenue")
@limiter.limit("20/minute")
async def analysis_revenue(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    return await get_total_revenue_per_category(session)


@router.get("/mrr-downloads")
@limiter.limit("20/minute")
async def analysis_mrr_per_download(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    return await get_mrr_per_download_per_category(session)
