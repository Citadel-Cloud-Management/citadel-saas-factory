#!/usr/bin/env bash
# Citadel SaaS Factory — Claude Code Master Prompt Setup
# Usage: ./scripts/setup-claude-code.sh [TARGET_DIR]
#
# Installs the Claude Code master prompt as CLAUDE.md in any project.
# If TARGET_DIR is omitted, installs in the current repo.
# Idempotent — safe to run multiple times.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACTORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MASTER_PROMPT="$FACTORY_ROOT/CLAUDE_CODE_MASTER_PROMPT.md"
TARGET_DIR="${1:-$FACTORY_ROOT}"

# Resolve to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
  echo "ERROR: Target directory does not exist: $1"
  echo "Usage: ./scripts/setup-claude-code.sh [TARGET_DIR]"
  exit 1
}

echo "============================================"
echo "  Claude Code Master Prompt — Setup"
echo "============================================"
echo ""
echo "  Source:  $MASTER_PROMPT"
echo "  Target:  $TARGET_DIR"
echo ""

# ── 1. Verify source exists ──
if [[ ! -f "$MASTER_PROMPT" ]]; then
  echo "ERROR: CLAUDE_CODE_MASTER_PROMPT.md not found at $FACTORY_ROOT"
  echo "  Clone the factory first: git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git"
  exit 1
fi

# ── 2. Install CLAUDE.md ──
TARGET_CLAUDE="$TARGET_DIR/CLAUDE.md"
if [[ -f "$TARGET_CLAUDE" ]]; then
  echo "  CLAUDE.md already exists at $TARGET_CLAUDE"
  echo "  Backing up to CLAUDE.md.bak..."
  cp "$TARGET_CLAUDE" "$TARGET_CLAUDE.bak"
fi
cp "$MASTER_PROMPT" "$TARGET_CLAUDE"
echo "  ✓ CLAUDE.md installed"

# ── 3. Create .claude/ directory structure ──
CLAUDE_DIR="$TARGET_DIR/.claude"
mkdir -p "$CLAUDE_DIR"/{agents,commands,hooks,rules,skills,memory,mcp,templates}
echo "  ✓ .claude/ directory structure created"

# ── 4. Create .claudeignore if missing ──
CLAUDEIGNORE="$TARGET_DIR/.claudeignore"
if [[ ! -f "$CLAUDEIGNORE" ]]; then
  cat > "$CLAUDEIGNORE" << 'IGNORE'
# Dependencies
node_modules/
vendor/
.venv/
__pycache__/

# Build output
dist/
build/
.next/
out/
target/

# Secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Large binaries
*.zip
*.tar.gz
*.sqlite
*.db
*.log

# Generated
*.generated.*
__generated__/

# IDE / OS
.DS_Store
.idea/
.vscode/
IGNORE
  echo "  ✓ .claudeignore created"
else
  echo "  ✓ .claudeignore already exists"
fi

# ── 5. Create starter commands if commands dir is empty ──
COMMANDS_DIR="$CLAUDE_DIR/commands"
if [[ ! -f "$COMMANDS_DIR/review.md" ]]; then
  cat > "$COMMANDS_DIR/review.md" << 'CMD'
Run a code review on the current git diff.

Protocol:
1. Run `git diff --staged` (or `git diff` if nothing staged) and read the full output.
2. For each changed file, check for: security flaws, bugs, performance issues, style violations.
3. Produce a Markdown report: Summary (3 bullets), P0 (must fix), P1 (should fix), P2 (nice-to-have), Verdict.
CMD
  echo "  ✓ /review command created"
fi

if [[ ! -f "$COMMANDS_DIR/test-all.md" ]]; then
  cat > "$COMMANDS_DIR/test-all.md" << 'CMD'
Run the full test suite for this project.

1. Detect the test framework (pytest, jest, vitest, go test, cargo test).
2. Run all tests with verbose output.
3. Report: total, passed, failed, skipped, coverage if available.
4. If any tests fail, show the failure details and suggest fixes.
CMD
  echo "  ✓ /test-all command created"
fi

if [[ ! -f "$COMMANDS_DIR/deploy.md" ]]; then
  cat > "$COMMANDS_DIR/deploy.md" << 'CMD'
Deploy to the specified environment.

