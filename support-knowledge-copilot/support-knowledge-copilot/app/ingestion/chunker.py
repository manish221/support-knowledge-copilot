from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Any

@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any]


def heading_chunks(doc_id: str, text: str, metadata: dict[str, Any]) -> list[Chunk]:
    lines = text.splitlines()
    chunks: list[Chunk] = []
    current_heading = metadata.get("section_heading", "Introduction")
    buffer: list[str] = []
    index = 0

    def flush() -> None:
        nonlocal index, buffer
        body = "\n".join(buffer).strip()
        if body:
            chunk_meta = {**metadata, "section_heading": current_heading, "chunking_strategy": "heading"}
            chunks.append(Chunk(f"{doc_id}_h_{index:03d}", body, chunk_meta))
            index += 1
        buffer = []

    for line in lines:
        match = re.match(r"^#{1,3}\s+(.*)", line.strip())
        if match:
            flush()
            current_heading = match.group(1).strip()
        else:
            buffer.append(line)
    flush()
    return chunks


def fixed_chunks(doc_id: str, text: str, metadata: dict[str, Any], size: int = 900, overlap: int = 150) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(words):
        end = min(len(words), start + size)
        chunk_text = " ".join(words[start:end])
        chunk_meta = {**metadata, "section_heading": metadata.get("section_heading", "Full Document"), "chunking_strategy": "fixed_overlap"}
        chunks.append(Chunk(f"{doc_id}_f_{index:03d}", chunk_text, chunk_meta))
        if end == len(words):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks
