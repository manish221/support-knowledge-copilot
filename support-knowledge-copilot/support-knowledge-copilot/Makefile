.PHONY: install ingest eval test api ui

install:
	pip install -r requirements.txt

ingest:
	python -m app.ingestion.ingest --source data/raw_docs --rebuild

eval:
	python -m app.evaluation.eval --strategy hybrid

test:
	pytest -q

api:
	uvicorn app.main:app --reload --port 8000

ui:
	streamlit run ui/streamlit_app.py
