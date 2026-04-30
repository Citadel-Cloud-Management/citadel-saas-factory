# Universal Agent Instructions

> **Canonical context**: [`context.md`](context.md) — all architecture, standards, conventions, and agent system details.
> This file is read by OpenAI Codex Cloud, Google Jules, Factory AI Droids, and any tool supporting the AGENTS.md convention.
> For Claude Code, see CLAUDE.md. For Cursor, see AGENT.md. For Copilot, see .github/copilot-instructions.md.

## Quick Reference

| What | Where |
|------|-------|
| **Full project context** | [`context.md`](context.md) |
| Agent registry | `.claude/agents/_registry.yaml` |
| Model catalog | `models/catalog.yaml` |
| Model routing | `models/routing.yaml` |
| Rules | `.claude/rules/` |
| Skills | `.claude/skills/` |
| Subagents | `subagents/catalog.yaml` |
| Tools | `tools/catalog.yaml` |
| MCP servers | `mcp/registry.yaml` |
| Evals | `evals/promptfoo.yaml` |
| Docs | `docs/vault/` |
| Bootstrap | `scripts/parallel-bootstrap.sh` |

## Codex/Jules-Specific

- **Approval mode**: `suggest` — agents propose changes, human approves
- **Sandbox**: enabled — agents run in isolated environments
- **Instructions file**: this file (`AGENTS.md`)
- **Config**: `.codex/config.toml`

## Getting Started

```bash
git clone <repo-url>
cd citadel-saas-factory
./scripts/parallel-bootstrap.sh
```

For full stack, conventions, security, testing, and agent system details, see [`context.md`](context.md).
