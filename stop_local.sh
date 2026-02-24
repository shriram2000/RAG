#!/usr/bin/env bash
set -euo pipefail

if [ ! -f logs/pids.txt ]; then
  echo "[info] logs/pids.txt not found; nothing to stop."
  exit 0
fi

source logs/pids.txt || true

for pid in ${OLLAMA_PID:-} ${API_PID:-} ${UI_PID:-}; do
  if [ -n "${pid:-}" ] && kill -0 "$pid" >/dev/null 2>&1; then
    kill "$pid" || true
    echo "[info] Stopped PID $pid"
  fi
done

echo "[done] Stop signal sent."
