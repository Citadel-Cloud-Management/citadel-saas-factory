#!/bin/bash
set -euo pipefail

# ─── Citadel SaaS Factory — Claude Code Agentic Setup ───
# Run this after cloning to verify the agentic workflow is functional.
# Usage: bash scripts/setup.sh

echo "============================================"
echo "  Citadel SaaS Factory — Agentic Setup"
echo "  Verifying Claude Code Configuration"
echo "============================================"
echo ""

ERRORS=0
WARNINGS=0

# ─── 1. Check Claude Code is installed ───
echo "1. Checking Claude Code installation..."
if command -v claude >/dev/null 2>&1; then
  echo "   OK: Claude Code $(claude --version 2>/dev/null || echo 'installed')"
else
  echo "   WARNING: Claude Code not installed"
  echo "   Install: curl -fsSL https://claude.ai/install.sh | bash"
  echo "   Or: brew install --cask claude-code"
  echo "   Or: winget install Anthropic.ClaudeCode"
  WARNINGS=$((WARNINGS + 1))
fi

# ─── 2. Verify CLAUDE.md exists ───
echo ""
echo "2. Checking CLAUDE.md..."
if [ -f ".claude/CLAUDE.md" ]; then
  LINES=$(wc -l < .claude/CLAUDE.md)
  echo "   OK: .claude/CLAUDE.md ($LINES lines)"
elif [ -f "CLAUDE.md" ]; then
  LINES=$(wc -l < CLAUDE.md)
  echo "   OK: CLAUDE.md ($LINES lines)"
else
  echo "   ERROR: No CLAUDE.md found"
  ERRORS=$((ERRORS + 1))
fi

# ─── 3. Verify settings.json ───
echo ""
echo "3. Checking settings.json..."
if [ -f ".claude/settings.json" ]; then
  if python3 -c "import json; json.load(open('.claude/settings.json'))" 2>/dev/null || \
     python -c "import json; json.load(open('.claude/settings.json'))" 2>/dev/null || \
     node -e "JSON.parse(require('fs').readFileSync('.claude/settings.json'))" 2>/dev/null; then
    echo "   OK: .claude/settings.json (valid JSON)"
  else
    echo "   ERROR: .claude/settings.json is invalid JSON"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "   WARNING: No .claude/settings.json found"
  WARNINGS=$((WARNINGS + 1))
fi

# ─── 4. Verify agent registry ───
echo ""
echo "4. Checking agent registry..."
if [ -f ".claude/agents/_registry.yaml" ]; then
  AGENT_COUNT=$(grep -c "^  - name:" .claude/agents/_registry.yaml 2>/dev/null || echo "0")
  echo "   OK: _registry.yaml ($AGENT_COUNT agents)"
else
  echo "   WARNING: No agent registry found"
  WARNINGS=$((WARNINGS + 1))
fi

# ─── 5. Verify agent definitions ───
echo ""
echo "5. Checking agent definitions..."
AGENT_DEFS=$(find .claude/agents -name "*.md" -not -name "_*" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $AGENT_DEFS agent definition files"

# ─── 6. Verify skills ───
echo ""
echo "6. Checking skills..."
SKILL_COUNT=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $SKILL_COUNT skills with SKILL.md"

# ─── 7. Verify commands ───
echo ""
echo "7. Checking commands..."
CMD_COUNT=$(find .claude/commands -name "*.md" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $CMD_COUNT commands"

# ─── 8. Verify hooks ───
echo ""
echo "8. Checking hooks..."
HOOK_COUNT=$(find .claude/hooks -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $HOOK_COUNT hook scripts"

# ─── 9. Verify templates ───
echo ""
echo "9. Checking templates..."
TMPL_COUNT=$(find .claude/templates -name "*.tmpl" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $TMPL_COUNT code generation templates"

# ─── 10. Verify rules ───
echo ""
echo "10. Checking rules..."
RULE_COUNT=$(find .claude/rules -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $RULE_COUNT rule files"

# ─── 11. Verify MCP configs ───
echo ""
echo "11. Checking MCP configs..."
MCP_COUNT=$(find .claude/mcp -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $MCP_COUNT MCP server configs"

# ─── 12. Verify cross-IDE configs ───
echo ""
echo "12. Checking cross-IDE support..."
IDE_CONFIGS=0
for f in AGENTS.md GEMINI.md AGENT.md .cursor/mcp.json .codex/config.toml .continue/config.json \
         .devin/config.yml .jules/config.yml .factory/droids.yml .antigravity/agent-manager.yaml \
         .windsurf/rules/project.md .daytona/workspace.yaml .codegen/config.yml; do
  if [ -f "$f" ]; then
    IDE_CONFIGS=$((IDE_CONFIGS + 1))
  fi
done
echo "   OK: $IDE_CONFIGS IDE/agent platform configs"

# ─── 13. Verify model catalog ───
echo ""
echo "13. Checking model catalog..."
for f in models/catalog.yaml models/routing.yaml models/embeddings.yaml; do
  if [ -f "$f" ]; then
    echo "   OK: $f"
  else
    echo "   WARNING: Missing $f"
    WARNINGS=$((WARNINGS + 1))
  fi
done

# ─── 14. Verify GitHub Actions ───
echo ""
echo "14. Checking CI/CD..."
GH_WORKFLOWS=$(find .github/workflows -name "*.yml" 2>/dev/null | wc -l | tr -d ' ')
echo "   OK: $GH_WORKFLOWS GitHub Actions workflows"

# ─── 15. Environment file ───
echo ""
echo "15. Checking environment..."
if [ -f ".env" ]; then
  echo "   OK: .env exists"
elif [ -f ".env.example" ]; then
  echo "   INFO: .env.example found — run: cp .env.example .env"
else
  echo "   WARNING: No .env or .env.example"
  WARNINGS=$((WARNINGS + 1))
fi

# ─── Summary ───
echo ""
echo "============================================"
echo "  Setup Verification Complete"
echo "============================================"

TOTAL_FILES=$(git ls-files | wc -l | tr -d ' ')
echo ""
echo "  Repository: $(git remote get-url origin 2>/dev/null || echo 'local')"
echo "  Branch:     $(git branch --show-current 2>/dev/null || echo 'detached')"
echo "  Files:      $TOTAL_FILES tracked"
echo "  Agents:     $AGENT_DEFS definitions + registry"
echo "  Skills:     $SKILL_COUNT"
echo "  Commands:   $CMD_COUNT"
echo "  Hooks:      $HOOK_COUNT"
echo "  Templates:  $TMPL_COUNT"
echo "  Rules:      $RULE_COUNT"
echo "  IDE Configs: $IDE_CONFIGS platforms"
echo ""

if [ $ERRORS -gt 0 ]; then
  echo "  RESULT: $ERRORS errors, $WARNINGS warnings"
  echo "  Fix errors before starting Claude Code."
  exit 1
elif [ $WARNINGS -gt 0 ]; then
  echo "  RESULT: $WARNINGS warnings (non-blocking)"
  echo ""
  echo "  Ready to start! Run: claude"
  exit 0
else
  echo "  RESULT: All checks passed"
  echo ""
  echo "  Ready to start! Run: claude"
  exit 0
fi
