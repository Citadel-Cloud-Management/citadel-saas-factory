#!/bin/bash
# On-security-alert hook: escalate security findings
set -euo pipefail

SEVERITY="${1:-UNKNOWN}"
FINDING="${2:-No details}"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "[SECURITY ALERT] ${SEVERITY}: ${FINDING}"

if [ "$SEVERITY" = "CRITICAL" ] || [ "$SEVERITY" = "HIGH" ]; then
  echo "[hook] BLOCKING: Critical/High security finding must be resolved before proceeding"
  exit 1
fi

echo "[hook] on-security-alert: logged (non-blocking for ${SEVERITY})"
