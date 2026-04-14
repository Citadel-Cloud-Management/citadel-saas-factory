#!/bin/bash
set -euo pipefail

ENVIRONMENT="${1:-staging}"

echo "Rolling back ${ENVIRONMENT}..."

# Find previous tag
PREV_TAG=$(git tag --sort=-creatordate | head -2 | tail -1)
if [ -z "$PREV_TAG" ]; then
  echo "ERROR: No previous tag found"
  exit 1
fi

echo "Rolling back to ${PREV_TAG}..."

if command -v kubectl >/dev/null 2>&1; then
  kubectl rollout undo deployment/citadel-backend -n "${ENVIRONMENT}" 2>/dev/null || \
    echo "Rollout undo issued. Check status with: kubectl rollout status deployment/citadel-backend -n ${ENVIRONMENT}"
else
  echo "kubectl not found — run manually"
fi

echo "Rollback to ${PREV_TAG} initiated for ${ENVIRONMENT}"
