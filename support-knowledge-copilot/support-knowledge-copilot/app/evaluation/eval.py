from __future__ import annotations
import argparse
import json
from pathlib import Path
from app.main import ask
from app.schemas import AskRequest
from app.evaluation.report_generator import write_reports


def load_golden(path: str) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run_eval(strategy: str = "hybrid", golden_path: str = "data/golden_qa/golden_questions.jsonl") -> dict:
    rows = []
    for item in load_golden(golden_path):
        response = ask(AskRequest(question=item["question"], strategy=strategy, access_level="internal"))
        retrieved_sources = {c["metadata"].get("source_name") for c in response.retrieved_chunks}
        expected = set(item.get("expected_chunks", []))
        source_hit = True if not expected else bool(expected & retrieved_sources)
        citation_total = len(response.citations)
        citation_supported = sum(1 for c in response.citations if c.support_verdict == "supported")
        rows.append({
            "question": item["question"],
            "answer_type": item["answer_type"],
            "source_hit": source_hit,
            "expected_sources": ", ".join(expected),
            "retrieved_sources": ", ".join(sorted(retrieved_sources)),
            "confidence": response.confidence_score,
            "citation_total": citation_total,
            "citation_supported": citation_supported,
            "answer": response.answer,
        })
    return write_reports(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="hybrid", choices=["hybrid", "dense", "sparse"])
    parser.add_argument("--golden", default="data/golden_qa/golden_questions.jsonl")
    args = parser.parse_args()
    result = run_eval(args.strategy, args.golden)
    print(json.dumps(result["summary"], indent=2))
    print(f"Markdown report: {result['markdown']}")
    print(f"HTML report: {result['html']}")
