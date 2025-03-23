from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.app_model import App
from fastapi import HTTPException
from typing import List
from src.schemas.app_schema import AppSchema
from src.core.config import settings

async def get_apps_paginated(
    session: AsyncSession,
    skip: int = 0,
    limit: int = settings.PAGE_SIZE,
) -> List[AppSchema]:
    stmt = select(App).offset(skip).limit(limit)
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
