import re
from typing import Any


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    metadata: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()
            text = parts[2]
    else:
        metadata_lines = []
        body_lines = []
        in_metadata = True
        for line in text.splitlines():
            if in_metadata and ":" in line and len(line) < 160:
                metadata_lines.append(line)
            else:
                in_metadata = False
                body_lines.append(line)
        for line in metadata_lines:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
        if body_lines:
            text = "\n".join(body_lines)
    return metadata, clean_text(text)


def clean_text(text: str) -> str:
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
