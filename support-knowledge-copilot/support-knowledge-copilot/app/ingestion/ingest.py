from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

from app.config import settings
from app.ingestion.loaders import load_document
from app.ingestion.cleaner import parse_front_matter
from app.ingestion.chunker import heading_chunks, fixed_chunks
from app.retrieval.sparse_bm25 import build_bm25_index

SUPPORTED = {".md", ".txt", ".html", ".htm", ".pdf"}


def ingest(source: str, rebuild: bool = False) -> int:
    source_path = Path(source)
    if rebuild and settings.storage_dir.exists():
        shutil.rmtree(settings.storage_dir)
    settings.storage_dir.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    for path in sorted(source_path.rglob("*")):
        if path.suffix.lower() not in SUPPORTED:
            continue
        raw_text = load_document(path)
        metadata, cleaned = parse_front_matter(raw_text)
        doc_id = path.stem.lower().replace(" ", "_")
        metadata = {
            "source_name": metadata.get("source_name", path.stem),
            "document_type": metadata.get("document_type", "unknown"),
            "last_updated": metadata.get("last_updated", "unknown"),
            "access_level": metadata.get("access_level", "public"),
            "product": metadata.get("product", "unknown"),
            "version": metadata.get("version", "unknown"),
            "source_path": str(path),
        }
        all_chunks.extend(heading_chunks(doc_id, cleaned, metadata))
        all_chunks.extend(fixed_chunks(doc_id, cleaned, metadata, size=180, overlap=35))

    with settings.chunk_store_path.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps({"chunk_id": chunk.chunk_id, "text": chunk.text, "metadata": chunk.metadata}) + "\n")

    corpus = [c.text for c in all_chunks]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)
    matrix = vectorizer.fit_transform(corpus)
    nn = NearestNeighbors(metric="cosine", algorithm="brute")
    nn.fit(matrix)
    joblib.dump({"vectorizer": vectorizer, "matrix": matrix, "nn": nn, "chunk_ids": [c.chunk_id for c in all_chunks]}, settings.dense_index_path)

    joblib.dump(build_bm25_index(all_chunks), settings.sparse_index_path)
    return len(all_chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/raw_docs")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    count = ingest(args.source, args.rebuild)
    print(f"Indexed {count} chunks")
