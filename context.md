---
version: "1.0.0"
last_updated: "2026-04-30"
schema_version: 1
compatible_tools:
  - claude-code
  - codex
  - cursor
  - gemini
  - copilot
  - continue
  - openhands
  - antigravity
---

# Citadel SaaS Factory — Canonical Context

> **Single source of truth** for all AI agents, IDEs, CI/CD pipelines, and human contributors.
> Referenced by: CLAUDE.md, AGENTS.md, AGENT.md, GEMINI.md, copilot-instructions.md, .cursor/rules/, .antigravity/rules.md
>
> Version: 1.0.0 | License: MIT | Owner: Citadel Cloud Management
> Repository: github.com/kogunlowo123/citadel-saas-factory

---

## 1. Repository Identity

| Field | Value |
|-------|-------|
| **Project** | Citadel SaaS Factory |
| **Mission** | Universal full-stack SaaS production framework with 500+ autonomous business agents across 30 domains |
| **Architecture Vision** | Infrastructure-agnostic, zero vendor lock-in, zero software cost, production-grade from day one |
| **Product Scope** | Complete SaaS lifecycle — from agent-driven development to autonomous business operations |
| **Deployment Targets** | Any Linux server with SSH + Docker; K3s for orchestration; ArgoCD for GitOps |
| **Environments** | local (Docker Compose) → staging (K3s) → production (K3s + ArgoCD) |
| **Primary Domain** | citadelcloudmanagement.com |

---

## 2. System Architecture

### 2.1 Frontend

| Attribute | Value |
|-----------|-------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript (strict mode) |
| React | 18 (server components by default) |
| State | Zustand (client), TanStack Query (server) |
| Styling | Tailwind CSS (utility-first) |
| Testing | Vitest (co-located as `*.test.ts`) |
| Location | `frontend/` |

### 2.2 Backend

| Attribute | Value |
|-----------|-------|
| Framework | FastAPI |
| Language | Python 3.12 |
| ORM | SQLAlchemy 2.0+ |
| Migrations | Alembic |
| Architecture | Clean layers: routes → services → repositories → models |
| API prefix | `/api/v1/` |
| Multi-tenant | `tenant_id` set via middleware |
| Async | All endpoints use `async def` |
| Location | `backend/` |

### 2.3 Database & Storage

| Service | Technology | Purpose |
|---------|-----------|---------|
| Primary DB | PostgreSQL 16 (pgvector, RLS) | Relational data, vector embeddings, row-level security |
| Cache | Redis 7 | Hot data caching, session store |
| Object Storage | MinIO (S3-compatible) | File uploads, assets |
| Messaging | RabbitMQ | Event-driven async communication |

### 2.4 Auth & Security

| Component | Technology |
|-----------|-----------|
| Identity Provider | Keycloak 24 (OAuth2, RBAC, MFA) |
| Service Mesh | Linkerd (mTLS between services) |
| Secrets | HashiCorp Vault (production), `.env` (development) |
| TLS | Everywhere in production |

### 2.5 Infrastructure & Orchestration

| Component | Technology |
|-----------|-----------|
| Container Orchestration | K3s |
| GitOps | ArgoCD + Kustomize overlays |
| Reverse Proxy | Traefik |
| IaC | Terraform + Helm + Ansible |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry |

### 2.6 Observability

| Component | Technology |
|-----------|-----------|
| Metrics | Prometheus |
| Dashboards | Grafana |
| Logs | Loki |
| Tracing | Tempo |
| Alerting | Alertmanager |

### 2.7 Security Tooling

| Tool | Purpose |
|------|---------|
| Semgrep | SAST (static analysis) |
| Trivy | Container + dependency scanning |
| Falco | Runtime threat detection |
| Kyverno | Kubernetes policy enforcement |
| Gitleaks | Secret scanning (pre-commit) |
| Guardrails AI | LLM output validation |
| DeepEval | LLM evaluation in CI |
| NeMo Guardrails | Additional LLM safety |

---

## 3. Engineering Standards

### 3.1 Code Style

- **Immutability by default** — always create new objects, never mutate existing ones
- **Small files**: 200–400 lines typical, 800 max
- **Small functions**: under 50 lines, single responsibility
- **No deep nesting**: max 4 levels
- **No dead code** — remove unused imports, functions, variables

