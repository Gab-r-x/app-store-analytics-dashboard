# src/services/app_service.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.app_model import App
from fastapi import HTTPException
from typing import List
from src.schemas.app_schema import AppSchema

async def get_apps_paginated(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 20,
) -> List[AppSchema]:
    stmt = select(App).offset(skip).limit(limit)
    result = await session.execute(stmt)
    apps = result.scalars().all()

    if not apps:
        raise HTTPException(status_code=404, detail="No apps found.")

    return [AppSchema.from_orm(app) for app in apps]
