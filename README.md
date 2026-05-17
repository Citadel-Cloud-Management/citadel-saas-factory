<p align="center">
  <img src="https://img.shields.io/badge/Agents-265-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Domains-15-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Models-12_Providers-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Skills-24-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MCP_Servers-43-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cost-%240%2Fmo-brightgreen?style=for-the-badge" />
</p>

<h1 align="center">🏰 Citadel SaaS Factory</h1>

<p align="center">
  <strong>Universal full-stack SaaS production framework with 265 autonomous AI agents,<br/>multi-model routing, and infrastructure-agnostic deployment.</strong>
</p>

<p align="center">
  <a href="https://github.com/Citadel-Cloud-Management/citadel-saas-factory/actions"><img src="https://img.shields.io/badge/CI%2FCD-8_workflows-2088FF?logo=github-actions&logoColor=white" /></a>
  <a href="#cross-ide-support"><img src="https://img.shields.io/badge/IDE_Support-10+_platforms-764ABC?logo=visualstudiocode&logoColor=white" /></a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white" />
</p>

---

## ⚡ Quick Start

```bash
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory
cp .env.example .env          # Add your ANTHROPIC_API_KEY
bash scripts/setup.sh         # Verify agentic infrastructure
claude                        # Start Claude Code
```

Or via npm:

```bash
npx @citadelcloud/saas-factory init my-saas
```

---

## 🏗️ Architecture

```
Clients (Browser / Mobile / API)
         │
    ┌────▼────┐
    │ Traefik │  TLS, routing, middleware
    └──┬──┬──┬┘
       │  │  │
  ┌────▼┐ ▼  ▼────────┐
  │Next.js│FastAPI│Keycloak│  UI · API · Auth
  └──────┘──┬───┘────────┘
            │
  ┌─────────┼─────────┐
  │         │         │
PostgreSQL Redis  RabbitMQ       Data · Cache · Messaging
  │
MinIO + Vault                    Storage · Secrets
  │
K3s + ArgoCD + Linkerd           Orchestration · GitOps · Mesh
  │
Prometheus + Grafana + Loki      Observability
```

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| 🐍 Backend | **FastAPI** (Python 3.12) | REST/GraphQL API, business logic |
| ⚛️ Frontend | **Next.js 14** (TypeScript) | SSR/SSG UI, React components |
| 🗄️ Database | **PostgreSQL 16** | Primary store, RLS, pgvector |
| ⚡ Cache | **Redis 7** | Sessions, rate limiting, pub/sub |
| 🔐 Auth | **Keycloak 24** | OAuth2, RBAC, MFA, SSO |
| 📦 Storage | **MinIO** | S3-compatible object storage |
| 📨 Messaging | **RabbitMQ** | Async events, DLQ |
| ☸️ Orchestration | **K3s + ArgoCD** | Lightweight K8s, GitOps |
| 🌐 Proxy | **Traefik** | TLS termination, routing |
| 🔗 Mesh | **Linkerd** | mTLS, traffic policies |
| 🔑 Secrets | **HashiCorp Vault** | Rotation, encryption |
| 📊 Monitoring | **Prometheus + Grafana + Loki** | Metrics, dashboards, logs |

---

## 📂 Project Structure

```
citadel-saas-factory/
├── backend/              🐍 FastAPI (Python 3.12, SQLAlchemy, Alembic)
├── frontend/             ⚛️ Next.js 14 (TypeScript, Zustand, TanStack Query)
├── backbone/             🧠 10-layer autonomous agent framework
├── infrastructure/       🏗️ Terraform · Helm · Ansible · Mesh · Agent Protocols
├── gitops/               🔄 ArgoCD manifests, Kustomize overlays
├── security/             🛡️ Falco · Kyverno · OPA · Trivy · Guardrails · Sigma
├── compliance/           📋 SOC2 · ISO27001 · GDPR · HIPAA · PCI DSS
├── monitoring/           📊 Prometheus · Grafana · Loki · AlertManager
├── models/               🤖 Multi-model catalog, routing tiers, embeddings
├── mcp/                  🔌 43 MCP server configurations
├── evals/                🧪 DeepEval + promptfoo test suites
├── docs/                 📚 ADRs · Runbooks · References · Obsidian Vault
├── scripts/              ⚙️ Bootstrap · Deploy · Verify · Setup
├── starter-kit/          🚀 Minimal SaaS template for rapid scaffolding
├── tasks/                📝 Lessons · Decisions · Anti-patterns
├── .claude/              🤖 265 agents · 24 skills · 37 commands · 21 rules
├── .github/              🔧 8 CI/CD workflows (incl. claude-code-action)
└── [10 IDE configs]      🖥️ Cursor · Codex · Jules · Devin · Windsurf · ...
```

