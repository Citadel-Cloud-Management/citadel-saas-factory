#!/bin/bash
# On-test-fail hook: analyze failure and suggest fixes
set -euo pipefail

TEST_FILE="${1:-}"
echo "[hook] on-test-fail: ${TEST_FILE}"
echo "[hook] Suggested actions:"
echo "  1. Check test isolation — ensure no shared state"
echo "  2. Verify mocks match current interfaces"
echo "  3. Run with verbose output for details"
echo "  4. Use tdd-guide agent for assistance"
