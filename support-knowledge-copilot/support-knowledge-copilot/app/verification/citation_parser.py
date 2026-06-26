from __future__ import annotations
import re


def parse_cited_claims(answer: str) -> list[dict]:
    pattern = re.compile(r"([^.!?]+[.!?]?)\s*\[([^\]]+)\]")
    claims = []
    for match in pattern.finditer(answer):
        claims.append({"claim": match.group(1).strip(), "chunk_id": match.group(2).strip()})
    return claims
