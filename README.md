# Agentic RAG (Open Source, Production-Oriented)

This repository provides an end-to-end **agentic RAG** stack using fully open-source building blocks:

- **Agentic orchestration**: LangGraph
- **Reasoning model runtime**: Ollama
- **UI (primary workflow)**: Streamlit
- **Document parsing (with image-aware extraction)**: Docling
- **Vector DB**: FAISS (local file-based)
- **Tracing/observability for LLM flows**: Langfuse (optional)
- **Internet data ingestion**: URL download + local folder storage before indexing

## No-Docker setup (recommended)

You can run everything locally **without Docker**.

### 1) Install and prepare environment

```bash
./setup.sh
```

### 2) Start API + UI

```bash
./start_local.sh
```

Open:

- Streamlit UI (upload here): http://localhost:8501
- API docs: http://localhost:8000/docs

## Use Streamlit for uploading files (recommended)

1. Open **http://localhost:8501**
2. In **Ingest document (UI upload)**, choose your file and click **Ingest file**
3. (Optional) In **Ingest internet URL**, paste URL and click **Download + index URL**
4. Ask questions in **Ask a question**

> API endpoints still exist for automation/integrations, but normal usage should be through Streamlit UI.

## Architecture

1. Upload files from Streamlit UI (or API if needed).
2. Or ingest internet content from Streamlit/API `/ingest/url` (downloads into `data/downloads`).
3. Docling parses source documents into markdown text (image references preserved in parser output).
4. Text is chunked, embedded (SentenceTransformers), and indexed in FAISS.
5. LangGraph agent retrieves top chunks and asks Ollama for grounded answers.
6. Optional traces are sent to Langfuse when keys are configured.

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
- If Ollama is not installed, install from `https://ollama.com/download`.
