#!/usr/bin/env bash
# setup-skills.sh — Initialize the claude-skills integration after cloning
# Usage: ./scripts/setup-skills.sh [--verify]
#
# This script ensures the integrated claude-skills library (from alirezarezvani/claude-skills)
# is properly configured and executable within the Citadel SaaS Factory.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.claude/skills"
COMMANDS_DIR="$REPO_ROOT/.claude/commands"
AGENTS_DIR="$REPO_ROOT/.claude/agents"
SCRIPTS_DIR="$REPO_ROOT/scripts"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERR]${NC} $1"; }

echo "============================================"
echo "  Citadel SaaS Factory — Skills Setup"
echo "  Source: alirezarezvani/claude-skills v2.3.0"
echo "============================================"
echo ""

# --- Verify directory structure ---
echo "Checking directory structure..."

SKILL_COUNT=$(find "$SKILLS_DIR" -maxdepth 1 -type d | wc -l)
COMMAND_COUNT=$(find "$COMMANDS_DIR" -type f \( -name "*.md" -o -name "*.yaml" \) | wc -l)
AGENT_COUNT=$(find "$AGENTS_DIR" -name "*.md" -type f | wc -l)

if [ "$SKILL_COUNT" -ge 200 ]; then
  info "Skills: $SKILL_COUNT directories"
else
  error "Skills: only $SKILL_COUNT (expected 200+)"
  exit 1
fi

if [ "$COMMAND_COUNT" -ge 50 ]; then
  info "Commands: $COMMAND_COUNT files"
else
  warn "Commands: $COMMAND_COUNT (expected 50+)"
fi

info "Agents: $AGENT_COUNT definitions"

# --- Make scripts executable ---
echo ""
echo "Setting script permissions..."
for script in "$SCRIPTS_DIR"/*.sh "$SCRIPTS_DIR"/*.py; do
  [ -f "$script" ] && chmod +x "$script"
done
info "All scripts marked executable"

# --- Verify key files exist ---
echo ""
echo "Verifying key integration files..."

REQUIRED_FILES=(
  ".claude/skills/senior-architect/SKILL.md"
  ".claude/skills/tdd-guide/SKILL.md"
  ".claude/skills/rag-architect/SKILL.md"
  ".claude/agents/personas/startup-cto.md"
  ".claude/commands/prd.md"
  ".claude-plugin/marketplace.json"
  "docs/INSTALLATION.md"
  "docs/SKILL-AUTHORING-STANDARD.md"
)

ALL_OK=true
for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$REPO_ROOT/$f" ]; then
    info "$f"
  else
    error "Missing: $f"
    ALL_OK=false
  fi
done

# --- Summary ---
echo ""
echo "============================================"
if [ "$ALL_OK" = true ]; then
  info "All checks passed. Skills library is ready."
  echo ""
  echo "Quick Start:"
  echo "  - Invoke any skill:  /senior-architect, /tdd-guide, /rag-architect"
  echo "  - Run commands:      /prd, /retro, /sprint-plan, /okr"
  echo "  - Convert formats:   ./scripts/convert.sh --tool all"
  echo "  - Install into project: ./scripts/install.sh --tool cursor --target ."
  echo ""
  echo "Docs: docs/INSTALLATION.md"
else
  error "Some checks failed. Run from repo root after a clean clone."
  exit 1
fi
