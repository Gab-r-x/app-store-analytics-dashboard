import logging
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def reduce_embeddings_dimensionality(embeddings: list[list[float]], n_components: int = 2) -> np.ndarray:
    """Reduz a dimensionalidade dos embeddings para visualização."""
    logger.info(f"📉 Reducing embeddings from {len(embeddings[0])}D to {n_components}D with PCA...")
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(embeddings)
    logger.info("✅ PCA reduction complete.")
    return reduced

def cluster_embeddings(embeddings: list[list[float]], n_clusters: int = 8):
    """Aplica KMeans clustering nos embeddings."""
    logger.info(f"🔍 Clustering {len(embeddings)} embeddings into {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_ids = kmeans.fit_predict(embeddings)
    logger.info("✅ Clustering complete.")
    return cluster_ids, kmeans

def plot_clusters(reduced_embeddings: np.ndarray, cluster_ids: list[int], title="Cluster Visualization"):
    """Gera e exibe um gráfico 2D dos clusters."""
    logger.info("📊 Plotting clusters...")
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=cluster_ids, cmap="tab10", alpha=0.7)
    plt.title(title)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar(scatter)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
