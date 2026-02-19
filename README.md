# Agentic RAG (Open Source, Production-Oriented)

This repository provides an end-to-end **agentic RAG** blueprint where every major runtime component is open source and deployable in production.

## What is included

- **API + orchestration**: FastAPI + LangGraph
- **LLM runtime**: Ollama (e.g., Llama 3.1 model)
- **Embeddings**: SentenceTransformers (BGE family)
- **Vector database**: Qdrant
- **State/cache**: Redis
- **Metadata DB**: PostgreSQL
- **Object storage**: MinIO
- **Observability**: Prometheus + Grafana
- **Container orchestration (local/prod-like)**: Docker Compose

## Architecture

1. Documents are uploaded to `/ingest`.
2. The API extracts text, chunks it, generates embeddings, and stores vectors in Qdrant.
3. User questions hit `/chat`.
4. A LangGraph agent executes:
   - Retrieve relevant chunks from Qdrant.
   - Grounded generation through Ollama.
5. API returns an answer + source attribution.

## Quickstart

```bash
cp .env.example .env

docker compose up -d --build
```

Pull a model in Ollama:

```bash
docker exec -it ollama ollama pull llama3.1:8b
```

API docs:
- http://localhost:8000/docs

Prometheus:
- http://localhost:9090

Grafana:
- http://localhost:3000

## Production notes

- Replace Compose with Kubernetes (Helm/Kustomize).
- Add authn/authz (OIDC/API keys + tenant isolation).
- Add background workers (Celery/Arq) for ingestion and retries.
- Configure Qdrant replication/sharding and backups.
- Use TLS and secrets manager (Vault/SOPS/KMS).
- Add reranker and guardrails (e.g., bge-reranker + policy checks).
- Add trace telemetry (OpenTelemetry + Tempo/Jaeger).

## API

### `POST /ingest`
Upload a PDF and index chunks.

### `POST /chat`
```json
{ "question": "What does the policy say about retention?" }
```

Returns:
```json
{
  "answer": "...",
  "sources": ["policy.pdf"]
}
```
