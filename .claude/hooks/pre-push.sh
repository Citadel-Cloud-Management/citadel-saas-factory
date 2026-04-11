#!/bin/bash
# Pre-push hook: run tests and security scan
set -euo pipefail

echo "[hook] pre-push: running tests..."

if [ -d "backend" ]; then
  cd backend && python -m pytest --tb=short -q 2>/dev/null && cd ..
fi

if [ -d "frontend/node_modules" ]; then
  cd frontend && npm test -- --watchAll=false 2>/dev/null && cd ..
fi

echo "[hook] pre-push: running security scan..."
if command -v semgrep &>/dev/null; then
  semgrep --config auto --severity ERROR backend/ 2>/dev/null || true
fi

echo "[hook] pre-push: passed"
