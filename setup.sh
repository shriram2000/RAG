#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "[error] docker is required but not installed."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "[error] docker compose plugin is required but not available."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[info] Created .env from .env.example"
else
  echo "[info] Using existing .env"
fi

mkdir -p data/index data/downloads data/uploads

echo "[info] Starting all services (build + up)..."
docker compose up -d --build

echo "[info] Waiting for Ollama API..."
for _ in $(seq 1 40); do
  if curl -fsS "http://localhost:11434/api/tags" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

echo "[info] Pulling Ollama model: llama3.1:8b"
docker exec ollama ollama pull llama3.1:8b || true

echo

echo "[done] Setup complete. Open:"
echo "  - Streamlit UI (upload here): http://localhost:8501"
echo "  - API docs:                  http://localhost:8000/docs"
echo "  - Langfuse:                  http://localhost:3001"
echo "  - Prometheus:                http://localhost:9090"
echo "  - Grafana:                   http://localhost:3000"
