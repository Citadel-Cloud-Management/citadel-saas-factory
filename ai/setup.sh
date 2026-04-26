#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AI_DIR="$ROOT/ai"

# ─── Colors ───
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { printf "${CYAN}[ai-setup]${NC} %s\n" "$1"; }
ok()   { printf "${GREEN}  ✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}  ⚠${NC} %s\n" "$1"; }
fail() { printf "${RED}  ✗${NC} %s\n" "$1"; }

ERRORS=0

# ─── Step 1: Check runtimes ───
log "Checking runtimes..."

if command -v node >/dev/null 2>&1; then
  NODE_VER=$(node -v | sed 's/v//')
  NODE_MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 18 ]; then
    ok "Node.js $NODE_VER"
  else
    fail "Node.js $NODE_VER found but >=18 required"
    ERRORS=$((ERRORS + 1))
  fi
else
  fail "Node.js not found (>=18 required)"
  ERRORS=$((ERRORS + 1))
fi

if command -v python3 >/dev/null 2>&1; then
  PY_VER=$(python3 --version | awk '{print $2}')
  ok "Python $PY_VER"
elif command -v python >/dev/null 2>&1; then
  PY_VER=$(python --version | awk '{print $2}')
  ok "Python $PY_VER"
else
  warn "Python not found — ai/agents/run.py will not work"
fi

# ─── Step 2: Verify directory structure ───
log "Verifying ai/ directory structure..."

EXPECTED_DIRS=(
  "ai/prompts/system"
  "ai/prompts/tasks"
  "ai/prompts/tools"
  "ai/data/raw"
  "ai/data/processed"
  "ai/agents/skills"
  "ai/agents/tools"
  "ai/evals/tests"
  "ai/evals/traces"
  "ai/evals/scorecards"
)

for dir in "${EXPECTED_DIRS[@]}"; do
  target="$ROOT/$dir"
  if [ -d "$target" ]; then
    ok "$dir"
  else
    mkdir -p "$target"
    ok "$dir (created)"
  fi
done

# ─── Step 3: Verify required files ───
log "Verifying required files..."

EXPECTED_FILES=(
  "ai/prompts/system/base.md"
  "ai/prompts/tasks/example_task.md"
  "ai/prompts/tools/example_tool.md"
  "ai/agents/agent_config.yaml"
  "ai/evals/tests/example_test.json"
  "ai/evals/scorecards/rubric.md"
  "ai-layer.config.yaml"
)

for file in "${EXPECTED_FILES[@]}"; do
  target="$ROOT/$file"
  if [ -f "$target" ]; then
    ok "$file"
  else
    fail "$file missing"
    ERRORS=$((ERRORS + 1))
  fi
done

# ─── Step 4: Verify executables have +x ───
log "Setting executable permissions..."

EXECUTABLES=(
  "ai/setup.sh"
  "ai/evals/run.js"
  "ai/prompts/lint.js"
  "ai/agents/run.py"
)

for exe in "${EXECUTABLES[@]}"; do
  target="$ROOT/$exe"
  if [ -f "$target" ]; then
    chmod +x "$target"
    ok "$exe"
  else
    fail "$exe missing"
    ERRORS=$((ERRORS + 1))
  fi
done

# ─── Step 5: Check API key ───
log "Checking environment..."

if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  ok "ANTHROPIC_API_KEY is set"
else
  warn "ANTHROPIC_API_KEY not set — agent runner will use mock mode"
  warn "  Set it: export ANTHROPIC_API_KEY=sk-ant-..."
fi

# ─── Step 6: Run prompt lint as smoke test ───
log "Running prompt lint smoke test..."

if node "$AI_DIR/prompts/lint.js" 2>/dev/null; then
  ok "All prompts pass lint"
else
  fail "Prompt lint found issues (run: node ai/prompts/lint.js)"
  ERRORS=$((ERRORS + 1))
fi

# ─── Summary ───
echo ""
if [ "$ERRORS" -eq 0 ]; then
  printf "${GREEN}━━━ AI layer ready ━━━${NC}\n"
  echo ""
  echo "  Run evals:        make ai-eval"
  echo "  Run agent:        python3 ai/agents/run.py --task summarize-document"
  echo "  Lint prompts:     make ai-prompt-lint"
  echo "  Run single test:  node ai/evals/run.js --id sum-001"
  echo ""
else
  printf "${RED}━━━ Setup completed with $ERRORS error(s) ━━━${NC}\n"
  exit 1
fi
