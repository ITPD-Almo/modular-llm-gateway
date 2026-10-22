#!/bin/bash
# Usage: ./run.sh <config-name>
# Starts the LiteLLM proxy with config-<name>.yaml, sends the setup guide's request twice, then stops it.
# Needs `pip install 'litellm[proxy]'`. Set TIMEOUT to change the curl limit (default 20 s).
cd "$(dirname "$0")"
LITELLM_MASTER_KEY=sk-local-check litellm --config "config-$1.yaml" --port 4011 > "proxy-$1.log" 2>&1 &
P=$!
for i in $(seq 60); do curl -s -o /dev/null localhost:4011/health/liveliness && break; sleep 1; done
for n in 1 2; do
  curl -s -m "${TIMEOUT:-20}" -D "hdr-$1-$n.txt" -o "body-$1-$n.json" -w "HTTP %{http_code} in %{time_total}s\n" \
    -X POST localhost:4011/v1/chat/completions -H "Authorization: Bearer sk-local-check" -H "Content-Type: application/json" \
    -d '{"model":"fake","messages":[{"role":"user","content":"hello"}]}'
done
kill "$P"
