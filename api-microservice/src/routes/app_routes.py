# src/routes/app_routes.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.database.session import get_async_session
from src.schemas.app_schema import AppSchema
from src.services.app_service import get_apps_paginated

router = APIRouter(prefix="/apps", tags=["Apps"])


@router.get("/", response_model=List[AppSchema])
async def list_apps(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(20, description="Maximum number of items to return"),
):
    return await get_apps_paginated(session=session, skip=skip, limit=limit)
