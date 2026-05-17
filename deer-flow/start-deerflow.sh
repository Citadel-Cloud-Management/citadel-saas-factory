#!/usr/bin/env bash
# DeerFlow Quick Start for Windows (Git Bash)
# Usage: ./start-deerflow.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Add local nginx to PATH
export PATH="$REPO_ROOT/nginx:$PATH"

# Set UTF-8 for Python
export PYTHONIOENCODING=utf-8

# Check for API key
if [ -f .env ]; then
    source .env
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set in .env"
    echo "   Edit deer-flow/.env and add your key, then re-run this script."
    echo ""
    echo "   Example: ANTHROPIC_API_KEY=sk-ant-api03-..."
    exit 1
fi

echo "🦌 Starting DeerFlow 2.0..."
echo "   Access at: http://localhost:2026"
echo ""

# Start services
./scripts/serve.sh --dev
