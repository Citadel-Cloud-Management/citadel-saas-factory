# Citadel SaaS Factory

Universal full-stack SaaS production framework with autonomous AI agents, multi-model routing, and infrastructure-agnostic deployment.

**265 agents | 15 domains | 12 model providers | $0/month software cost**

---

## Quick Start

```bash
# Clone and bootstrap
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory
cp .env.example .env
./scripts/parallel-bootstrap.sh
./scripts/verify-install.sh
```

Or via npm:

```bash
npx @citadelcloud/saas-factory init my-saas
cd my-saas
cp .env.example .env
./scripts/parallel-bootstrap.sh
```

---

## Architecture

```
Clients (Browser / Mobile / API)
         │
    ┌────▼────┐
    │ Traefik │  TLS termination, routing, middleware
    └──┬──┬──┬┘
       │  │  │
  ┌────▼┐ ▼  ▼────────┐
  │Next.js│FastAPI│Keycloak│  Frontend, API, Auth
  └──────┘──┬───┘────────┘
            │
  ┌─────────┼─────────┐
  │         │         │
PostgreSQL Redis  RabbitMQ     Data, cache, messaging
  │
MinIO + Vault                  Storage, secrets
  │
K3s + ArgoCD + Linkerd         Orchestration, GitOps, mesh
  │
Prometheus + Grafana + Loki    Observability
```

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

---

## Project Structure

```
citadel-saas-factory/
├── backend/              FastAPI application (Python 3.12, SQLAlchemy, Alembic)
│   ├── app/              Application code, routers, models, services
│   └── tests/            Test suites
├── frontend/             Next.js 14 (TypeScript, Zustand, TanStack Query)
│   └── public/           Static assets
├── backbone/             10-layer autonomous agent framework
│   ├── agents/           Agent definitions and behaviors
│   ├── orchestrator/     Multi-agent coordination
│   ├── memory/           Agent memory and state
│   ├── governance/       Policy enforcement
│   ├── observability/    Agent monitoring
│   └── ...
├── infrastructure/       Deployment and networking
│   ├── terraform/        Infrastructure as code modules
│   ├── helm/             Kubernetes Helm charts
│   ├── ansible/          Configuration management playbooks
│   ├── mesh/             Service mesh configuration
│   └── agent-protocols/  Inter-agent communication
├── gitops/               ArgoCD GitOps manifests
│   ├── argocd/           ArgoCD application definitions
│   ├── base/             Base Kustomize resources
│   └── overlays/         Environment-specific overlays
├── security/             Security tooling and policies
│   ├── falco/            Runtime threat detection rules
│   ├── kyverno/          Kubernetes admission policies
│   ├── guardrails/       LLM output validation
│   ├── opa/              Open Policy Agent rules
│   ├── trivy/            Container vulnerability scanning
│   └── sigma/            Detection rules
├── compliance/           Regulatory frameworks
│   ├── frameworks/       SOC2, ISO27001, GDPR, HIPAA, PCI DSS
│   ├── policies/         Policy documents
│   ├── checklists/       Audit checklists
│   ├── evidence/         Compliance evidence
│   └── automation/       Automated compliance checks
├── monitoring/           Observability stack
│   ├── prometheus/       Metrics collection and alerting rules
│   ├── grafana/          Dashboard definitions
│   ├── loki/             Log aggregation configuration
│   └── alertmanager/     Alert routing and notification
├── models/               Multi-model AI catalog
│   ├── engines/          Engine switching (paid, free, local)
│   ├── catalog.yaml      Model definitions and capabilities
│   ├── routing.yaml      Tier-based model routing
│   └── embeddings.yaml   Embedding model configuration
├── mcp/                  Model Context Protocol server registry
│   └── registry.yaml     60+ MCP server configurations
├── evals/                Model evaluation framework
│   └── deepeval/         DeepEval + promptfoo test suites
├── docs/                 Documentation
│   ├── adr/              Architecture Decision Records
│   ├── agents/           Agent skill configuration
│   ├── runbooks/         Operational runbooks
│   ├── references/       Reference materials
│   └── vault/            Obsidian knowledge vault (wiki, raw sources)
├── scripts/              Automation scripts
│   ├── parallel-bootstrap.sh
│   ├── verify-install.sh
│   └── ...
├── tasks/                Persistent task tracking
│   ├── lessons.md        Root causes and corrective actions
│   ├── decisions.md      Architecture decisions with rationale
│   └── anti-patterns.md  Failure patterns and alternatives
├── starter-kit/          Minimal SaaS template for rapid scaffolding
├── bin/                  CLI entrypoint
│   └── cli.js            npx @citadelcloud/saas-factory
├── .claude/              Claude Code configuration
│   ├── agents/           Agent registry, subagents, tools catalog
│   ├── commands/         Slash commands
│   ├── hooks/            Pre/post tool execution hooks
│   ├── rules/            Coding standards and conventions
│   ├── skills/           Agent skills (TDD, diagnose, triage, etc.)
│   ├── templates/        Code generation templates
│   └── CLAUDE.md         Primary orchestration file
├── .github/              GitHub Actions CI/CD workflows
├── .cursor/              Cursor IDE rules
├── .codex/               OpenAI Codex configuration
├── .jules/               Google Jules configuration
├── .windsurf/            Windsurf rules
├── .continue/            Continue.dev configuration
├── .antigravity/         Antigravity configuration
├── .devin/               Devin configuration
├── .factory/             Factory AI configuration
├── .codegen/             Codegen configuration
├── .daytona/             Daytona workspace configuration
├── docker-compose.yml    Local development stack
├── Makefile              Build and automation targets
├── Justfile              just command runner recipes
├── AGENTS.md             Universal agent instructions (cross-IDE)
├── AGENT.md              Cursor agent configuration
├── GEMINI.md             Gemini/Jules agent configuration
└── .env.example          Environment variable template
```

