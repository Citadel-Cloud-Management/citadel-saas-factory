# Agent System

Overview of the 265 autonomous business agents powering Citadel SaaS Factory.

## What Are Agents?

Each agent is a specialized autonomous unit responsible for a specific business function. Agents operate independently, communicate through RabbitMQ events, and persist their state in PostgreSQL. Together, they form a complete SaaS operations layer that handles everything from marketing to security compliance.

## Architecture

```
Agent Registry (agents/_registry.yaml)
       |
       v
Agent Orchestrator
  |-- Schedules agent runs based on configuration
  |-- Routes events between agents via RabbitMQ
  |-- Monitors agent health and retries on failure
  |
  +-- Agent Instance
        |-- Reads configuration from registry
        |-- Executes domain-specific logic
        |-- Publishes results as events
        |-- Persists state to PostgreSQL
```

### CYCLE_INTERVAL=0

By default, `CYCLE_INTERVAL=0` means agents run **on-demand** rather than on a polling loop. This is the recommended mode for development and cost-sensitive deployments.

- Agents are triggered by events, API calls, or manual invocation
- No idle CPU consumption from continuous polling
- Set `CYCLE_INTERVAL=300` (seconds) for autonomous continuous operation
- Each agent respects its own interval override if defined in the registry

## 15 Domains, 265 Agents

| Domain | Agent Count | Description |
|--------|------------|-------------|
| Executive and Strategy | 12 | High-level business strategy, OKR tracking, board reporting |
| Marketing and Growth | 22 | SEO, content marketing, social media, email campaigns, PPC, PR |
| Sales and Revenue | 18 | Lead qualification, proposal generation, CRM management, forecasting |
| Customer Success | 15 | Onboarding flows, ticket management, churn prediction, NPS tracking |
| Product and UI/UX | 20 | UI design, wireframing, design system management, accessibility |
| Engineering | 25 | API development, data models, auth, caching, search, WebSocket |
| Frontend | 18 | Component library, pages, forms, charts, state management, PWA |
| DevOps | 28 | CI/CD, GitOps, Kubernetes, Helm charts, Terraform, canary deploys |
| Security | 22 | SAST, DAST, secret scanning, Falco rules, Kyverno policies, pentesting |
| Data and Analytics | 18 | Schema design, ETL pipelines, dashboards, forecasting, vector search |
| QA and Testing | 22 | Unit tests, E2E tests, load testing, chaos engineering, mutation testing |
| HR and People | 12 | Job postings, interview scheduling, onboarding, performance reviews |
| Finance and Billing | 15 | Stripe integration, subscriptions, tax calculation, revenue tracking |
| Legal and Governance | 8 | Terms of Service, DPA, GDPR compliance, SOC2 preparation, SLA management |
| Content and Communications | 10 | Technical writing, documentation, changelogs, case studies |

## Agent Registry

All agents are defined in `agents/_registry.yaml`. Each entry includes:

```yaml
- id: marketing-seo-optimizer
  domain: marketing
  name: SEO Optimizer
  description: Analyzes and optimizes content for search engine visibility
  trigger: event  # event | schedule | manual
  cycle_interval: 0  # seconds (0 = on-demand)
  dependencies:
    - marketing-content-writer
    - data-analytics-dashboard
  inputs:
    - content_url
    - target_keywords
  outputs:
    - seo_score
    - optimization_recommendations
```

## How Agents Work

### 1. Trigger

An agent is activated by one of three mechanisms:

- **Event**: Another agent publishes a RabbitMQ event that this agent subscribes to
- **Schedule**: A cron-like interval triggers the agent periodically (when `CYCLE_INTERVAL > 0`)
- **Manual**: A user or API call invokes the agent directly

### 2. Execute

The agent:

1. Reads its configuration from the registry
2. Fetches required inputs (from database, API, or event payload)
3. Executes its domain-specific logic
4. Validates outputs against its schema

### 3. Publish

After execution, the agent:

1. Persists results to PostgreSQL
2. Publishes completion events to RabbitMQ
3. Updates its health status in the registry
4. Logs execution metrics (duration, success/failure, output size)

## Agent Communication

Agents communicate through a publish/subscribe model via RabbitMQ:

```
Agent A (SEO Optimizer)
  --> publishes: content.seo.optimized
       |
       +--> Agent B (Content Writer) subscribes: content.seo.*
       +--> Agent C (Analytics Dashboard) subscribes: content.*
```

### Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "content.seo.optimized",
  "source_agent": "marketing-seo-optimizer",
  "timestamp": "2026-04-11T10:00:00Z",
  "tenant_id": "uuid",
  "payload": {
    "content_url": "https://...",
    "seo_score": 92,
    "recommendations": []
  }
}
```

## Running Agents

### Single Agent

```bash
python -m agents.run --agent ceo-strategist
```

### Entire Domain

```bash
python -m agents.run --domain marketing
```

### All Agents (Continuous Mode)

```bash
CYCLE_INTERVAL=300 python -m agents.run --all
```

### List All Agents

```bash
python -m agents.registry --list
python -m agents.registry --list --domain security
```

## Tool Integrations

Agents leverage external tool integrations for enhanced capabilities:

| Tool | Purpose | Agents Using It |
|------|---------|-----------------|
| Ruflo | Multi-agent swarm orchestration (314 MCP tools) | All agents (mesh topology) |
| Graphify | Codebase knowledge graph (Tree-sitter AST) | Engineering, Frontend, QA |
| GitHub Actions | CI/CD with security gates | DevOps, Security, QA |
| Semgrep | Static analysis (SAST) | Security agents |
| Trivy | Container vulnerability scanning | DevOps, Security agents |

## Monitoring Agents

Agent health and performance are tracked through:

- **Prometheus metrics**: Execution count, duration, error rate per agent
- **Grafana dashboards**: Per-domain and per-agent views
- **Alerting**: Alerts fire when agent error rate exceeds 5% or execution time exceeds SLA
- **Logs**: Structured JSON logs with agent ID, execution ID, and correlation ID via Loki

## Adding a New Agent

1. Add the agent definition to `agents/_registry.yaml`
2. Create the agent module under `agents/{domain}/{agent_name}.py`
3. Implement the `BaseAgent` interface: `execute()`, `validate_output()`
4. Define input/output schemas using Pydantic models
5. Write unit tests in `tests/agents/{domain}/test_{agent_name}.py`
6. Register event subscriptions in the agent's `subscriptions` config
7. Run `python -m agents.registry --validate` to verify the registry
