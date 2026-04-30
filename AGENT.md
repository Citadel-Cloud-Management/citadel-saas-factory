# Agent Instructions

> **Canonical context**: [`context.md`](context.md) — all architecture, standards, conventions, and agent system details.
> This file is read by Cursor (AGENT.md) and any tool supporting this convention.
> It complements CLAUDE.md (Claude Code) and AGENTS.md (Codex/Jules).

## For AI Agents

When working in this repo:

1. **Read [`context.md`](context.md)** for full project context, stack, conventions, and security rules
2. **Check model routing** — `models/routing.yaml` for which model tier applies to your task
3. **Check agent registry** — `.claude/agents/_registry.yaml` for available specialized agents
4. **Check rules** — `.claude/rules/` and `.cursor/rules/` define mandatory conventions
5. **Check MCP** — `.cursor/mcp.json` and `.mcp.json` define available tool servers
6. **Use guardrails** — All LLM output must pass through the guardrails validation layer

## Quick Reference

| What | Where |
|------|-------|
| **Full project context** | [`context.md`](context.md) |
| Agent registry | `.claude/agents/_registry.yaml` |
| Model catalog | `models/catalog.yaml` |
| Model routing | `models/routing.yaml` |
| Embeddings | `models/embeddings.yaml` |
| Rerankers | `models/rerankers.yaml` |
| Vision/multimodal | `models/vision.yaml` |
| Rules | `.claude/rules/`, `.cursor/rules/` |
| Skills | `.claude/skills/` |
| MCP servers | `.cursor/mcp.json`, `mcp/registry.yaml` |
| Subagents | `subagents/catalog.yaml` |
| Tools | `tools/catalog.yaml` |
| Evals | `evals/promptfoo.yaml` |
| Docs | `docs/vault/` |
| Networks | `networks/` |

## Cursor-Specific

- Cursor rules: `.cursor/rules/project-context.mdc`, `.cursor/rules/multi-model.mdc`
- Cursor MCP: `.cursor/mcp.json`
- Cursor settings: `.cursor/settings.json`
