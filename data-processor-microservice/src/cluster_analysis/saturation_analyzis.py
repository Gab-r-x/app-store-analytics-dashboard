import logging
from collections import Counter
from cluster_analysis.embeddings import generate_all_embeddings
from cluster_analysis.clustering import reduce_embeddings_dimensionality, cluster_embeddings, plot_clusters

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def run_saturation_analysis(n_clusters: int = 8, plot: bool = True):
    logger.info("🔍 Starting saturation analysis pipeline...")

    import asyncio
    labeled_embeddings = asyncio.run(generate_all_embeddings())

    if not labeled_embeddings:
        logger.warning("⚠️ No embeddings found. Exiting.")
        return

    ids = [item["id"] for item in labeled_embeddings]
    embeddings = [item["embedding"] for item in labeled_embeddings]

    # Clustering
    cluster_ids, model = cluster_embeddings(embeddings, n_clusters=n_clusters)

    # Contagem de apps por cluster (saturação)
    saturation_count = Counter(cluster_ids)
    logger.info("📈 Cluster saturation:")
    for cluster_id, count in saturation_count.items():
        logger.info(f"Cluster {cluster_id}: {count} apps")

    # Visualização
    if plot:
        reduced = reduce_embeddings_dimensionality(embeddings)
        plot_clusters(reduced, cluster_ids)

    logger.info("✅ Saturation analysis complete.")

    return {
        "ids": ids,
        "clusters": cluster_ids,
        "saturation": saturation_count
    }
