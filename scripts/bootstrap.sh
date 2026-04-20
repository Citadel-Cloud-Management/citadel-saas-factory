#!/bin/bash
set -euo pipefail

echo "============================================"
echo "  Citadel SaaS Factory — Bootstrap"
echo "============================================"

# Install Claude Code master prompt
echo ""
echo "Installing Claude Code master prompt..."
bash "$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )/setup-claude-code.sh" "$(pwd)" 2>/dev/null || echo "  (skipped — run manually: ./scripts/setup-claude-code.sh)"

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

# Install hallucination prevention (Guardrails AI + DeepEval)
echo ""
echo "Installing Guardrails AI hallucination prevention..."
pip install guardrails-ai deepeval 2>/dev/null && guardrails configure --disable-metrics --disable-remote-inferencing 2>/dev/null || echo "  (skipped — run ./scripts/setup-guardrails.sh to install)"

# Install frontend dependencies
if [ -f "frontend/package.json" ]; then
  echo ""
  echo "Installing frontend dependencies..."
  cd frontend
  npm install 2>/dev/null || echo "  (skipped — install manually with: cd frontend && npm install)"
  cd ..
fi

# Generate Obsidian vault and knowledge graph
echo ""
echo "Generating Obsidian vault (docs/vault/)..."
python scripts/generate-vault.py 2>/dev/null || echo "  (skipped — run manually with: make vault-generate)"
python scripts/sync-vault-memory.py 2>/dev/null || true

echo ""
echo "Building Graphify knowledge graph into vault..."
graphify . --obsidian-dir docs/vault/knowledge-graph 2>/dev/null || echo "  (skipped — install graphify and run: make vault-sync)"

# Initialize the three-layer LLM Wiki brain memory (Karpathy pattern)
echo ""
echo "Initializing LLM Wiki three-layer structure (docs/vault/raw, wiki, SCHEMA.md)..."
mkdir -p docs/vault/raw/articles \
         docs/vault/raw/transcripts \
         docs/vault/raw/architecture \
         docs/vault/raw/incidents \
         docs/vault/raw/customer \
         docs/vault/raw/clippings \
         docs/vault/raw/data \
         docs/vault/wiki/entities \
         docs/vault/wiki/concepts \
         docs/vault/wiki/sources \
         docs/vault/wiki/comparisons \
         docs/vault/wiki/contradictions \
         docs/vault/wiki/knowledge-graph

if [ ! -f docs/vault/wiki/index.md ]; then
  echo "  (wiki/index.md missing — run: git checkout docs/vault/wiki/index.md or regenerate)"
fi
if [ ! -f docs/vault/SCHEMA.md ]; then
  echo "  (SCHEMA.md missing — run: git checkout docs/vault/SCHEMA.md)"
fi
echo "  LLM Wiki layers ready. Drop raw sources into docs/vault/raw/ and run: make wiki-ingest FILE=raw/<path>"

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
