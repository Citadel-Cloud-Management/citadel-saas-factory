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

check "Ruflo installed" \
  "npx ruflo@latest --version" \
  "curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash"

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

echo ""
echo "Results: $PASS passed, $FAIL failed (out of 10)"

if [[ $FAIL -eq 0 ]]; then
  echo "All checks passed. Ready to go."
else
  echo "Fix the failures above, then re-run this script."
  exit 1
fi
