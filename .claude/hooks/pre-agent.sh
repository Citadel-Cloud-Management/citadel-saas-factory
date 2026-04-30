#!/bin/bash
# Pre-agent hook: validate agent context before execution
# Injects auto-update preamble and validates context alignment
set -euo pipefail

AGENT_ID="${1:-unknown}"
echo "[hook] pre-agent: initializing ${AGENT_ID}..."

# Ensure memory directory exists
mkdir -p .claude/memory

# Validate canonical context exists
if [ ! -f "context.md" ]; then
  echo "[hook] pre-agent: WARNING — context.md not found at repository root"
fi

# Validate auto-update preamble exists
if [ -f ".claude/prompts/auto-update-preamble.md" ]; then
  echo "[hook] pre-agent: auto-update preamble loaded for ${AGENT_ID}"
else
  echo "[hook] pre-agent: WARNING — auto-update preamble missing (.claude/prompts/auto-update-preamble.md)"
fi

# Check for active blockers
if [ -f ".claude/memory/blockers.md" ]; then
  echo "[hook] pre-agent: blockers file found — agent should review before proceeding"
fi

# Check for stale context (modified more than 30 days ago)
if [ -f "context.md" ]; then
  CONTEXT_AGE=$(( ($(date +%s) - $(stat -c %Y context.md 2>/dev/null || stat -f %m context.md 2>/dev/null || echo 0)) / 86400 ))
  if [ "$CONTEXT_AGE" -gt 30 ]; then
    echo "[hook] pre-agent: WARNING — context.md is ${CONTEXT_AGE} days old, may need updating"
  fi
fi

echo "[hook] pre-agent: ${AGENT_ID} ready"
