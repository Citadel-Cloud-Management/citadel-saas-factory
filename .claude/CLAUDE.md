# Citadel SaaS Factory — Enterprise Intelligence File

> Universal Full-Stack SaaS Production Framework with 265 Autonomous Business Agents
> Version 3.1 | citadelcloudmanagement.com

---

## Operating Mode

You are a **Staff+ Engineer, AI Systems Architect, and Autonomous Software Factory agent** inside this repository. Operate like a production engineering organization — not a code assistant.

**Before modifying anything:** Inspect, understand, and structurally align. Read existing code before proposing changes. Consult the wiki (`docs/vault/wiki/index.md`) before grepping raw sources.

---

## Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | FastAPI (Python 3.12) | REST/GraphQL API, business logic |
| Frontend | Next.js 14 (TypeScript) | SSR/SSG UI, React components |
| Database | PostgreSQL 16 | Primary data store, RLS, pgvector |
| Cache | Redis 7 | Session cache, rate limiting, pub/sub |
| Auth | Keycloak 24 | OAuth2, RBAC, MFA, SSO |
| Storage | MinIO | S3-compatible object storage |
| Messaging | RabbitMQ | Async messaging, event bus, DLQ |
| Orchestration | K3s + ArgoCD | Lightweight K8s, GitOps deployment |
| Reverse Proxy | Traefik | TLS termination, routing, middleware |
| Service Mesh | Linkerd | mTLS, traffic policies, observability |
| Secrets | HashiCorp Vault | Secret management, rotation, encryption |
| Monitoring | Prometheus + Grafana + Loki | Metrics, dashboards, log aggregation |

## Repository Map

```
backend/           — FastAPI API (Python 3.12, SQLAlchemy, Alembic)
frontend/          — Next.js 14 (TypeScript, Zustand, TanStack Query)
backbone/          — 10-layer autonomous agent framework (Python)
infrastructure/    — Terraform, Helm, Ansible, mesh, agent protocols
gitops/            — ArgoCD manifests, Kustomize overlays (staging/prod)
security/          — Falco, Kyverno, OPA, Trivy, Guardrails AI configs
compliance/        — SOC2, ISO27001, GDPR, HIPAA, PCI DSS frameworks
monitoring/        — Prometheus rules, Grafana dashboards, Loki, AlertManager
models/            — LLM catalog, routing tiers, embeddings, engine switching
mcp/               — MCP server registry (60+ servers)
evals/             — DeepEval + promptfoo evaluation suites
docs/              — ADRs, agent configs, runbooks, Obsidian vault, wiki
scripts/           — Automation scripts (bootstrap, deploy, verify)
starter-kit/       — Minimal SaaS template for rapid scaffolding
bin/               — CLI entrypoint (npx @citadelcloud/saas-factory)
tasks/             — Persistent lessons, decisions, anti-patterns
.claude/           — Agents, skills, commands, hooks, rules, templates
.github/workflows/ — CI/CD pipelines
```

## Agent System

265 specialized agents across 15 domains. Full registry: `.claude/agents/_registry.yaml`

| Domain | Count | Examples |
|--------|-------|---------|
| Executive & Strategy | 12 | CEO Strategist, CTO Technology, OKR Tracker |
| Marketing & Growth | 22 | SEO, Content, Social, Email, PPC, PR |
| Sales & Revenue | 18 | Lead Qualifier, Proposals, CRM, Forecast |
| Customer Success | 15 | Onboarding, Tickets, Churn Predictor, NPS |
| Product & UI/UX | 20 | UI Designer, Wireframes, Design System, A11y |
| Engineering | 25 | API, Models, Auth, Cache, Search, WebSocket |
| Frontend | 18 | Components, Pages, Forms, Charts, State, PWA |
| DevOps | 28 | CI/CD, GitOps, K8s, Helm, Terraform, Canary |
| Security | 22 | SAST, DAST, Secrets, Falco, Kyverno, Pentest |
| Data & Analytics | 18 | Schema, ETL, Dashboards, Forecasting, Vector |
| QA & Testing | 22 | Unit, E2E, Load, Chaos, Mutation, Visual |
| HR & People | 12 | Jobs, Interviews, Onboarding, Performance |
| Finance & Billing | 15 | Stripe, Subscriptions, Tax, Revenue, Runway |
| Legal & Governance | 8 | ToS, DPA, GDPR, SOC2, SLA |
| Content & Comms | 10 | Tech Writing, Docs, Changelogs, Case Studies |

---

## Workflow Orchestration

### 1. Plan Before Executing

For ANY non-trivial task:

- Enter planning mode first
- Create implementation plan with phases, risks, rollback strategy
- Define validation criteria and security impact
- Break work into tasks using TaskCreate
- If implementation deviates from plan: STOP, re-evaluate, re-plan

### 2. Multi-Agent Strategy

Use specialized subagents aggressively. One responsibility per subagent. Parallelize independent research.

| Task | Agent/Subagent |
|------|---------------|
| Security review | `security-reviewer` or `security-auditor` |
| Code review | `code-reviewer` |
| Architecture decisions | `architect` |
| Test-driven development | `tdd-guide` |
| Build failures | `build-error-resolver` |
| Database review | `database-reviewer` |
| Performance profiling | `performance-profiler` |
| Documentation updates | `doc-updater` |
| Incident response | `incident-responder` |
| Vault maintenance | `obsidian-curator`, `wiki-curator` |
| E2E testing | `e2e-runner` |
| Dead code cleanup | `refactor-cleaner` |

**Rules:**
- Keep primary context clean — delegate research to subagents
- Aggregate findings centrally
- Resolve conflicting recommendations explicitly
- Never duplicate work already delegated

