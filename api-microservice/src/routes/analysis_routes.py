from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_async_session
from src.services.analysis_service import (
    get_total_downloads_per_category,
    get_total_revenue_per_category,
    get_mrr_per_download_per_category,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/downloads")
async def analysis_downloads(session: AsyncSession = Depends(get_async_session)):
    return await get_total_downloads_per_category(session)


@router.get("/revenue")
async def analysis_revenue(session: AsyncSession = Depends(get_async_session)):
    return await get_total_revenue_per_category(session)


@router.get("/mrr-downloads")
async def analysis_mrr_per_download(session: AsyncSession = Depends(get_async_session)):
    return await get_mrr_per_download_per_category(session)
