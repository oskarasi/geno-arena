#!/usr/bin/env bash
# Thin entrypoint for the arena scorer.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/harness/score.py" "$@"
