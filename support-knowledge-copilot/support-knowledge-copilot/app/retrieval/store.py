from __future__ import annotations
import json
from app.config import settings


def load_chunks() -> list[dict]:
    if not settings.chunk_store_path.exists():
        raise FileNotFoundError("Chunk store not found. Run: python -m app.ingestion.ingest --source data/raw_docs --rebuild")
    with settings.chunk_store_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def chunk_map() -> dict[str, dict]:
    return {c["chunk_id"]: c for c in load_chunks()}
