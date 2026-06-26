from __future__ import annotations
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict
from typing import Any


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_\-\.]+", text.lower())


class SimpleBM25:
    def __init__(self, tokenized_corpus: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.corpus = tokenized_corpus
        self.k1 = k1
        self.b = b
        self.doc_len = [len(doc) for doc in tokenized_corpus]
        self.avgdl = sum(self.doc_len) / max(len(self.doc_len), 1)
        self.term_freqs = [Counter(doc) for doc in tokenized_corpus]
        df = defaultdict(int)
        for doc in tokenized_corpus:
            for term in set(doc):
                df[term] += 1
        n = len(tokenized_corpus)
        self.idf = {term: math.log(1 + (n - freq + 0.5) / (freq + 0.5)) for term, freq in df.items()}

    def get_scores(self, query_tokens: list[str]) -> list[float]:
        scores = []
        for i, tf in enumerate(self.term_freqs):
            score = 0.0
            dl = self.doc_len[i] or 1
            for term in query_tokens:
                if term not in tf:
                    continue
                freq = tf[term]
                idf = self.idf.get(term, 0.0)
                denom = freq + self.k1 * (1 - self.b + self.b * dl / max(self.avgdl, 1))
                score += idf * (freq * (self.k1 + 1) / denom)
            scores.append(score)
        return scores


def build_bm25_index(chunks: list[Any]) -> dict:
    records = []
    for chunk in chunks:
        record = asdict(chunk) if hasattr(chunk, "__dataclass_fields__") else chunk
        records.append(record)
    tokenized = [tokenize(r["text"]) for r in records]
    bm25 = SimpleBM25(tokenized)
    return {"bm25": bm25, "chunk_ids": [r["chunk_id"] for r in records], "tokenized": tokenized}


def sparse_search(question: str, index: dict, top_k: int = 20) -> list[dict]:
    tokens = tokenize(question)
    scores = index["bm25"].get_scores(tokens)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
    max_score = max([float(s) for _, s in ranked] or [1.0]) or 1.0
    return [
        {"chunk_id": index["chunk_ids"][idx], "rank": rank, "score": float(score / max_score), "retriever": "bm25"}
        for rank, (idx, score) in enumerate(ranked, start=1)
    ]
