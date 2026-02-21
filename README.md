# Agentic RAG (Open Source, Production-Oriented)

This repository provides an end-to-end **agentic RAG** stack using fully open-source building blocks:

- **Agentic orchestration**: LangGraph
- **Reasoning model runtime**: Ollama
- **UI (primary workflow)**: Streamlit
- **Document parsing (with image-aware extraction)**: Docling
- **Vector DB**: FAISS
- **Tracing/observability for LLM flows**: Langfuse
- **Internet data ingestion**: URL download + local folder storage before indexing

## One-command setup

Run this script to set up everything (env file, folders, containers, and Ollama model):

```bash
./setup.sh
```

## Use Streamlit for uploading files (recommended)

You asked to upload in the UI. ✅

Use the **Streamlit UI** as the main place to ingest files and URLs:

1. Open **http://localhost:8501**
2. In **Ingest document**, choose your file and click **Ingest file**
3. (Optional) In **Ingest internet URL**, paste URL and click **Download + index URL**
4. Ask questions in **Ask a question**

> The API endpoints still exist for automation/integrations, but for normal usage upload via Streamlit UI.

## Architecture

1. Upload files from Streamlit UI (or API if needed).
2. Or ingest internet content from Streamlit/API `/ingest/url` (downloads into `data/downloads`).
3. Docling parses source documents into markdown text (image references preserved in parser output).
4. Text is chunked, embedded (SentenceTransformers), and indexed in FAISS.
5. LangGraph agent retrieves top chunks and asks Ollama for grounded answers.
6. Optional traces are sent to Langfuse when keys are configured.

## Quickstart

```bash
cp .env.example .env
docker compose up -d --build
```

Pull an Ollama model:

```bash
docker exec -it ollama ollama pull llama3.1:8b
```

Open services:

- API docs: http://localhost:8000/docs
- Streamlit UI (upload here): http://localhost:8501
- Langfuse: http://localhost:3001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## API Endpoints (optional for integrations)

### `POST /ingest`
Upload file and index it.

### `POST /ingest/url`
```json
{ "url": "https://example.com" }
```
Downloads internet content to `data/downloads/` and indexes it.

### `POST /chat`
```json
{ "question": "What does the document say?" }
```

## Notes

- FAISS is local-file backed (`data/index`).
- URL ingestion is useful for building a continuously updated internet-fed knowledge folder.
- For production: move ingestion to background workers and add auth, retry queues, and model/reranker routing.
