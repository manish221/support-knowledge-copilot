from __future__ import annotations
import joblib
from app.config import settings


def dense_search(question: str, top_k: int = 20) -> list[dict]:
    index = joblib.load(settings.dense_index_path)
    vector = index["vectorizer"].transform([question])
    distances, indices = index["nn"].kneighbors(vector, n_neighbors=min(top_k, len(index["chunk_ids"])))
    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), start=1):
        results.append({"chunk_id": index["chunk_ids"][idx], "rank": rank, "score": float(1 - dist), "retriever": "dense"})
    return results