### 3.2 Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| Python functions/variables | `snake_case` | `get_user_by_id` |
| Python classes | `PascalCase` | `UserService` |
| TypeScript functions/variables | `camelCase` | `getUserById` |
| TypeScript components/types | `PascalCase` | `UserProfile` |
| Files | `kebab-case` | `user-service.py`, `auth-form.tsx` |
| Database tables/columns | `snake_case` (plural tables) | `users.created_at` |
| Environment variables | `UPPER_SNAKE_CASE` | `DATABASE_URL` |

### 3.3 Architecture Principles

- **Clean architecture**: domain → use cases → interfaces → infrastructure
- **Dependency direction**: outer layers depend on inner layers, never reverse
- **Repository pattern** for data access
- **Service layer** for business logic
- **No business logic in controllers or routes**
- **Domain-driven design**: ubiquitous language, bounded contexts

### 3.4 API Design

- RESTful conventions: nouns for resources, HTTP verbs for actions
- Consistent response envelope: `{ data, error, meta }`
- API versioning via URL prefix: `/api/v1/`
- Pagination on all list endpoints (cursor or offset)
- OpenAPI spec for all endpoints
- Rate limiting headers in responses

### 3.5 Error Handling

- Structured error responses with error codes
- Never swallow errors silently
- User-friendly messages in API responses
- Detailed error context in server logs
- Retry with exponential backoff for transient failures

### 3.6 Linting & Formatting

| Language | Linter | Formatter |
|----------|--------|-----------|
| Python | `ruff check` | `ruff format` |
| TypeScript | ESLint | Prettier |

### 3.7 Testing

- **TDD mandatory**: write tests first (RED), implement (GREEN), refactor (IMPROVE)
- **80% minimum** code coverage
- **Test pyramid**: unit > integration > E2E
- **Backend**: `pytest --cov=app` (co-located test files)
- **Frontend**: `npm test` (Vitest, co-located as `*.test.ts`)
- **E2E**: Playwright in `tests/e2e/`
- **Tests must be independent and deterministic**
- **Mock external services, not internal modules**

### 3.8 Git & Version Control

- **Conventional commits**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
- **Branch naming**: `feature/<ticket>-<slug>`, `fix/<ticket>-<slug>`, `chore/<slug>`
- **Squash-merge** to main; never rebase shared branches
- **PR required** for all changes, 1 approval minimum
- **CI must pass** (lint, test, security scan) before merge
- **No force push** to main/production

### 3.9 Dependencies

- Lock files committed (`package-lock.json`, `poetry.lock`)
- Regular security audits (`npm audit`, `pip-audit`)
- Minimal dependencies — avoid bloat
- License check: MIT, Apache-2.0, BSD preferred
- Pin major versions, allow minor/patch updates

---

## 4. AI Agent Operating Rules

### 4.1 Execution Policy

- **Plan before destructive ops** — state the plan, wait for approval on anything that touches production, deletes data, or costs money
- **Delegate research to subagents** — keep the main context clean
- **Use hooks for determinism** — don't rely on the LLM to remember to lint
- **Prefer skills over long prompts** — repeatable instruction sets belong in `.claude/skills/`
- **When uncertain, ask** — a clarifying question is cheaper than a rollback

### 4.2 Tool Usage Hierarchy

1. Check `docs/vault/wiki/index.md` before grepping raw sources
2. Use dedicated tools over shell commands (Read > cat, Grep > grep, Glob > find)
3. Use MCP tools when available for external systems
4. Use subagents for parallel research tasks

### 4.3 Validation Requirements

- **No hallucination**: all agent responses must be validated against source data or RAG context
- **Evidence-based generation**: cite sources, file paths, line numbers
- **Schema enforcement**: all structured outputs must specify and pass a JSON schema
- **Hallucination threshold**: outputs below 0.85 confidence trigger retry (max 3)

### 4.4 Guardrails (Mandatory)

Every LLM call routes through `backend/app/middleware/guardrails.py`:

| Validator | Purpose |
|-----------|---------|
| `hallucination_free` | Fabricated fact detection (threshold ≥ 0.85) |
| `provenance_llm` | RAG grounding verification |
| `toxic_language` | Toxic content filter |
| `detect_pii` | PII masking |

- Direct LLM client calls are **prohibited** — use `guard_llm_call()` wrapper
- Fail-closed in production: if guardrails library unavailable, reject LLM outputs
- All validations logged with timestamp, correlation ID, scores

