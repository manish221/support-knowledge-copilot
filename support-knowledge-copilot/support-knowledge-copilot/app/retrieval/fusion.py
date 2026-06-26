from __future__ import annotations
from collections import defaultdict


def reciprocal_rank_fusion(result_lists: list[list[dict]], k: int = 60, weights: list[float] | None = None) -> list[dict]:
    weights = weights or [1.0] * len(result_lists)
    scores = defaultdict(float)
    detail = defaultdict(list)
    for list_idx, results in enumerate(result_lists):
        for item in results:
            contribution = weights[list_idx] * (1.0 / (k + item["rank"]))
            scores[item["chunk_id"]] += contribution
            detail[item["chunk_id"]].append({"retriever": item["retriever"], "rank": item["rank"], "score": item["score"]})
    fused = [{"chunk_id": cid, "score": score, "rank_detail": detail[cid]} for cid, score in scores.items()]
    return sorted(fused, key=lambda x: x["score"], reverse=True)