---

## 🤖 Agent System

**265 agents** across **15 domains**. Registry: `.claude/agents/_registry.yaml`

| Domain | Count | Examples |
|:-------|------:|:--------|
| 👔 Executive & Strategy | 12 | CEO Strategist, CTO Technology, OKR Tracker |
| 📈 Marketing & Growth | 22 | SEO, Content, Social, Email, PPC, PR |
| 💰 Sales & Revenue | 18 | Lead Qualifier, Proposals, CRM, Forecast |
| 🤝 Customer Success | 15 | Onboarding, Tickets, Churn Predictor, NPS |
| 🎨 Product & UI/UX | 20 | UI Designer, Wireframes, Design System, A11y |
| ⚙️ Engineering | 25 | API, Models, Auth, Cache, Search, WebSocket |
| 🖥️ Frontend | 18 | Components, Pages, Forms, Charts, State, PWA |
| 🚀 DevOps & Infrastructure | 28 | CI/CD, GitOps, K8s, Helm, Terraform, Canary |
| 🛡️ Security & Compliance | 22 | SAST, DAST, Secrets, Falco, Kyverno, Pentest |
| 📊 Data & Analytics | 18 | Schema, ETL, Dashboards, Forecasting, Vector |
| 🧪 QA & Testing | 22 | Unit, E2E, Load, Chaos, Mutation, Visual |
| 👥 HR & People | 12 | Jobs, Interviews, Onboarding, Performance |
| 💳 Finance & Billing | 15 | Stripe, Subscriptions, Tax, Revenue, Runway |
| ⚖️ Legal & Governance | 8 | ToS, DPA, GDPR, SOC2, SLA |
| ✍️ Content & Comms | 10 | Tech Writing, Docs, Changelogs, Case Studies |

---

## 🧠 Agentic Infrastructure

The harness is the product. **98.4% deterministic infrastructure, 1.6% AI decision logic.**

| Component | Count | Description |
|:----------|------:|:------------|
| 🤖 Agent Registry | 265 | Full YAML definitions across 15 domains |
| ⚡ Skills | 24 | TDD, deploy, diagnose, triage, code-review, security-audit, ... |
| 💬 Commands | 37 | `/deploy`, `/audit`, `/scaffold`, `/six-docs`, `/guardrails`, ... |
| 📏 Rules | 21 | Code quality, security, API design, testing, naming, ... |
| 🪝 Hooks | 11 | SessionStart context, PostToolUse auto-format, vault autolink |
| 📐 Templates | 20 | API endpoint, component, service, migration, test, Dockerfile, ... |
| 🧠 Memory | 8 | Project, architecture, agent-learnings, errors, workflow, tools, ... |
| 🔌 MCP Servers | 43 | GitHub, Postgres, Redis, Slack, Figma, Jira, Notion, K8s, ... |
| 📊 Model Tiers | 12 | reasoning_deep through open_frontier |

---

## 🔀 Multi-Model Routing

Agents reference **tiers**, not models. Swap providers by changing one env var.

| Tier | Primary | Use Case |
|:-----|:--------|:---------|
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

**12 providers:** Anthropic, OpenAI, Google, xAI, DeepSeek, Mistral, Cohere, Meta, Alibaba (Qwen), Zhipu (GLM), MiniMax, Ollama

---

## 🖥️ Cross-IDE Support

Works with **10+ AI coding platforms** out of the box.

| Tool | Config File |
|:-----|:------------|
| 🟣 Claude Code | `.claude/CLAUDE.md`, `.claude/settings.json` |
| 🔵 Cursor | `.cursor/rules/`, `AGENT.md` |
| 🟢 GitHub Copilot | `.github/copilot-instructions.md` |
| ⬜ OpenAI Codex | `.codex/config.toml`, `AGENTS.md` |
| 🔴 Google Jules | `.jules/config.yml`, `GEMINI.md` |
| 🟡 Antigravity | `.antigravity/rules.md` |
| 🔷 Windsurf | `.windsurf/rules/` |
| 🟠 Continue.dev | `.continue/config.json` |
| ⚫ Devin | `.devin/config.yml` |
| 🟤 Factory AI | `.factory/droids.yml` |

