#!/usr/bin/env bash
# Convenience wrapper that forwards to engines/switch-engine.sh so users can
# `source scripts/switch-engine.sh` if they habitually keep shell helpers in scripts/.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/../engines/switch-engine.sh"
