# Citadel SaaS Factory — Project Constitution

> Universal Full-Stack SaaS Production Framework — 500+ Autonomous Business Agents across 30 Domains
> Version 4.0 | citadelcloudmanagement.com | MIT License

---

## Tech Stack & Architecture

| Layer | Technology | Location |
|-------|-----------|----------|
| Backend | FastAPI (Python 3.12) | `backend/` |
| Frontend | Next.js 14 (TypeScript) | `frontend/` |
| Database | PostgreSQL 16 (pgvector, RLS) | `docker-compose.yml` |
| Cache | Redis 7 | `docker-compose.yml` |
| Auth | Keycloak 24 (OAuth2, RBAC, MFA) | `docker-compose.yml` |
| Storage | MinIO (S3-compatible) | `docker-compose.yml` |
| Messaging | RabbitMQ | `docker-compose.yml` |
| Orchestration | K3s + ArgoCD (GitOps) | `gitops/`, `infrastructure/` |
| Reverse Proxy | Traefik | `docker-compose.yml` |
| Service Mesh | Linkerd (mTLS) | `networks/service-mesh/` |
| Secrets | HashiCorp Vault | `infrastructure/` |
| Monitoring | Prometheus + Grafana + Loki + Tempo | `monitoring/` |
| Security | Falco + Kyverno + Semgrep + Trivy | `security/` |
| Guardrails | Guardrails AI + DeepEval + NeMo | `security/guardrails/` |

## Repository Structure

```
citadel-saas-factory/
├── CLAUDE.md                      ← YOU ARE HERE (project constitution)
├── .claude/                       ← intelligence layer
│   ├── agents/                    ← 500+ agent definitions (15 domain folders + standalone)
│   │   └── _registry.yaml         ← master agent registry
│   ├── commands/                  ← /deploy, /review, /test, /audit, etc.
│   ├── hooks/                     ← pre-commit, post-deploy, vault-autolink
│   ├── rules/                     ← 23 coding standards (security, testing, api-design, etc.)
│   ├── skills/                    ← specialist capabilities (code-review, guardrails, llm-wiki)
│   ├── memory/                    ← persistent project memory
│   ├── mcp/                       ← MCP server configs (github, postgres, docker, k8s, etc.)
│   ├── templates/                 ← code generation templates (.py, .ts, .tsx, .tf, .yml)
│   └── settings.json              ← hooks, permissions, model routing
├── backend/                       ← FastAPI (Python 3.12) — see backend/CLAUDE.md
├── frontend/                      ← Next.js 14 (TypeScript) — see frontend/CLAUDE.md
├── backbone/                      ← agent orchestrator, memory, governance, tools
├── agents/                        ← agent providers + router
├── subagents/                     ← subagent catalog
├── infrastructure/                ← Terraform, Helm, Ansible
├── gitops/                        ← ArgoCD + Kustomize overlays
├── monitoring/                    ← Prometheus rules, Grafana dashboards, Loki, Alertmanager
├── security/                      ← Falco, Kyverno, OPA, Sigma, Trivy, Guardrails
├── compliance/                    ← frameworks, checklists, evidence, policies
├── networks/                      ← agent protocols, service mesh, VPN, discovery
├── models/                        ← model catalog, routing, embeddings, rerankers, vision
├── mcp/                           ← MCP gateway + registry
├── engines/                       ← LLM engine configs (paid, free, local-ollama)
├── evals/                         ← deepeval + promptfoo evaluation
├── docs/                          ← ADRs, runbooks, vault (Obsidian), references
│   └── vault/                     ← Obsidian knowledge vault + LLM Wiki
├── scripts/                       ← bootstrap, deploy, verify, setup-claude-code
├── starter-kit/                   ← standalone starter for new projects
├── tools/                         ← tool catalog
├── docker-compose.yml             ← local dev stack
├── Makefile                       ← all commands: dev, test, lint, deploy, wiki-*, setup-claude
└── .env.example                   ← environment variable contract
```

## Commands

