#!/bin/bash
# On-error hook: capture error context for debugging
set -euo pipefail

ERROR_MSG="${1:-Unknown error}"
AGENT_ID="${2:-unknown}"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "[hook] on-error: ${AGENT_ID} encountered error"

# Log to error patterns
cat >> .claude/memory/error-patterns.md << EOF

### ${TIMESTAMP} — ${AGENT_ID}
- Error: ${ERROR_MSG}
- Status: Needs investigation
EOF

echo "[hook] on-error: logged to error-patterns.md"