### 4.5 Autonomous Execution Limits

- No unsupervised deployments to production
- No deletion of data without explicit approval
- No secret creation/rotation without approval
- No PR merges without CI passing
- Financial operations require human confirmation

---

## 5. Security Standards

### 5.1 Secrets Management

| Environment | Method |
|-------------|--------|
| Production | HashiCorp Vault only |
| Development | `.env` files (never committed, gitignored) |
| CI/CD | GitHub Secrets (masked in logs) |
| Rotation | Every 90 days |
| Pre-commit | Gitleaks + TruffleHog scanning |

### 5.2 Application Security

- **No hardcoded secrets** in source code — ever
- **Validate all user input** at system boundaries
- **Parameterized queries only** — no SQL string concatenation
- **Rate limiting** on all API endpoints
- **CORS, CSRF, XSS protection** on all routes
- **TLS everywhere** in production
- **Container image scanning** before deployment (Trivy)

### 5.3 Infrastructure Security

- **Least privilege** IAM for all service accounts
- **Network policies** enforced via Kyverno
- **mTLS** between services via Linkerd
- **Runtime monitoring** via Falco
- **PII redaction** in all logs
- **SBOM generation** for supply chain security

### 5.4 Compliance Frameworks

Tracked in `compliance/`:
- GDPR
- SOC2
- HIPAA
- PCI-DSS

---

## 6. DevOps & Infrastructure

### 6.1 Local Development

```bash
make dev                    # Start full Docker stack (postgres, redis, keycloak, minio, rabbitmq, mailhog)
make stop                   # Stop all services
make backend                # Start backend dev server (port 8000)
make frontend               # Start frontend dev server
```

### 6.2 Build & Test

```bash
make test                   # Run all tests (backend pytest + frontend vitest)
make lint                   # Run linters (ruff + eslint)
make security               # Security scans (semgrep + trivy)
```

### 6.3 Deployment

```bash
make deploy                 # Deploy to target environment
./scripts/rollback.sh       # Emergency rollback
```

- **GitOps**: all infrastructure as code, all changes via git
- **Immutable infrastructure**: never patch in place, rebuild
- **Rolling deployments** with automatic rollback on failure
- **Health probes**: liveness, readiness, startup on all services
- **Resource limits** on all containers (CPU + memory)

### 6.4 CI/CD Pipeline