```bash
# Development
make dev                    # Start full Docker stack
make stop                   # Stop all services
make backend                # Start backend dev server (port 8000)
make frontend               # Start frontend dev server

# Quality
make test                   # Run all tests
make lint                   # Run linters (ruff + eslint)
make security               # Security scans (semgrep + trivy)

# Deployment
make deploy                 # Deploy to target environment
./scripts/rollback.sh       # Emergency rollback

# Claude Code Setup
make setup-claude           # Install master prompt + .claude/ scaffolding
make setup-claude-target TARGET=/path/to/project  # Install into any project

# Bootstrap
make bootstrap-parallel     # Full parallel install (models, MCP, hooks, agents)
make bootstrap-dry          # Dry-run bootstrap
make detect-business        # Detect business vertical
make install-models         # Install Ollama + open-weights models
make install-mcp            # Install MCP server dependencies
make install-hooks          # Install git hooks (Lefthook)

# Knowledge Layer
make vault-generate         # Regenerate agent notes in docs/vault/
make vault-sync             # Refresh Graphify + memory mirrors
make vault-audit            # Audit vault integrity
make wiki-ingest FILE=raw/x # Ingest source into LLM Wiki
make wiki-lint              # Wiki health-check
make wiki-sync              # Refresh wiki + lint

# Engines
make run-paid               # Claude via Anthropic API
make run-free               # Claude via OpenRouter free tier
make run-local              # Claude via local Ollama

# Status
make status                 # System health (agents, models, rules, skills, providers)
```

## Style & Conventions

- **Immutability**: Always create new objects, never mutate existing ones
- **Small files**: 200-400 lines typical, 800 max
- **Small functions**: Under 50 lines, single responsibility
- **No deep nesting**: Max 4 levels
- **Naming**: kebab-case files, PascalCase components, camelCase variables, snake_case Python
- **Error handling**: Handle at every level, never swallow silently, structured error responses
- **Input validation**: Validate at system boundaries, fail fast with clear messages

## Testing

- **TDD mandatory**: Write tests first (RED), implement (GREEN), refactor (IMPROVE)
- **80% minimum** code coverage
- **Test pyramid**: unit > integration > E2E
- **Backend**: `pytest --cov=app` (co-located test files)
- **Frontend**: `npm test` (Vitest, co-located as `*.test.ts`)
- **E2E**: Playwright in `tests/e2e/`
- **Tests must be independent and deterministic**

## Git Workflow

- **Conventional commits**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
- **Branch naming**: `feature/<ticket>-<slug>`, `fix/<ticket>-<slug>`, `chore/<slug>`
- **Squash-merge** to main; never rebase shared branches
- **PR required** for all changes, 1 approval minimum
- **CI must pass** (lint, test, security scan) before merge
- **No force push** to main/production

## Security Rules

- **No hardcoded secrets** — use `.env.local` (gitignored) or HashiCorp Vault
- **Validate all user input** at system boundaries
- **Parameterized queries only** — no SQL string concatenation
- **Rate limiting** on all API endpoints
- **CORS, CSRF, XSS protection** on all routes
- **Container image scanning** before deployment (Trivy)
- **Secret scanning** in pre-commit hooks (gitleaks)
- **TLS everywhere** in production
- **Pre-commit hook** runs `gitleaks` + secret scan; blocks on failure
- `.env.example` is the contract — update it with every new variable

## Agent System — 500+ Agents, 30 Domains

Full registry: `.claude/agents/_registry.yaml`

| Domain | Agents | Location |
|--------|--------|----------|
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
| Mobile Engineering | 18 | `_registry.yaml` (scaffold with `make render-agents`) |
| SRE & Reliability | 14 | `_registry.yaml` (scaffold with `make render-agents`) |
| ML Engineering | 16 | `_registry.yaml` (scaffold with `make render-agents`) |
| Supply Chain | 12 | `_registry.yaml` (scaffold with `make render-agents`) |
| Platform Engineering | 12 | `_registry.yaml` (scaffold with `make render-agents`) |
| Internationalization | 10 | `_registry.yaml` (scaffold with `make render-agents`) |
| AI/ML Operations | 16 | `_registry.yaml` (scaffold with `make render-agents`) |
| IoT & Edge | 10 | `_registry.yaml` (scaffold with `make render-agents`) |
| Education & Training | 8 | `_registry.yaml` (scaffold with `make render-agents`) |
| Compliance & Risk | 12 | `_registry.yaml` (scaffold with `make render-agents`) |
| Brand & Creative | 10 | `_registry.yaml` (scaffold with `make render-agents`) |
| Revenue Operations | 12 | `_registry.yaml` (scaffold with `make render-agents`) |
| Documentation | 10 | `_registry.yaml` (scaffold with `make render-agents`) |
| Developer Experience | 10 | `_registry.yaml` (scaffold with `make render-agents`) |
| Research & Intelligence | 10 | `_registry.yaml` (scaffold with `make render-agents`) |

