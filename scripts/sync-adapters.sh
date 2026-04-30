#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# sync-adapters.sh — Verify all AI instruction adapter files reference context.md
#
# The Citadel SaaS Factory uses a unified context.md architecture. Each
# IDE/agent adapter file (CLAUDE.md, GEMINI.md, .cursor/rules/*, etc.) must
# reference context.md as the canonical source of project instructions.
#
# This script checks that:
#   1. context.md exists at the repository root
#   2. Every known adapter file contains a reference to context.md
#   3. Prints a summary and exits 0 (all in sync) or 1 (missing references)
#
# Usage:
#   ./scripts/sync-adapters.sh
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# Resolve repo root (directory containing this script's parent)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Step 1: Verify context.md exists ─────────────────────────────────────────

if [ ! -f "$REPO_ROOT/context.md" ]; then
    echo "ERROR: context.md not found at repository root ($REPO_ROOT)"
    echo "       The unified context architecture requires context.md to exist."
    exit 1
fi

echo "OK: context.md found at repository root"
echo ""

# ── Step 2: Define adapter files to check ────────────────────────────────────

ADAPTER_FILES=(
    "CLAUDE.md"
    "AGENTS.md"
    "AGENT.md"
    "GEMINI.md"
    ".github/copilot-instructions.md"
    ".antigravity/rules.md"
    ".cursor/rules/project-context.mdc"
)

# ── Step 3: Check each adapter for a reference to context.md ─────────────────

in_sync=0
out_of_sync=0
missing_files=0

echo "Checking adapter files for context.md references..."
echo "────────────────────────────────────────────────────"

for adapter in "${ADAPTER_FILES[@]}"; do
    full_path="$REPO_ROOT/$adapter"

    if [ ! -f "$full_path" ]; then
        echo "  SKIP  $adapter  (file does not exist)"
        missing_files=$((missing_files + 1))
        continue
    fi

    if grep -q "context\.md" "$full_path" 2>/dev/null; then
        echo "  OK    $adapter"
        in_sync=$((in_sync + 1))
    else
        echo "  FAIL  $adapter  (no reference to context.md)"
        out_of_sync=$((out_of_sync + 1))
    fi
done

# ── Step 4: Print summary ────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════════════"
echo "Summary"
echo "  In sync:      $in_sync"
echo "  Out of sync:  $out_of_sync"
echo "  Skipped:      $missing_files (file not found)"
echo "════════════════════════════════════════════════════"

if [ "$out_of_sync" -gt 0 ]; then
    echo ""
    echo "ACTION REQUIRED: $out_of_sync adapter file(s) do not reference context.md."
    echo "Add a reference to context.md in each failing file."
    exit 1
fi

echo ""
echo "All existing adapter files reference context.md."
exit 0
