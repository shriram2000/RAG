#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "[error] .venv not found. Run ./setup.sh first."
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate
mkdir -p data/logs

pkill -f "uvicorn app.main:app" >/dev/null 2>&1 || true
pkill -f "streamlit run ui/streamlit_app.py" >/dev/null 2>&1 || true

nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > data/logs/api.log 2>&1 &
nohup streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 > data/logs/streamlit.log 2>&1 &

echo "[done] Started local services (no Docker)."
echo "  - Streamlit UI: http://localhost:8501"
echo "  - API docs: http://localhost:8000/docs"
echo "  - API log: data/logs/api.log"
echo "  - UI log: data/logs/streamlit.log"
