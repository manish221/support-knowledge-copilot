from __future__ import annotations
from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse, Citation, ConfidenceBreakdown
from app.retrieval.pipeline import retrieve
from app.retrieval.store import chunk_map
from app.generation.answer_generator import generate_answer
from app.verification.citation_parser import parse_cited_claims
from app.verification.citation_verifier import verify_citations
from app.verification.confidence import score_confidence

app = FastAPI(title="Support Knowledge Copilot", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    retrieved = retrieve(req.question, access_level=req.access_level, strategy=req.strategy, product=req.product)
    generated = generate_answer(req.question, retrieved)
    chunks_by_id = chunk_map()
    cited_claims = parse_cited_claims(generated["answer"])
    verdicts = verify_citations(cited_claims, chunks_by_id)
    confidence = score_confidence(retrieved, verdicts, generated["answer"])

    citations = []
    unverified = list(generated.get("what_i_could_not_verify", []))
    for verdict in verdicts:
        chunk = verdict.get("chunk")
        if not chunk:
            unverified.append(f"Citation {verdict['chunk_id']} was not found.")
            continue
        meta = chunk["metadata"]
        if verdict["verdict"] != "supported":
            unverified.append(f"Claim may not be fully supported by {verdict['chunk_id']}: {verdict['claim']}")
        citations.append(Citation(
            chunk_id=verdict["chunk_id"],
            source=meta.get("source_name", "Unknown"),
            section=meta.get("section_heading", "Unknown"),
            last_updated=meta.get("last_updated", "unknown"),
            document_type=meta.get("document_type", "unknown"),
            support_verdict=verdict["verdict"],
            quote=chunk["text"][:500],
        ))

    return AskResponse(
        answer=generated["answer"],
        citations=citations,
        confidence_score=confidence["confidence_score"],
        confidence_breakdown=ConfidenceBreakdown(**confidence["breakdown"]),
        what_i_could_not_verify=unverified,
        retrieved_chunks=retrieved,
    )
