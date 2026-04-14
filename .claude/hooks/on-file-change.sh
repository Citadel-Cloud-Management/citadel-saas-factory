#!/bin/bash
# On-file-change hook: trigger relevant checks when files change
set -euo pipefail

CHANGED_FILE="${1:-}"
echo "[hook] on-file-change: ${CHANGED_FILE}"

case "$CHANGED_FILE" in
  *.py)    echo "[hook] Python file changed — run ruff + pytest" ;;
  *.ts|*.tsx) echo "[hook] TypeScript file changed — run lint + vitest" ;;
  *.yaml|*.yml) echo "[hook] YAML file changed — validate schema" ;;
  *.tf)    echo "[hook] Terraform file changed — run plan" ;;
  Dockerfile*) echo "[hook] Dockerfile changed — rebuild image" ;;
esac
