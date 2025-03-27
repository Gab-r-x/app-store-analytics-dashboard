from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Literal
from src.database.session import get_async_session
from src.schemas.app_schema import AppSchema
from src.services.app_service import (
    get_apps_paginated,
    get_app_by_id,
    get_all_categories,
    get_all_labels,
    search_apps
)
from slowapi.extension import Limiter as LimiterExtension

# Rate limiter instance (already attached in main)
limiter: LimiterExtension

router = APIRouter(prefix="/apps", tags=["Apps"])

@router.get("/", response_model=dict)
@limiter.limit("30/minute")
async def list_apps(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    category: Optional[str] = Query(None),
    label: Optional[str] = Query(None),
    has_in_app_purchases: Optional[bool] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    downloads_min: Optional[float] = Query(None),
    downloads_max: Optional[float] = Query(None),
    revenue_min: Optional[float] = Query(None),
    revenue_max: Optional[float] = Query(None),
    screenshots_min: Optional[int] = Query(None),
    rating_min: Optional[float] = Query(None),
    list_type: Optional[str] = Query(None),
    sort_by: Optional[Literal["name", "rank", "downloads", "revenue"]] = Query(None),
    sort_order: Optional[Literal["asc", "desc"]] = Query("desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100)
):
    total, apps = await get_apps_paginated(
        session=session,
        skip=skip,
        limit=limit,
        category=category,
        label=label,
        has_in_app_purchases=has_in_app_purchases,
        price_min=price_min,
        price_max=price_max,
        downloads_min=downloads_min,
        downloads_max=downloads_max,
        revenue_min=revenue_min,
        revenue_max=revenue_max,
        screenshots_min=screenshots_min,
        rating_min=rating_min,
        list_type=list_type,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return {"total": total, "apps": apps}


@router.get("/search")
@limiter.limit("15/minute")
async def search_apps_route(
    request: Request,
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, le=100),
    skip: int = Query(0),
    session: AsyncSession = Depends(get_async_session),
):
    return await search_apps(session, query=q, limit=limit, skip=skip)


@router.get("/{apple_id}", response_model=AppSchema)
@limiter.limit("60/minute")
async def get_app(
    request: Request,
    apple_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    app = await get_app_by_id(session, apple_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return app


@router.get("/filters/categories", response_model=List[str])
@limiter.limit("20/minute")
async def get_categories(request: Request, session: AsyncSession = Depends(get_async_session)):
    return await get_all_categories(session)


@router.get("/filters/labels", response_model=List[str])
@limiter.limit("20/minute")
async def get_labels(request: Request, session: AsyncSession = Depends(get_async_session)):
    return await get_all_labels(session)
