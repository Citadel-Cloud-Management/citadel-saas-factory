#!/usr/bin/env bash
# Citadel SaaS Factory — Engine Switcher
#
# Source this file in your shell profile (~/.bashrc or ~/.zshrc) to get
# cc-paid, cc-free, cc-local, and cc-status aliases for fast engine switching.
#
#   echo "source $(pwd)/engines/switch-engine.sh" >> ~/.bashrc
#   source ~/.bashrc
#
# Then use:
#   cc-paid     # Launch Claude Code against Anthropic direct
#   cc-free     # Launch Claude Code against OpenRouter free tier
#   cc-local    # Launch Claude Code against local Ollama
#   cc-status   # Print the currently configured engine

CITADEL_ENGINES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

_citadel_unset_all() {
  unset ANTHROPIC_API_KEY
  unset ANTHROPIC_AUTH_TOKEN
  unset ANTHROPIC_BASE_URL
  unset ANTHROPIC_MODEL
  unset ANTHROPIC_SMALL_FAST_MODEL
  unset CITADEL_ENGINE
  unset CITADEL_ENGINE_PROVIDER
}

cc-paid() {
  _citadel_unset_all
  # shellcheck source=/dev/null
  source "$CITADEL_ENGINES_DIR/paid.env"
  claude "$@"
}

cc-free() {
  _citadel_unset_all
  # shellcheck source=/dev/null
  source "$CITADEL_ENGINES_DIR/openrouter-free.env"
  claude "$@"
}

cc-local() {
  _citadel_unset_all
  # shellcheck source=/dev/null
  source "$CITADEL_ENGINES_DIR/local-ollama.env"
  claude "$@"
}

cc-status() {
  echo "─── Citadel Engine Status ───"
  echo "  Engine:    ${CITADEL_ENGINE:-unset}"
  echo "  Provider:  ${CITADEL_ENGINE_PROVIDER:-unset}"
  echo "  Model:     ${ANTHROPIC_MODEL:-unset}"
  echo "  Small:     ${ANTHROPIC_SMALL_FAST_MODEL:-unset}"
  echo "  Base URL:  ${ANTHROPIC_BASE_URL:-api.anthropic.com (direct)}"
  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    echo "  Auth:      API_KEY set (${ANTHROPIC_API_KEY:0:8}...)"
  elif [ -n "${ANTHROPIC_AUTH_TOKEN:-}" ]; then
    echo "  Auth:      AUTH_TOKEN set (${ANTHROPIC_AUTH_TOKEN:0:8}...)"
  else
    echo "  Auth:      none"
  fi
}

export -f cc-paid cc-free cc-local cc-status _citadel_unset_all 2>/dev/null || true
