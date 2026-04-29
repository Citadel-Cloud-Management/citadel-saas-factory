---
name: ms-mcp-ecosystem
description: MCP tool ecosystem orchestration — GitHub, Jira, Linear, Notion, AWS, Azure, GCP, Kubernetes, Docker, PostgreSQL, Redis, Supabase, Pinecone, Grafana, Prometheus, Vault, Stripe, PostHog, Slack, and 40+ integrations.
type: framework
priority: 8
---

# MCP Tool Ecosystem

## Core Rule

Use MCP server integrations whenever operationally beneficial. Prefer live system queries over assumptions.

## Available MCP Servers by Category

### Source Control
| Server | Capabilities |
|--------|-------------|
| GitHub | Repos, PRs, issues, Actions, code search, releases |
| GitLab | MRs, pipelines, registries, wikis |
| Bitbucket | PRs, pipelines, deployments |

### Project Management
| Server | Capabilities |
|--------|-------------|
| Jira | Issues, sprints, boards, workflows |
| Linear | Issues, cycles, projects, roadmaps |
| Notion | Pages, databases, kanban, docs |
| Confluence | Spaces, pages, templates, search |

### Cloud Providers
| Server | Capabilities |
|--------|-------------|
| AWS | EC2, S3, RDS, Lambda, IAM, CloudFormation |
| Azure | VMs, Storage, SQL, Functions, AD, ARM |
| GCP | Compute, GCS, Cloud SQL, Functions, IAM |
| Cloudflare | Workers, D1, R2, KV, DNS, WAF |

### Infrastructure
| Server | Capabilities |
|--------|-------------|
| Kubernetes | Pods, services, deployments, configmaps |
| Docker | Containers, images, networks, volumes |
| Terraform | State, plans, applies, workspaces |
| Helm | Charts, releases, repositories |

### Databases
| Server | Capabilities |
|--------|-------------|
| PostgreSQL | Queries, schemas, migrations, stats |
| MySQL | Queries, schemas, procedures |
| MongoDB | Collections, aggregations, indexes |
| Redis | Keys, streams, pub/sub, cluster |
| Supabase | Tables, RPC, auth, realtime, storage |

### AI & Memory
| Server | Capabilities |
|--------|-------------|
| Pinecone | Vectors, namespaces, indexes |
| Qdrant | Collections, search, filtering |
| Weaviate | Classes, objects, search |
| Chroma | Collections, embeddings, queries |
| Mem0 | Memory store, retrieval, context |

### Monitoring
| Server | Capabilities |
|--------|-------------|
| Grafana | Dashboards, panels, alerts |
| Prometheus | Metrics, queries, rules, alerts |
| Datadog | Metrics, traces, logs, monitors |
| New Relic | APM, infrastructure, synthetics |
| Sentry | Errors, performance, releases |

### Security
| Server | Capabilities |
|--------|-------------|
| Vault | Secrets, policies, auth methods |
| Wiz | Vulnerabilities, compliance, CSPM |
| Okta | Users, groups, applications, policies |
| Auth0 | Tenants, connections, rules |

### Communications
| Server | Capabilities |
|--------|-------------|
| Slack | Messages, channels, threads, reactions |
| Discord | Messages, channels, roles |
| Gmail | Messages, drafts, labels, threads |
| Outlook | Mail, calendar, contacts |

### Payments & Analytics
| Server | Capabilities |
|--------|-------------|
| Stripe | Customers, subscriptions, payments |
| PostHog | Events, feature flags, experiments |
| HubSpot | Contacts, deals, tickets, marketing |
| Segment | Sources, destinations, events |

## Orchestration Patterns

### Query Before Acting
```
1. MCP query current state
2. Compare with desired state
3. Generate minimal change set
4. Apply changes
5. MCP verify final state
```

### Cross-System Coordination
```
GitHub (PR merged) → Jira (move to Done) → Slack (notify team) → ArgoCD (deploy)
```

### State Verification
```
Before deployment:
  - GitHub: branch is clean, CI passed
  - K8s: cluster healthy, pods running
  - Vault: secrets accessible
  - Monitoring: no active alerts
```
