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

if [ ! -d "$VENV_DIR" ]; then
  echo "[info] Creating virtual environment at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -e .

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[info] Created .env from .env.example"
else
  echo "[info] Using existing .env"
fi

mkdir -p data/index data/downloads data/uploads data/logs

if ! command -v ollama >/dev/null 2>&1; then
  cat <<'EOF'
[warning] Ollama CLI not found.
Install Ollama from https://ollama.com/download and start it, then run:
  ollama pull llama3.1:8b
EOF
else
  echo "[info] Checking Ollama daemon..."
  if ! curl -fsS "http://localhost:11434/api/tags" >/dev/null 2>&1; then
    echo "[info] Starting ollama service"
    ollama serve >/tmp/ollama.log 2>&1 &
    sleep 2
  fi

  echo "[info] Pulling Ollama model: llama3.1:8b"
  ollama pull llama3.1:8b || true
fi

cat <<'EOF'

[done] Local setup complete (no Docker).
Run services in two terminals:

Terminal 1 (API):
  source .venv/bin/activate
  uvicorn app.main:app --host 0.0.0.0 --port 8000

Terminal 2 (Streamlit UI):
  source .venv/bin/activate
  streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0

Then open:
  - Streamlit UI (upload here): http://localhost:8501
  - API docs:                  http://localhost:8000/docs
EOF
