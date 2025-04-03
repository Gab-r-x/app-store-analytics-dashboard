import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import AppCluster

logger = logging.getLogger(__name__)

async def save_clusters_to_db(session: AsyncSession, cluster_data: list[dict]):
    """
    Save clustering results into the app_clusters table.

    Each entry should have: app_id, cluster, x, y
    """
    logger.info(f"💾 Saving {len(cluster_data)} cluster entries to the database...")

    try:
        for entry in cluster_data:
            stmt = insert(AppCluster).values(**entry).on_conflict_do_update(
                index_elements=[AppCluster.app_id],
                set_={
                    "cluster": entry["cluster"],
                    "x": entry["x"],
                    "y": entry["y"],
                }
            )
            await session.execute(stmt)

        await session.commit()
        logger.info("✅ Cluster data committed to database.")
    except Exception as e:
        logger.error(f"❌ Failed to save cluster data: {e}")
        await session.rollback()
