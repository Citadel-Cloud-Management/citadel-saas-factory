# Agent Instructions

> This file is the universal agent instruction file read by Cursor (AGENT.md), and any tool supporting this convention. It complements CLAUDE.md (Claude Code) and AGENTS.md (Codex/Jules).

## Overview

Citadel SaaS Factory — infrastructure-agnostic SaaS framework with 265 autonomous business agents across 15 domains. Zero vendor lock-in, zero software cost.

## For AI Agents

When working in this repo:

1. **Check model routing** — Read `models/routing.yaml` to understand which model tier applies to your task
2. **Check agent registry** — Read `.claude/agents/_registry.yaml` for available specialized agents
3. **Check rules** — Rules at `.claude/rules/` and `.cursor/rules/` define mandatory conventions
4. **Check MCP** — MCP configs at `.cursor/mcp.json` and `.mcp.json` define available tool servers
5. **Use guardrails** — All LLM output must pass through the guardrails validation layer

## Quick Reference

| What | Where |
|------|-------|
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
| Bootstrap | `scripts/parallel-bootstrap.sh` |
| Evals | `evals/promptfoo.yaml` |
| Docs | `docs/vault/` |
| Networks | `networks/` |

## Stack

- Backend: FastAPI (Python 3.12)
- Frontend: Next.js 14 (TypeScript)
- Database: PostgreSQL 16 + Redis 7
- Auth: Keycloak 24
- Orchestration: K3s + ArgoCD

## Conventions

- Immutability by default
- Small files (200-400 lines, 800 max)
- TDD mandatory (80% coverage)
- Conventional commits
- Clean architecture
- No hardcoded secrets
