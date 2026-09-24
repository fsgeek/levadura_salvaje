#!/bin/bash
# Run a levadura-salvaje job against our own Qwen llama-server, inside an
# ayllu-gpu lease (Hamut'ay's GPU orchestrator). Never touches the resident's
# server on 8081; `ayllu-gpu run` rests the resident and stops it for us.
#
# Usage: scripts/qwen_under_lease.sh <ttl> "<purpose>" <command...>
#   e.g. scripts/qwen_under_lease.sh 2h "qwen second judge: ~2,000 tax-regulation classifications" \
#          uv run python scripts/measure_currency_qwen.py http://127.0.0.1:8091
set -euo pipefail
TTL=$1; PURPOSE=$2; shift 2
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
exec /home/tony/projects/hamutay/deploy/ayllu-gpu run --holder levadura-salvaje --purpose "$PURPOSE" --ttl "$TTL" -- \
  bash -c '
    set -euo pipefail
    cd "'"$ROOT"'"
    /home/tony/src/llama.cpp/build/bin/llama-server \
      -m /home/tony/models/Qwen3.8-27B-GGUF/Qwen3.8-27B-Q4_K_M.gguf --alias qwen3.8-27b-q4km \
      -ngl 99 -c 65536 -np 2 -fa on --jinja --host 127.0.0.1 --port 8091 > /tmp/levadura-llama-server.log 2>&1 &
    SERVER=$!
    trap "kill $SERVER 2>/dev/null; wait $SERVER 2>/dev/null || true" EXIT
    for i in $(seq 1 180); do
      curl -sf http://127.0.0.1:8091/v1/models >/dev/null && break
      kill -0 $SERVER 2>/dev/null || { echo "llama-server died"; tail -20 /tmp/levadura-llama-server.log; exit 1; }
      sleep 2
    done
    curl -sf http://127.0.0.1:8091/v1/models >/dev/null || { echo "llama-server not ready"; exit 1; }
    "$@"
  ' _ "$@"
