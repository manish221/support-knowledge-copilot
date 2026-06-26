from __future__ import annotations
import re
from app.retrieval.sparse_bm25 import tokenize


def lexical_rerank(question: str, candidates: list[dict], chunks_by_id: dict[str, dict], top_k: int = 5) -> list[dict]:
    q_tokens = set(tokenize(question))
    ranked = []
    for item in candidates:
        chunk = chunks_by_id[item["chunk_id"]]
        c_tokens = set(tokenize(chunk["text"]))
        overlap = len(q_tokens & c_tokens) / max(len(q_tokens), 1)
        final_score = 0.75 * float(item.get("score", 0)) + 0.25 * overlap
        ranked.append({**item, "rerank_score": final_score, "text": chunk["text"], "metadata": chunk["metadata"]})
    return sorted(ranked, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
