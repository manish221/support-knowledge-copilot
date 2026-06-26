from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix in {".html", ".htm"}:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        return soup.get_text("\n")
    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError("pypdf is required to read PDFs")
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError(f"Unsupported file type: {path}")
