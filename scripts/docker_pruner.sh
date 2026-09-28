#!/usr/bin/env bash
set -e

echo "[Docker Pruner] Started background monitoring daemon..."
while true; do
  USAGE=$(df / | awk 'NR==2 {gsub("%",""); print $5}')
  if [ "$USAGE" -gt 60 ]; then
    echo "[Docker Pruner] Disk usage is at ${USAGE}%. Auto-pruning finished containers and unused images..."
    docker container prune -f || true
    docker image prune -a -f --filter "until=3m" || docker image prune -a -f || true
  fi
  sleep 25
done
