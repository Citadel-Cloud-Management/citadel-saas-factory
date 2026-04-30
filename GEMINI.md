# Gemini Instructions

> **Canonical context**: [`context.md`](context.md) — all architecture, standards, conventions, and agent system details.
> This file configures Google Gemini Code Assist, Jules, and Antigravity for this repository.

## Gemini-Specific Context

### Multi-Model Tiers (Gemini Roles)

| Tier | Gemini Role |
|------|-------------|
| `long_context` | Gemini 3.1 Pro is primary (2M tokens) |
| `cheap_fast` | Gemini 3 Flash is fallback |
| `reasoning_deep` | Gemini 3 Pro is fallback |
| `reasoning_fast` | Gemini 3 Pro is fallback |

See `models/catalog.yaml` for full provider catalog.

### Tool Mapping

Gemini CLI tools map to Claude Code tools as follows:

| Gemini | Claude Code |
|--------|-------------|
| `read_file` | `Read` |
| `write_file` | `Write` |
| `edit_file` | `Edit` |
| `run_terminal` | `Bash` |
| `search_files` | `Grep` |
| `list_files` | `Glob` |

### Antigravity Integration

- Agent definitions live at `.claude/agents/` and are cross-rendered to `.antigravity/workflows/` for Gemini-based execution
- Run `./scripts/render-agents.sh` to sync formats
- Antigravity config: `.antigravity/agent-manager.yaml`, `.antigravity/artifacts.config.yaml`

### Key Files

| What | Where |
|------|-------|
| **Full project context** | [`context.md`](context.md) |
| Agent registry | `.claude/agents/_registry.yaml` |
| Model catalog | `models/catalog.yaml` |
| Model routing | `models/routing.yaml` |
| Rules | `.claude/rules/` |
| Skills | `.claude/skills/` |
| Bootstrap | `scripts/parallel-bootstrap.sh` |

For full stack, conventions, security, testing, and agent system details, see [`context.md`](context.md).
