#!/usr/bin/env bash
set -euo pipefail

# Docker-free setup entrypoint.
# Kept as the main command for convenience.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

exec ./setup_local.sh
