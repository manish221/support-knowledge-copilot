# Support Knowledge Copilot with Verified Citations

Enterprise-grade RAG portfolio project for a support knowledge assistant that answers employee/customer support questions using internal-style documentation, returns source citations, verifies whether each cited chunk supports the attached claim, and reports confidence plus what could not be verified.

## What this project demonstrates

- Multi-source document ingestion: Markdown, HTML, TXT, PDF-ready loader interface
- Metadata-first indexing: source, section, date, doc type, product, version, access level
- Multiple chunking strategies: heading-based and fixed-size overlap
- Hybrid retrieval: dense/semantic retrieval + sparse/BM25 retrieval over the same chunk IDs
- Reciprocal Rank Fusion and optional reranking
- Grounded answer generation with citations
- Citation verification after generation
- Confidence scoring and uncertainty handling
- Golden Q&A evaluation suite
- FastAPI backend and Streamlit dashboard
- Docker-ready project structure

## Demo corpus

The sample corpus under `data/raw_docs/` is original, public-demo support documentation created for this project. It is safe to publish and does not contain private company data. The content is modeled after common publicly available support-document patterns such as FAQs, release notes, API guides, onboarding instructions, troubleshooting guides, and support policies.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m app.ingestion.ingest --source data/raw_docs --rebuild
python -m app.evaluation.eval --strategy hybrid
streamlit run ui/streamlit_app.py
```

Optional API:

```bash
uvicorn app.main:app --reload --port 8000
```

## Example API request

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What should I do if I get ERR-429?", "access_level":"public"}'
```

## Repository layout

```text
support-knowledge-copilot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   ├── verification/
│   └── evaluation/
├── data/
│   ├── raw_docs/
│   └── golden_qa/
├── ui/
├── reports/
├── scripts/
├── tests/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Interview talking point

Dense and sparse indexes are built over the same chunk IDs so retrieval fusion, metadata filtering, citation rendering, access control, and evaluation all operate on one canonical evidence object. Dense retrieval handles semantic intent; BM25 handles exact phrases, API names, SKUs, and error codes.
