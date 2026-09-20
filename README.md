<div align="center">

<!-- HERO BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:5b8dff&height=300&section=header&text=Citadel%20SaaS%20Factory&fontSize=60&fontColor=e6e9f5&animation=fadeIn&fontAlignY=35&desc=265%20Autonomous%20AI%20Agents%20%E2%80%A2%2015%20Domains%20%E2%80%A2%20Zero%20Software%20Cost&descSize=20&descAlignY=55&descColor=8b92ab" width="100%"/>

<br/>

<!-- STAT PILLS -->
<img src="https://img.shields.io/badge/AI_Agents-265-5b8dff?style=for-the-badge&labelColor=0d1117" alt="265 Agents"/>
<img src="https://img.shields.io/badge/Domains-15-b5e0ae?style=for-the-badge&labelColor=0d1117" alt="15 Domains"/>
<img src="https://img.shields.io/badge/Tests-20_Passing-b5e0ae?style=for-the-badge&labelColor=0d1117" alt="20 Tests"/>
<img src="https://img.shields.io/badge/Software_Cost-$0/mo-f0b866?style=for-the-badge&labelColor=0d1117" alt="$0/month"/>
<img src="https://img.shields.io/badge/Infrastructure-Any-e06070?style=for-the-badge&labelColor=0d1117" alt="Any Infrastructure"/>

<br/><br/>

<!-- TECH BADGES -->
<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
<img src="https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/K3s-ArgoCD-FFC61C?style=flat-square&logo=kubernetes&logoColor=white" alt="K3s"/>
<img src="https://img.shields.io/badge/Claude-Opus_4-7B61FF?style=flat-square&logo=anthropic&logoColor=white" alt="Claude"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT"/>

<br/><br/>

**Clone. Set one API key. Run any of 265 agents. Ship to any server.**

