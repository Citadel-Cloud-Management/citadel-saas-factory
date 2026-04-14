#!/usr/bin/env bash
# Auto-insert backlinks after writing a vault note.
# Triggered by PostToolUse hook on Write(docs/vault/*.md).
# Scans the newly written file for [[wikilink]] candidates and ensures
# matching vault notes are added to the file's <!-- linked-notes --> block.

set -euo pipefail

FILE="${1:-${file:-}}"
if [[ -z "${FILE}" || ! -f "${FILE}" ]]; then
  exit 0
fi

# Only process files inside the vault.
case "${FILE}" in
  *docs/vault/*) ;;
  *) exit 0 ;;
esac

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LINKER="${REPO_ROOT}/scripts/vault-autolink.py"

if [[ -x "${LINKER}" ]] || [[ -f "${LINKER}" ]]; then
  python "${LINKER}" "${FILE}" 2>/dev/null || true
fi

exit 0