---

## Multi-Model Routing

Agents reference model tiers, not specific models. Swap providers by changing one env var.

| Tier | Primary | Use Case |
|------|---------|----------|
| `reasoning_deep` | Claude Opus 4.6 | Architecture, critical decisions |
| `reasoning_fast` | Claude Sonnet 4.6 | Default coding tasks |
| `cheap_fast` | Claude Haiku 4.5 | Completion, boilerplate |
| `long_context` | Gemini 3.1 Pro | Full codebase analysis (2M tokens) |
| `code_specialist` | Codestral 25 | Code generation and review |
| `vision` | Claude Opus 4.6 | Screenshot/design to code |
| `local_only` | Llama 4 Maverick | Air-gapped, zero cost |
| `ultra_context` | Llama 4 Scout | Massive full-repo analysis (10M tokens) |
| `reasoning_chain` | o4 | Multi-step chain-of-thought |
| `multilingual` | Mistral Large 2 | Non-English, translation |
| `rag_specialist` | Command A | RAG with source grounding |
| `open_frontier` | GLM-5 | Best open-weights |

12 providers: Anthropic, OpenAI, Google, xAI, DeepSeek, Mistral, Cohere, Meta, Alibaba (Qwen), Zhipu (GLM), MiniMax, Ollama.

See `models/catalog.yaml`, `models/routing.yaml`, `models/embeddings.yaml`.

---

## Agent System

265 agents across 15 domains. Full registry: `.claude/agents/_registry.yaml`

| Domain | Count | Examples |
|--------|-------|---------|
| Executive & Strategy | 12 | CEO Strategist, CTO Technology, OKR Tracker |
| Marketing & Growth | 22 | SEO, Content, Social, Email, PPC, PR |
| Sales & Revenue | 18 | Lead Qualifier, Proposals, CRM, Forecast |
| Customer Success | 15 | Onboarding, Tickets, Churn Predictor, NPS |
| Product & UI/UX | 20 | UI Designer, Wireframes, Design System, A11y |
| Engineering | 25 | API, Models, Auth, Cache, Search, WebSocket |
| Frontend | 18 | Components, Pages, Forms, Charts, State, PWA |
| DevOps & Infrastructure | 28 | CI/CD, GitOps, K8s, Helm, Terraform, Canary |
| Security & Compliance | 22 | SAST, DAST, Secrets, Falco, Kyverno, Pentest |
| Data & Analytics | 18 | Schema, ETL, Dashboards, Forecasting, Vector |
| QA & Testing | 22 | Unit, E2E, Load, Chaos, Mutation, Visual |
| HR & People | 12 | Jobs, Interviews, Onboarding, Performance |
| Finance & Billing | 15 | Stripe, Subscriptions, Tax, Revenue, Runway |
| Legal & Governance | 8 | ToS, DPA, GDPR, SOC2, SLA |
| Content & Comms | 10 | Tech Writing, Docs, Changelogs, Case Studies |

