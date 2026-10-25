#!/bin/bash
# Usage: ./run.sh <path-to-gateway-checkout-at-v0.1.0>
# Measures v0.1.0 with a hanging plugin: one hung request, then 45 concurrent hung requests.
# Needs the checkout's virtual environment (pip install -e ".[test]"), curl and Linux /proc.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$1"
start() { # port, hang seconds
  HANG_SECONDS=$2 PYTHONPATH="$HERE" GATEWAY_CONFIG="$HERE/hanging.json" \
    .venv/bin/python -m uvicorn gateway.main:create_app --factory --port "$1" > "$HERE/server-$1.log" 2>&1 &
  P=$!
  for i in $(seq 30); do curl -s -o /dev/null "localhost:$1/health" && break; sleep 0.3; done
}
chat() { curl -s -o /dev/null -w "HTTP %{http_code} in %{time_total}s (curl exit %{exitcode})\n" --max-time "$3" \
  -H 'content-type: application/json' -d "{\"messages\":[{\"role\":\"user\",\"content\":\"$2\"}]}" "localhost:$1/v1/chat/completions"; }
health() { curl -s -o /dev/null -w "HTTP %{http_code} in %{time_total}s (curl exit %{exitcode})\n" --max-time 10 "localhost:$1/health"; }

echo "v0.1.0 at $(git rev-parse --short HEAD), $(.venv/bin/python --version)"
echo "== one hung request (plugin sleeps 60 s, client limit 10 s)"
start 8765 60
chat 8765 hang 10 > "$HERE/one-chat.txt" &
C=$!
sleep 1
echo -n "health during the hang: "; health 8765
wait $C; echo -n "hung request: "; cat "$HERE/one-chat.txt"
kill -9 $P; wait $P 2>/dev/null

echo "== 45 concurrent hung requests (plugin sleeps 30 s), then health and a healthy request (limit 10 s)"
start 8766 30
for i in $(seq 45); do chat 8766 hang 40 > /dev/null & done
sleep 2
echo -n "health: "; health 8766
echo -n "healthy request: "; chat 8766 hello 10
echo "server threads: $(ls /proc/$P/task | wc -l)"
kill -9 $P; wait 2>/dev/null
rm -f "$HERE/one-chat.txt"
