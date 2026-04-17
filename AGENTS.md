# Universal Agent Instructions

> This file is read by OpenAI Codex Cloud, Google Jules, Factory AI Droids, and any tool that supports the AGENTS.md convention. For Claude Code, see CLAUDE.md. For Cursor, see .cursor/rules/. For Copilot, see .github/copilot-instructions.md.

## Project Overview

Citadel SaaS Factory is an infrastructure-agnostic SaaS framework with 265 autonomous business agents across 15 domains. It runs on any Linux server with SSH and Docker. Zero vendor lock-in. Total software cost: $0/month.

## Stack

- Backend: FastAPI (Python 3.12)
- Frontend: Next.js 14 (TypeScript)
- Database: PostgreSQL 16 + Redis 7
- Auth: Keycloak 24 (OAuth2, RBAC, MFA)
- Storage: MinIO (S3-compatible)
- Messaging: RabbitMQ
- Orchestration: K3s + ArgoCD (GitOps)
- Reverse Proxy: Traefik
- Service Mesh: Linkerd (mTLS)
- Secrets: HashiCorp Vault

## Conventions

- Immutability by default — create new objects, never mutate
- Small files: 200-400 lines typical, 800 max
- TDD mandatory: write tests first, 80% minimum coverage
- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci
- Clean architecture: domain > use cases > interfaces > infrastructure
- No hardcoded secrets — use env vars or Vault
- Parameterized queries only
- Rate limiting on all endpoints
- WCAG 2.1 AA accessibility minimum

## Multi-Model Support

This repo supports multiple AI model providers. See `models/routing.yaml` for tier-based model selection. Agents reference model tiers, not specific models:

| Tier | Primary | Use Case |
|------|---------|----------|
| `reasoning_deep` | Claude Opus 4.6 | Architecture, critical decisions |
| `reasoning_fast` | Claude Sonnet 4.6 | Default coding tasks |
| `cheap_fast` | Claude Haiku 4.5 | Completion, boilerplate |
| `long_context` | Gemini 3.1 Pro | Full codebase analysis (2M tokens) |
| `code_specialist` | Codestral 25 | Code generation and review |
| `vision` | Claude Opus 4.6 | Screenshot/design to code |
| `local_only` | Llama 3.3 70B | Air-gapped, zero cost |

## Agent System

265 agents across 15 domains defined in `.claude/agents/_registry.yaml`. Each agent has tools, model tier, and approval requirements specified in YAML frontmatter.

Domains: Executive, Marketing, Sales, Customer Success, Product, Engineering, Frontend, DevOps, Security, Data, QA, HR, Finance, Legal, Content.

## Directory Structure

```
backend/          — FastAPI application
frontend/         — Next.js application
infrastructure/   — Helm charts, Terraform
gitops/           — ArgoCD manifests
security/         — Kyverno, Falco, Trivy, Guardrails
monitoring/       — Prometheus, Grafana, Loki
docs/             — Vault, ADRs, runbooks, API docs
models/           — Multi-model catalog and routing
agents/           — Provider configs and runtime
scripts/          — Bootstrap and install scripts
evals/            — Model evaluation framework
mcp/              — MCP server registry and gateway
subagents/        — Parallel worker definitions
tools/            — Agent tool catalog
networks/         — Mesh, VPN, discovery, protocols
compliance/       — GDPR, SOC2, HIPAA, PCI frameworks
```

## Security

- No hardcoded secrets — use environment variables or Vault
- All user input validated at system boundaries
- Parameterized queries only — no SQL string concatenation
- Rate limiting on all API endpoints
- Container image scanning before deployment
- Secret scanning in pre-commit hooks
- All LLM output passes through guardrails validation

## Getting Started

```bash
git clone <repo-url>
cd citadel-saas-factory
./scripts/parallel-bootstrap.sh
```
