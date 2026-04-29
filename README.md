<div align="center">

# 🏰 Citadel SaaS Factory

### Universal Full-Stack SaaS Production Framework

**500+ Autonomous Business Agents | 12 Model Providers | 30 Domains | Cross-IDE**

[![npm](https://img.shields.io/npm/v/@citadelcloud/saas-factory?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/@citadelcloud/saas-factory)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Agents](https://img.shields.io/badge/Agents-500+-FF6B35?style=for-the-badge&logo=probot&logoColor=white)](.claude/agents/_registry.yaml)
[![Models](https://img.shields.io/badge/Models-12_Providers-8B5CF6?style=for-the-badge&logo=openai&logoColor=white)](models/catalog.yaml)
[![Domains](https://img.shields.io/badge/Domains-30-E91E63?style=for-the-badge&logo=target&logoColor=white)](#-all-500-agents--30-domains)
[![IDEs](https://img.shields.io/badge/IDEs-12_Supported-0078D4?style=for-the-badge&logo=visualstudiocode&logoColor=white)](#-cross-ide-support)
[![Cost](https://img.shields.io/badge/Cost-$0/month-00C853?style=for-the-badge&logo=cashapp&logoColor=white)](#-free-toolchain)
[![AI Powered](https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge)](#)

<br/>

[📦 npm Package](https://www.npmjs.com/package/@citadelcloud/saas-factory) &nbsp;|&nbsp; [🏢 citadelcloudmanagement.com](https://citadelcloudmanagement.com)

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
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git my-saas
cd my-saas && cp .env.example .env    # Set at least one API key
./scripts/setup-claude-code.sh        # Install master prompt + .claude/ scaffolding
./scripts/parallel-bootstrap.sh       # Install models, MCP, hooks, agents
claude                                # Or open in Cursor, Codex, Jules, Copilot...
```

**Install into an existing project** (no need to clone the full factory):

```bash
# One-liner: clone factory, run setup against your project, done
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git /tmp/citadel
/tmp/citadel/scripts/setup-claude-code.sh /path/to/your/project
cd /path/to/your/project && claude
```

> See the **[full step-by-step guide](#-launch-your-saas-business--step-by-step-guide)** below for detailed setup of Claude Code, OpenAI Codex, Google Jules, and GitHub Copilot.

---

## 🚀 Launch Your SaaS Business — Step-by-Step Guide

> **Use this framework to launch any SaaS product.** Clone once, configure for your business, connect your AI tools, and deploy. Works with Claude Code, OpenAI Codex, Google Jules, GitHub Copilot, Cursor, and 6 more IDEs.

### Step 1: Create Your Business Folder

Create a dedicated project directory and initialize it from the Citadel factory:

```bash
# Option A: npm scaffold (creates a clean project folder)
npx @citadelcloud/saas-factory init my-company-saas
cd my-company-saas

# Option B: git clone (full framework with all 500+ agents)
git clone https://github.com/Citadel-Cloud-Management/citadel-saas-factory.git my-company-saas
cd my-company-saas
git remote rename origin upstream
git remote add origin https://github.com/YOUR-ORG/my-company-saas.git

# Option C: fork on GitHub (best for long-term tracking of upstream updates)
# 1. Fork https://github.com/Citadel-Cloud-Management/citadel-saas-factory on GitHub
# 2. Clone your fork:
git clone https://github.com/YOUR-ORG/my-company-saas.git
cd my-company-saas
```

Your project folder structure after init:

```
my-company-saas/
├── .claude/              # AI intelligence layer (agents, rules, skills, hooks)
├── .github/              # CI/CD workflows, Copilot instructions
├── backend/              # FastAPI (Python 3.12) — API, business logic, guardrails
├── frontend/             # Next.js 14 (TypeScript) — UI, components, state
├── infrastructure/       # Terraform, Helm, K8s manifests
├── monitoring/           # Prometheus rules, Grafana dashboards, Loki pipelines
├── security/             # Semgrep, Trivy, Kyverno, guardrails validators
├── scripts/              # Bootstrap, verify, migrate, deploy
├── docs/vault/           # Obsidian knowledge vault + LLM Wiki
├── models/               # Model catalog, routing config, embeddings
├── mcp/                  # MCP server registry
├── .env.example          # All environment variables with documentation
├── docker-compose.yml    # Local dev stack (Postgres, Redis, Keycloak, etc.)
└── Makefile              # Common commands: test, lint, deploy, wiki-ingest
```

### Step 2: Configure Your Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env — set at minimum ONE model provider API key:
# ANTHROPIC_API_KEY=sk-ant-...    (for Claude Code, Ruflo, agents)
# OPENAI_API_KEY=sk-...           (for Codex, GPT-5, o4)
# GOOGLE_API_KEY=...              (for Gemini, Jules)
# GITHUB_TOKEN=ghp_...            (for GitHub CLI, Actions, MCP)
```

### Step 3: Connect Claude Code

Claude Code is the primary AI coding agent. The setup script installs the master prompt as `CLAUDE.md` and scaffolds the full `.claude/` intelligence layer.

```bash
# Install Claude Code (if not already installed)
npm install -g @anthropic-ai/claude-code

# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Run the setup script — installs CLAUDE.md, commands, hooks, settings, .claudeignore
./scripts/setup-claude-code.sh

# Launch Claude Code in your project folder
cd my-company-saas
claude
```

**What the setup script installs:**

```
my-company-saas/
├── CLAUDE.md                  ← master operating prompt (project constitution)
├── .claudeignore              ← excludes build artifacts, secrets, node_modules
├── .mcp.json                  ← MCP server template (GitHub + filesystem)
└── .claude/
    ├── settings.json          ← model routing (Haiku/Sonnet/Opus) + guardrails
    ├── commands/              ← /review, /test-all, /deploy, /security-audit
    ├── hooks/                 ← auto-lint on file write
    ├── agents/                ← ready for 500+ agent definitions
    ├── rules/                 ← coding standards, security policies
    ├── skills/                ← specialist capabilities
    ├── memory/                ← persistent project memory
    ├── mcp/                   ← MCP server configs
    └── templates/             ← code generation templates
```

**Install into any existing project** (the key feature):

```bash
# From the factory repo, target any project on your machine
./scripts/setup-claude-code.sh /path/to/any/project

# Or use make
make setup-claude-target TARGET=/path/to/any/project
```

**Claude Code commands after setup:**

```bash
claude                            # Start interactive session
claude "scaffold user auth"       # One-shot task
/review                           # Code review on current diff
/test-all                         # Run full test suite
/deploy staging                   # Deploy to staging
/security-audit                   # Security scan
```

### Step 4: Connect OpenAI Codex

OpenAI Codex reads `AGENTS.md` and `.codex/config.toml` — both ship with the factory.

```bash
# Install Codex CLI
npm install -g @openai/codex

# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"

# Launch Codex in your project folder
cd my-company-saas
codex

# Codex automatically detects:
#   AGENTS.md              → agent instructions and project context
#   .codex/config.toml     → Codex-specific configuration
```

**Codex config** (`.codex/config.toml`):

```toml
model = "o4-mini"               # or "gpt-5", "o4" for complex reasoning
approval_mode = "suggest"       # "auto-edit" for autonomous mode
provider = "openai"
```

### Step 5: Connect Google Jules & Gemini CLI

Google Jules reads `.jules/config.yml` and `GEMINI.md` — both ship with the factory.

```bash
# Install Gemini CLI
npm install -g @anthropic-ai/gemini-cli   # or: npx @anthropic-ai/gemini-cli

# Set your Google API key
export GOOGLE_API_KEY="your-key-here"

# Launch Gemini CLI / Jules in your project folder
cd my-company-saas
gemini

# Jules and Gemini CLI automatically detect:
#   GEMINI.md              → Gemini-specific instructions
#   .jules/config.yml      → Jules project configuration
```

### Step 6: Connect GitHub Copilot

GitHub Copilot reads `.github/copilot-instructions.md` — ships with the factory.

```bash
# Copilot activates automatically in VS Code / JetBrains
# The factory includes:
#   .github/copilot-instructions.md   → project-aware Copilot context
#   .github/workflows/                → CI/CD pipelines
```

### Step 7: Bootstrap & Verify

```bash
# Run the parallel bootstrap (installs models, MCP servers, hooks, agents)
./scripts/parallel-bootstrap.sh

# Verify everything is connected (green/red status report)
./scripts/verify-install.sh

# Expected output:
# ✅ Claude Code    — connected (claude-sonnet-4-6)
# ✅ OpenAI Codex   — connected (o4-mini)
# ✅ GitHub Copilot — detected (.github/copilot-instructions.md)
# ✅ MCP servers    — 12 active (github, filesystem, postgres, ...)
# ✅ Agents         — 500+ registered, 42 enabled for your stack
# ✅ Guardrails     — active (threshold: 0.85, validators: 4)
# ✅ Docker stack   — running (postgres, redis, keycloak, minio, rabbitmq)
```

### Step 8: Start Building Your Product

```bash
# Start local infrastructure
docker compose up -d

# Launch your AI coding agent of choice
claude                     # Claude Code (recommended — full agent integration)
codex                      # OpenAI Codex
# Or open in Cursor, Windsurf, Antigravity, Continue.dev...

# Example first tasks:
claude "scaffold the user authentication module with Keycloak"
claude "create the Stripe billing integration with subscription tiers"
claude "build the admin dashboard with usage analytics"
claude "set up CI/CD pipeline for staging and production"
```

### Multi-IDE Workflow (Use All Three Together)

You can run Claude Code, Codex, and Copilot simultaneously — each reads its own config file, and all share the same codebase:

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR PROJECT FOLDER                       │
│                                                             │
│  Claude Code ←── .claude/CLAUDE.md (500+ agents, guardrails)│
│  OpenAI Codex ←── AGENTS.md + .codex/config.toml           │
│  Copilot ←── .github/copilot-instructions.md               │
│  Cursor ←── .cursor/rules/ + AGENT.md                      │
│  Jules ←── .jules/config.yml + GEMINI.md                   │
│  Windsurf ←── .windsurf/rules/                             │
│                                                             │
│  All share: docker-compose.yml, .env, Makefile, git history │
└─────────────────────────────────────────────────────────────┘
```

**Recommended workflow:**
- **Claude Code** for architecture, multi-file features, agent orchestration, deployments
- **OpenAI Codex** for rapid code generation, one-shot tasks, reasoning chains
- **GitHub Copilot** for inline autocomplete while editing in VS Code/JetBrains
- **Cursor** for visual AI-assisted editing with diff preview
- **Jules** for long-running background tasks with Gemini's 2M context window

### Using the Master Prompt (Advanced)

For full autonomous factory integration, download the [Master Prompt v3](https://github.com/Citadel-Cloud-Management/citadel-saas-factory) and fill in the YAML configuration block:

```yaml
target_project:
  name: "My SaaS Product"
  slug: "my-saas-product"
  repo_url: "https://github.com/my-org/my-saas-product"
  stack:
    primary_language: "python"           # python | typescript | go | rust
    framework_backend: "FastAPI"         # FastAPI | NestJS | Django | Express
    framework_frontend: "Next.js 14"    # Next.js 14 | React Native | Remix
  infrastructure:
    cloud_target: "Hetzner-VPS"         # AWS | Azure | GCP | Hetzner | bare-metal
    compute: "K3s"                      # K3s | EKS | Docker | Lambda
  data:
    primary_db: "Postgres"
    cache: "Redis"
  ai_policy:
    claude_code_enabled: true
    model_routing:
      default: "claude-sonnet-4-6"
      cheap: "claude-haiku-4-5-20251001"
      premium: "claude-opus-4-7"
```

Paste the filled YAML + master prompt into Claude Code, and it will execute a 10-phase autonomous pipeline: fetch, scaffold, install intelligence layers, extract aligned assets, gap analysis, integration plan, ship code, validate, execute, and enter continuous autonomous operation.

### Claude Code Project Constitution

This repo ships with a unified [`CLAUDE.md`](CLAUDE.md) — the project constitution that Claude Code reads automatically. It covers the full stack, all 500+ agents, commands, rules, hooks, MCP connections, model routing, guardrails, and the knowledge layer. A separate [`CLAUDE_CODE_MASTER_PROMPT.md`](CLAUDE_CODE_MASTER_PROMPT.md) provides the deep-dive operating manual (7-layer stack, ADK, LLM API internals, RAG architecture, playbooks).

```bash
# Automated: run the setup script (installs CLAUDE.md + full .claude/ scaffolding)
./scripts/setup-claude-code.sh                     # current project
./scripts/setup-claude-code.sh /path/to/project    # any other project
make setup-claude                                   # via Makefile
make setup-claude-target TARGET=/path/to/project    # any other project via Makefile

# Manual: just copy the files
cp CLAUDE.md /path/to/project/CLAUDE.md                            # project constitution
cp CLAUDE_CODE_MASTER_PROMPT.md /path/to/project/CLAUDE.md         # or use the deep-dive version
cp CLAUDE_CODE_MASTER_PROMPT.md ~/.claude/CLAUDE.md                 # personal global defaults
```

> [!IMPORTANT]
> **Minimum requirements:** One API key (Anthropic, OpenAI, or Google), Docker, Git, Node.js 20+, Python 3.12+. Total software cost: **$0/month** — you only pay for API usage.

---

## 🗂️ Project Structure

```
citadel-saas-factory/
│
├── CLAUDE.md                             # Project constitution (Claude Code reads this)
├── AGENTS.md                             # OpenAI Codex / multi-agent instructions
├── GEMINI.md                             # Google Jules / Gemini CLI instructions
├── AGENT.md                              # Cursor agent config
├── CLAUDE_CODE_MASTER_PROMPT.md          # Deep-dive operating manual
├── docker-compose.yml                    # Local dev stack (12 services)
├── Makefile / Justfile                   # All CLI commands
├── .env.example                          # Environment variable contract
├── .mcp.json                             # MCP server configuration
│
├── .claude/                              # ── AI INTELLIGENCE LAYER ──
│   │
│   ├── agents/                           # 500+ agent definitions
│   │   ├── _registry.yaml                #   Master registry (id, domain, model, entrypoint)
│   │   ├── executive/                    #   18 agents: CEO, CTO, CFO, OKR, Board, M&A
│   │   ├── marketing/                    #   28 agents: SEO, Content, Social, Email, PPC
│   │   ├── sales/                        #   24 agents: Lead Qualifier, CRM, Deal Desk
│   │   ├── customer-success/             #   20 agents: Onboarding, Churn, NPS, QBR
│   │   ├── product-design/               #   26 agents: UI, Wireframes, A11y, Research
│   │   ├── engineering/                  #   35 agents: API, Auth, Cache, CQRS, SDK
│   │   ├── frontend/                     #   24 agents: Components, Forms, PWA, SSR
│   │   ├── devops/                       #   34 agents: CI/CD, K8s, Terraform, FinOps
│   │   ├── security/                     #   28 agents: SAST, DAST, Falco, Zero Trust
│   │   ├── data-analytics/               #   24 agents: ETL, Dashboards, Vector, dbt
│   │   ├── qa-testing/                   #   28 agents: Unit, E2E, Load, Chaos, Mutation
│   │   ├── hr-people/                    #   16 agents: Jobs, Onboarding, DEI, Culture
│   │   ├── finance/                      #   20 agents: Stripe, Tax, Revenue, FP&A
│   │   ├── legal/                        #   14 agents: GDPR, SOC2, AI Ethics, IP
│   │   └── content/                      #   16 agents: Tech Writing, Case Studies
│   │
│   ├── rules/                            # 23 coding standards
│   │   ├── code-quality.md               #   Immutability, small files, no dead code
│   │   ├── architecture.md               #   Clean architecture, DDD, bounded contexts
│   │   ├── api-design.md                 #   REST conventions, response envelope
│   │   ├── security.md                   #   No hardcoded secrets, input validation
│   │   ├── testing.md                    #   TDD mandatory, 80% coverage
│   │   ├── database.md                   #   Migrations, RLS, indexes
│   │   ├── guardrails.md                 #   Mandatory LLM validation pipeline
│   │   ├── llm-wiki.md                   #   Wiki-first lookup, ingest protocol
│   │   ├── obsidian-backlinks.md         #   Bidirectional linking, vault integration
│   │   ├── frontend.md                   #   Components, a11y, responsive-first
│   │   ├── devops.md                     #   GitOps, immutable infra, health probes
│   │   ├── monitoring.md                 #   Structured logging, RED metrics
│   │   ├── performance.md               #   Caching, pagination, connection pools
│   │   ├── error-handling.md             #   Structured errors, retry strategies
│   │   ├── naming.md                     #   snake_case, PascalCase, kebab-case
│   │   ├── secrets.md                    #   Vault, rotation, scanning
│   │   ├── git.md                        #   Conventional commits, squash merge
│   │   ├── review.md                     #   PR required, CI must pass
│   │   ├── dependencies.md               #   Lock files, license check
│   │   ├── documentation.md              #   ADRs, OpenAPI, changelogs
│   │   └── accessibility.md              #   WCAG 2.1 AA, ARIA, keyboard nav
│   │
│   ├── skills/                           # 262+ specialist capabilities
│   │   ├── master-system/                #   🔥 26-plugin autonomous engineering system
│   │   │   ├── SKILL.md                  #     Orchestrator + plugin registry
│   │   │   ├── 01-no-gatekeeping.md      #     Complete implementation guidance
│   │   │   ├── 02-real-world-execution.md#     Production-oriented outputs
│   │   │   ├── 03-multi-domain-validation#     Cross-domain validation
│   │   │   ├── 04-tool-first-execution.md#     MCP tools > assumptions
│   │   │   ├── 05-execution-ready-output #     Standardized response format
│   │   │   ├── 06-security-first.md      #     Zero trust, OWASP, threat modeling
│   │   │   ├── 07-autonomous-agents.md   #     13 agent archetypes
│   │   │   ├── 08-mcp-ecosystem.md       #     40+ MCP server integrations
│   │   │   ├── 09-saas-factory.md        #     End-to-end SaaS generation
│   │   │   ├── 10-engineering-standards  #     Backend/frontend/infra/DB
│   │   │   ├── 11-observability.md       #     OTel + Prometheus + Grafana
│   │   │   ├── 12-agent-safety.md        #     Safety controls + circuit breakers
│   │   │   ├── 13-context-engineering.md #     Memory, ADRs, decision logs
│   │   │   ├── 14-response-quality.md    #     Pre-response validation
│   │   │   ├── 15-folder-structure.md    #     Default project layout
│   │   │   ├── 16-new-project-outputs.md #     13 required artifacts
│   │   │   ├── 17-cicd-standards.md      #     Pipeline stages + tooling
│   │   │   ├── 18-cloud-security.md      #     AWS/Azure/GCP security
│   │   │   ├── 19-execution-priority.md  #     Security > stability > velocity
│   │   │   ├── 20-failure-handling.md    #     Retry, circuit breakers, DLQ
│   │   │   ├── 21-business-awareness.md  #     ROI, cost, vendor lock-in
│   │   │   ├── 22-self-check.md          #     Final validation checklist
│   │   │   ├── 23-plugin-execution.md    #     Claude Code safety protocol
│   │   │   ├── 24-saas-business.md       #     Billing, CRM, analytics
│   │   │   ├── 25-enterprise-docs.md     #     Auto-generated documentation
│   │   │   └── 26-never-blind.md         #     Verified state > assumptions
│   │   ├── code-review/SKILL.md          #   Automated code review patterns
│   │   ├── testing/SKILL.md              #   Test framework patterns
│   │   ├── guardrails/SKILL.md           #   LLM output validation
│   │   ├── llm-wiki/SKILL.md             #   Knowledge base management
│   │   ├── obsidian-linker/SKILL.md      #   Vault cross-linking
│   │   ├── graphify/SKILL.md             #   Codebase knowledge graph
│   │   ├── deploy/SKILL.md               #   Deployment automation
│   │   ├── onboard/SKILL.md              #   Developer onboarding
│   │   ├── security-audit/SKILL.md       #   Security scanning
│   │   └── (250+ more...)               #   AWS, Azure, Django, React, etc.
│   │
│   ├── hooks/                            # 11 lifecycle scripts
│   │   ├── pre-commit.sh                 #   Secret scan + lint + test
│   │   ├── pre-push.sh                   #   Full validation before push
│   │   ├── pre-agent.sh                  #   Before agent spawn
│   │   ├── post-agent.sh                 #   After agent complete
│   │   ├── pre-deploy.sh                 #   Pre-deployment checks
│   │   ├── post-deploy.sh                #   Post-deployment verification
│   │   ├── on-error.sh                   #   Error handling
│   │   ├── on-test-fail.sh               #   Test failure handling
│   │   ├── on-deploy-fail.sh             #   Deployment failure handling
│   │   ├── on-security-alert.sh          #   Security incident response
│   │   └── vault-autolink.sh             #   Auto-backlink vault writes
│   │
│   ├── memory/                           # Persistent project memory
│   │   ├── project-context.md            #   Current project state
│   │   ├── architecture-decisions.md     #   Architectural choices
│   │   ├── agent-learnings.md            #   Agent knowledge base
│   │   ├── error-patterns.md             #   Common error patterns
│   │   ├── deployment-history.md         #   Deployment records
│   │   └── team-preferences.md           #   Team conventions
│   │
│   ├── commands/                         # 34 slash commands
│   │   ├── deploy.md                     #   /deploy staging|production
│   │   ├── review.md                     #   /review (code review)
│   │   ├── test.md                       #   /test (run test suite)
│   │   ├── wiki-ingest.md                #   /wiki-ingest (add to wiki)
│   │   ├── wiki-query.md                 #   /wiki-query (search wiki)
│   │   ├── wiki-lint.md                  #   /wiki-lint (health check)
│   │   └── (28 more...)                  #   audit, backup, build, cert...
│   │
│   ├── templates/                        # 20 code generation templates
│   │   ├── api-endpoint.py.tmpl          #   FastAPI endpoint scaffold
│   │   ├── component.tsx.tmpl            #   React component scaffold
│   │   ├── test-unit.py.tmpl             #   pytest test scaffold
│   │   ├── terraform-module.tf.tmpl      #   Terraform module scaffold
│   │   └── (16 more...)                  #   model, service, migration...
│   │
│   ├── mcp/                              # 8 MCP server configs
│   │   ├── github.json                   #   GitHub repos, PRs, issues
│   │   ├── postgres.json                 #   Database queries
│   │   ├── docker.json                   #   Container management
│   │   ├── kubernetes.json               #   Cluster operations
│   │   ├── filesystem.json               #   File access
│   │   ├── redis.json                    #   Cache operations
│   │   ├── vault.json                    #   Secret management
│   │   └── prometheus.json               #   Metrics queries
│   │
│   └── settings.json                     # Model routing + hook config
│
├── backbone/                             # ── AGENT ORCHESTRATOR ──
│   │
│   ├── memory/                           # 8-Layer AI Memory System
│   │   ├── __init__.py                   #   Package exports
│   │   ├── schemas.py                    #   Frozen dataclass models (all 8 layers)
│   │   ├── config.py                     #   Environment-based configuration
│   │   ├── orchestrator.py               #   Main coordinator (assemble + post-inference)
│   │   ├── working_memory.py             #   L1: Context window management
│   │   ├── short_term_memory.py          #   L2: Redis conversation buffer
│   │   ├── long_term_memory.py           #   L3: PostgreSQL persistent user data
│   │   ├── episodic_memory.py            #   L4: PostgreSQL event timeline
│   │   ├── semantic_memory.py            #   L5: pgvector RAG retrieval
│   │   ├── procedural_memory.py          #   L6: PostgreSQL workflow patterns
│   │   ├── entity_memory.py              #   L7: PostgreSQL + Neo4j entity profiles
│   │   ├── shared_memory.py              #   L8: Redis multi-agent coordination
│   │   ├── manager.py                    #   Legacy 4-tier manager (backward compat)
│   │   └── api/
│   │       └── routes.py                 #   FastAPI endpoints for all layers
│   ├── orchestrator/                     #   Agent lifecycle management
│   ├── governance/                       #   Policy enforcement
│   ├── workflows/                        #   Workflow definitions
│   ├── tools/                            #   Tool catalog
│   ├── validation/                       #   Input/output validation
│   ├── observability/                    #   Logging, metrics, tracing
│   └── runtime/                          #   Agent execution runtime
│
├── backend/                              # ── FastAPI (Python 3.12) ──
│   ├── app/
│   │   ├── api/                          #   REST endpoints
│   │   ├── core/                         #   Config, security, dependencies
│   │   ├── domain/                       #   Business entities, value objects
│   │   ├── middleware/
│   │   │   └── guardrails.py             #   LLM validation pipeline
│   │   ├── services/                     #   Business logic layer
│   │   └── repositories/                 #   Data access layer
│   ├── alembic/                          #   Database migrations
│   └── tests/                            #   pytest test suite
│
├── frontend/                             # ── Next.js 14 (TypeScript) ──
│   ├── src/
│   │   ├── app/                          #   App router pages
│   │   ├── components/                   #   React components
│   │   ├── hooks/                        #   Custom React hooks
│   │   ├── lib/                          #   Utilities, API client
│   │   └── stores/                       #   Zustand state management
│   └── tests/                            #   Vitest + Playwright
│
├── security/                             # ── SECURITY POLICIES ──
│   ├── falco/                            #   Runtime threat detection rules
│   ├── guardrails/                       #   LLM output validators
│   ├── kyverno/                          #   Kubernetes policy enforcement
│   ├── opa/                              #   Open Policy Agent rules
│   ├── sigma/                            #   SIEM detection rules
│   └── trivy/                            #   Container vulnerability scanning
│
├── infrastructure/                       # ── INFRASTRUCTURE AS CODE ──
│   ├── terraform/                        #   Cloud provisioning
│   ├── helm/                             #   Kubernetes Helm charts
│   └── ansible/                          #   Configuration management
│
├── monitoring/                           # ── OBSERVABILITY ──
│   ├── prometheus/                       #   Metric collection rules
│   ├── grafana/                          #   Dashboard definitions
│   ├── loki/                             #   Log aggregation config
│   └── alertmanager/                     #   Alert routing rules
│
├── docs/                                 # ── DOCUMENTATION ──
│   ├── ai-memory-architecture.md         #   8-Layer Memory System design
│   ├── architecture.md                   #   Clean architecture overview
│   ├── agents.md                         #   Agent system documentation
│   ├── deployment.md                     #   Deployment guide
│   ├── adr/                              #   Architecture Decision Records
│   ├── runbooks/                         #   Operational procedures
│   └── vault/                            #   Obsidian knowledge vault
│       ├── raw/                          #     Immutable source documents
│       ├── wiki/                         #     LLM-maintained compiled knowledge
│       │   ├── index.md                  #       Content catalog (first lookup)
│       │   ├── entities/                 #       One page per agent/service/tool
│       │   ├── concepts/                 #       Cross-cutting topics
│       │   ├── sources/                  #       Ingested source summaries
│       │   └── contradictions/           #       Flagged conflicts
│       └── SCHEMA.md                     #     Governance rules
│
├── agents/                               # Agent providers + router
├── models/                               # Model catalog + routing
│   ├── catalog.yaml                      #   40+ models across 12 providers
│   ├── routing.yaml                      #   Tier-based model selection
│   └── embeddings.yaml                   #   Embedding model configs
├── mcp/                                  # MCP gateway + registry
├── engines/                              # LLM engine configs (paid, free, local)
├── evals/                                # DeepEval + PromptFoo evaluation
├── compliance/                           # Regulatory frameworks
├── networks/                             # Service mesh, agent protocols
├── tools/                                # Tool catalog
├── scripts/                              # Bootstrap, deploy, verify
├── gitops/                               # ArgoCD + Kustomize overlays
└── starter-kit/                          # Standalone starter for new projects
```

---

## 🧠 8-Layer AI Memory Architecture

> Production-grade memory system that makes the AI feel persistent, context-aware, and stateful across sessions, users, and workflows. Full docs: [`docs/ai-memory-architecture.md`](docs/ai-memory-architecture.md)

### Memory Layer Summary

| # | Layer | Storage | Latency | What It Stores |
|---|-------|---------|---------|----------------|
| 1 | **Working** | In-process | <1ms | Current context window tokens, system prompt |
| 2 | **Short-Term** | Redis | 1-5ms | Recent conversation turns within a session |
| 3 | **Long-Term** | PostgreSQL (RLS) | 5-20ms | User preferences, facts, corrections across sessions |
| 4 | **Episodic** | PostgreSQL (partitioned) | 5-20ms | Timestamped interaction events, error logs, decisions |
| 5 | **Semantic** | pgvector (HNSW) | 10-50ms | Embedded knowledge chunks for RAG retrieval |
| 6 | **Procedural** | PostgreSQL | 5-20ms | Learned workflows, tool-call sequences, success rates |
| 7 | **Entity** | PostgreSQL + Neo4j | 5-50ms | Structured profiles: users, orgs, products, agents |
| 8 | **Shared** | Redis (pub/sub) | 1-5ms | Multi-agent state, distributed locks, broadcasts |

### System Architecture

```
                    ┌─────────────────────────────┐
                    │     USER / API CONSUMER      │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │     MEMORY ORCHESTRATOR      │
                    │  backbone/memory/            │
                    │  orchestrator.py             │
                    └──┬──┬──┬──┬──┬──┬──┬──┬─────┘
                       │  │  │  │  │  │  │  │
       ┌───────────────┘  │  │  │  │  │  │  └───────────────┐
       │           ┌──────┘  │  │  │  │  └──────┐           │
       ▼           ▼         ▼  ▼  ▼  ▼         ▼           ▼
  ┌─────────┐ ┌─────────┐ ┌────┐┌────┐┌────┐ ┌─────────┐ ┌──────��──┐
  │L1 WORK- │ │L2 SHORT │ │ L3 ││ L4 ││ L5 │ │L6 PROCE-│ │L7 ENTITY│
  │ING      │ │TERM     │ │LONG││EPIS││SEMA│ │DURAL    │ │         │
  │         │ │         │ │TERM││ODIC││NTIC│ │         │ │         │
  │In-proc  │ │Redis    │ │PG  ││PG  ││pgv │ │PG      │ │PG+Neo4j │
  └─────────┘ └─────────┘ └────┘└────┘└────┘ └─────────┘ └─────────┘
                                                           ┌─────────┐
                                                           │L8 SHARED│
                                                           │Redis    │
                                                           │pub/sub  │
                                                           └─────────┘
```

### Data Flow — Per Request

```
  PRE-INFERENCE (assemble context)
  ─────────────────────────────────────────────────────────────────
  Step 1  Working Memory    Load system prompt, allocate token budget
  Step 2  Entity Memory     Load user profile, inject as system context
  Step 3  Long-Term Memory  Query preferences, facts, corrections
  Step 4  Semantic Memory   RAG retrieval: embed query → search → rerank
  Step 5  Procedural Memory Find applicable workflows for this context
  Step 6  Episodic Memory   Load relevant past interactions
  Step 7  Shared Memory     Load multi-agent coordination state
  Step 8  Short-Term Memory Load recent conversation turns
  Step 9  Working Memory    Truncate all injections to fit context window

  INFERENCE
  ─────────────────────────────────────────────────────────────────
  Send assembled context → LLM → Receive response
  Guardrails validation (hallucination, PII, toxicity)

  POST-INFERENCE (write back)
  ─────────────────────────────────────────────────────────────────
  Step 1  Short-Term Memory Append user message + assistant response
  Step 2  Episodic Memory   Record conversation episode with timestamp
  Step 3  Long-Term Memory  Extract and store any new facts learned
  Step 4  Entity Memory     Update interaction count, last_seen, attributes
  Step 5  Procedural Memory If workflow completed, update success stats
  Step 6  Shared Memory     If multi-agent, broadcast state update
```

### Retrieval Strategy

| Query Type | Strategy | Memory Layer | Method |
|------------|----------|-------------|--------|
| Factual question about user | Structured query | Long-Term + Entity | Exact key lookup |
| Open-ended knowledge question | Vector search | Semantic | Embed → HNSW → Rerank |
| Mixed specific + general | Hybrid | Semantic | 70% vector + 30% keyword |
| Recall past interaction | Time-range query | Episodic | Temporal filter on event log |
| How to do something | Trigger match | Procedural | Pattern match on conditions |
| Multi-agent coordination | Namespace scan | Shared | Direct key-value in Redis |

### Multi-Agent Shared Memory

```
  Agent A (planner)
       │
       │  write task to shared namespace
       ▼
  ┌──────────────────────────────┐
  │  SHARED MEMORY (Redis)       │
  │  namespace: task-1           │
  │                              │
  │  Distributed Locks           │
  │  Optimistic Versioning       │
  │  Pub/Sub Broadcast           │
  └──────┬───────┬───────┬───────┘
         │       │       │
    notify  notify  notify
         │       │       │
         ▼       ▼       ▼
   Agent B  Agent C  Agent D
   (coder)  (tester) (reviewer)
       │       │       │
       └───────┼───────┘
               │
         write results back
               │
               ▼
  Shared Memory (conflict resolution)
  ─ last-writer-wins (non-critical)
  ─ merge (additive state)
  ─ reject (critical / locked)
  ─ version check (optimistic concurrency)
```

### Cost Model (~$95/mo baseline)

| Component | Purpose | Estimate |
|-----------|---------|----------|
| PostgreSQL (RDS t3.small) | L3 + L4 + L5 + L6 + L7 | ~$25/mo |
| Redis (ElastiCache t3.small) | L2 + L8 | ~$25/mo |
| Embeddings (text-embedding-3-small) | L5 ingestion | ~$0.10/mo |
| Reranking (Cohere Rerank v3) | L5 search quality | ~$20/mo |
| Storage (gp3 EBS) | All layers | ~$4/mo |
| **Total** | | **~$74/mo** |

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

## 🤖 All 500+ Agents — 30 Domains

<div align="center">

| # | Domain | Agents | Highlights |
|---|--------|--------|------------|
| 1 | 👔 **Executive & Strategy** | 18 | CEO Strategist, CTO Technology, OKR Tracker, Board Reporter, M&A Analyst, Investor Relations |
| 2 | 📈 **Marketing & Growth** | 28 | SEO, Content, Social, Email, PPC, PR, PLG, ABM, Podcast, Influencer, Events, Marketplace |
| 3 | 💰 **Sales & Revenue** | 24 | Lead Qualifier, Proposals, CRM, Forecast, Deal Desk, Enterprise AE, Channel Sales, SDR Coach |
| 4 | 🎯 **Customer Success** | 20 | Onboarding, Tickets, Churn Predictor, NPS, QBR, Health Score, Expansion, Advocacy |
| 5 | 🎨 **Product & UI/UX** | 26 | UI Designer, Wireframes, Design System, A11y, Micro-interactions, User Research, Analytics |
| 6 | ⚙️ **Engineering** | 35 | API, Models, Auth, Cache, Search, WebSocket, GraphQL, gRPC, Event Sourcing, CQRS, SDK |
| 7 | 🖥️ **Frontend** | 24 | Components, Pages, Forms, Charts, State, PWA, i18n, Micro-frontends, Web Perf, SSR |
| 8 | 📱 **Mobile Engineering** | 18 | React Native, Flutter, Native iOS, Native Android, Expo, OTA Updates, App Store, Deep Links |
| 9 | 🚀 **DevOps** | 34 | CI/CD, GitOps, K8s, Helm, Terraform, Canary, FinOps, Container, Registry, Secrets Rotation |
| 10 | 🔧 **SRE & Reliability** | 14 | SLO Manager, Error Budget, Incident Commander, Chaos Engineer, Capacity Planner, Postmortem |
| 11 | 🔒 **Security** | 28 | SAST, DAST, Secrets, Falco, Kyverno, Pentest, Zero Trust, SBOM, Threat Model, Red Team |
| 12 | 📊 **Data & Analytics** | 24 | Schema, ETL, Dashboards, Forecasting, Vector, Lakehouse, dbt, Data Quality, Lineage |
| 13 | 🧠 **ML Engineering** | 16 | Model Training, Feature Store, Experiment Tracker, Hyperparameter Tuner, Data Labeling, MLflow |
| 14 | 🧪 **QA & Testing** | 28 | Unit, E2E, Load, Chaos, Mutation, Visual, Contract, Property-based, Accessibility, API |
| 15 | 👥 **HR & People** | 16 | Jobs, Interviews, Onboarding, Performance, DEI, L&D, Culture, Workforce Planning |
| 16 | 💳 **Finance & Billing** | 20 | Stripe, Subscriptions, Tax, Revenue, Runway, FP&A, Treasury, Accounts Payable |
| 17 | ⚖️ **Legal & Governance** | 14 | ToS, DPA, GDPR, SOC2, SLA, AI Ethics, IP, Export Control, Contract Review |
| 18 | ✍️ **Content & Comms** | 16 | Tech Writing, Changelogs, Case Studies, Video Scripts, Podcasts, Internal Comms |
| 19 | 📦 **Supply Chain & Procurement** | 12 | Vendor Scoring, RFP Generator, Inventory Optimizer, Demand Forecast, Logistics |
| 20 | 🏗️ **Platform Engineering** | 12 | IDP Builder, Service Catalog, Golden Paths, Developer Portal, Backstage, Scaffolder |
| 21 | 🌐 **Internationalization** | 10 | i18n Manager, Locale Sync, RTL Adapter, Currency Converter, Translation QA, Geo Routing |
| 22 | 🤖 **AI/ML Operations** | 16 | Model Registry, Serving, Drift Detection, Prompt Optimizer, Eval Runner, Cost Tracker |
| 23 | 📡 **IoT & Edge** | 10 | Device Manager, Telemetry Collector, Edge Deployer, OTA Updater, Fleet Monitor, Protocol |
| 24 | 🎓 **Education & Training** | 8 | Course Builder, Quiz Generator, Skill Assessor, Learning Path, Cert Tracker, Lab Runner |
| 25 | 🏥 **Compliance & Risk** | 12 | Risk Scorer, Audit Trail, Policy Enforcer, Incident Reporter, Vendor Risk, SOX Compliance |
| 26 | 🎨 **Brand & Creative** | 10 | Brand Identity, Visual Language, Creative Director, Asset Library, Style Guide, Logo System |
| 27 | 💹 **Revenue Operations** | 12 | Pipeline Analytics, Territory Design, Compensation Plans, CRM Hygiene, Attribution, Quota |
| 28 | 📚 **Documentation & Knowledge** | 10 | API Docs, Runbook Writer, Architecture Docs, Onboarding Guides, Knowledge Base, ADR Writer |
| 29 | 🛠️ **Developer Experience** | 10 | DX Tooling, Internal SDK, CLI Builder, Dev Onboarding, Sandbox Manager, API Playground |
| 30 | 🔬 **Research & Intelligence** | 10 | Market Research, Competitive Analysis, Tech Radar, Patent Monitor, Trend Forecaster, Benchmarker |

</div>

> **Total: 535 agents across 30 domains.** Each domain has distinct, non-overlapping responsibilities. See [`.claude/agents/_registry.yaml`](.claude/agents/_registry.yaml) for the full registry with IDs, models, and entrypoints.

<details>
<summary><b>📋 View all 500+ agents with IDs and descriptions (first 3 domains shown)</b></summary>

### 👔 Domain 1: Executive & Strategy (18 Agents)

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
| 13 | `exec-ma-analyst` | M&A Analyst | Acquisition targets, due diligence checklists, valuation modeling, synergy analysis |
| 14 | `exec-investor-relations` | Investor Relations | Investor communications, quarterly earnings, cap table management |
| 15 | `exec-strategic-partnerships` | Strategic Partnerships | Partnership pipeline, joint ventures, ecosystem mapping, co-sell programs |
| 16 | `exec-risk-officer` | Chief Risk Officer | Enterprise risk assessment, risk register, mitigation planning |
| 17 | `exec-culture-architect` | Culture Architect | Values alignment, culture metrics, engagement programs, eNPS tracking |
| 18 | `exec-transformation` | Digital Transformation | Transformation roadmaps, change management, innovation pipeline |

### 📈 Domain 2: Marketing & Growth (28 Agents)

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
| 23 | `mktg-plg-specialist` | PLG Specialist | Product-led growth funnels, activation metrics, self-serve optimization |
| 24 | `mktg-abm-strategist` | ABM Strategist | Account-based marketing, target account lists, personalized campaigns |
| 25 | `mktg-event-coordinator` | Event Coordinator | Event planning, sponsorship management, conference strategy |
| 26 | `mktg-creative-director` | Creative Director | Creative briefs, visual campaign direction, ad creative review |
| 27 | `mktg-marketplace` | Marketplace Manager | Listing optimization, marketplace SEO, multi-channel selling |
| 28 | `mktg-partnerships` | Partnership Marketing | Co-marketing campaigns, partner content, joint webinars |

### 💰 Domain 3: Sales & Revenue (24 Agents)

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
| 19 | `sales-revops-analyst` | RevOps Analyst | Pipeline analytics, revenue attribution, sales efficiency metrics |
| 20 | `sales-deal-desk` | Deal Desk Manager | Deal structuring, discount approvals, non-standard contract negotiations |
| 21 | `sales-enablement` | Sales Enablement | Training content, playbooks, competitive battle cards, onboarding |
| 22 | `sales-channel` | Channel Sales | Partner recruitment, channel strategy, reseller programs, co-sell |
| 23 | `sales-enterprise` | Enterprise AE | Enterprise account strategy, multi-threaded selling, procurement navigation |
| 24 | `sales-sdr-coach` | SDR Coach | Outreach coaching, sequence optimization, meeting conversion analytics |

### 🎯 Domains 4–30: See [`.claude/agents/_registry.yaml`](.claude/agents/_registry.yaml) for the complete registry with all 500+ agents

</details>

---

## 📖 LLM Wiki — Brain Memory

> Citadel's agent fleet uses the LLM Wiki pattern as persistent brain memory. Knowledge **compounds** across all 500+ agents — every ingest adds, every query answer is filed back.

> [!NOTE]
> **Why not RAG?** The LLM Wiki treats knowledge like code compilation. The LLM reads sources, extracts key info, and integrates it into the wiki — updating entities, revising summaries, noting contradictions. Unlike RAG, knowledge compounds instead of being re-retrieved from scratch every session.

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

## 🔧 Master System — 26 Autonomous Engineering Plugins

> Production-grade plugin system that transforms Claude Code into a full-stack autonomous engineering, DevSecOps, and SaaS factory operator. Located at `.claude/skills/master-system/`.

### Plugin Registry

| # | Plugin | Skill ID | Purpose |
|---|--------|----------|---------|
| 1 | No Gatekeeping | `ms-no-gatekeeping` | Complete implementation guidance — no vague summaries |
| 2 | Real-World Execution | `ms-real-world-execution` | Production-oriented, operationally realistic outputs |
| 3 | Multi-Domain Validation | `ms-multi-domain-validation` | Cross-domain validation (arch, security, DevOps, SRE, cost) |
| 4 | Tool-First Execution | `ms-tool-first-execution` | Prioritize MCP tools and runtime context over assumptions |
| 5 | Execution-Ready Output | `ms-execution-ready-output` | Standardized response format with all artifacts |
| 6 | Security-First | `ms-security-first` | Zero trust, least privilege, OWASP Top 10, threat modeling |
| 7 | Autonomous Agents | `ms-autonomous-agents` | 13 agent archetypes with scoped permissions |
| 8 | MCP Ecosystem | `ms-mcp-ecosystem` | Orchestrate 40+ MCP servers across domains |
| 9 | SaaS Factory | `ms-saas-factory` | End-to-end SaaS business generation |
| 10 | Engineering Standards | `ms-engineering-standards` | Backend, frontend, infrastructure, database standards |
| 11 | Observability | `ms-observability` | OpenTelemetry + Prometheus + Grafana + Loki + Tempo |
| 12 | Agent Safety | `ms-agent-safety` | Safety controls, circuit breakers, approval gates |
| 13 | Context Engineering | `ms-context-engineering` | Long-term memory, ADRs, decision logs, changelogs |
| 14 | Response Quality | `ms-response-quality` | Pre-response validation checklist |
| 15 | Folder Structure | `ms-folder-structure` | Default project organization template |
| 16 | New Project Outputs | `ms-new-project-outputs` | 13 required artifacts for new systems |
| 17 | CI/CD Standards | `ms-cicd-standards` | Pipeline stages, tooling, approval gates |
| 18 | Cloud Security | `ms-cloud-security` | AWS/Azure/GCP security baseline |
| 19 | Execution Priority | `ms-execution-priority` | Security > stability > reliability > ... > velocity |
| 20 | Failure Handling | `ms-failure-handling` | Retry, circuit breakers, DLQ, rollback |
| 21 | Business Awareness | `ms-business-awareness` | ROI, cost, vendor lock-in, monetization |
| 22 | Self-Check | `ms-self-check` | Final validation before every response |
| 23 | Plugin Execution | `ms-plugin-execution` | Claude Code plugin safety protocol |
| 24 | SaaS Business Mode | `ms-saas-business` | Billing, CRM, analytics, onboarding, support |
| 25 | Enterprise Docs | `ms-enterprise-docs` | Auto-generated ADRs, runbooks, SOPs, compliance |
| 26 | Never Operate Blindly | `ms-never-blind` | Verified state over assumptions |

### Usage

```bash
# Activate the full system
/master-system

# Use individual plugins
/ms-security-first
/ms-saas-factory
/ms-cicd-standards

# Composite workflows
# New Project:  ms-folder-structure -> ms-new-project-outputs -> ms-cicd-standards -> ms-security-first
# Security Audit: ms-security-first -> ms-cloud-security -> ms-self-check
# SaaS Launch:  ms-saas-factory -> ms-saas-business -> ms-observability -> ms-enterprise-docs
```

### Execution Priority Order

Every autonomous decision follows this strict priority:

```
1. SECURITY           (non-negotiable)
2. STABILITY
3. RELIABILITY
4. OBSERVABILITY
5. MAINTAINABILITY
6. SCALABILITY
7. PERFORMANCE
8. COST OPTIMIZATION
9. FEATURE VELOCITY
```

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

<div align="center">

## 👤 Author

**Kehinde Ogunlowo**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kehinde-ogunlowo/)
[![Architecture](https://img.shields.io/badge/Architecture_Diagram-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://citadelcloudmanagement.com/architecture-diagram/)
[![Sponsor](https://img.shields.io/badge/❤️_Sponsor_via_Cash_App-00C853?style=for-the-badge&logo=cashapp&logoColor=white)](https://cash.app/$KennyOgunlowo)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for full terms.

Copyright (c) Citadel Cloud Management

---

**Citadel Cloud Management** | [citadelcloudmanagement.com](https://citadelcloudmanagement.com)

</div>
