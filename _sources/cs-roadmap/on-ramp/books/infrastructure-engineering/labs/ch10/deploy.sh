#!/usr/bin/env bash
# Replace the running tinyapp container with a new image.
# If the new one is not healthy in time, put the old one back.
set -euo pipefail

NEW_IMAGE="$1"
NAME="tinyapp"

start() {
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker run -d --name "$NAME" -p 8080:8000 \
    -e APP_VERSION="${1##*:}" "$1" >/dev/null
}

wait_until_healthy() {
  for _ in $(seq 1 30); do
    status="$(docker inspect --format '{{.State.Health.Status}}' "$NAME")"
    echo "  health: $status"
    case "$status" in
      healthy) return 0 ;;
      unhealthy) return 1 ;;
    esac
    sleep 2
  done
  return 1
}

OLD_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$NAME" 2>/dev/null || true)"
echo "Running now: ${OLD_IMAGE:-nothing}"
echo "Deploying:   $NEW_IMAGE"
start "$NEW_IMAGE"

if wait_until_healthy; then
  echo "Deploy succeeded: $NEW_IMAGE is healthy"
  exit 0
fi

echo "Deploy FAILED: $NEW_IMAGE is not healthy"
if [ -n "$OLD_IMAGE" ]; then
  echo "Rolling back to $OLD_IMAGE"
  start "$OLD_IMAGE"
  wait_until_healthy && echo "Rollback succeeded"
fi
exit 1
