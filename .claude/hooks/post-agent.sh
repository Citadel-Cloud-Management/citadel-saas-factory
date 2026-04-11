#!/bin/bash
# Post-agent hook: log agent activity and update learnings
set -euo pipefail

AGENT_ID="${1:-unknown}"
echo "[hook] post-agent: logging ${AGENT_ID} activity..."

# Append to deployment history if applicable
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
echo "- ${TIMESTAMP}: ${AGENT_ID} completed task" >> .claude/memory/agent-learnings.md

echo "[hook] post-agent: ${AGENT_ID} logged"