Defined in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci-cd.yml` | Push/PR | Lint, test, security scan, build |
| `nightly-security.yml` | Cron | Full security audit |
| `release.yml` | Tag | Production release |
| `claude.yml` | Issue/PR | Claude Code automation |
| `parallel-agents.yml` | Manual | Multi-agent execution |
| `eval-models.yml` | Manual | Model evaluation |

### 6.5 Environment Promotion

`local` → `staging` → `production`

- `.env.example` is the environment variable contract — update with every new variable
- GitOps overlays in `gitops/` for each environment
- Kustomize for environment-specific configuration

---

## 7. Product Context

### 7.1 Business Goals

- Provide a complete, production-ready SaaS framework that any team can deploy
- Zero vendor lock-in: runs on any Linux server with SSH + Docker
- Zero software cost: all open-source components
- Agent-driven development: 500+ autonomous agents handle business operations

### 7.2 User Personas

- **Solo Founders** — need full-stack SaaS without a team
- **Small Engineering Teams** — need production-ready infrastructure
- **Enterprise DevOps** — need agent-driven automation at scale
- **AI Engineers** — need multi-model orchestration framework

### 7.3 Scaling Expectations

- Multi-tenant architecture with row-level security
- Horizontal scaling via K3s
- Connection pooling for database and Redis
- CDN for static assets
- Code splitting and lazy loading for frontend

---

## 8. AI/LLM Architecture

### 8.1 Model Routing

Defined in `models/routing.yaml`. Agents reference **tiers**, not specific models:

| Tier | Primary Model | Use Case |
|------|--------------|----------|
| `reasoning_deep` | Claude Opus 4.6 | Architecture, critical decisions |
| `reasoning_fast` | Claude Sonnet 4.6 | Default coding tasks |
| `cheap_fast` | Claude Haiku 4.5 | Tab completion, boilerplate |
| `long_context` | Gemini 3.1 Pro | Full codebase analysis (2M tokens) |
| `code_specialist` | Codestral 25 | Code generation and review |
| `vision` | Claude Opus 4.6 | Screenshot/design to code |
| `local_only` | Llama 4 Maverick | Air-gapped, zero cost |
| `ultra_context` | Llama 4 Scout | Full-repo analysis (1M–10M tokens) |
| `reasoning_chain` | o4 | Multi-step chain-of-thought |

12 providers supported — switch by changing one env var.
Full catalog: `models/catalog.yaml`

### 8.2 Agent System — 500+ Agents, 30 Domains

Full registry: `.claude/agents/_registry.yaml`

| Domain | Count | Location |
|--------|-------|----------|
| Executive & Strategy | 18 | `.claude/agents/executive/` |
| Marketing & Growth | 28 | `.claude/agents/marketing/` |
| Sales & Revenue | 24 | `.claude/agents/sales/` |
| Customer Success | 20 | `.claude/agents/customer-success/` |
| Product & UI/UX | 26 | `.claude/agents/product-design/` |
| Engineering | 35 | `.claude/agents/engineering/` |
| Frontend | 24 | `.claude/agents/frontend/` |
| DevOps | 34 | `.claude/agents/devops/` |
| Security | 28 | `.claude/agents/security/` |
| Data & Analytics | 24 | `.claude/agents/data-analytics/` |
| QA & Testing | 28 | `.claude/agents/qa-testing/` |
| HR & People | 16 | `.claude/agents/hr-people/` |
| Finance & Billing | 20 | `.claude/agents/finance/` |
| Legal & Governance | 14 | `.claude/agents/legal/` |
| Content & Comms | 16 | `.claude/agents/content/` |
| + 15 more domains | ~165 | `_registry.yaml` (scaffold with `make render-agents`) |

### 8.3 Memory Architecture

- **Project memory**: `.claude/memory/` (persistent across sessions)
- **LLM Wiki**: `docs/vault/wiki/` (compiled knowledge, Karpathy pattern)
- **Raw sources**: `docs/vault/raw/` (immutable, LLM reads never modifies)
- **Obsidian vault**: `docs/vault/` (bidirectional wikilinks, graph view)

### 8.4 Guardrails Pipeline

```
LLM Call → Schema Check → HallucinationFree (≥0.85) → ProvenanceLLM → ToxicLanguage → DetectPII → Output
                                                                                          ↓ (fail)
                                                                                    Re-ask (max 3) → Reject
```

- DeepEval in CI: hallucination rate ≤ 5% per PR
- All validations logged to `.claude/memory/`

### 8.5 Evaluation

- **promptfoo**: `evals/promptfoo.yaml` — model evaluation framework
- **DeepEval**: CI integration for hallucination detection
- **AI layer evals**: `ai/evals/` — task-specific evaluation

### 8.6 MCP Connections

| Server | Purpose |
|--------|---------|
| GitHub | Repos, PRs, issues, Actions |
| PostgreSQL | Database queries |
| Docker | Container management |
| Kubernetes | Cluster operations |
| Filesystem | File access |
| Redis | Cache operations |
| Vault | Secret management |
| Prometheus | Metrics queries |

Configs: `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor)

---

## 9. Repository Execution Map

### 9.1 Startup & Development

```bash
# First time setup
git clone <repo>
cp .env.example .env        # Fill in secrets
make dev                     # Start Docker stack
make backend                 # Start backend (port 8000)
make frontend                # Start frontend (port 3000)
```

### 9.2 Full Command Reference

```bash
# Development
make dev                     # Start full Docker stack
make stop                    # Stop all services
make backend                 # Backend dev server
make frontend                # Frontend dev server

# Quality
make test                    # Run all tests
make lint                    # Run linters
make security                # Security scans

# Deployment
make deploy                  # Deploy to environment
./scripts/rollback.sh        # Emergency rollback

# AI Layer
make ai-setup                # Bootstrap AI layer
make ai-eval                 # Run eval suite
make ai-eval-mock            # Eval without API key
make ai-agent TASK=<task>    # Run agent task
make ai-validate             # Validate ai/ layer integrity

# Knowledge Layer
make vault-generate          # Regenerate agent notes
make vault-sync              # Refresh Graphify + memory
make vault-audit             # Audit vault integrity
make wiki-ingest FILE=<path> # Ingest into LLM Wiki
make wiki-lint               # Wiki health-check

# Bootstrap
make bootstrap-parallel      # Full parallel install
make setup-claude            # Install Claude Code scaffolding
make render-agents           # Render agents to Cursor/Antigravity
make eval                    # Run promptfoo evaluation

# Engine Selection
make run-paid                # Claude via Anthropic API
make run-free                # Claude via OpenRouter free tier
make run-local               # Claude via local Ollama
make engine-status           # Print current engine config

# Status
make status                  # System health report
```