[Quick Start](#-quick-start) | [Agent Fleet](#-the-265-agent-fleet) | [Architecture](#-architecture) | [Runtime Engine](#-runtime-engine) | [Free Toolchain](#-free-toolchain)

</div>

---

## Why This Exists

Most SaaS frameworks give you scaffolding. This one gives you a **full autonomous workforce**.

265 AI agents across 15 business domains -- from CEO strategy to DevOps canary deploys -- each with its own system prompt, RAG retrieval pipeline, model tier, and guardrails. The entire stack runs on any Linux server with Docker. No AWS. No vendor lock-in. No monthly SaaS bills.

```
You:     "Analyze our API for security vulnerabilities"
Citadel: Routes to sec-sast agent (reasoning_deep tier, Claude Opus)
         -> Retrieves codebase context via RAG
         -> Runs OWASP Top 10 analysis
         -> Returns grounded findings with citations
         -> Output validated through triple-layer guardrails
```

---

## Quick Start

```bash
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git
cd citadel-saas-factory
cp .env.example .env          # Add your ANTHROPIC_API_KEY
docker compose up -d           # Postgres, Redis, Keycloak, MinIO, RabbitMQ
cd backbone && pip install -e ".[dev]" && cd ..
```

**Run your first agent in 3 lines:**

```python
from backbone.runtime.agent_sdk import AgentSDK
sdk = AgentSDK()
result = await sdk.run_agent("eng-api-designer", prompt="Design a health check endpoint")
```

**Or use the CLI:**

```bash
python -m backbone.cli run "Analyze competitor pricing strategy"
python -m backbone.cli health
python -m backbone.cli agents
```

---

## The 265-Agent Fleet

Every agent has: a system prompt, RAG retrieval pipeline, model tier routing, and guardrails validation.

```python
sdk.list_agents(domain="engineering")   # 25 agents
sdk.list_agents(domain="security")      # 22 agents
sdk.list_agents(domain="devops")        # 28 agents
sdk.list_agents()                       # all 265
```

<table>
<tr>
<td width="50%" valign="top">

### Executive and Strategy `12`
CEO Strategist, COO Operations, CFO Finance, CTO Technology, CMO Marketing, CPO Product, VP Engineering, VP Sales, OKR Tracker, Board Reporter, Competitive Intel, Decision Logger

### Marketing and Growth `22`
SEO, Content, Social Media, Email, PPC, Analytics, Landing Page, Brand Voice, PR, Influencer, Video, Podcast, Community, Growth Hacker, A/B Testing, Competitor Monitor, Newsletter, Webinar, Affiliate, Product Launch, Persona, Retention

### Sales and Revenue `18`
Lead Qualifier, Outbound, Proposals, CRM, Demo Prep, Contracts, Forecast, Win/Loss, Pricing, Territory, Upsell, Scheduler, Objection Handler, Referral, Partner, Call Analyzer, Pipeline Cleaner, Commission

### Customer Success `15`
Onboarding, Ticket Router, Response Drafter, Escalation, Churn Predictor, Health Scorer, NPS, Knowledge Builder, Chatbot, Feedback, Renewal, QBR, Adoption, SLA Monitor, Voice of Customer

### Product and Design `20`
UI Designer, UX Research, Wireframes, Prototyping, Design System, Accessibility, Responsive, Color Palette, Typography, Icons, Animation, Illustration, Data Viz, User Flow, Heuristic Eval, Onboarding UX, Form UX, Search UX, Notifications, Mobile

### Engineering `25`
API Designer, Models, Schemas, Services, Repositories, Migrations, Middleware, Events, Workers, Auth, Cache, Search, Webhooks, Email, File Handling, Pagination, Rate Limiting, Health, WebSockets, GraphQL, Multi-tenant, Error Handling, Logging, Config, Code Review

</td>
<td width="50%" valign="top">

### Frontend `18`
Components, Pages, Layouts, Forms, Tables, Charts, Auth, State, API Client, Accessibility, Responsive, i18n, SEO, Performance, Testing, Animation, Error Boundaries, PWA

### DevOps and Infrastructure `28`
CI, CD, GitOps, Image Build, Image Scan, Image Sign, Helm, Terraform, Ansible, K8s, Scaling, Debugging, Canary, Rollback, Release, Certs, DNS, Backup, Restore, Monitoring, Alerts, Logs, Service Mesh, Ingress, Storage, Queue, Cost, Capacity

### Security `22`
SAST, SCA, DAST, Secrets, Container, IaC, Runtime, Policy, Incidents, Vulnerabilities, Patching, Access Review, RBAC, Encryption, Audit, Compliance, Pentest, Threat Hunt, Network, WAF, PII Detection, Supply Chain

### Data and Analytics `18`
Schema, Migrations, Indexes, Query Optimization, RLS, Backups, ETL, Analytics, Vectors, Warehouse, Reports, Dashboards, Events, Cohorts, A/B Analysis, Forecasting, Anomaly, Privacy

### QA and Testing `22`
Unit, Integration, E2E, API, Load, Performance, Security, Accessibility, Visual Regression, Coverage, Mutation, Contract, Chaos, Fixtures, Mocks, Regression, Flaky Detection, Prioritization, Smoke, Compatibility, Data Validation, Reporting

### HR, Finance, Legal, Content `45`
Job Descriptions, Interviews, Onboarding, Performance, Billing/Stripe, Subscriptions, Tax, Revenue, Runway, ToS, DPA, GDPR, SOC2, Tech Writing, Blog, Docs, Changelog, Case Studies, and 27 more

</td>
</tr>
</table>

<details>
<summary><b>Full agent registry (click to expand)</b></summary>

See [`.claude/agents/_registry.yaml`](.claude/agents/_registry.yaml) for all 265 entries with IDs, domains, and descriptions.

Each agent definition lives in `.claude/agents/<domain>/<agent-id>.md` with:
- YAML frontmatter (id, domain, tier, rag_enabled, tools, skills)
- RAG Retrieval Prompt with domain-scoped metadata filters
- LLM System Prompt with role, rules, and escalation protocol

</details>

---

## Architecture

```
                              CLIENTS
                    Browser / Mobile / API
                              |
                    +---------+---------+
                    |                   |
              +-----v------+    +------v-------+
              |  FRONTEND  |    | AUTH GATEWAY  |
              | Next.js 14 |    | Keycloak 24   |
              +-----+------+    +------+-------+
                    |                  |
              +-----v------------------v-------+
              |          BACKEND API           |
              |   FastAPI + Agent Runtime      |
              |   /agent/run  /agent/browse    |
              +-----+------+------+------+-----+
                    |      |      |      |
            +-------v+  +-v----+ +v-----+ +v--------+
            |Postgres|  |Redis | |MinIO | |RabbitMQ  |
            |16+pgvec|  |  7   | | (S3) | |          |
            +--------+  +-----+ +------+ +---------+
                    |
            +-------v----------------------------+
            |        AGENT RUNTIME (backbone/)   |
            |  ModelRouter -> AgentSDK -> RAG    |
            |  Planner -> Guardrails -> Tracer   |
            +-------+---------------------------+
                    |
            +-------v----------------------------+
            |         ORCHESTRATION              |
            |   K3s + ArgoCD + Linkerd (mTLS)    |
            +------------------------------------+
```

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | **FastAPI** (Python 3.12) | Async-first, Pydantic validation, OpenAPI |
| Agent Runtime | **backbone/** (LiteLLM + structlog) | Multi-model routing, budget control, RAG |
| Frontend | **Next.js 14** (TypeScript) | SSR/SSG, React Server Components |
| Database | **PostgreSQL 16** + pgvector | HNSW vector search, JSONB, RLS |
| Cache | **Redis 7** | Session, rate limiting, pub/sub |
| Auth | **Keycloak 24** | OAuth2, RBAC, MFA, SSO |
| Storage | **MinIO** | S3-compatible, self-hosted |
| Messaging | **RabbitMQ** | Async events, DLQ |
| Orchestration | **K3s + ArgoCD** | Lightweight K8s, GitOps |
| Service Mesh | **Linkerd** | mTLS between all services |
| Secrets | **HashiCorp Vault** | Rotation, encryption |
| Observability | **Prometheus + Grafana + Loki** | Metrics, dashboards, logs |

---

## Runtime Engine

The `backbone/` package powers the agent fleet with 5 model tiers, agentic RAG, and triple-layer guardrails.

### Model Routing (5 tiers, automatic fallback)

```yaml
reasoning_deep:   Claude Opus 4     -> Sonnet 4       # Architecture, security
reasoning_fast:   Claude Sonnet 4   -> Haiku 4.5      # Development, reviews
cheap_fast:       Claude Haiku 4.5  -> --              # Content, high volume
rag_specialist:   Claude Sonnet 4   -> Haiku 4.5      # RAG with citations
local_only:       Ollama Llama 3.1  -> Mistral         # Budget fallback
```

Daily budget cap ($50 default). Exceeds? Auto-routes to `local_only`. Service continues, quality degrades gracefully.

### Agent SDK

```python
from backbone.runtime.agent_sdk import AgentSDK

sdk = AgentSDK()

# Run any agent by ID
result = await sdk.run_agent("sec-sast", prompt="Scan auth module for injection")

# Spawn sub-agents (depth-capped at 3, fan-out at 5)
await sdk.spawn_sub_agent("parent-id", "sec-pentest", prompt="Deep scan /api/auth")

# List by domain
sdk.list_agents(domain="security")  # 22 agents
```

### Agentic RAG Pipeline

```
Query -> Retrieve (vector + keyword + RRF) -> Grade (LLM-as-judge)
                                                |
                                    relevance < 0.5?
                                     /           \
                                   yes            no
                                    |              |
                                 Rewrite       Generate [chunk-id] citations
                                    |              |
                              (loop, max 3)    Self-check grounding
                                                   |
                                                Result
```

- **Store**: PostgreSQL 16 + pgvector (HNSW index, metadata GIN)
- **Embeddings**: Voyage 3 (prod) or Ollama nomic-embed-text (local)
- **Reranking**: Voyage Rerank 2 (prod) or Reciprocal Rank Fusion (local)

### Orchestrator (Plan, Execute, Critique)

```python
from backbone.orchestrator.planner import PlannerLoop
loop = PlannerLoop(router=model_router, max_replans=3)
result = await loop.run(goal="Redesign the authentication flow")
# Planner decomposes -> Executor runs -> Critic approves or revises
```

### Triple-Layer Guardrails

| Layer | What | How |
|-------|------|-----|
| 1. Output Validation | Hallucination, toxicity, PII | Guardrails AI Hub validators |
| 2. Input Sanitization | Prompt injection in RAG docs and browser content | 16 regex patterns, truncation |
| 3. Action Enforcement | Out-of-scope tool calls | 10-action allowlist, fail-closed |

Threshold: 0.85. Below? Retry (max 3). Still below? Reject. No exceptions.

### Chrome Extension

Manifest V3 side-panel assistant at `extensions/chrome/`. Captures active tab text on explicit user click, sanitizes through injection filters, routes through `POST /agent/browse`.

---

## Harness (`.claude/`)

The full agent harness lives in `.claude/`:

| Component | Count | Purpose |
|-----------|-------|---------|
| **Agents** | 265 generated + 11 hand-written | Executable definitions with RAG prompts |
| **Skills** | 10 | Deep reference: code-review, deploy, guardrails, llm-wiki, testing, etc. |
| **Commands** | 38 (20 YAML + 18 MD) | `/deploy`, `/audit`, `/scaffold`, `/wiki-ingest`, etc. |
| **Hooks** | 11 scripts + settings.json | pre-commit, post-deploy, on-security-alert, vault-autolink |
| **Templates** | 20 | FastAPI endpoints, React components, Helm charts, Terraform modules |
| **Rules** | 21 | Architecture, security, testing, naming, guardrails, obsidian backlinks |
| **MCP Servers** | 6 | GitHub, filesystem, PostgreSQL, Docker, Kubernetes, Ruflo |

---

## Free Toolchain

**Total monthly software cost: $0**

<table>
<tr>
<td width="33%" valign="top">

**Orchestration**
- ArgoCD (replaces Spinnaker)
- K3s (replaces EKS/GKE)
- Traefik (replaces AWS ALB)
- Linkerd (replaces Istio)

**Security**
- Semgrep (replaces SonarQube)
- Trivy (replaces Snyk)
- Falco (replaces Sysdig)
- Kyverno (replaces OPA GK)
- OWASP ZAP (replaces Burp)
- TruffleHog (replaces GitGuardian)

</td>
<td width="33%" valign="top">

**Identity and Secrets**
- Keycloak (replaces Auth0)
- HashiCorp Vault (replaces AWS SM)
- Certbot (replaces commercial TLS)

**Observability**
- Prometheus (replaces Datadog)
- Grafana (replaces Datadog dashboards)
- Loki (replaces Splunk)
- Grafana OnCall (replaces PagerDuty)

</td>
<td width="33%" valign="top">

**Storage and Messaging**
- MinIO (replaces AWS S3)
- RabbitMQ (replaces SQS)
- Velero (replaces Kasten K10)

**Deployment**
- Ansible (replaces Puppet/Chef)
- Flagsmith (replaces LaunchDarkly)

**AI/ML Security**
- Guardrails AI
- DeepEval

</td>
</tr>
</table>

---

## Docker Compose (One Command)

```bash
docker compose up -d
```

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL 16 | 5432 | Primary database + pgvector |
| Redis 7 | 6379 | Cache, sessions, rate limiting |
| Keycloak 24 | 8080 | Auth server (admin console) |
| MinIO | 9000/9001 | Object storage and console |
| RabbitMQ | 5672/15672 | Message broker and management |
| MailHog | 1025/8025 | Local email capture |
| Backend | 8000 | FastAPI API |
| Frontend | 3000 | Next.js UI |

---

## Infrastructure Agnostic

Runs on **any** Linux server with SSH and Docker. No cloud vendor lock-in.

- Any VPS (Hetzner, DigitalOcean, Linode, Vultr)
- Bare metal servers
- On-premises infrastructure
- Edge deployments
- Home lab

---

## LLM Wiki (Karpathy Pattern)

The agent fleet uses Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) as persistent brain memory:

```
docs/vault/
  raw/          # Immutable source documents (never modified by LLM)
  wiki/         # LLM-maintained compiled knowledge
    index.md    # Master index (always consulted first)
    entities/   # People, tools, services
    concepts/   # Patterns, principles
    sources/    # Source metadata
  SCHEMA.md     # Governance (co-evolved with human)
```

Every session adds to the wiki. Every valuable answer is filed back. Knowledge compounds across all 265 agents instead of dying with the chat.

---

## Security

- **OWASP LLM Top 10 mapped**: `security/ai-security-by-design.html`
- **Sigma detection rules** for injection attempts and repeated rejections
- **OPA policies** for browse endpoint rate limiting
- **Kyverno policies** for agent container restrictions
- All outputs validated. All inputs sanitized. Fail-closed by default.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD mandatory, 80% coverage minimum)
4. Run: `make lint && make test && make security`
5. Commit: `feat: add user auth`
6. Open a PR, wait for CI, get 1 approval

---

## License

MIT License. See [LICENSE](LICENSE).

Copyright (c) Citadel Cloud Management

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:5b8dff&height=120&section=footer" width="100%"/>

**[citadelcloudmanagement.com](https://citadelcloudmanagement.com)**

<sub>Built with Claude Code. Powered by 265 autonomous agents. $0/month software cost.</sub>

</div>

<!-- project-structure -->
## Project structure

```text
├── .antigravity/
├── .claude/
├── .codegen/
├── .codex/
├── .continue/
├── .cursor/
├── .daytona/
├── .devin/
├── .factory/
├── .github/
├── .jules/
├── .windsurf/
├── backbone/
│   ├── agents/
│   ├── data/
│   ├── governance/
│   ├── memory/
│   ├── observability/
│   ├── orchestrator/
│   ├── policies/
│   ├── rag/
│   └── … 10 more
├── backend/
│   ├── app/
│   ├── tests/
│   ├── CLAUDE.md
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic.ini
│   └── pyproject.toml
├── bin/
│   └── cli.js
├── compliance/
│   ├── automation/
│   ├── checklists/
│   ├── evidence/
│   ├── frameworks/
│   ├── policies/
│   └── README.md
├── docs/
│   ├── adr/
│   ├── agents/
│   ├── references/
│   ├── runbooks/
│   ├── templates/
… (truncated)
```

<!-- architecture -->
## Architecture

![Architecture diagram](docs/architecture.svg)
