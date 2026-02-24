#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-.venv}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "[error] python3 is required but not installed."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[info] Created .env from .env.example"
else
  echo "[info] Using existing .env"
fi

mkdir -p data/index data/downloads data/uploads logs

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  echo "[info] Created virtualenv at $VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e .

if command -v ollama >/dev/null 2>&1; then
  echo "[info] Pulling Ollama model: llama3.1:8b"
  ollama pull llama3.1:8b || true
else
  echo "[warn] Ollama CLI not found. Install from https://ollama.com/download"
  echo "[warn] Then run: ollama pull llama3.1:8b"
fi

cat <<'EOF'

[done] Local setup complete (no Docker).

Start everything:
  ./run_local.sh

Stop everything:
  ./stop_local.sh

Open:
  - Streamlit UI (upload here): http://localhost:8501
  - API docs:                  http://localhost:8000/docs

Optional observability services (Langfuse/Prometheus/Grafana) are not started in no-Docker mode.
EOF
