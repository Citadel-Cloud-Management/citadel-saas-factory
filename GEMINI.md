# Gemini Instructions

> This file configures Google Gemini Code Assist, Jules, and Antigravity for this repository.

## Project

Citadel SaaS Factory — 265-agent SaaS framework. FastAPI (Python 3.12) + Next.js 14 (TypeScript) + PostgreSQL 16 + K3s.

## Conventions

Follow the same conventions as AGENTS.md. Key points:

- Python: snake_case functions/variables, PascalCase classes, type hints required
- TypeScript: camelCase functions/variables, PascalCase components/types, strict mode
- Files: kebab-case (e.g., user-service.py, auth-form.tsx)
- Immutability by default — create new objects, never mutate
- TDD: tests first, 80% coverage minimum
- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci
- No hardcoded secrets — use env vars or Vault
- Clean architecture: domain > use cases > interfaces > infrastructure

## Multi-Model Context

This repo uses a model routing system at `models/routing.yaml`. Gemini models are included as primary or fallback in several tiers:

| Tier | Gemini Role |
|------|-------------|
| `long_context` | Gemini 3.1 Pro is primary (2M tokens) |
| `cheap_fast` | Gemini 3 Flash is fallback |
| `reasoning_deep` | Gemini 3 Pro is fallback |
| `reasoning_fast` | Gemini 3 Pro is fallback |

See `models/catalog.yaml` for full provider catalog.

## Tool Mapping

Gemini CLI tools map to Claude Code tools as follows:

| Gemini | Claude Code |
|--------|-------------|
| `read_file` | `Read` |
| `write_file` | `Write` |
| `edit_file` | `Edit` |
| `run_terminal` | `Bash` |
| `search_files` | `Grep` |
| `list_files` | `Glob` |

## Agent Definitions

Agent definitions live at `.claude/agents/` and are cross-rendered to `.antigravity/workflows/` for Gemini-based execution. Run `./scripts/render-agents.sh` to sync formats.

## Rules

Universal rules at `.claude/rules/` apply to all AI tools. Gemini-specific overrides in `.antigravity/rules.md`.

## Key Files

| What | Where |
|------|-------|
| Agent registry | `.claude/agents/_registry.yaml` |
| Model catalog | `models/catalog.yaml` |
| Model routing | `models/routing.yaml` |
| Rules | `.claude/rules/` |
| Skills | `.claude/skills/` |
| Bootstrap | `scripts/parallel-bootstrap.sh` |
