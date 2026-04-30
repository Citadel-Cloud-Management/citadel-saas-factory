# GitHub Copilot Instructions

> **Canonical context**: [`context.md`](../context.md) — all architecture, standards, conventions, and agent system details.

## Project

Citadel SaaS Factory — 500+ agent SaaS framework. FastAPI (Python 3.12) + Next.js 14 (TypeScript) + PostgreSQL 16 + K3s + ArgoCD.

## Key Rules for Copilot Suggestions

- **Immutability**: always create new objects, never mutate
- **Type safety**: Python type hints required, TypeScript strict mode
- **Security**: no hardcoded secrets, parameterized queries only, validate all input
- **Testing**: TDD mandatory, 80% minimum coverage
- **Architecture**: clean layers (domain → use cases → interfaces → infrastructure)
- **Git**: conventional commits (feat, fix, refactor, docs, test, chore, perf, ci)
- **Guardrails**: all LLM output passes through guardrails validation

## Multi-Model

See `models/routing.yaml` for tier-based model selection across 12 providers.

For full details, see [`context.md`](../context.md).
