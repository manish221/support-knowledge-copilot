from __future__ import annotations
from app.retrieval.sparse_bm25 import tokenize

STOP = {"the", "a", "an", "and", "or", "to", "of", "in", "from", "with", "for", "is", "are", "can", "should", "must", "be", "this", "that", "if", "when"}


def content_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in STOP and len(t) > 2}


def verify_claim_against_chunk(claim: str, chunk_text: str) -> dict:
    claim_tokens = content_tokens(claim)
    chunk_tokens = content_tokens(chunk_text)
    if not claim_tokens:
        return {"verdict": "not_found", "support_score": 0.0}
    overlap = len(claim_tokens & chunk_tokens) / max(len(claim_tokens), 1)
    if overlap >= 0.70:
        verdict = "supported"
    elif overlap >= 0.40:
        verdict = "partially_supported"
    else:
        verdict = "unsupported"
    return {"verdict": verdict, "support_score": round(overlap, 3)}


def verify_citations(cited_claims: list[dict], chunks_by_id: dict[str, dict]) -> list[dict]:
    verdicts = []
    for item in cited_claims:
        chunk = chunks_by_id.get(item["chunk_id"])
        if not chunk:
            verdicts.append({**item, "verdict": "not_found", "support_score": 0.0})
            continue
        check = verify_claim_against_chunk(item["claim"], chunk["text"])
        verdicts.append({**item, **check, "chunk": chunk})
    return verdicts