---

## 🛡️ Hallucination Prevention

Every LLM call routes through a **triple-layer guardrails stack**. No agent output reaches users without validation.

```
Agent Output
    │
    ▼
┌─────────────────────┐
│  Guardrails AI      │  Schema enforcement, hub validators
├─────────────────────┤
│  NeMo Guardrails    │  Colang dialogue control, trust scoring
├─────────────────────┤
│  DeepEval           │  Continuous hallucination monitoring (CI/CD)
└─────────┬───────────┘
          │
    Score ≥ 0.85 → ✅ Validated
    Score < 0.85 → 🔄 Retry (max 3) → ❌ Reject
```

---

## 📚 LLM Wiki (Karpathy Pattern)

Persistent knowledge layer. Knowledge compounds across agents and sessions.

```
docs/vault/
├── raw/           📄 Immutable source documents
├── wiki/          🧠 LLM-maintained compiled knowledge
│   ├── index.md   🔍 Content catalog (first lookup point)
│   ├── entities/  📌 Per-agent, service, tool, component
│   ├── concepts/  💡 Cross-cutting topics (10 documented)
│   └── patterns/  🔧 Reusable design patterns (7 documented)
├── architecture/  🏗️ ADRs and component pages
├── memory/        🧠 8-type memory system mirror
└── SCHEMA.md      📐 Governance, co-evolved human + LLM
```

---

## 🐳 Docker Compose

```bash
docker compose up -d                        # Core stack
docker compose --profile monitoring up -d   # + Observability
docker compose --profile ai up -d           # + Ollama local AI
```

| Service | Port | Description |
|:--------|:-----|:------------|
| 🗄️ PostgreSQL 16 | 5432 | Primary database with pgvector |
| ⚡ Redis 7 | 6379 | Cache, sessions, rate limiting |
| 🔐 Keycloak 24 | 8080 | Auth (OAuth2, RBAC, MFA) |
| 📦 MinIO | 9000/9001 | Object storage / console |
| 📨 RabbitMQ | 5672/15672 | Message broker / management |
| ✉️ Mailpit | 1025/8025 | Local email capture |
| 🌐 Traefik | 80/443/8082 | Reverse proxy / dashboard |
| 📊 Prometheus | 9090 | Metrics (monitoring profile) |
| 📈 Grafana | 3001 | Dashboards (monitoring profile) |
| 🤖 Ollama | 11434 | Local LLM inference (ai profile) |

---

## 🔑 Token Setup

```bash
cp .env.example .env
# Edit .env with your keys
```

**Required:**

| Token | Purpose |
|:------|:--------|
| `ANTHROPIC_API_KEY` | Claude models, primary agent runtime |
| `GITHUB_TOKEN` | GitHub CLI, Actions, MCP server |

**Optional model providers:** `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY`, `OPENROUTER_API_KEY`, `GROQ_API_KEY`

**Optional services:** `STRIPE_SECRET_KEY`, `SENDGRID_API_KEY`, `SENTRY_DSN`, `SLACK_WEBHOOK_URL`

---

## 💸 Free Toolchain

**Total monthly software cost: $0**

ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Tempo, Falco, Kyverno, Semgrep, Trivy, ZAP, TruffleHog, Flagsmith, Grafana OnCall, Velero, MinIO, Ansible, n8n, Ollama, vLLM, LiteLLM, Playwright, Certbot, OpenSearch.

---

## 🌍 Infrastructure Agnostic

Runs on **any Linux server** with SSH and Docker. No cloud vendor lock-in.

- Any VPS (Hetzner, DigitalOcean, Linode, Vultr)
- Bare metal servers
- On-premises infrastructure
- Edge deployments
- Home lab

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD mandatory, 80%+ coverage)
4. Run `make lint` and `make security`
5. Commit: `feat: add user auth`
6. Open a pull request — CI must pass, 1 approval minimum

---

## 📄 License

MIT License. See [LICENSE](LICENSE).
