# Agentic RAG (Local, No-Docker)

This repository provides an end-to-end **agentic RAG** stack that runs locally without Docker:

- **Agentic orchestration**: LangGraph
- **Reasoning model runtime**: Ollama
- **UI (primary workflow)**: Streamlit
- **Document parsing (image-aware)**: Docling
- **Vector DB**: FAISS
- **Tracing hooks**: Langfuse (optional if you run it separately)
- **Internet ingestion**: URL download + local folder indexing

## Setup (no Docker)

```bash
./setup.sh
```

`setup.sh` now uses the no-Docker bootstrap (`setup_local.sh`).

## Run locally

```bash
./run_local.sh
```

## Stop local services

```bash
./stop_local.sh
```

## Open

- Streamlit UI (upload here): http://localhost:8501
- API docs: http://localhost:8000/docs

## Use Streamlit for uploading files

1. Open **http://localhost:8501**
2. In **Ingest document (UI upload)** choose your file and click **Ingest file**
3. (Optional) In **Ingest internet URL**, paste URL and click **Download + index URL**
4. Ask questions in **Ask a question**

## API Endpoints (optional for integrations)

- `POST /ingest`
- `POST /ingest/url`
- `POST /chat`
