# import logging
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import func, and_
# from src.models.app_model import App
# from src.schemas.app_schema import AppSchema
# from fastapi import HTTPException
# from typing import List

# logger = logging.getLogger(__name__)

# async def search_apps(session: AsyncSession, query: str, limit: int = 20) -> List[AppSchema]:
#     ts_query = func.websearch_to_tsquery("english", query)

#     stmt = (
#         select(App)
#         .where(
#             and_(
#                 App.search_vector.op("@@")(ts_query),
#             )
#         )
#         .limit(limit)
#     )

#     logger.info(f"[SEARCH] Executing query: websearch_to_tsquery('english', '{query}')")

#     result = await session.execute(stmt)
#     apps = result.scalars().all()

#     logger.info(f"[SEARCH] {len(apps)} apps found for query: '{query}'")

#     if not apps:
#         raise HTTPException(status_code=404, detail="No apps found matching the search criteria.")

#     return [AppSchema.model_validate(app) for app in apps]
