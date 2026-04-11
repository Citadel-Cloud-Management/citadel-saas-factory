# Citadel SaaS Factory

**Universal Full-Stack SaaS Production Framework — 265 Autonomous Business Agents**

Clone. Configure. Deploy. Any infrastructure. Zero software cost.

---

## Quick Start

```bash
git clone https://github.com/kogunlowo123/citadel-saas-factory.git
cd citadel-saas-factory
pip install graphifyy && graphify install
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash
./scripts/bootstrap.sh
claude
```

---

## What's Inside

265 specialized autonomous agents across 15 business domains:

| Domain | Agents | Covers |
|--------|--------|--------|
| Executive & Strategy | 12 | CEO, COO, CFO, CTO, CMO, CPO, OKRs, board reports |
| Marketing & Growth | 22 | SEO, content, social, email, PPC, PR, influencer, A/B |
| Sales & Revenue | 18 | Lead qual, outbound, proposals, CRM, forecasting |
| Customer Success | 15 | Onboarding, tickets, churn prediction, NPS, renewals |
| Product & UI/UX | 20 | UI, UX research, wireframes, design system, a11y |
| Engineering | 25 | API, models, auth, cache, search, WebSocket, GraphQL |
| Frontend | 18 | React, Next.js, forms, charts, state, PWA |
| DevOps | 28 | CI/CD, GitOps, K8s, Helm, Terraform, canary deploys |
| Security | 22 | SAST, DAST, secrets, runtime, compliance, pentest |
| Data & Analytics | 18 | Schema, ETL, dashboards, forecasting, vector search |
| QA & Testing | 22 | Unit, E2E, load, chaos, mutation, visual regression |
| HR & People | 12 | Jobs, interviews, onboarding, performance reviews |
| Finance & Billing | 15 | Stripe, subscriptions, tax, revenue recognition |
| Legal & Governance | 8 | ToS, DPA, GDPR, SOC2, SLA |
| Content & Comms | 10 | Tech writing, docs, changelogs, case studies |

---

## Architecture

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.12) |
| Frontend | Next.js 14 (TypeScript) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Auth | Keycloak 24 |
| Storage | MinIO (S3-compatible) |
| Messaging | RabbitMQ |
| Orchestration | K3s + ArgoCD |
| Reverse Proxy | Traefik |
| Service Mesh | Linkerd |
| Secrets | HashiCorp Vault |
| Monitoring | Prometheus + Grafana + Loki |

---

## Infrastructure Agnostic

Runs on any Linux server with SSH and Docker. No cloud vendor lock-in.

- Any VPS provider (Hetzner, DigitalOcean, Linode, Vultr)
- Bare metal servers
- On-premises infrastructure
- Edge deployments
- Home lab

---

## Key Tools

**Ruflo** — Multi-agent swarm orchestration with 314 MCP tools. Hive-mind intelligence, self-learning neural routing. [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)

**Graphify** — Turn any codebase into a queryable knowledge graph. 20 languages via Tree-sitter AST. [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)

**Free Toolchain** — ArgoCD, K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy, ZAP, Flagsmith, Grafana OnCall, Velero, MinIO, Ansible. Total: $0/month.

---

## Repository Structure

```
citadel-saas-factory/
  .claude/
    CLAUDE.md                    Master intelligence file
    memory/                      Project context, ADRs, learnings
    agents/                      265 agent definitions (15 domains)
    hooks/                       10 lifecycle hooks
    rules/                       18 governance rules
    commands/                    20 slash commands
    templates/                   20 code generation templates
    skills/                      15 reusable skills
    mcp/                         8 MCP server configs
  backend/                       FastAPI application
  frontend/                      Next.js application
  infrastructure/
    terraform/                   Cloud-agnostic modules
    ansible/                     Server provisioning
    helm/                        Kubernetes charts
  gitops/
    base/                        Kustomize base manifests
    overlays/                    Staging + production
  security/                      Kyverno, Falco, SIGMA, OPA, Trivy
  monitoring/                    Grafana, Prometheus, Alertmanager, Loki
  docs/                          MkDocs documentation site
  scripts/                       Bootstrap, deploy, rollback
  .github/                       CI/CD, templates, CODEOWNERS
```

---

## Installation

Only 2 tokens required:

1. **Anthropic API Key** — [console.anthropic.com](https://console.anthropic.com) (powers Claude Code, Ruflo, and Graphify)
2. **GitHub PAT** — [github.com/settings/tokens](https://github.com/settings/tokens) (powers GitHub CLI, GHCR, Actions)

```bash
cp .env.example .env
# Edit .env with your tokens
```

See the full 10-step installation guide in `docs/installation.md`.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests first (TDD)
4. Ensure 80%+ coverage
5. Run security scan: `make security`
6. Commit with conventional format: `feat: add user auth`
7. Open a pull request

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Citadel Cloud Management | [kogunlowo123](https://github.com/kogunlowo123) | [citadelcloudmanagement.com](https://citadelcloudmanagement.com)
