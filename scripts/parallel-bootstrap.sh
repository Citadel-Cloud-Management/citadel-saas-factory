#!/usr/bin/env bash
# Citadel SaaS Factory — Parallel Bootstrap
# Usage: ./scripts/parallel-bootstrap.sh [--dry-run]
# Installs all subsystems in parallel. Idempotent — safe to run multiple times.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARALLELISM="${PARALLELISM:-$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)}"
if [[ "${1:-}" == "--dry-run" ]]; then DRY_RUN="--dry-run"; else DRY_RUN=""; fi
LOG_DIR="${REPO_ROOT}/logs/bootstrap"

mkdir -p "$LOG_DIR"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

run_task() {
  local script="$1"
  local name
  name="$(basename "$script" .sh)"
  log "Starting: $name"
  if [[ "$DRY_RUN" == "--dry-run" ]]; then
    log "  [DRY RUN] Would execute: $script"
    return 0
  fi
  if bash "$script" > "$LOG_DIR/$name.log" 2>&1; then
    log "  Completed: $name"
  else
    log "  FAILED: $name (see $LOG_DIR/$name.log)"
    return 1
  fi
}

export DRY_RUN LOG_DIR

log "=== Citadel SaaS Factory — Parallel Bootstrap ==="
log "Parallelism: $PARALLELISM"
log "Dry run: ${DRY_RUN:-no}"
log ""

# Phase 1: Detection (must run first)
log "Phase 1: Business detection"
run_task "$REPO_ROOT/scripts/detect-business.sh"

# Phase 2: Parallel installation
log ""
log "Phase 2: Parallel subsystem installation"
tasks=(
  "$REPO_ROOT/scripts/install-models.sh"
  "$REPO_ROOT/scripts/install-mcp.sh"
  "$REPO_ROOT/scripts/install-hooks.sh"
  "$REPO_ROOT/scripts/render-agents.sh"
)

printf '%s\n' "${tasks[@]}" | xargs -I{} -P "$PARALLELISM" bash -c '
  script="$1"
  name="$(basename "$script" .sh)"
  echo "[$(date "+%H:%M:%S")] Starting: $name"
  if [[ "$DRY_RUN" == "--dry-run" ]]; then
    echo "[$(date "+%H:%M:%S")]   [DRY RUN] Would execute: $script"
    exit 0
  fi
  if bash "$script" > "$LOG_DIR/$name.log" 2>&1; then
    echo "[$(date "+%H:%M:%S")]   Completed: $name"
  else
    echo "[$(date "+%H:%M:%S")]   FAILED: $name (see $LOG_DIR/$name.log)"
    exit 1
  fi
' _ {} || {
  log "One or more parallel tasks failed. Check logs in $LOG_DIR/"
  exit 1
}

# Phase 3: Verification
log ""
log "Phase 3: Verification"
run_task "$REPO_ROOT/scripts/verify-install.sh"

log ""
log "=== Bootstrap complete ==="
log "Logs at: $LOG_DIR/"
log "Run 'make status' or 'just status' for system health."
