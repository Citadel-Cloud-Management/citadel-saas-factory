#!/usr/bin/env bash
# Render agent definitions from .claude/agents/ to Cursor and Antigravity formats
# Idempotent: overwrites target files each run
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CURSOR_DIR="$REPO_ROOT/.cursor/subagents"
ANTIGRAVITY_DIR="$REPO_ROOT/.antigravity/workflows"

log() { echo "[render] $*"; }

mkdir -p "$CURSOR_DIR" "$ANTIGRAVITY_DIR"

count=0

render_agent() {
  local agent_file="$1"
  local name
  name=$(basename "$agent_file" .md)
  [[ "$name" == "_registry" ]] && return
  [[ "$name" == "README" ]] && return

  local parent_dir
  parent_dir=$(basename "$(dirname "$agent_file")")

  # Extract description from first non-header, non-empty line
  local desc
  desc=$(grep -m1 "^[^#\-]" "$agent_file" 2>/dev/null | head -1 | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/ /g' || echo "Agent: $name")
  [[ -z "$desc" ]] && desc="Agent: $name"
  # Ensure single-line (strip newlines)
  desc="${desc//$'\n'/ }"

  # Cursor subagent format (JSON)
  cat > "$CURSOR_DIR/$name.json" << JSON
{
  "name": "$name",
  "description": "$desc",
  "source": ".claude/agents/$parent_dir/$name.md"
}
JSON

  # Antigravity workflow format (YAML)
  cat > "$ANTIGRAVITY_DIR/$name.yaml" << YAML
name: $name
description: "$desc"
source: .claude/agents/$parent_dir/$name.md
model: gemini-3-pro
artifacts: [plan, diff]
YAML

  count=$((count + 1))
}

# Process all agent markdown files
for agent_file in "$REPO_ROOT"/.claude/agents/*.md; do
  [[ -f "$agent_file" ]] && render_agent "$agent_file"
done

for agent_dir in "$REPO_ROOT"/.claude/agents/*/; do
  [[ -d "$agent_dir" ]] || continue
  for agent_file in "$agent_dir"*.md; do
    [[ -f "$agent_file" ]] && render_agent "$agent_file"
  done
done

log "Rendered $count agents to Cursor and Antigravity formats"
