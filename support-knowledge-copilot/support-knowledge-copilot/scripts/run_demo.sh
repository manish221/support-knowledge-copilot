#!/usr/bin/env bash
set -e
python -m app.ingestion.ingest --source data/raw_docs --rebuild
python -m app.evaluation.eval --strategy hybrid
streamlit run ui/streamlit_app.py