---

## Cross-IDE Support

| Tool | Config File |
|------|-------------|
| Claude Code | `.claude/CLAUDE.md` |
| Cursor | `.cursor/rules/`, `AGENT.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| OpenAI Codex | `.codex/config.toml`, `AGENTS.md` |
| Google Jules | `.jules/config.yml`, `GEMINI.md` |
| Antigravity | `.antigravity/rules.md` |
| Windsurf | `.windsurf/rules/` |
| Continue.dev | `.continue/config.json` |
| Devin | `.devin/config.yml` |
| CodeRabbit | `.coderabbit.yml` |
| Factory AI | `.factory/droids.yml` |
| OpenHands | `.claude/config.toml` |

---

## Hallucination Prevention

Every LLM call routes through a triple-layer guardrails stack. No agent output reaches users without validation.

```
Agent Output
    │
    ▼
Layer 1: Guardrails AI       Schema enforcement, hub validators
Layer 2: NeMo Guardrails     Colang dialogue control, trustworthiness scoring
Layer 3: DeepEval            Continuous hallucination monitoring in CI/CD
    │
    ▼
Score >= 0.85 → Validated    Score < 0.85 → Retry (max 3) → Reject
```

---

## LLM Wiki (Karpathy Pattern)

Persistent knowledge layer using Andrej Karpathy's LLM Wiki pattern. Knowledge compounds across agents and sessions.

```
docs/vault/
├── raw/           Immutable source documents (LLM reads, never modifies)
├── wiki/          LLM-maintained compiled knowledge
│   ├── index.md   Content catalog (first lookup point)
│   ├── entities/  One page per agent, service, tool, component
│   ├── concepts/  Cross-cutting topics
│   └── ...
└── SCHEMA.md      Governance, co-evolved between human and LLM
```

---

## Docker Compose (Local Development)

```bash
docker compose up -d                        # Core stack
docker compose --profile monitoring up -d   # + Observability
docker compose --profile ai up -d           # + Ollama local AI
```

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL 16 | 5432 | Primary database with pgvector |
| Redis 7 | 6379 | Cache, sessions, rate limiting |
| Keycloak 24 | 8080 | Auth server (OAuth2, RBAC, MFA) |
| MinIO | 9000/9001 | Object storage / console |
| RabbitMQ | 5672/15672 | Message broker / management |
| Mailpit | 1025/8025 | Local email capture |
| Traefik | 80/443/8082 | Reverse proxy / dashboard |
| Prometheus | 9090 | Metrics (monitoring profile) |
| Grafana | 3001 | Dashboards (monitoring profile) |
| Ollama | 11434 | Local LLM inference (ai profile) |

---

## Token Setup

At minimum you need one model provider API key. Set it in `.env`.

**Required:**

| Token | Purpose |
|-------|---------|
| `ANTHROPIC_API_KEY` | Claude models, primary agent runtime |
| `GITHUB_TOKEN` | GitHub CLI, Actions, MCP server |

**Model providers (optional, set any for multi-model routing):**

`OPENAI_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`

**Services (optional):**

`STRIPE_SECRET_KEY`, `SENDGRID_API_KEY`, `SENTRY_DSN`, `SLACK_WEBHOOK_URL`

---

## Free Toolchain

Total monthly software cost: **$0**

ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Tempo, Falco, Kyverno, Semgrep, Trivy, ZAP, TruffleHog, Flagsmith, Grafana OnCall, Velero, MinIO, Ansible, n8n, Ollama, vLLM, LiteLLM, Playwright, Certbot, OpenSearch.

---

## Infrastructure Agnostic

Runs on any Linux server with SSH and Docker. No cloud vendor lock-in.

- Any VPS provider (Hetzner, DigitalOcean, Linode, Vultr)
- Bare metal servers
- On-premises infrastructure
- Edge deployments
- Home lab

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD mandatory)
4. Ensure 80%+ code coverage
5. Run security scan: `make security`
6. Run linter: `make lint`
7. Commit with conventional format: `feat: add user auth`
8. Open a pull request
9. CI must pass before merge
10. 1 approval minimum

---

## License

MIT License. See [LICENSE](LICENSE) for full terms.
