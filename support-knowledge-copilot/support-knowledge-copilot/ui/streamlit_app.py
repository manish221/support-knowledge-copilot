from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.main import ask
from app.schemas import AskRequest
from app.ingestion.ingest import ingest

st.set_page_config(page_title="Support Knowledge Copilot", layout="wide")
st.title("Support Knowledge Copilot with Verified Citations")
st.caption("Hybrid RAG + citation verification + confidence scoring")

with st.sidebar:
    st.header("Controls")
    strategy = st.selectbox("Retrieval strategy", ["hybrid", "dense", "sparse"])
    access_level = st.selectbox("Access level", ["public", "internal", "restricted"], index=1)
    if st.button("Rebuild index"):
        count = ingest("data/raw_docs", rebuild=True)
        st.success(f"Indexed {count} chunks")

question = st.text_input("Ask a support question", "What should I do if I get ERR-429?")

if st.button("Ask"):
    try:
        response = ask(AskRequest(question=question, strategy=strategy, access_level=access_level))
        st.subheader("Answer")
        st.write(response.answer)
        st.metric("Confidence", response.confidence_score)

        st.subheader("What I could not verify")
        if response.what_i_could_not_verify:
            for item in response.what_i_could_not_verify:
                st.warning(item)
        else:
            st.success("All cited claims were verified as supported.")

        st.subheader("Citations")
        citation_rows = [c.model_dump() for c in response.citations]
        st.dataframe(pd.DataFrame(citation_rows), use_container_width=True)

        st.subheader("Retrieved Evidence Chunks")
        for chunk in response.retrieved_chunks:
            meta = chunk["metadata"]
            with st.expander(f"{chunk['chunk_id']} | {meta.get('source_name')} | {meta.get('section_heading')}"):
                st.write(chunk["text"])
                st.json({k: v for k, v in meta.items() if k != "source_path"})
                st.write({"rrf_or_score": chunk.get("score"), "rerank_score": chunk.get("rerank_score")})
    except Exception as exc:
        st.error(str(exc))
        st.info("Run: python -m app.ingestion.ingest --source data/raw_docs --rebuild")