> **15 domains** have dedicated folders in `.claude/agents/`. The remaining 15 are defined in `_registry.yaml` and scaffolded on demand with `make render-agents`.

## Tool Integrations

- **Ruflo** — Multi-agent swarm orchestration (mesh topology, CYCLE_INTERVAL=0)
- **Graphify** — Codebase knowledge graph (Tree-sitter AST, 25 languages)
- **GitHub Actions** — CI/CD with security gates (SAST, SCA, secret scan, container scan)
- **Obsidian** — Knowledge vault at `docs/vault/` with bidirectional wikilinks
- **LLM Wiki** — Karpathy pattern: `docs/vault/raw/` (immutable) + `docs/vault/wiki/` (compiled)

## Model Routing

| Tier | Model | Use Case |
|------|-------|----------|
| Default | Claude Sonnet 4.6 | Standard coding tasks |
| Cheap | Claude Haiku 4.5 | Classification, routing, extraction |
| Premium | Claude Opus 4.7 | Architecture, complex reasoning, agentic |

Routing config: `models/routing.yaml` | Catalog: `models/catalog.yaml`
12 providers supported — switch by changing one env var.

## Guardrails (Mandatory)

Every LLM call routes through `backend/app/middleware/guardrails.py`:
- Schema check → HallucinationFree (threshold ≥ 0.85) → ProvenanceLLM → ToxicLanguage → DetectPII
- Re-ask up to 3 times on failure, then reject
- All validations logged to `.claude/memory/`
- deepeval in CI: hallucination rate ≤ 5% per PR

## MCP Connections

Configured in `.claude/mcp/` and `.mcp.json`:

| Server | Config | Purpose |
|--------|--------|---------|
| GitHub | `.claude/mcp/github.json` | Repos, PRs, issues, Actions |
| PostgreSQL | `.claude/mcp/postgres.json` | Database queries |
| Docker | `.claude/mcp/docker.json` | Container management |
| Kubernetes | `.claude/mcp/kubernetes.json` | Cluster operations |
| Filesystem | `.claude/mcp/filesystem.json` | File access |
| Redis | `.claude/mcp/redis.json` | Cache operations |
| Vault | `.claude/mcp/vault.json` | Secret management |
| Prometheus | `.claude/mcp/prometheus.json` | Metrics queries |

## Hooks (settings.json)

| Event | Trigger | Action |
|-------|---------|--------|
| PreToolUse | Write `*.py` | `ruff check` |
| PreToolUse | Write `*.ts`/`*.tsx` | `npx eslint` |
| PreToolUse | Grep/Glob | Remind to check LLM Wiki first |
| PostToolUse | Write `*.py` | `ruff format` |
| PostToolUse | Write `*.ts`/`*.tsx` | `npx prettier` |
| PostToolUse | Write `docs/vault/*.md` | `vault-autolink.sh` |

## Knowledge Layer

### Obsidian Vault (`docs/vault/`)
- Every `.md` file must have a `## Vault Links` section with `[[wikilinks]]`
- Bidirectional linking enforced by `vault-autolink.sh`
- Graph view: `docs/vault/_index.md` is the entry point

### LLM Wiki (Karpathy Pattern)
- `docs/vault/raw/` — immutable source documents (LLM reads, never modifies)
- `docs/vault/wiki/` — LLM-maintained compiled knowledge
- `docs/vault/wiki/index.md` — **always consult before grepping raw sources**
- `docs/vault/SCHEMA.md` — governance, co-evolved between human and LLM

## Do / Don't

DO:
- Run `make test` before every commit
- Update `.env.example` when adding env vars
- Write ADRs for decisions that affect architecture (`docs/adr/`)
- Use `.claude/templates/` for code generation
- Check `docs/vault/wiki/index.md` before grepping the codebase
- Keep startup deterministic: clone → env → bootstrap → run

DON'T:
- Commit to `main` directly
- Commit secrets (`.env`, `*.pem`, `*.key`)
- Install new top-level deps without a PR discussion
- Introduce a new framework without an ADR
- Bypass guardrails or skip validation
- Force push to main/production
- Invent new architecture at runtime — prefer reusable templates
