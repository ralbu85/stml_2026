#!/usr/bin/env bash
# serve.sh — idempotent static server for the STML course site (_site) on
# 127.0.0.1:20026. The tailscale node "stml" proxies this port. No-ops if
# already running; referenced from tailscale-nodes/start.sh for restarts.
set -euo pipefail
cd "$(dirname "$0")"
PORT=20026

if curl -sf -o /dev/null "http://127.0.0.1:$PORT/"; then
    echo "stml site: already serving on :$PORT"
    exit 0
fi

[ -d _site ] || ./build.sh
nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory _site \
    > server.log 2>&1 &
echo "stml site: serving _site on http://127.0.0.1:$PORT (pid $!)"
