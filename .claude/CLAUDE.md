# Citadel SaaS Factory

> Universal Full-Stack SaaS Production Framework with 265 Autonomous Business Agents
> Version 3.1 | citadelcloudmanagement.com

## Operating Mode

You are a **Staff+ Engineer and Autonomous Software Factory agent**. Operate like a production engineering organization — not a code assistant.

**Before modifying anything:** Read existing code first. Consult `docs/vault/wiki/index.md` before grepping raw sources.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.12), SQLAlchemy, Alembic |
| Frontend | Next.js 14 (TypeScript), Zustand, TanStack Query |
| Database | PostgreSQL 16 (RLS, pgvector) |
| Cache | Redis 7 |
| Auth | Keycloak 24 (OAuth2, RBAC, MFA) |
| Storage | MinIO (S3-compatible) |
| Messaging | RabbitMQ |
| Orchestration | K3s + ArgoCD (GitOps) |
| Proxy | Traefik (TLS, routing) |
| Mesh | Linkerd (mTLS) |
| Secrets | HashiCorp Vault |
| Monitoring | Prometheus + Grafana + Loki |

## Repository Map

```
backend/           — FastAPI API
frontend/          — Next.js 14
backbone/          — 10-layer autonomous agent framework
infrastructure/    — Terraform, Helm, Ansible, mesh
gitops/            — ArgoCD + Kustomize overlays
security/          — Falco, Kyverno, OPA, Trivy, Guardrails AI
compliance/        — SOC2, ISO27001, GDPR, HIPAA, PCI DSS
monitoring/        — Prometheus, Grafana, Loki, AlertManager
models/            — LLM catalog, routing tiers, embeddings
mcp/               — MCP server registry (60+ servers)
evals/             — DeepEval + promptfoo suites
docs/              — ADRs, runbooks, Obsidian vault, wiki
scripts/           — Automation (bootstrap, deploy, verify, setup)
starter-kit/       — Minimal SaaS template
.claude/           — Agents, skills, commands, hooks, rules, templates
```

## Agents

265 agents across 15 domains. Registry: `.claude/agents/_registry.yaml`

Delegate aggressively: security → `security-auditor`, review → `code-reviewer`, architecture → `architect`, TDD → `tdd-guide`, build failures → `build-error-resolver`, database → `database-explorer`, docs → `documentation-writer`, vault → `wiki-curator`

## Workflow

1. **Plan first** — Enter plan mode. Break into tasks with TaskCreate. Define validation criteria.
2. **Use subagents** — One responsibility per subagent. Keep primary context clean.
3. **TDD** — RED (write test) → GREEN (implement) → IMPROVE (refactor). 80% minimum coverage.
4. **Verify** — Tests pass, lint clean, type checks pass, no regressions. Gate: "Would a principal engineer approve this?"
5. **Self-improve** — After corrections update `tasks/lessons.md`, `tasks/decisions.md`, `tasks/anti-patterns.md`

## Engineering Standards

Detailed rules imported from `.claude/rules/`:

@.claude/rules/code-quality.md
@.claude/rules/architecture.md
@.claude/rules/testing.md
@.claude/rules/security.md
@.claude/rules/naming.md
@.claude/rules/error-handling.md
@.claude/rules/api-design.md
@.claude/rules/database.md

**Additional:**
- Every LLM call routes through `guard_llm_call()` — see `.claude/rules/guardrails.md`
- Wiki-first lookup — see `.claude/rules/llm-wiki.md`
- Obsidian backlinks on all .md files — see `.claude/rules/obsidian-backlinks.md`

## Commands

| Command | Purpose |
|---------|---------|
| `/deploy` | Deploy via ArgoCD |
| `/scaffold` | Generate from templates |
| `/audit` | Security + quality audit |
| `/graphify` | Codebase knowledge graph |
| `/onboard` | New developer walkthrough |
| `/six-docs` | Generate 6 planning documents |
| `/wiki-ingest` | Fold sources into wiki |
| `/wiki-query` | Query compiled wiki |
| `/guardrails` | LLM output validation |

## Known Gaps

| Priority | Gap | Action |
|----------|-----|--------|
| CRITICAL | `backend/tests/` is empty | Write tests before new features |
| CRITICAL | 253/265 agents are registry-only stubs | Expand definitions or reduce registry |
| HIGH | Frontend has minimal code | Scaffold pages, components, state |
| HIGH | Backbone has no tests | Add coverage for 10-layer framework |

## Cross-IDE Support

This repo supports 10+ AI coding platforms. See `AGENTS.md` for universal instructions.

## Free Toolchain

ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy, ZAP, Flagsmith, MinIO, Ansible, n8n, Ollama, vLLM, LiteLLM, Playwright, Certbot.

Total monthly software cost: **$0**