Usage: /deploy [staging|production]

Protocol:
1. Run all tests first. Abort if any fail.
2. Run security scan (semgrep/trivy if available). Abort on CRITICAL findings.
3. Build the project.
4. Deploy to the specified environment.
5. Run smoke tests against the deployed environment.
6. Report: deployment URL, version, status.

IMPORTANT: Production deployments require explicit user confirmation.
CMD
  echo "  ✓ /deploy command created"
fi

if [[ ! -f "$COMMANDS_DIR/security-audit.md" ]]; then
  cat > "$COMMANDS_DIR/security-audit.md" << 'CMD'
Run a security audit on the current codebase.

Protocol:
1. Check for hardcoded secrets (API keys, passwords, tokens).
2. Check for SQL injection, XSS, CSRF vulnerabilities.
3. Check dependency versions for known CVEs.
4. Check file permissions and .gitignore coverage.
5. Report findings by severity: CRITICAL > HIGH > MEDIUM > LOW.
CMD
  echo "  ✓ /security-audit command created"
fi

# ── 6. Create starter hooks ──
HOOKS_DIR="$CLAUDE_DIR/hooks"
if [[ ! -f "$HOOKS_DIR/auto-lint.sh" ]]; then
  cat > "$HOOKS_DIR/auto-lint.sh" << 'HOOK'
#!/usr/bin/env bash
set -euo pipefail
# Auto-run formatter after Claude writes a file
CHANGED_FILE="${1:-}"
[ -z "$CHANGED_FILE" ] && exit 0

case "$CHANGED_FILE" in
  *.ts|*.tsx|*.js|*.jsx) npx prettier --write "$CHANGED_FILE" 2>/dev/null && npx eslint --fix "$CHANGED_FILE" 2>/dev/null || true ;;
  *.py)                   ruff format "$CHANGED_FILE" 2>/dev/null && ruff check --fix "$CHANGED_FILE" 2>/dev/null || true ;;
  *.go)                   gofmt -w "$CHANGED_FILE" 2>/dev/null || true ;;
  *.rs)                   rustfmt "$CHANGED_FILE" 2>/dev/null || true ;;
esac
HOOK
  chmod +x "$HOOKS_DIR/auto-lint.sh"
  echo "  ✓ auto-lint hook created"
fi

# ── 7. Create .mcp.json template if missing ──
MCP_JSON="$TARGET_DIR/.mcp.json"
if [[ ! -f "$MCP_JSON" ]]; then
  cat > "$MCP_JSON" << 'MCP'
{
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
MCP
  echo "  ✓ .mcp.json template created"
else
  echo "  ✓ .mcp.json already exists"
fi

# ── 8. Create settings.json if missing ──
SETTINGS="$CLAUDE_DIR/settings.json"
if [[ ! -f "$SETTINGS" ]]; then
  cat > "$SETTINGS" << 'SETTINGS'
{
  "model_routing": {
    "default": "claude-sonnet-4-6",
    "cheap": "claude-haiku-4-5-20251001",
    "premium": "claude-opus-4-7"
  },
  "prompt_caching": true,
  "guardrails": {
    "enabled": true,
    "hallucination_threshold": 0.85,
    "reask_budget": 3
  }
}
SETTINGS
  echo "  ✓ .claude/settings.json created"
else
  echo "  ✓ .claude/settings.json already exists"
fi

echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  Installed:"
echo "    ✓ CLAUDE.md              — master operating prompt (project constitution)"
echo "    ✓ .claude/commands/      — /review, /test-all, /deploy, /security-audit"
echo "    ✓ .claude/hooks/         — auto-lint on file write"
echo "    ✓ .claude/settings.json  — model routing + guardrails config"
echo "    ✓ .claudeignore          — exclude build artifacts and secrets"
echo "    ✓ .mcp.json              — MCP server template (GitHub + filesystem)"
echo ""
echo "  Next steps:"
echo "    1. Edit .env with your API key (ANTHROPIC_API_KEY or OPENAI_API_KEY)"
echo "    2. Run: claude"
echo "    3. Try: /review, /test-all, /security-audit"
echo ""
echo "  To install into a DIFFERENT project:"
echo "    ./scripts/setup-claude-code.sh /path/to/your/project"
echo ""
