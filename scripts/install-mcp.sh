#!/usr/bin/env bash
# Install MCP server dependencies
# Idempotent: skips already-installed servers
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() { echo "[mcp] $*"; }

# Install core MCP servers via npm (if npm is available)
if command -v npm &>/dev/null; then
  log "Installing core MCP servers..."
  servers=(
    "@modelcontextprotocol/server-filesystem"
    "@modelcontextprotocol/server-fetch"
    "@modelcontextprotocol/server-memory"
    "@modelcontextprotocol/server-sequential-thinking"
    "@modelcontextprotocol/server-github"
  )
  for server in "${servers[@]}"; do
    if ! npm list -g "$server" &>/dev/null; then
      npm install -g "$server" 2>/dev/null && log "  Installed: $server" || log "  Skipped: $server (install manually)"
    else
      log "  Already installed: $server"
    fi
  done
else
  log "npm not found — skip MCP server install. Install Node.js 20+ first."
fi

log "MCP installation complete"
