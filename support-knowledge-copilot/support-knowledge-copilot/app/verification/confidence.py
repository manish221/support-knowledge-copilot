from __future__ import annotations


def score_confidence(retrieved_chunks: list[dict], citation_verdicts: list[dict], answer: str) -> dict:
    retrieval_score = 0.0
    if retrieved_chunks:
        retrieval_score = min(1.0, max(float(c.get("rerank_score", 0.0)) for c in retrieved_chunks) * 10)

    if citation_verdicts:
        supported = sum(1 for v in citation_verdicts if v["verdict"] == "supported")
        partial = sum(1 for v in citation_verdicts if v["verdict"] == "partially_supported")
        citation_support_rate = (supported + 0.5 * partial) / len(citation_verdicts)
    else:
        citation_support_rate = 0.0

    answer_completeness = 0.85 if len(answer.split()) >= 20 else 0.45
    no_answer_risk = 0.85 if "could not" in answer.lower() else max(0.0, 1.0 - retrieval_score)

    final = (
        0.35 * retrieval_score
        + 0.35 * citation_support_rate
        + 0.20 * answer_completeness
        + 0.10 * (1.0 - no_answer_risk)
    )
    return {
        "confidence_score": round(final, 3),
        "breakdown": {
            "retrieval_score": round(retrieval_score, 3),
            "citation_support_rate": round(citation_support_rate, 3),
            "answer_completeness": round(answer_completeness, 3),
            "no_answer_risk": round(no_answer_risk, 3),
        },
    }
