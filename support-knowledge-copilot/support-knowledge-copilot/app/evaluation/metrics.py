from __future__ import annotations


def source_hit_rate(results: list[dict]) -> float:
    if not results:
        return 0.0
    hits = sum(1 for row in results if row["source_hit"])
    return round(hits / len(results), 3)


def average_confidence(results: list[dict]) -> float:
    if not results:
        return 0.0
    return round(sum(row["confidence"] for row in results) / len(results), 3)


def citation_accuracy(results: list[dict]) -> float:
    total = sum(row["citation_total"] for row in results)
    if total == 0:
        return 0.0
    supported = sum(row["citation_supported"] for row in results)
    return round(supported / total, 3)
