#!/usr/bin/env bash
set -uo pipefail

PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  local fix="$3"

  if eval "$cmd" > /dev/null 2>&1; then
    echo "  [PASS] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $name"
    echo "         Fix: $fix"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Citadel SaaS Factory — Installation Verification ==="
echo ""

check "Claude Code installed" \
  "claude --version" \
  "npm install -g @anthropic-ai/claude-code"

check "Graphify installed" \
  "graphify --version" \
  "pip install graphifyy && graphify install"

check "Graphify skill exists" \
  "test -f .claude/skills/graphify/SKILL.md" \
  "graphify claude install"

check "GitHub CLI authenticated" \
  "gh auth status" \
  "./scripts/setup-tokens.sh"

check "Docker running" \
  "docker info" \
  "Install Docker: https://docs.docker.com/get-docker/"

check "Node.js 18+" \
  "node -e 'process.exit(parseInt(process.version.slice(1)) >= 18 ? 0 : 1)'" \
  "Install Node.js 18+: https://nodejs.org"

check "ANTHROPIC_API_KEY set" \
  "test -n \"\${ANTHROPIC_API_KEY:-}\"" \
  "./scripts/setup-tokens.sh"

check "GITHUB_TOKEN set" \
  "test -n \"\${GITHUB_TOKEN:-}\${GITHUB_PERSONAL_ACCESS_TOKEN:-}\"" \
  "./scripts/setup-tokens.sh"

check "CLAUDE.md exists" \
  "test -f .claude/CLAUDE.md" \
  "Run: claude /init"

# ─── Multi-Model System ───
echo ""
echo "=== Multi-Model System ==="

check "Model catalog exists" \
  "test -f models/catalog.yaml" \
  "Missing models/catalog.yaml — run parallel-bootstrap.sh"

check "Model routing exists" \
  "test -f models/routing.yaml" \
  "Missing models/routing.yaml — run parallel-bootstrap.sh"

check "Embeddings config exists" \
  "test -f models/embeddings.yaml" \
  "Missing models/embeddings.yaml"

check "Provider configs exist" \
  "ls agents/providers/*.yaml 2>/dev/null | grep -q ." \
  "Missing agents/providers/ — run parallel-bootstrap.sh"

check "Model router config exists" \
  "test -f agents/router/config.yaml" \
  "Missing agents/router/config.yaml"

check "Ollama installed" \
  "command -v ollama" \
  "Install: curl -fsSL https://ollama.ai/install.sh | sh"

# ─── Cross-IDE Configuration ───
echo ""
echo "=== Cross-IDE Configuration ==="

check "AGENTS.md (Codex/Jules/Factory)" \
  "test -f AGENTS.md" \
  "Missing AGENTS.md — run parallel-bootstrap.sh"

check "GEMINI.md (Gemini/Jules)" \
  "test -f GEMINI.md" \
  "Missing GEMINI.md"

check "AGENT.md (Cursor)" \
  "test -f AGENT.md" \
  "Missing AGENT.md"

check "Copilot instructions" \
  "test -f .github/copilot-instructions.md" \
  "Missing .github/copilot-instructions.md"

check "Cursor rules" \
  "test -f .cursor/rules/project-context.mdc" \
  "Missing .cursor/rules/"

check "Cursor MCP config" \
  "test -f .cursor/mcp.json" \
  "Missing .cursor/mcp.json"

check "Antigravity rules" \
  "test -f .antigravity/rules.md" \
  "Missing .antigravity/rules.md"

check "CodeRabbit config" \
  "test -f .coderabbit.yml" \
  "Missing .coderabbit.yml"

check "Codex config" \
  "test -f .codex/config.toml" \
  "Missing .codex/config.toml"

# ─── Bootstrap System ───
echo ""
echo "=== Bootstrap System ==="

check "Parallel bootstrap script" \
  "test -x scripts/parallel-bootstrap.sh" \
  "Missing or not executable: scripts/parallel-bootstrap.sh"

check "Env example" \
  "test -f .env.example" \
  "Run: ./scripts/install-models.sh"

check "MCP registry" \
  "test -f mcp/registry.yaml" \
  "Missing mcp/registry.yaml"

check "Evals config" \
  "test -f evals/promptfoo.yaml" \
  "Missing evals/promptfoo.yaml"

check "Subagents catalog" \
  "test -f subagents/catalog.yaml" \
  "Missing subagents/catalog.yaml"

check "Tools catalog" \
  "test -f tools/catalog.yaml" \
  "Missing tools/catalog.yaml"

check "Justfile" \
  "test -f Justfile" \
  "Missing Justfile"

check "Lefthook config" \
  "test -f lefthook.yml" \
  "Missing lefthook.yml"

TOTAL=$((PASS + FAIL))
echo ""
echo "Results: $PASS passed, $FAIL failed (out of $TOTAL)"

if [[ $FAIL -eq 0 ]]; then
  echo "All checks passed. Ready to go."
else
  echo "Fix the failures above, then re-run this script."
  exit 1
fi
