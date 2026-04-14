#!/bin/bash
# Post-deploy hook: smoke tests and notifications
set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "[hook] post-deploy: running smoke tests on ${ENVIRONMENT}..."

# Health check
HEALTH_URL="${APP_URL:-http://localhost:8000}/health"
if curl -sf "$HEALTH_URL" >/dev/null 2>&1; then
  echo "[hook] post-deploy: health check passed"
else
  echo "[ALERT] Health check failed on ${ENVIRONMENT}"
  exit 1
fi

echo "[hook] post-deploy: ${ENVIRONMENT} deployment verified"
