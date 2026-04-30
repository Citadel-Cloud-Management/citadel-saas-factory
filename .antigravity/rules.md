# Antigravity Rules

> **Canonical context**: [`context.md`](../context.md) — all architecture, standards, conventions, and agent system details.

## Project

Citadel SaaS Factory — 500+ agent SaaS framework. FastAPI + Next.js + PostgreSQL + K3s.

## Key Rules

- Immutability by default — create new objects, never mutate
- Small files (200-400 lines, 800 max)
- TDD mandatory (80% coverage)
- Conventional commits: feat, fix, refactor, docs, test, chore
- Clean architecture: domain > use cases > interfaces > infrastructure
- No hardcoded secrets — use env vars or Vault
- Parameterized queries only
- Rate limiting on all endpoints
- WCAG 2.1 AA accessibility

## Multi-Model

See `models/routing.yaml` for tier-based model selection.
See `models/catalog.yaml` for full provider catalog.

## Agents

500+ agents defined at `.claude/agents/_registry.yaml`.
Antigravity workflows at `.antigravity/workflows/`.

## Key Files

- Full context: [`context.md`](../context.md)
- Agent registry: `.claude/agents/_registry.yaml`
- Model catalog: `models/catalog.yaml`
- Model routing: `models/routing.yaml`
- Bootstrap: `scripts/parallel-bootstrap.sh`
