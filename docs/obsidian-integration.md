# Obsidian + Claude Code Integration

Connect your Obsidian vault to Citadel SaaS Factory for persistent knowledge management across coding sessions.

## Strategy 1: Dedicated Developer Vault (Recommended)

Create a dedicated vault and symlink your project:

```bash
# Create vault
mkdir ~/Developer-Vault
cd ~/Developer-Vault

# Symlink Claude Code global config
ln -s ~/.claude claude-global

# Symlink this project
ln -s /path/to/citadel-saas-factory citadel
```

### Obsidian Configuration

Add to `.obsidian/app.json`:

```json
{
  "userIgnoreFilters": [
    "node_modules/",
    ".next/",
    "dist/",
    ".git/",
    ".vercel/",
    "public/",
    "__pycache__/",
    ".venv/",
    "graphify-out/"
  ]
}
```

## Strategy 2: MCP Bridge

Run Claude Code in your repo while an MCP server provides Obsidian vault access.

### Setup

1. Install the `obsidian-claude-code-mcp` plugin in Obsidian
2. It auto-discovers vaults via WebSocket on port 22360
3. Claude queries your vault without changing working directory

```bash
cd citadel-saas-factory
claude
# Claude can now query your Obsidian vault for context
```

## Strategy 3: Session Sync

Auto-export Claude Code sessions to Obsidian as searchable notes.

### Components

- **QMD**: Semantic search over markdown (60%+ token reduction vs grep)
- **sync-claude-sessions**: Auto-exports sessions to markdown on close
- **`/recall` skill**: Pulls relevant context before starting new sessions

## Required Obsidian Plugins

| Plugin | Purpose |
|--------|---------|
| File Explorer++ | Filter by wildcard/regex, toggle filters |
| Dataview | Query across all project files and metadata |
| Templater | Create standardized CLAUDE.md templates |

### Claude Code Integration (choose one)

| Plugin | Approach |
|--------|---------|
| Claudian | Sidebar chat with permission modes |
| Agent Client | Claude Code in side panel, @mention notes |
| Claude Sidebar | Embedded terminal, auto-launches Claude Code |

### MCP Plugins (choose one)

| Plugin | Approach |
|--------|---------|
| obsidian-claude-code-mcp | Auto-discover vaults via WebSocket |
| Claudesidian MCP | Full agent mode with semantic search via Ollama |

## Dataview Queries

### Add frontmatter to CLAUDE.md files

```yaml
---
type: claude-config
project: citadel-saas-factory
stack: [fastapi, nextjs, postgresql, redis]
status: active
---
```

### Query all project configs

```dataview
TABLE project, stack, status
FROM ""
WHERE type = "claude-config"
SORT project ASC
```

## Best Practices

- **Agents read, humans write** — keep Claude outputs in `.claude/`, authentic thinking in vault
- Use `/graphify .` to build knowledge graph, then export to Obsidian with `--obsidian-dir`
- Filter non-markdown files aggressively in Obsidian settings
- Disable "Detect all file extensions" in Settings > Files & Links

## Graphify + Obsidian Export

```bash
# Build knowledge graph and export to Obsidian
graphify build . --obsidian-dir ~/Developer-Vault/citadel-graph
```

This creates interlinked markdown notes from your codebase that Obsidian renders as a navigable knowledge graph.

## Reference

Full guide: [blog.starmorph.com/blog/obsidian-claude-code-integration-guide](https://blog.starmorph.com/blog/obsidian-claude-code-integration-guide)
