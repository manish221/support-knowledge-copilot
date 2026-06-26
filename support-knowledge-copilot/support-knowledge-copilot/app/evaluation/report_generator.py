from __future__ import annotations
from pathlib import Path
import pandas as pd
from app.evaluation.metrics import source_hit_rate, average_confidence, citation_accuracy


def write_reports(results: list[dict], output_dir: str = "reports") -> dict:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results)
    summary = {
        "questions": len(results),
        "source_hit_rate": source_hit_rate(results),
        "average_confidence": average_confidence(results),
        "citation_accuracy": citation_accuracy(results),
    }
    md_path = Path(output_dir) / "evaluation_report.md"
    html_path = Path(output_dir) / "evaluation_report.html"
    md = ["# Evaluation Report", "", "## Summary", ""]
    for k, v in summary.items():
        md.append(f"- **{k}**: {v}")
    md.extend(["", "## Details", "", df.to_markdown(index=False)])
    md_path.write_text("\n".join(md), encoding="utf-8")
    html_path.write_text(df.to_html(index=False, escape=False), encoding="utf-8")
    return {"summary": summary, "markdown": str(md_path), "html": str(html_path)}
