from __future__ import annotations
import re
from app.retrieval.sparse_bm25 import tokenize


def _best_sentences(question: str, chunks: list[dict], max_sentences: int = 4) -> list[tuple[str, str]]:
    q = set(tokenize(question))
    candidates: list[tuple[float, str, str]] = []
    for chunk in chunks:
        sentences = re.split(r"(?<=[.!?])\s+", chunk["text"].strip())
        for sent in sentences:
            terms = set(tokenize(sent))
            score = len(q & terms) / max(len(q), 1)
            if score > 0:
                candidates.append((score, sent.strip(), chunk["chunk_id"]))
    candidates = sorted(candidates, key=lambda x: x[0], reverse=True)
    seen = set()
    selected = []
    for _, sent, cid in candidates:
        key = sent.lower()
        if key not in seen and len(sent) > 20:
            selected.append((sent, cid))
            seen.add(key)
        if len(selected) >= max_sentences:
            break
    return selected


def generate_answer(question: str, chunks: list[dict]) -> dict:
    if not chunks:
        return {
            "answer": "I could not find this in the available support documentation.",
            "what_i_could_not_verify": ["No relevant evidence chunks were retrieved."],
        }

    selected = _best_sentences(question, chunks)
    if not selected:
        closest = ", ".join(c["metadata"].get("section_heading", "Unknown") for c in chunks[:3])
        return {
            "answer": "I could not verify a direct answer from the available documentation.",
            "what_i_could_not_verify": [f"Closest matching sections: {closest}"],
        }

    answer_parts = [f"{sent} [{cid}]" for sent, cid in selected]
    return {
        "answer": " ".join(answer_parts),
        "what_i_could_not_verify": [],
    }
