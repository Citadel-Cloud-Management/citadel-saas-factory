#!/bin/bash
# Pre-agent hook: validate agent context before execution
set -euo pipefail

AGENT_ID="${1:-unknown}"
echo "[hook] pre-agent: initializing ${AGENT_ID}..."

# Ensure memory directory exists
mkdir -p .claude/memory

# Check for active blockers
if [ -f ".claude/memory/blockers.md" ]; then
  echo "[hook] pre-agent: blockers file found — agent should review before proceeding"
fi

echo "[hook] pre-agent: ${AGENT_ID} ready"
