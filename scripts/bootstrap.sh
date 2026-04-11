#!/bin/bash
set -euo pipefail

echo "============================================"
echo "  Citadel SaaS Factory — Bootstrap"
echo "============================================"

# Check prerequisites
echo ""
echo "Checking prerequisites..."

command -v git >/dev/null 2>&1 || { echo "ERROR: git is required"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker is required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js 18+ is required"; exit 1; }

NODE_V=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_V" -lt 18 ]; then
  echo "ERROR: Node.js 18+ required (found v${NODE_V})"
  exit 1
fi

echo "  git: OK"
echo "  docker: OK"
echo "  node: OK ($(node --version))"

# Environment setup
if [ ! -f .env ]; then
  echo ""
  echo "Creating .env from .env.example..."
  cp .env.example .env
  echo "  IMPORTANT: Edit .env with your API keys before starting"
fi

# Install backend dependencies
if [ -f "backend/pyproject.toml" ]; then
  echo ""
  echo "Installing backend dependencies..."
  cd backend
  pip install -e ".[dev]" 2>/dev/null || pip install -e . 2>/dev/null || echo "  (skipped — install manually with: cd backend && pip install -e .)"
  cd ..
fi

# Install frontend dependencies
if [ -f "frontend/package.json" ]; then
  echo ""
  echo "Installing frontend dependencies..."
  cd frontend
  npm install 2>/dev/null || echo "  (skipped — install manually with: cd frontend && npm install)"
  cd ..
fi

# Start Docker services
echo ""
echo "Starting Docker services..."
docker compose up -d 2>/dev/null || echo "  (skipped — start manually with: docker compose up -d)"

echo ""
echo "============================================"
echo "  Bootstrap complete!"
echo "============================================"
echo ""
echo "  Next steps:"
echo "    1. Edit .env with your API keys"
echo "    2. Run: claude"
echo "    3. In Claude Code: /graphify ."
echo ""
