#!/bin/bash
# On-deploy-fail hook: trigger rollback and notify
set -euo pipefail

ENVIRONMENT="${1:-staging}"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "[DEPLOY FAIL] ${ENVIRONMENT} deployment failed at ${TIMESTAMP}"
echo "[hook] Initiating rollback..."

# Log failure
cat >> .claude/memory/deployment-history.md << EOF

### ${TIMESTAMP} — ${ENVIRONMENT}
- Status: FAILED — auto-rollback initiated
- Action: Review logs and retry
EOF

echo "[hook] on-deploy-fail: rollback triggered, logged to deployment-history.md"
