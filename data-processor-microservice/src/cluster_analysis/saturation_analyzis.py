import logging
from collections import Counter
from cluster_analysis.embeddings import generate_all_embeddings
from cluster_analysis.clustering import reduce_embeddings_dimensionality, cluster_embeddings, plot_clusters
from cluster_analysis.save_clusters_to_db import save_clusters_to_db
from database.postgres_connection import AsyncSessionLocal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def run_saturation_analysis(n_clusters: int = 50, plot: bool = True):
    logger.info("🔍 Starting saturation analysis pipeline...")

    import asyncio
    labeled_embeddings = asyncio.run(generate_all_embeddings())

    if not labeled_embeddings:
        logger.warning("⚠️ No embeddings found. Exiting.")
        return

    # Extract app IDs and embeddings
    ids = [app.id for app, _ in labeled_embeddings]
    embeddings = [embedding for _, embedding in labeled_embeddings]

    # Cluster the embeddings
    cluster_ids, model = cluster_embeddings(embeddings, n_clusters=n_clusters)

    # Count saturation per cluster
    saturation_count = Counter(cluster_ids)
    logger.info("📈 Cluster saturation:")
    for cluster_id, count in saturation_count.items():
        logger.info(f"Cluster {cluster_id}: {count} apps")

    # Reduce dimensionality to 2D for visualization and DB persistence
    reduced = reduce_embeddings_dimensionality(embeddings)

    # Deactivated to save cpu and memory for now
    # if plot:
    #     plot_clusters(reduced, cluster_ids)

    # Prepare data for DB
    cluster_data = []
    for app_id, cluster_id, coords in zip(ids, cluster_ids, reduced):
        cluster_data.append({
            "app_id": app_id,
            "cluster": int(cluster_id),
            "x": float(coords[0]),
            "y": float(coords[1])
        })

    # Persist to DB
    async def persist():
        async with AsyncSessionLocal() as session:
            await save_clusters_to_db(session, cluster_data)

    asyncio.run(persist())

    logger.info("✅ Saturation analysis complete.")

    return {
        "ids": ids,
        "clusters": cluster_ids,
        "saturation": saturation_count
    }
