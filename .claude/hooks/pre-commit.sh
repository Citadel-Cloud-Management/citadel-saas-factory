#!/bin/bash
# Pre-commit hook: lint, format, secret scan
set -euo pipefail

echo "[hook] pre-commit: running checks..."

# Secret scanning
if command -v trufflehog &>/dev/null; then
  trufflehog filesystem --directory . --only-verified 2>/dev/null || {
    echo "[BLOCKED] Secrets detected. Remove them before committing."
    exit 1
  }
fi

# Python linting
if [ -d "backend" ] && command -v ruff &>/dev/null; then
  ruff check backend/ --fix
  ruff format backend/
fi

# Frontend linting
if [ -d "frontend/node_modules" ]; then
  cd frontend && npx next lint --fix 2>/dev/null && cd ..
fi

echo "[hook] pre-commit: passed"
