from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.database.session import get_async_session
from src.schemas.app_schema import AppSchema
from src.services.app_service import (
    get_apps_paginated,
    get_app_by_id,
    get_all_categories,
    get_all_labels,
    search_apps
)

router = APIRouter(prefix="/apps", tags=["Apps"])


@router.get("/", response_model=List[AppSchema])
async def list_apps(
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
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100)
):
    return await get_apps_paginated(
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
    )
    

@router.get("/search", response_model=List[AppSchema])
async def search_apps_route(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    return await search_apps(session, query=q, limit=limit)


@router.get("/{apple_id}", response_model=AppSchema)
async def get_app(apple_id: str, session: AsyncSession = Depends(get_async_session)):
    app = await get_app_by_id(session, apple_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return app


@router.get("/filters/categories", response_model=List[str])
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    return await get_all_categories(session)


@router.get("/filters/labels", response_model=List[str])
async def get_labels(session: AsyncSession = Depends(get_async_session)):
    return await get_all_labels(session)
