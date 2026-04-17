<div align="center">

# 🏰 Citadel SaaS Factory

### Universal Full-Stack SaaS Production Framework

**385+ Autonomous Business Agents | 12 Model Providers | 22 Domains | Cross-IDE**

[![npm](https://img.shields.io/npm/v/@citadelcloud/saas-factory?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/@citadelcloud/saas-factory)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Agents](https://img.shields.io/badge/Agents-385+-FF6B35?style=for-the-badge&logo=probot&logoColor=white)](.claude/agents/_registry.yaml)
[![Models](https://img.shields.io/badge/Models-12_Providers-8B5CF6?style=for-the-badge&logo=openai&logoColor=white)](models/catalog.yaml)
[![Domains](https://img.shields.io/badge/Domains-22-E91E63?style=for-the-badge&logo=target&logoColor=white)](#-all-385-agents--22-domains)
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
| 🧠 `reasoning_deep` | Claude Opus 4.6 | Gemini 3 Pro, DeepSeek R1, GPT-5.4 | Architecture, critical decisions |
| ⚡ `reasoning_fast` | Claude Sonnet 4.6 | Gemini 3 Pro, GPT-5, DeepSeek V3.1 | Default coding tasks |
| 💨 `cheap_fast` | Claude Haiku 4.5 | Gemini 3 Flash, GPT-5 Mini | Completion, boilerplate |
| 📚 `long_context` | Gemini 3.1 Pro | Gemini 3 Pro, Claude Opus, GPT-4.1 | Full codebase analysis (2M tokens) |
| 🔧 `code_specialist` | Codestral 25 | Qwen 2.5 Coder, DeepSeek V3.1 | Code generation and review |
| 👁️ `vision` | Claude Opus 4.6 | Gemini 3 Pro, GPT-5, Llama 4 Maverick | Screenshot/design to code |
| 🏠 `local_only` | Llama 4 Maverick | Llama 4 Scout, DeepSeek V3.1, Qwen 3 | Air-gapped, zero cost |
| 🔭 `ultra_context` | Llama 4 Scout | Gemini 3.1 Pro, GPT-4.1, Grok 4 | Massive full-repo analysis (10M tokens) |
| 🔗 `reasoning_chain` | o4 | DeepSeek R1-0528, DeepSeek R1, Opus | Multi-step chain-of-thought |
| 🌍 `multilingual` | Mistral Large 2 | Qwen 3.5, Gemini 3 Pro, Sonnet | Non-English, translation |
| 📖 `rag_specialist` | Command A | Command R+, Sonnet, Gemini 3 Pro | RAG with source grounding |
| 🏆 `open_frontier` | GLM-5 | MiniMax M2.5, Qwen 3.5, Llama 4 Maverick | Best open-weights, matches closed models |

<div align="center">

**12 providers** &nbsp;·&nbsp; **8 gateways** &nbsp;·&nbsp; **5 local runtimes** &nbsp;·&nbsp; **40+ models**

<img src="https://img.shields.io/badge/Anthropic-D97757?style=flat-square&logo=anthropic&logoColor=white" />
<img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/Google-4285F4?style=flat-square&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/xAI-000000?style=flat-square&logo=x&logoColor=white" />
<img src="https://img.shields.io/badge/DeepSeek-4D6BFF?style=flat-square" />
<img src="https://img.shields.io/badge/Mistral-FF7000?style=flat-square" />
<img src="https://img.shields.io/badge/Cohere-39594D?style=flat-square" />
<img src="https://img.shields.io/badge/Meta_Llama_4-0467DF?style=flat-square&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/Qwen_3.5-FF6A00?style=flat-square" />
<img src="https://img.shields.io/badge/GLM--5-00B4D8?style=flat-square" />
<img src="https://img.shields.io/badge/MiniMax-8B5CF6?style=flat-square" />
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

## 🤖 All 385+ Agents — 22 Domains

<div align="center">

| Domain | Agents | Highlights |
|--------|--------|------------|
| 👔 **Executive & Strategy** | 15 | CEO Strategist, CTO Technology, OKR Tracker, Board Reporter, M&A Analyst |
| 📈 **Marketing & Growth** | 26 | SEO, Content, Social, Email, PPC, PR, PLG, ABM, Podcast, Influencer |
| 💰 **Sales & Revenue** | 22 | Lead Qualifier, Proposals, CRM, Forecast, Revenue Ops, Deal Desk |
| 🎯 **Customer Success** | 18 | Onboarding, Tickets, Churn Predictor, NPS, QBR, Health Score |
| 🎨 **Product & UI/UX** | 24 | UI Designer, Wireframes, Design System, A11y, Micro-interactions, User Research |
| ⚙️ **Engineering** | 30 | API, Models, Auth, Cache, Search, WebSocket, GraphQL, gRPC, Event Sourcing |
| 🖥️ **Frontend** | 22 | Components, Pages, Forms, Charts, State, PWA, i18n, Micro-frontends |
| 🚀 **DevOps** | 32 | CI/CD, GitOps, K8s, Helm, Terraform, Canary, FinOps, Platform Eng |
| 🔒 **Security** | 26 | SAST, DAST, Secrets, Falco, Kyverno, Pentest, Zero Trust, SBOM |
| 📊 **Data & Analytics** | 22 | Schema, ETL, Dashboards, Forecasting, Vector, Lakehouse, dbt |
| 🧪 **QA & Testing** | 26 | Unit, E2E, Load, Chaos, Mutation, Visual, Contract, Property-based |
| 👥 **HR & People** | 15 | Jobs, Interviews, Onboarding, Performance, DEI, L&D, Culture |
| 💳 **Finance & Billing** | 18 | Stripe, Subscriptions, Tax, Revenue, Runway, FP&A, Treasury |
| ⚖️ **Legal & Governance** | 12 | ToS, DPA, GDPR, SOC2, SLA, AI Ethics, IP, Export Control |
| ✍️ **Content & Comms** | 14 | Tech Writing, Docs, Changelogs, Case Studies, Video Scripts, Podcasts |
| 📦 **Supply Chain & Procurement** | 12 | Vendor Scoring, RFP Generator, Inventory Optimizer, Demand Forecast, Logistics |
| 🏗️ **Platform Engineering** | 10 | IDP Builder, Service Catalog, Golden Paths, Developer Portal, Backstage |
| 🌐 **Internationalization** | 8 | i18n Manager, Locale Sync, RTL Adapter, Currency Converter, Translation QA |
| 🤖 **AI/ML Operations** | 14 | Model Registry, Feature Store, Experiment Tracker, Prompt Optimizer, Eval Runner |
| 📡 **IoT & Edge** | 8 | Device Manager, Telemetry Collector, Edge Deployer, OTA Updater, Fleet Monitor |
| 🎓 **Education & Training** | 6 | Course Builder, Quiz Generator, Skill Assessor, Learning Path, Cert Tracker |
| 🏥 **Compliance & Risk** | 10 | Risk Scorer, Audit Trail, Policy Enforcer, Incident Reporter, Vendor Risk |

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

> [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo) &nbsp;·&nbsp; [npm: claude-flow](https://www.npmjs.com/package/claude-flow) &nbsp;·&nbsp; [MCP Market](https://mcpmarket.com/server/ruflo)

```bash
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash
ruflo init
```

> [!TIP]
> Most adopted open-source multi-agent platform of 2026 — **84.8% SWE-bench solve rate**, **75% API cost savings** vs direct Claude Code.

| Feature | Description |
|---------|-------------|
| 🕸️ **Mesh topology** | Peer-to-peer agent communication, no central bottleneck |
| 🧰 **87 native MCP tools** | Orchestration, swarm coordination, neural processing, system management |
| 🧠 **SONA neural routing** | Sub-millisecond HNSW vector memory with 9 reinforcement learning algorithms |
| 🎯 **16 specialist agent roles** | Pre-built + custom types in coordinated swarms |
| 🔄 **Self-learning swarms** | Fault-tolerant consensus with enterprise-grade security |
| ⚡ **CYCLE_INTERVAL=0** | Zero-latency agent activation |
| 📊 **RAG integration** | Built-in retrieval-augmented generation pipelines |
| 🔌 **Claude Code + Codex native** | MCP namespace `mcp__claude-flow__` for direct tool access |
| 🛡️ **Enterprise security** | Distributed swarm intelligence with access controls |
| 💾 **Memory persistence** | Agent learnings persist across sessions via hive-mind |

---

## 🕸️ Graphify — Codebase Knowledge Graph

> [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify) &nbsp;·&nbsp; [PyPI: graphifyy](https://pypi.org/project/graphifyy/) &nbsp;·&nbsp; [graphify.net](https://graphify.net/)

```bash
pip install graphifyy && graphify install && graphify index .
```

> [!TIP]
> **71.5x fewer tokens** per query vs reading raw files. Code processed locally via Tree-sitter — no file contents leave your machine.

| Feature | Description |
|---------|-------------|
| 🌳 **Tree-sitter AST parsing** | 25 languages: Python, JS, TS, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Obj-C, Julia, Verilog, SystemVerilog, Vue, Svelte, Dart |
| 🔍 **Semantic search** | Find code by meaning, not just text — concept-based queries |
| 📊 **Architecture visualization** | Auto-generate dependency diagrams and community clusters |
| 🔗 **Symbol resolution** | Cross-file dependency tracking with call graphs |
| 📝 **Wiki export** (`--wiki`) | Wikipedia-style markdown articles per community with `index.md` entry point |
| 👁️ **Vision support** | LLMs extract concepts from prose; vision models read diagrams |
| 🔄 **Auto-sync** (`--watch`) | Graph updates live as your codebase changes — instant AST rebuilds |
| 🔒 **Privacy-first** | Code files parsed locally via Tree-sitter — zero data exfiltration |
| 🌐 **Cross-IDE** | Works with Claude Code, Codex, Cursor, Gemini CLI, Copilot CLI, Antigravity, OpenClaw, Factory Droid, Trae |
| 📈 **Leiden clustering** | NetworkX + Leiden community detection for god-node and surprising-connection discovery |

---

## 📖 LLM Wiki — Brain Memory (Karpathy Pattern)

> Citadel's agent fleet uses Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as persistent brain memory. Knowledge **compounds** across all 385+ agents — every ingest adds, every query answer is filed back.

> [!NOTE]
> **Why not RAG?** Karpathy's insight: treat knowledge like code compilation. The LLM reads sources, extracts key info, and integrates it into the wiki — updating entities, revising summaries, noting contradictions. Unlike RAG, knowledge compounds instead of being re-retrieved from scratch every session.

```
docs/vault/
├── 📂 raw/        → Layer 1: immutable source documents (LLM reads, never modifies)
│                     Articles, papers, transcripts, architecture docs, meeting notes,
│                     customer feedback, incidents, Obsidian Web Clipper output
├── 📂 wiki/       → Layer 2: LLM-maintained compiled knowledge
│   ├── index.md         — content-oriented catalog (first lookup)
│   ├── log.md           — append-only chronological activity log
│   ├── overview.md      — evolving synthesis of everything known
│   ├── entities/        — one page per agent, service, tool, component
│   ├── concepts/        — cross-cutting topics (multi-tenancy, canary-deploys, ...)
│   ├── sources/         — one summary per ingested raw source
│   ├── comparisons/     — analysis pages generated from queries
│   ├── contradictions/  — flagged conflicts between sources
│   └── knowledge-graph/ — Graphify AST output, feeds entity/concept pages
└── 📄 SCHEMA.md   → Layer 3: governance, co-evolved between human and LLM
```

| Operation | Command | What it does |
|-----------|---------|--------------|
| 📥 **Ingest** | `make wiki-ingest FILE=raw/<path>` | Read raw source, update 10-15 wiki pages, flag contradictions |
| 🔍 **Query** | `/project:wiki-query <question>` | Consult wiki first, file valuable answers back as new pages |
| 🧹 **Lint** | `make wiki-lint` | Health-check for orphans, stale claims, missing cross-refs |
| 🔄 **Sync** | `make wiki-sync` | Refresh Graphify output + run lint pass |

**Key principle:** LLMs don't get bored. They don't forget to update cross-references. They can touch 15 files in one pass. The tedious bookkeeping that makes humans abandon wikis is exactly what LLMs excel at.

---

## 🛡️ Hallucination Prevention

> Every LLM call routes through a **triple-layer guardrails stack**. No agent output reaches users without passing validation. Cuts hallucination risk **71-89%** when all layers are active.

```
Agent Output
    ↓
┌─────────────────────────────────────────┐
│  Layer 1: Guardrails AI                 │
│  Schema enforcement + hub validators    │
│  (hallucination_free, provenance_llm,   │
│   toxic_language, detect_pii)           │
├─────────────────────────────────────────┤
│  Layer 2: NVIDIA NeMo Guardrails        │
│  Colang dialogue control + Cleanlab TLM │
│  Trustworthiness scoring via            │
│  uncertainty estimation                 │
├─────────────────────────────────────────┤
│  Layer 3: DeepEval Continuous Eval      │
│  Hallucination rate monitoring in CI/CD │
│  Faithfulness + relevance + toxicity    │
└─────────────┬───────────────────────────┘
              ↓
    Score ≥ 0.85 → ✅ Validated Output
    Score < 0.85 → 🔄 Retry with grounding (max 3) → ❌ Reject
```

| Problem | Solution | Tool |
|---------|----------|------|
| 🤥 Model makes things up | Validates against rules and source data | Guardrails AI |
| 📭 No grounding | RAG provenance validators | Guardrails Hub |
| 🔀 Inconsistent answers | Schema enforcement with deterministic outputs | Guardrails AI |
| ⚠️ Unsafe agent behavior | Colang dialogue management, behavioral constraints | NeMo Guardrails |
| 🔐 PII leakage | Automatic PII detection and masking | detect_pii validator |
| 📊 Drift detection | Continuous hallucination rate monitoring in CI | DeepEval |
| 💰 Cost optimization | Validator caching — same input skips re-scan | All layers |
| ⏱️ Low latency | GPU-accelerated (50-200ms), Haiku 4.5 for validators | NeMo + Guardrails |

---

## 🔌 MCP — Model Context Protocol

> **5,000+ MCP servers** available. Any MCP server works in Claude Code, Cursor, Windsurf, and every tool supporting the protocol. Configure once, portable everywhere.

| Category | Servers | Purpose |
|----------|---------|---------|
| 🔧 **Core** | filesystem, fetch, memory, sequential-thinking | Foundation tools |
| 🔀 **Version Control** | github, gitlab, bitbucket | Repos, PRs, issues |
| 🔍 **Search** | brave-search, exa, tavily, perplexity | Web research |
| 🌐 **Browser** | playwright, browserbase, chrome-devtools | Browser automation |
| 💬 **Comms** | slack, discord, gmail, teams | Messaging |
| 📋 **Project** | linear, jira, notion, asana | Task management |
| 📊 **Observability** | datadog, sentry, grafana, prometheus | Monitoring |
| 🗄️ **Database** | postgres, redis, supabase, mongodb, snowflake | Data access |
| 🧠 **Vector** | qdrant, chroma, pinecone, weaviate | Embeddings |
| ☁️ **Cloud** | aws, cloudflare, docker, kubernetes | Infrastructure |
| 💳 **Payments** | stripe, paddle | Billing |
| 🤖 **AI** | anthropic, openai, huggingface, replicate, ollama | Model access |
| 🎨 **Design** | figma, mermaid | Design tools |
| 📚 **Knowledge** | obsidian, context7 | Documentation |

See [`mcp/registry.yaml`](mcp/registry.yaml) for the full catalog with env vars and install commands.

---

## 💰 Free Toolchain

> Total monthly software cost: **$0** — replaces **$5,000+/mo** in paid SaaS

<details>
<summary><b>💎 View the full free toolchain (30 tools)</b></summary>

| Name | License | Replaces | Savings |
|------|---------|----------|---------|
| **Orchestration** | | | |
| ArgoCD | Apache-2.0 | Spinnaker, Harness | $500+/mo |
| K3s | Apache-2.0 | EKS, GKE, AKS | $75-300/mo |
| Flux CD | Apache-2.0 | GitLab Premium CI/CD | $400/mo |
| **Networking** | | | |
| Traefik | MIT | AWS ALB, Cloudflare | $20+/mo |
| Linkerd | Apache-2.0 | Istio, AWS App Mesh | $200+/mo |
| **Identity** | | | |
| Keycloak | Apache-2.0 | Auth0 ($23-240/mo), Okta ($2/user) | $240+/mo |
| Authentik | BUSL | Auth0, Clerk alternatives | $100+/mo |
| **Secrets** | | | |
| HashiCorp Vault | BUSL-1.1 | AWS Secrets Manager ($0.40/secret) | $50+/mo |
| **Observability** | | | |
| Prometheus | Apache-2.0 | Datadog metrics ($15/host/mo) | $300+/mo |
| Grafana | AGPL-3.0 | Datadog dashboards ($15/host/mo) | $300+/mo |
| Loki | AGPL-3.0 | Splunk ($150+/GB), Datadog Logs | $500+/mo |
| Tempo | AGPL-3.0 | Jaeger SaaS, Datadog APM | $200+/mo |
| Grafana OnCall | AGPL-3.0 | PagerDuty ($21/user/mo) | $100+/mo |
| OpenSearch | Apache-2.0 | Elasticsearch/Elastic Cloud | $200+/mo |
| **Security** | | | |
| Falco | Apache-2.0 | Sysdig, Aqua Security | $500+/mo |
| Kyverno | Apache-2.0 | OPA Gatekeeper, Styra DAS | $200+/mo |
| Semgrep | LGPL-2.1 | SonarQube ($150+/mo), Snyk Code | $150+/mo |
| Trivy | Apache-2.0 | Snyk Container ($25+/mo) | $100+/mo |
| OWASP ZAP | Apache-2.0 | Burp Suite Pro ($449/yr) | $37/mo |
| TruffleHog | AGPL-3.0 | GitGuardian ($30/dev/mo) | $150+/mo |
| **Feature Management** | | | |
| Flagsmith | BSD-3 | LaunchDarkly ($10/seat/mo) | $100+/mo |
| **Backup** | | | |
| Velero | Apache-2.0 | Kasten K10, Portworx Backup | $200+/mo |
| **Storage** | | | |
| MinIO | AGPL-3.0 | AWS S3 ($0.023/GB/mo) | $50+/mo |
| **Automation** | | | |
| Ansible | GPL-3.0 | Puppet, Chef, SaltStack | $100+/mo |
| n8n | Sustainable-Use | Zapier ($20+/mo), Make | $50+/mo |
| **AI Infrastructure** | | | |
| Ollama | MIT | OpenAI API (pay-per-token) | $200+/mo |
| vLLM | Apache-2.0 | Hosted inference APIs | $500+/mo |
| LiteLLM | MIT | Multi-provider management | $50+/mo |
| **Testing** | | | |
| Playwright | Apache-2.0 | Cypress Cloud ($75+/mo) | $75+/mo |
| Certbot | Apache-2.0 | Commercial TLS certs ($100+/yr) | $8/mo |

</details>

---

## 🐳 Docker Compose — Local Development

```bash
docker compose up -d                        # Core stack
docker compose --profile monitoring up -d   # + Observability
docker compose --profile ai up -d           # + Ollama local AI
```

> [!TIP]
> Run apps on your host for hot-reload; use Docker only for infrastructure (databases, caches, identity) that stays stable.

| Service | Port | Description |
|---------|------|-------------|
| 🐘 PostgreSQL 16 | 5432 | Primary database with pgvector |
| 🔴 Redis 7 | 6379 | Cache, sessions, rate limiting, pub/sub |
| 🔐 Keycloak 24 | 8080 | Auth server — OAuth2, RBAC, MFA, SSO |
| 📦 MinIO | 9000 / 9001 | S3-compatible object storage / console |
| 🐰 RabbitMQ | 5672 / 15672 | Message broker / management UI |
| 📧 Mailpit | 1025 / 8025 | Local email capture / web UI |
| 🌐 Traefik | 80 / 443 / 8082 | Reverse proxy / TLS / dashboard |
| 📊 Prometheus | 9090 | Metrics collection (monitoring profile) |
| 📈 Grafana | 3001 | Dashboards and alerting (monitoring profile) |
| 🤖 Ollama | 11434 | Local LLM inference (ai profile) |

---

## 🔑 Token Setup

> [!NOTE]
> At minimum you need **one** model provider API key. Set it in `.env`. Everything else is optional — activate providers as needed.

### Required

| Token | Source | Purpose |
|-------|--------|---------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Powers Claude Code, Ruflo, and Graphify |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) | GitHub CLI, GHCR, Actions, MCP server |

### Model Providers (set any for multi-model routing)

| Token | Source | Purpose |
|-------|--------|---------|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | GPT-5.4, o4 reasoning, GPT-4.1 long-context |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | Gemini 3.1 Pro (2M context), Gemini 3 Flash |
| `XAI_API_KEY` | [console.x.ai](https://console.x.ai) | Grok 4 (2M context, real-time X data) |
| `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) | DeepSeek R1 reasoning (90% cheaper than GPT) |
| `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai) | Codestral 25 (code), Mistral Large 2 (EU-hosted) |
| `COHERE_API_KEY` | [dashboard.cohere.com](https://dashboard.cohere.com) | Command A (agentic), Command R+ (RAG) |
| `OPENROUTER_API_KEY` | [openrouter.ai](https://openrouter.ai) | 300+ models through one endpoint |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | LPU-accelerated Llama, Qwen, DeepSeek |

### Services (optional)

| Token | Source | Purpose |
|-------|--------|---------|
| `STRIPE_SECRET_KEY` | [dashboard.stripe.com](https://dashboard.stripe.com) | Payment processing (billing agents) |
| `SENDGRID_API_KEY` | [sendgrid.com](https://sendgrid.com) | Transactional email delivery |
| `SENTRY_DSN` | [sentry.io](https://sentry.io) | Error tracking and monitoring |
| `SLACK_WEBHOOK_URL` | [api.slack.com](https://api.slack.com) | Deployment and alert notifications |

```bash
cp .env.example .env
# Edit .env with your tokens — set at minimum one model provider
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
