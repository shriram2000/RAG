#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "[error] .venv not found. Run ./setup_local.sh first."
  exit 1
fi

mkdir -p logs
source .venv/bin/activate

OLLAMA_PID=""
if command -v ollama >/dev/null 2>&1; then
  if ! curl -fsS "http://127.0.0.1:11434/api/tags" >/dev/null 2>&1; then
    nohup ollama serve > logs/ollama.log 2>&1 &
    OLLAMA_PID=$!
    sleep 2
  fi
else
  echo "[warn] Ollama not found in PATH. Ensure an Ollama-compatible endpoint is running."
fi

nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/api.log 2>&1 &
API_PID=$!
nohup streamlit run ui/streamlit_app.py --server.address 0.0.0.0 --server.port 8501 > logs/streamlit.log 2>&1 &
UI_PID=$!

cat > logs/pids.txt <<EOF
OLLAMA_PID=$OLLAMA_PID
API_PID=$API_PID
UI_PID=$UI_PID
EOF

echo "[done] Started local services (no Docker)."
[ -n "$OLLAMA_PID" ] && echo "- Ollama PID: $OLLAMA_PID (logs/ollama.log)"
echo "- API PID:    $API_PID (logs/api.log)"
echo "- UI PID:     $UI_PID (logs/streamlit.log)"
echo "Open: http://localhost:8501"
