---
name: ms-autonomous-agents
description: Autonomous agent operating model — create and coordinate specialized agents (Backend, Frontend, DevOps, SecOps, IAM, Infrastructure, AI, QA, Docs, Data, SRE, Product, Growth). Each with scoped permissions and audit trails.
type: framework
priority: 7
---

# Autonomous Agent Operating Model

## Core Rule

You may create and coordinate specialized agents to parallelize complex tasks. Each agent operates within strict boundaries with least privilege and produces auditable outputs.

## Available Agent Archetypes

| Agent | Responsibility | Model Tier | Permissions |
|-------|---------------|------------|-------------|
| Backend Agent | API design, business logic, data models | Sonnet | Read/Write backend/ |
| Frontend Agent | UI components, state, routing, UX | Sonnet | Read/Write frontend/ |
| DevOps Agent | CI/CD, containers, IaC, deployment | Sonnet | Read/Write infra/ |
| SecOps Agent | Security scanning, policy, threat modeling | Sonnet | Read all, Write security/ |
| IAM Agent | Auth, RBAC, identity, access policies | Sonnet | Read/Write auth/ |
| Infrastructure Agent | Cloud resources, networking, compute | Sonnet | Read/Write infrastructure/ |
| AI Agent | ML models, embeddings, prompts, evals | Opus | Read/Write ai/ |
| QA Agent | Testing, coverage, E2E, load testing | Sonnet | Read all, Write tests/ |
| Documentation Agent | ADRs, runbooks, API docs, guides | Haiku | Read all, Write docs/ |
| Data Engineering Agent | Pipelines, ETL, schemas, migrations | Sonnet | Read/Write data/ |
| SRE Agent | Reliability, incident response, SLOs | Sonnet | Read all, Write monitoring/ |
| Product Strategy Agent | PRDs, roadmaps, user research | Haiku | Read all, Write docs/product/ |
| Growth Automation Agent | Marketing, onboarding, analytics | Haiku | Read all, Write growth/ |

## Agent Requirements

Each spawned agent MUST:

1. **Have clear responsibilities** — single domain, defined scope
2. **Operate within scoped permissions** — cannot access outside its domain
3. **Use least privilege** — minimum tools needed for the task
4. **Produce auditable outputs** — log all decisions and actions
5. **Report dependencies and blockers** — surface integration points

## Agent Coordination Patterns

### Parallel Execution (Independent Tasks)
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Backend     │  │ Frontend    │  │ DevOps      │
│ Agent       │  │ Agent       │  │ Agent       │
│ (API impl)  │  │ (UI impl)   │  │ (CI/CD)     │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                  ┌─────────────┐
                  │ Orchestrator│
                  │ (merge)     │
                  └─────────────┘
```

### Sequential Execution (Dependencies)
```
SecOps Agent (threat model) 
    → Backend Agent (implement with security controls)
        → QA Agent (security + functional tests)
            → DevOps Agent (deploy with gates)
```

### Multi-Perspective Review
```
┌──────────────────┐
│ Code Change      │
└────────┬─────────┘
         │
    ┌────┼────┬────────┬──────────┐
    │    │    │        │          │
    ▼    ▼    ▼        ▼          ▼
  Func  Sec  Perf   Consist   Redundancy
  Rev   Rev  Rev    Rev       Rev
    │    │    │        │          │
    └────┼────┴────────┴──────────┘
         │
    ┌────▼────┐
    │ Merged  │
    │ Review  │
    └─────────┘
```

## Agent Spawn Template

```yaml
agent:
  type: <archetype>
  task: <specific objective>
  scope:
    read: [<allowed read paths>]
    write: [<allowed write paths>]
  constraints:
    - <constraint 1>
    - <constraint 2>
  success_criteria:
    - <measurable outcome>
  timeout: <max duration>
```

## Safety Rules

- Agents CANNOT deploy to production without human approval
- Agents CANNOT modify IAM/RBAC without explicit authorization
- Agents MUST log all file modifications
- Agents CANNOT disable tests or security checks
- Failed agent tasks trigger escalation, not retry loops
