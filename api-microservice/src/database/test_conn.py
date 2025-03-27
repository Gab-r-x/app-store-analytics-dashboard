import asyncio
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from session import async_engine

async def test_connection():
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Connected to DB")
    except SQLAlchemyError as e:
        print("❌ DB connection error:", str(e))

if __name__ == "__main__":
    asyncio.run(test_connection())