---

## 10. Directory Ownership Map

```
citadel-saas-factory/
├── context.md                     ← THIS FILE (canonical context)
├── CLAUDE.md                      ← Claude Code adapter → context.md
├── AGENTS.md                      ← Codex/Jules adapter → context.md
├── AGENT.md                       ← Cursor adapter → context.md
├── GEMINI.md                      ← Gemini adapter → context.md
├── CLAUDE_CODE_MASTER_PROMPT.md   ← Reference document (not operational)
├── .claude/                       ← Intelligence layer (agents, rules, skills, commands, hooks, memory)
├── .cursor/                       ← Cursor IDE config (rules, MCP, settings)
├── .codex/                        ← OpenAI Codex config
├── .continue/                     ← Continue.dev config
├── .antigravity/                  ← Gemini Antigravity config
├── .github/                       ← GitHub Actions, templates, Copilot instructions
├── backend/                       ← FastAPI application (Python 3.12)
├── frontend/                      ← Next.js 14 application (TypeScript)
├── agents/                        ← Agent provider configs and runtime router
├── subagents/                     ← Parallel worker definitions
├── backbone/                      ← Agent orchestrator, memory, governance, tools
├── ai/                            ← AI layer: prompts, evals, agents, tools
├── models/                        ← Model catalog, routing, embeddings, rerankers, vision
├── mcp/                           ← MCP gateway + registry
├── engines/                       ← LLM engine configs (paid, free, local-ollama)
├── evals/                         ← deepeval + promptfoo evaluation
├── tools/                         ← Agent tool catalog
├── infrastructure/                ← Terraform, Helm, Ansible
├── gitops/                        ← ArgoCD + Kustomize overlays
├── monitoring/                    ← Prometheus rules, Grafana dashboards, Loki, Alertmanager
├── security/                      ← Falco, Kyverno, OPA, Sigma, Trivy, Guardrails
├── compliance/                    ← GDPR, SOC2, HIPAA, PCI frameworks
├── networks/                      ← Agent protocols, service mesh, VPN, discovery
├── docs/                          ← Architecture, security, deployment, ADRs, runbooks
│   ├── vault/                     ← Obsidian knowledge vault + LLM Wiki
│   ├── adr/                       ← Architecture Decision Records
│   └── runbooks/                  ← Operational runbooks
├── scripts/                       ← Bootstrap, deploy, verify, setup
├── starter-kit/                   ← Standalone starter for new projects
├── docker-compose.yml             ← Local dev stack
├── Makefile                       ← All commands
├── Justfile                       ← Just runner (alternative to Make)
├── lefthook.yml                   ← Git hooks via Lefthook
└── .env.example                   ← Environment variable contract
```

---

## 11. Tool-Specific Adapters

Each AI tool has a dedicated instruction file that **references this context.md** rather than duplicating content. Tool-specific extensions (e.g., tool mappings, model configs) remain in each adapter.

| Tool | Adapter File | Extensions |
|------|-------------|------------|
| Claude Code | `CLAUDE.md` | Hooks, skills, commands, memory, MCP |
| OpenAI Codex | `AGENTS.md` | Approval mode, sandbox config |
| Cursor | `AGENT.md` | `.cursor/rules/`, `.cursor/mcp.json` |
| Gemini | `GEMINI.md` | Tool mapping, Antigravity workflows |
| GitHub Copilot | `.github/copilot-instructions.md` | Inline suggestions context |
| Continue.dev | `.continue/config.json` | Model selection, tab completion |
| OpenHands | `openhands/config.toml` | Sandbox, iteration limits |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-04-30 | Initial creation — consolidated from CLAUDE.md, AGENTS.md, AGENT.md, GEMINI.md, copilot-instructions.md, .cursor/rules/, .antigravity/rules.md |
