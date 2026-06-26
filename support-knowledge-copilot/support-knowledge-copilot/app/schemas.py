from typing import Any, Optional
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str
    access_level: str = "public"
    product: Optional[str] = None
    strategy: str = "hybrid"

class Citation(BaseModel):
    chunk_id: str
    source: str
    section: str
    last_updated: str
    document_type: str
    support_verdict: str
    quote: str

class ConfidenceBreakdown(BaseModel):
    retrieval_score: float
    citation_support_rate: float
    answer_completeness: float
    no_answer_risk: float

class AskResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    confidence_score: float
    confidence_breakdown: ConfidenceBreakdown
    what_i_could_not_verify: list[str] = Field(default_factory=list)
    retrieved_chunks: list[dict[str, Any]] = Field(default_factory=list)
