# src/routes/app_routes.py (continuado)

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.database.session import get_async_session
from src.schemas.app_schema import AppSchema
from src.services.app_service import get_apps_paginated, get_app_by_id

router = APIRouter(prefix="/apps", tags=["Apps"])


@router.get("/", response_model=List[AppSchema])
async def list_apps(
    session: AsyncSession = Depends(get_async_session),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100)
):
    return await get_apps_paginated(session, skip=skip, limit=limit)


@router.get("/{apple_id}", response_model=AppSchema)
async def get_app(apple_id: str, session: AsyncSession = Depends(get_async_session)):
    app = await get_app_by_id(session, apple_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return app
