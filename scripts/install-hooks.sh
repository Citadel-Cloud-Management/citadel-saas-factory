#!/usr/bin/env bash
# Install git hooks via Lefthook or fallback to manual
# Idempotent: skips if already installed
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() { echo "[hooks] $*"; }

cd "$REPO_ROOT"

# Try Lefthook first
if command -v lefthook &>/dev/null; then
  log "Installing hooks via Lefthook..."
  lefthook install 2>/dev/null || log "Lefthook install skipped (no lefthook.yml)"
elif command -v npx &>/dev/null; then
  log "Installing hooks via npx lefthook..."
  npx @evilmartians/lefthook install 2>/dev/null || log "Lefthook install skipped"
else
  log "No hook manager found — install lefthook: npm i -g @evilmartians/lefthook"
fi

log "Hooks installation complete"