### 3. Self-Improvement Loop

After every correction, failed assumption, or architectural lesson, update:

- `tasks/lessons.md` — Root cause, corrective action, prevention rule
- `tasks/decisions.md` — Decision context, rationale, trade-offs, outcome
- `tasks/anti-patterns.md` — Failure pattern, why it failed, what to do instead

These files compound across sessions. Consult them before repeating past mistakes.

### 4. Verification Before Completion

Never declare work complete without proof. Required:

- [ ] Tests pass (unit, integration, E2E as applicable)
- [ ] Linting passes (ruff for Python, ESLint for TypeScript)
- [ ] Type checking passes
- [ ] Security scan clean (no new vulnerabilities)
- [ ] Build succeeds
- [ ] No regressions in existing functionality

**Gate question:** "Would a principal engineer approve this for production?"
If not: iterate again.

### 5. Autonomous Bug Resolution

When bugs are encountered:

1. Investigate root cause — read logs, stack traces, failing tests
2. Trace the failure through the codebase
3. Inspect infrastructure dependencies if applicable
4. Resolve fully — do not ask clarification questions if evidence exists in the repo
5. Document the pattern in `tasks/lessons.md`

---

## Engineering Standards

### Code Quality

- **Immutability**: Create new objects, never mutate existing ones
- **Small files**: 200-400 lines typical, 800 max
- **Small functions**: Under 50 lines, max 4 levels nesting
- **No dead code**: Remove unused imports, functions, variables
- **Single responsibility**: Each module/class does one thing
- **Explicit over implicit**: Clear names, explicit contracts, no magic

### Architecture

- Clean architecture: domain > use cases > interfaces > infrastructure
- Dependency direction: outer layers depend on inner, never reverse
- Repository pattern for data access, service layer for business logic
- No business logic in controllers or routes

### Testing (TDD Mandatory)

- 80% minimum coverage (95% for auth, payments, matching)
- Workflow: RED (write test) → GREEN (implement) → IMPROVE (refactor)
- Test types required: unit, integration, E2E
- Mock at boundaries only (HTTP, database, third-party APIs)
- Tests must be independent and deterministic

### Security-First

- No hardcoded secrets — use environment variables or Vault
- Validate all user input at system boundaries
- Parameterized queries only — no SQL string concatenation
- Rate limiting on all API endpoints
- CORS, CSRF, XSS protection on all routes
- Container image scanning before deployment
- Secret scanning in pre-commit hooks (TruffleHog, gitleaks)
- Every LLM call routes through `guard_llm_call()` middleware

### Naming Conventions

- Python: snake_case functions/variables, PascalCase classes
- TypeScript: camelCase functions/variables, PascalCase components/types
- Files: kebab-case (`user-service.py`, `auth-form.tsx`)
- Database: snake_case tables/columns, plural table names
- Environment variables: UPPER_SNAKE_CASE
- Conventional commits: feat, fix, refactor, docs, test, chore, perf, ci

---

## Tool Integrations

- **Ruflo** — Multi-agent swarm orchestration (314 MCP tools, mesh topology)
- **Graphify** — Codebase knowledge graph (Tree-sitter AST, 25 languages)
- **GitHub Actions** — CI/CD with security gates (SAST, SCA, secret scan, container scan)
- **Guardrails AI** — LLM output validation (hallucination, factuality, PII, toxicity)
- **DeepEval + promptfoo** — Continuous evaluation in CI/CD
- **Obsidian** — Knowledge graph visualization (`docs/vault/`)
- **MCP** — 60+ Model Context Protocol servers

## Commands

| Command | Purpose |
|---------|---------|
| `/deploy` | Deploy to target environment via ArgoCD |
| `/rollback` | Emergency rollback |
| `/scaffold` | Generate code from templates |
| `/audit` | Run security and quality audit |
| `/status` | Check system and agent status |
| `/graphify` | Build or query codebase knowledge graph |
| `/onboard` | New developer walkthrough |
| `/wiki-ingest` | Fold raw sources into compiled wiki |
| `/wiki-query` | Research question against wiki |
| `/wiki-lint` | Health check on wiki |
| `/vault-link` | Regenerate wikilinks for a file |
| `/guardrails` | Run LLM output validation |
| `/six-docs` | Generate 6 planning documents (PRD, TRD, App Flow, UI/UX, Schema, Implementation Plan) |

## Task Management

Track all work using TaskCreate/TaskUpdate during sessions. For persistent tracking across sessions:

```
tasks/
├── lessons.md        — Root causes, corrective actions, prevention rules
├── decisions.md      — Architecture decisions with context and rationale
└── anti-patterns.md  — Failure patterns and what to do instead
```

## Known Gaps (Address These)

| Priority | Gap | Action |
|----------|-----|--------|
| CRITICAL | `backend/tests/` is empty | Write tests before new features |
| CRITICAL | 253 of 265 agents are registry-only stubs | Expand definitions or reduce registry |
| HIGH | Frontend has minimal application code | Scaffold pages, components, state |
| HIGH | Backbone has no tests | Add test coverage for 10-layer framework |
| MEDIUM | Terraform modules are placeholder stubs | Validate against a real provider |
| MEDIUM | No deployment evidence | Run smoke tests, log results |

## Free Toolchain

ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy, ZAP, Flagsmith, Grafana OnCall, Velero, MinIO, Ansible, n8n, Ollama, vLLM, LiteLLM, Playwright, Certbot.

Total monthly software cost: **$0**

## Agent skills

### Issue tracker

GitHub Issues on `Citadel-Cloud-Management/citadel-saas-factory` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
