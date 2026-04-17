<div align="center">

# 🏰 Citadel SaaS Factory

### Universal Full-Stack SaaS Production Framework

**265 Autonomous Business Agents | Multi-Model AI | Cross-IDE Support**

[![npm](https://img.shields.io/npm/v/@citadelcloud/saas-factory?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/@citadelcloud/saas-factory)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Agents](https://img.shields.io/badge/Agents-265-FF6B35?style=for-the-badge&logo=probot&logoColor=white)](.claude/agents/_registry.yaml)
[![Models](https://img.shields.io/badge/Models-9_Providers-8B5CF6?style=for-the-badge&logo=openai&logoColor=white)](models/catalog.yaml)
[![IDEs](https://img.shields.io/badge/IDEs-12_Supported-0078D4?style=for-the-badge&logo=visualstudiocode&logoColor=white)](#-cross-ide-support)
[![Cost](https://img.shields.io/badge/Cost-$0/month-00C853?style=for-the-badge&logo=cashapp&logoColor=white)](#-free-toolchain)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai/code)

<br/>

[🌐 Architecture Diagram](https://kogunlowo123.github.io/kehinde-architecture-diagram/) &nbsp;|&nbsp; [📦 npm Package](https://www.npmjs.com/package/@citadelcloud/saas-factory) &nbsp;|&nbsp; [**❤️ Sponsor**](https://cash.app/$KennyOgunlowo) &nbsp;|&nbsp; [🏢 citadelcloudmanagement.com](https://citadelcloudmanagement.com)

<br/>

**Clone. Configure. Deploy. Any infrastructure. Zero software cost.**

<br/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="K8s" />
<img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white" alt="ArgoCD" />
<img src="https://img.shields.io/badge/Keycloak-4D4D4D?style=flat-square&logo=keycloak&logoColor=white" alt="Keycloak" />
<img src="https://img.shields.io/badge/Vault-FFEC6E?style=flat-square&logo=vault&logoColor=black" alt="Vault" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus" />
<img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana" />
<img src="https://img.shields.io/badge/Traefik-24A1C1?style=flat-square&logo=traefikproxy&logoColor=white" alt="Traefik" />

</div>

---

## ⚡ Quick Start

```bash
# Option 1: npm (recommended)
npx @citadelcloud/saas-factory init my-saas
cd my-saas

# Option 2: git clone
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory

# Then:
cp .env.example .env                  # Set your API keys (at minimum one provider)
./scripts/parallel-bootstrap.sh       # Parallel install: models, MCP, hooks, agents
./scripts/verify-install.sh           # Green/red verification report
claude                                # Or open in Cursor, Antigravity, Copilot, Codex, Jules...
```

> [!TIP]
> You can also use `just bootstrap` if you have [just](https://github.com/casey/just) installed.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS                                  │
│              Browser / Mobile / API Consumers                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  🌐 REVERSE PROXY                               │
│                  Traefik (TLS, Routing)                          │
└──────────┬───────────────┬───────────────┬──────────────────────┘
           │               │               │
┌──────────▼───┐  ┌────────▼───┐  ┌────────▼──────────┐
│  🖥️ FRONTEND │  │ ⚙️ BACKEND │  │   🔐 AUTH GATEWAY  │
│  Next.js 14  │  │  FastAPI   │  │   Keycloak 24      │
│  TypeScript  │  │ Python 3.12│  │ OAuth2/RBAC/MFA    │
└──────────────┘  └─────┬──────┘  └────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼───┐  ┌────────▼───┐  ┌───────▼────────┐
│ 🗄️ DATABASE│  │ 💾 CACHE   │  │ 📨 MESSAGING   │
│ Postgres 16│  │  Redis 7   │  │   RabbitMQ     │
└───────────┘  └────────────┘  └────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│              📦 STORAGE  &  🔑 SECRETS                 │
│          MinIO (S3-compatible)  |  HashiCorp Vault      │
└───────────────────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                 ☸️ ORCHESTRATION                        │
│     K3s + ArgoCD (GitOps) | Linkerd (mTLS mesh)       │
└───────────────────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                 📊 OBSERVABILITY                       │
│       Prometheus | Grafana | Loki | Tempo | Falco     │
└───────────────────────────────────────────────────────┘
```

<details>
<summary><b>📋 Full Tech Stack Table</b></summary>

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

</details>

---

## 🤖 Multi-Model Support

> Agents reference model **tiers**, not specific models. Swap providers by changing one env var.

| Tier | Primary | Fallbacks | Use Case |
|------|---------|-----------|----------|
| 🧠 `reasoning_deep` | Claude Opus 4.6 | Gemini 3 Pro, DeepSeek R1, GPT-5 | Architecture, critical decisions |
| ⚡ `reasoning_fast` | Claude Sonnet 4.6 | Gemini 3 Pro, GPT-5, DeepSeek V3.1 | Default coding tasks |
| 💨 `cheap_fast` | Claude Haiku 4.5 | Gemini 3 Flash, GPT-5 Mini | Completion, boilerplate |
| 📚 `long_context` | Gemini 3.1 Pro | Gemini 3 Pro, Claude Opus, GPT-4.1 | Full codebase analysis (2M tokens) |
| 🔧 `code_specialist` | Codestral 25 | Qwen 2.5 Coder, DeepSeek V3.1 | Code generation and review |
| 👁️ `vision` | Claude Opus 4.6 | Gemini 3 Pro, GPT-5 | Screenshot/design to code |
| 🏠 `local_only` | Llama 3.3 70B | DeepSeek V3.1, Qwen 2.5 Coder | Air-gapped, zero cost |

<div align="center">

**9 providers** &nbsp;·&nbsp; **8 gateways** &nbsp;·&nbsp; **5 local runtimes**

<img src="https://img.shields.io/badge/Anthropic-D97757?style=flat-square&logo=anthropic&logoColor=white" />
<img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/Google-4285F4?style=flat-square&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/xAI-000000?style=flat-square&logo=x&logoColor=white" />
<img src="https://img.shields.io/badge/DeepSeek-4D6BFF?style=flat-square" />
<img src="https://img.shields.io/badge/Mistral-FF7000?style=flat-square" />
<img src="https://img.shields.io/badge/Cohere-39594D?style=flat-square" />
<img src="https://img.shields.io/badge/Meta-0467DF?style=flat-square&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/Ollama-000000?style=flat-square" />

</div>

See [`models/catalog.yaml`](models/catalog.yaml) · [`models/routing.yaml`](models/routing.yaml) · [`models/embeddings.yaml`](models/embeddings.yaml)

---

## 🔌 Cross-IDE Support

> This repo is recognized as a first-class project by every major AI coding tool.

| Tool | Config File | Status |
|------|-------------|--------|
| <img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=anthropic&logoColor=white" /> | `.claude/CLAUDE.md` | ✅ Native |
| <img src="https://img.shields.io/badge/Cursor-000000?style=flat-square&logo=cursor&logoColor=white" /> | `.cursor/rules/`, `AGENT.md` | ✅ Native |
| <img src="https://img.shields.io/badge/GitHub_Copilot-000000?style=flat-square&logo=githubcopilot&logoColor=white" /> | `.github/copilot-instructions.md` | ✅ Native |
| <img src="https://img.shields.io/badge/OpenAI_Codex-412991?style=flat-square&logo=openai&logoColor=white" /> | `.codex/config.toml`, `AGENTS.md` | ✅ Native |
| <img src="https://img.shields.io/badge/Google_Jules-4285F4?style=flat-square&logo=google&logoColor=white" /> | `.jules/config.yml`, `GEMINI.md` | ✅ Native |
| <img src="https://img.shields.io/badge/Antigravity-8B5CF6?style=flat-square" /> | `.antigravity/rules.md` | ✅ Native |
| <img src="https://img.shields.io/badge/Windsurf-06B6D4?style=flat-square" /> | `.windsurf/rules/` | ✅ Native |
| <img src="https://img.shields.io/badge/Continue.dev-000000?style=flat-square" /> | `.continue/config.json` | ✅ Native |
| <img src="https://img.shields.io/badge/Devin-FF6B35?style=flat-square" /> | `.devin/config.yml` | 🟢 Ready |
| <img src="https://img.shields.io/badge/CodeRabbit-FF6B35?style=flat-square" /> | `.coderabbit.yml` | 🟢 Ready |
| <img src="https://img.shields.io/badge/Factory_AI-000000?style=flat-square" /> | `.factory/droids.yml` | 🟢 Ready |
| <img src="https://img.shields.io/badge/OpenHands-000000?style=flat-square" /> | `openhands/config.toml` | 🟢 Ready |

---

## 🌍 Infrastructure Agnostic

> Runs on **any Linux server** with SSH and Docker. No cloud vendor lock-in.

- ☁️ Any VPS provider (Hetzner, DigitalOcean, Linode, Vultr)
- 🖥️ Bare metal servers
- 🏢 On-premises infrastructure
- 📡 Edge deployments
- 🏠 Home lab

---

## 🤖 All 265 Agents — 15 Domains

<div align="center">

| Domain | Agents | Highlights |
|--------|--------|------------|
| 👔 **Executive & Strategy** | 12 | CEO Strategist, CTO Technology, OKR Tracker |
| 📈 **Marketing & Growth** | 22 | SEO, Content, Social, Email, PPC, PR |
| 💰 **Sales & Revenue** | 18 | Lead Qualifier, Proposals, CRM, Forecast |
| 🎯 **Customer Success** | 15 | Onboarding, Tickets, Churn Predictor, NPS |
| 🎨 **Product & UI/UX** | 20 | UI Designer, Wireframes, Design System, A11y |
| ⚙️ **Engineering** | 25 | API, Models, Auth, Cache, Search, WebSocket |
| 🖥️ **Frontend** | 18 | Components, Pages, Forms, Charts, State, PWA |
| 🚀 **DevOps** | 28 | CI/CD, GitOps, K8s, Helm, Terraform, Canary |
| 🔒 **Security** | 22 | SAST, DAST, Secrets, Falco, Kyverno, Pentest |
| 📊 **Data & Analytics** | 18 | Schema, ETL, Dashboards, Forecasting, Vector |
| 🧪 **QA & Testing** | 22 | Unit, E2E, Load, Chaos, Mutation, Visual |
| 👥 **HR & People** | 12 | Jobs, Interviews, Onboarding, Performance |
| 💳 **Finance & Billing** | 15 | Stripe, Subscriptions, Tax, Revenue, Runway |
| ⚖️ **Legal & Governance** | 8 | ToS, DPA, GDPR, SOC2, SLA |
| ✍️ **Content & Comms** | 10 | Tech Writing, Docs, Changelogs, Case Studies |

</div>

<details>
<summary><b>📋 View all 265 agents with IDs and descriptions</b></summary>

### 👔 Domain 1: Executive & Strategy (12 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `exec-ceo-strategist` | CEO Strategist | Business strategy, OKR generation, competitive analysis, board decks |
| 2 | `exec-coo-operations` | COO Operations | Process optimization, cross-department coordination, resource allocation |
| 3 | `exec-cfo-finance` | CFO Finance | Financial modeling, revenue forecasting, burn rate, unit economics |
| 4 | `exec-cto-technology` | CTO Technology | Tech stack decisions, architecture reviews, build vs buy, tech debt |
| 5 | `exec-cmo-marketing` | CMO Marketing | Marketing strategy, brand positioning, channel mix, growth planning |
| 6 | `exec-cpo-product` | CPO Product | Product vision, roadmap, feature prioritization (RICE/ICE), market fit |
| 7 | `exec-vp-engineering` | VP Engineering | Engineering velocity, team structure, hiring plans, incident escalation |
| 8 | `exec-vp-sales` | VP Sales | Sales strategy, pipeline analysis, territory planning, quota setting |
| 9 | `exec-okr-tracker` | OKR Tracker | Company/team OKR tracking, progress reports, at-risk identification |
| 10 | `exec-board-reporter` | Board Reporter | Board reports, investor updates, KPI dashboards, milestone tracking |
| 11 | `exec-competitive-intel` | Competitive Intel | Competitor monitoring, market trends, competitive battle cards |
| 12 | `exec-decision-logger` | Decision Logger | Strategic decision recording with context, rationale, and outcomes |

### 📈 Domain 2: Marketing & Growth (22 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `mktg-seo-strategist` | SEO Strategist | Keyword research, on-page optimization, technical SEO, content gaps |
| 2 | `mktg-content-writer` | Content Writer | Blog posts, landing pages, emails, case studies, whitepapers |
| 3 | `mktg-social-media` | Social Media | Post scheduling, captions, hashtags, engagement analysis |
| 4 | `mktg-email-marketer` | Email Marketer | Campaigns, subject lines, segmentation, A/B testing, flows |
| 5 | `mktg-ppc-manager` | PPC Manager | Ad copy, bid strategy, audience targeting, ROAS optimization |
| 6 | `mktg-analytics` | Marketing Analytics | UTM tracking, attribution, funnel analysis, conversion optimization |
| 7 | `mktg-landing-page` | Landing Page | High-conversion page design and copy, CTA optimization |
| 8 | `mktg-brand-voice` | Brand Voice | Brand consistency, tone guidelines, style guide enforcement |
| 9 | `mktg-pr-outreach` | PR Outreach | Press releases, journalist pitching, media lists, coverage tracking |
| 10 | `mktg-influencer` | Influencer Agent | Influencer ID, outreach scripts, partnership terms, ROI tracking |
| 11 | `mktg-video-scripting` | Video Scriptwriter | YouTube scripts, social hooks, demo scripts, webinar outlines |
| 12 | `mktg-podcast` | Podcast Producer | Episode outlines, show notes, guest research, transcripts |
| 13 | `mktg-community` | Community Manager | Community engagement, UGC curation, feedback collection |
| 14 | `mktg-growth-hacker` | Growth Hacker | Viral loops, referral programs, PLG mechanics, activation experiments |
| 15 | `mktg-ab-tester` | A/B Test Designer | Hypothesis generation, stat significance, result analysis |
| 16 | `mktg-competitor` | Competitor Monitor | Competitor marketing moves, pricing changes, feature launches |
| 17 | `mktg-newsletter` | Newsletter Agent | Content curation, subject lines, send time optimization |
| 18 | `mktg-webinar` | Webinar Planner | Planning, registration copy, follow-up sequences, engagement |
| 19 | `mktg-affiliate` | Affiliate Manager | Program setup, commissions, partner recruitment, payouts |
| 20 | `mktg-product-launch` | Product Launch | Launch playbook, announcement copy, drip campaigns, press |
| 21 | `mktg-persona` | Persona Builder | ICP definition, buyer personas, jobs-to-be-done analysis |
| 22 | `mktg-retention` | Retention Agent | Churn signals, re-engagement campaigns, NPS follow-up |

### 💰 Domain 3: Sales & Revenue (18 Agents)

| # | Agent ID | Name | Description |
|---|----------|------|-------------|
| 1 | `sales-lead-qualifier` | Lead Qualifier | Lead scoring, data enrichment, ICP matching, routing |
| 2 | `sales-outbound-writer` | Outbound Writer | Cold emails, LinkedIn messages, follow-ups, objection handling |
| 3 | `sales-proposal-gen` | Proposal Generator | Custom proposals, SOWs, pricing tables, ROI calculations |
| 4 | `sales-crm-updater` | CRM Updater | Deal stage updates, activity logging, pipeline hygiene |
| 5 | `sales-demo-prepper` | Demo Prepper | Pre-demo research, custom scripts, competitive positioning |
| 6 | `sales-contract-drafter` | Contract Drafter | MSA and order forms, redline tracking, approval routing |
| 7 | `sales-forecast` | Forecast Analyst | Pipeline forecasting, deal velocity, revenue prediction |
| 8 | `sales-win-loss` | Win/Loss Analyst | Post-deal analysis, pattern identification, CI extraction |
| 9 | `sales-pricing` | Pricing Optimizer | Pricing models, discount impact, WTP estimation, tier optimization |
| 10 | `sales-territory` | Territory Planner | Territory mapping, account distribution, quota allocation |
| 11 | `sales-upsell` | Upsell Detector | Expansion opportunities, usage triggers, health signals |
| 12 | `sales-scheduler` | Meeting Scheduler | Calendar coordination, timezone handling, no-show follow-up |
| 13 | `sales-objection` | Objection Handler | Objection responses, battle cards, value proposition framing |
| 14 | `sales-referral` | Referral Agent | Referral program, ask timing, reward fulfillment, tracking |
| 15 | `sales-partner` | Partner Manager | Deal registration, co-selling, partner enablement content |
| 16 | `sales-call-analyzer` | Call Analyzer | Transcript analysis, talk ratio, next-step extraction |
| 17 | `sales-pipeline-cleaner` | Pipeline Cleaner | Stale deal ID, missing data alerts, stage-appropriate actions |
| 18 | `sales-commission` | Commission Calculator | Commission calculation, plan modeling, quota attainment |

### 🎯 Domain 4–15: See [`.claude/agents/_registry.yaml`](.claude/agents/_registry.yaml) for the complete registry

</details>

---

## 🔗 Ruflo — Multi-Agent Swarm Orchestration

> [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)

```bash
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash
ruflo init
```

- 🕸️ **Mesh topology** — Agents communicate peer-to-peer, no central bottleneck
- 🧰 **314 MCP tools** — Pre-built tool integrations for Claude Code
- 🧠 **Hive-mind intelligence** — Shared context and memory across all agents
- 🎯 **Self-learning neural routing** — Automatic task-to-agent matching
- ⚡ **CYCLE_INTERVAL=0** — Zero-latency agent activation

---

## 🕸️ Graphify — Codebase Knowledge Graph

> [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)

```bash
pip install graphifyy && graphify install && graphify index .
```

- 🌳 **Tree-sitter AST parsing** — 20 language support
- 🔍 **Semantic search** — Find code by meaning, not just text
- 📊 **Architecture visualization** — Generate dependency diagrams
- 🔗 **Symbol resolution** — Cross-file dependency tracking

---

## 📖 LLM Wiki — Brain Memory (Karpathy Pattern)

> Citadel's agent fleet uses Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as persistent brain memory.

```
docs/vault/
├── 📂 raw/        → Layer 1: immutable source documents (LLM reads, never modifies)
├── 📂 wiki/       → Layer 2: LLM-maintained compiled knowledge
│   ├── index.md         — content-oriented catalog (first lookup)
│   ├── entities/        — one page per agent, service, tool, component
│   ├── concepts/        — cross-cutting topics
│   ├── contradictions/  — flagged conflicts between sources
│   └── knowledge-graph/ — Graphify AST output
└── 📄 SCHEMA.md   → Layer 3: governance, co-evolved between human and LLM
```

| Operation | Command | What it does |
|-----------|---------|--------------|
| 📥 **Ingest** | `make wiki-ingest FILE=raw/<path>` | Read raw source, update 10-15 wiki pages |
| 🔍 **Query** | `/project:wiki-query <question>` | Consult wiki first, file answers back |
| 🧹 **Lint** | `make wiki-lint` | Health-check for orphans and gaps |

---

## 🛡️ Hallucination Prevention

> Every LLM call routes through a **Guardrails AI** validation layer. No agent output reaches users without passing guardrails.

```
Agent Output → Guardrails Validator → Schema Check → Hallucination Score (≥0.85)
    → Factuality Check → Provenance Verification → ✅ Validated Output
                                                  → ❌ Retry (max 3) → Reject
```

| Problem | Solution |
|---------|----------|
| 🤥 Model makes things up | Validates against rules and source data |
| 📭 No grounding | RAG provenance validators |
| 🔀 Inconsistent answers | Schema enforcement with deterministic outputs |
| ⚠️ Unsafe agent behavior | Pre/post execution guardrails |

---

## 💰 Free Toolchain

> Total monthly software cost: **$0**

<details>
<summary><b>💎 View the full free toolchain (21 tools, replaces $1000+/mo in SaaS)</b></summary>

| Name | License | Replaces |
|------|---------|----------|
| ArgoCD | Apache-2.0 | Spinnaker, Harness ($$$) |
| K3s | Apache-2.0 | EKS, GKE, AKS ($75-300/mo) |
| Traefik | MIT | AWS ALB, Cloudflare ($20+/mo) |
| Linkerd | Apache-2.0 | Istio, AWS App Mesh |
| Keycloak | Apache-2.0 | Auth0 ($23-240/mo), Okta ($2/user) |
| HashiCorp Vault | BUSL-1.1 | AWS Secrets Manager ($0.40/secret) |
| Prometheus | Apache-2.0 | Datadog ($15/host/mo) |
| Grafana | AGPL-3.0 | Datadog dashboards ($15/host/mo) |
| Loki | AGPL-3.0 | Splunk ($150+/GB), Datadog Logs |
| Tempo | AGPL-3.0 | Jaeger SaaS, Datadog APM |
| Falco | Apache-2.0 | Sysdig ($$$), Aqua Security |
| Kyverno | Apache-2.0 | OPA Gatekeeper, Styra DAS |
| Semgrep | LGPL-2.1 | SonarQube ($150+/mo), Snyk Code |
| Trivy | Apache-2.0 | Snyk Container ($25+/mo) |
| OWASP ZAP | Apache-2.0 | Burp Suite Pro ($449/yr) |
| Flagsmith | BSD-3 | LaunchDarkly ($10/seat/mo) |
| Grafana OnCall | AGPL-3.0 | PagerDuty ($21/user/mo) |
| Velero | Apache-2.0 | Kasten K10, Portworx Backup |
| MinIO | AGPL-3.0 | AWS S3 ($0.023/GB/mo) |
| Ansible | GPL-3.0 | Puppet, Chef, SaltStack |
| TruffleHog | AGPL-3.0 | GitGuardian ($30/dev/mo) |

</details>

---

## 🐳 Docker Compose — Local Development

```bash
docker compose up -d
```

| Service | Port | Description |
|---------|------|-------------|
| 🐘 PostgreSQL 16 | 5432 | Primary database |
| 🔴 Redis 7 | 6379 | Cache and session store |
| 🔐 Keycloak 24 | 8080 | Auth server (admin console) |
| 📦 MinIO | 9000 / 9001 | Object storage / console |
| 🐰 RabbitMQ | 5672 / 15672 | Message broker / management |
| 📧 Mailpit | 1025 / 8025 | Local email capture / web UI |
| 🌐 Traefik | 80 / 443 / 8082 | Proxy / TLS / dashboard |

---

## 🔑 Token Setup

> [!NOTE]
> At minimum you need **one** model provider API key. Set it in `.env`.

### Required

| Token | Source | Purpose |
|-------|--------|---------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Powers Claude Code, Ruflo, and Graphify |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) | GitHub CLI, GHCR, Actions, MCP server |

### Optional

| Token | Source | Purpose |
|-------|--------|---------|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | GPT-5 fallback models |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | Gemini long-context models |
| `STRIPE_SECRET_KEY` | [dashboard.stripe.com](https://dashboard.stripe.com) | Payment processing (billing agents) |
| `SENDGRID_API_KEY` | [sendgrid.com](https://sendgrid.com) | Transactional email delivery |

```bash
cp .env.example .env
# Edit .env with your tokens
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD mandatory)
4. Ensure 80%+ code coverage
5. Run security scan: `make security`
6. Run linter: `make lint`
7. Commit with conventional format: `feat: add user auth`
8. Open a pull request
9. Wait for CI to pass (lint, test, security scan)
10. Get 1 approval minimum before merge

---

## 📦 Install via npm

```bash
npx @citadelcloud/saas-factory init my-saas
cd my-saas
./scripts/parallel-bootstrap.sh
```

Or install globally:

```bash
npm install -g @citadelcloud/saas-factory
citadel-factory init my-saas
```

---

<div align="center">

## 👤 Author

**Kehinde Ogunlowo**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kehinde-ogunlowo/)
[![Architecture](https://img.shields.io/badge/Architecture_Diagram-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://kogunlowo123.github.io/kehinde-architecture-diagram/)
[![Sponsor](https://img.shields.io/badge/❤️_Sponsor_via_Cash_App-00C853?style=for-the-badge&logo=cashapp&logoColor=white)](https://cash.app/$KennyOgunlowo)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for full terms.

Copyright (c) Citadel Cloud Management

---

**Citadel Cloud Management** | [citadelcloudmanagement.com](https://citadelcloudmanagement.com)

</div>
