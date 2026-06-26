from __future__ import annotations
import joblib
from app.config import settings
from app.retrieval.store import chunk_map
from app.retrieval.dense import dense_search
from app.retrieval.sparse_bm25 import sparse_search
from app.retrieval.fusion import reciprocal_rank_fusion
from app.retrieval.reranker import lexical_rerank

ACCESS_ORDER = {"public": 0, "internal": 1, "restricted": 2}


def allowed(chunk: dict, access_level: str) -> bool:
    need = ACCESS_ORDER.get(chunk["metadata"].get("access_level", "public"), 0)
    have = ACCESS_ORDER.get(access_level, 0)
    return have >= need


def retrieve(question: str, access_level: str = "public", strategy: str = "hybrid", product: str | None = None) -> list[dict]:
    chunks = chunk_map()
    sparse_index = joblib.load(settings.sparse_index_path)

    dense = dense_search(question, settings.top_k_dense)
    sparse = sparse_search(question, sparse_index, settings.top_k_sparse)

    if strategy == "dense":
        candidates = dense
    elif strategy == "sparse":
        candidates = sparse
    else:
        candidates = reciprocal_rank_fusion([dense, sparse], k=settings.rrf_k, weights=[1.0, 1.0])[:25]

    filtered = []
    for item in candidates:
        chunk = chunks[item["chunk_id"]]
        if not allowed(chunk, access_level):
            continue
        if product and product.lower() not in chunk["metadata"].get("product", "").lower():
            continue
        filtered.append(item)
    return lexical_rerank(question, filtered, chunks, top_k=settings.top_k_final)
