---
name: master-system
description: Master autonomous engineering system — orchestrates 26 production-grade plugins covering architecture, security, DevSecOps, SaaS factory, and full-stack execution. Invoke when starting new projects, auditing systems, or running autonomous engineering workflows.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch]
---

# Master Autonomous Engineering System

> 26 production-grade plugins for full-stack autonomous engineering, DevSecOps, and SaaS factory operations.

## Plugin Registry

| # | Plugin | Skill ID | Purpose |
|---|--------|----------|---------|
| 1 | No Gatekeeping | `ms-no-gatekeeping` | Complete implementation guidance — no vague summaries |
| 2 | Real-World Execution | `ms-real-world-execution` | Production-oriented, operationally realistic outputs |
| 3 | Multi-Domain Validation | `ms-multi-domain-validation` | Cross-domain validation before producing results |
| 4 | Tool-First Execution | `ms-tool-first-execution` | Prioritize MCP tools, repos, runtime context |
| 5 | Execution-Ready Output | `ms-execution-ready-output` | Standardized response format with all artifacts |
| 6 | Security-First Engineering | `ms-security-first` | Zero trust, least privilege, threat modeling |
| 7 | Autonomous Agent Model | `ms-autonomous-agents` | Create and coordinate specialized agents |
| 8 | MCP Tool Ecosystem | `ms-mcp-ecosystem` | Orchestrate MCP servers across domains |
| 9 | SaaS Factory Mode | `ms-saas-factory` | End-to-end SaaS business generation |
| 10 | Engineering Standards | `ms-engineering-standards` | Backend, frontend, infra, DB standards |
| 11 | Observability | `ms-observability` | Logging, tracing, metrics, alerting |
| 12 | AI Agent Safety | `ms-agent-safety` | Safety controls for autonomous agents |
| 13 | Context Engineering | `ms-context-engineering` | Long-term memory, ADRs, decision logs |
| 14 | Response Quality | `ms-response-quality` | Final quality requirements for all outputs |
| 15 | Folder Structure | `ms-folder-structure` | Default project organization |
| 16 | New Project Outputs | `ms-new-project-outputs` | Required artifacts for new systems |
| 17 | CI/CD Standards | `ms-cicd-standards` | Pipeline stages, tooling, gates |
| 18 | Cloud Security | `ms-cloud-security` | AWS/Azure/GCP security requirements |
| 19 | Execution Priority | `ms-execution-priority` | Priority order for autonomous decisions |
| 20 | Failure Handling | `ms-failure-handling` | Retry, circuit breakers, rollback |
| 21 | Business Awareness | `ms-business-awareness` | ROI, cost, vendor lock-in, monetization |
| 22 | Self-Check | `ms-self-check` | Pre-response validation checklist |
| 23 | Plugin Execution Rules | `ms-plugin-execution` | Claude Code plugin safety rules |
| 24 | SaaS Business Mode | `ms-saas-business` | Autonomous SaaS business capabilities |
| 25 | Enterprise Documentation | `ms-enterprise-docs` | Auto-generated documentation standards |
| 26 | Never Operate Blindly | `ms-never-blind` | Verified state over assumptions |

## How to Use

Invoke individual plugins by skill ID, or invoke `master-system` to load the full orchestration layer.

### Full System Activation
```
/master-system
```

### Individual Plugin
```
/ms-security-first
/ms-saas-factory
/ms-cicd-standards
```

### Composite Workflows
- **New Project**: `ms-folder-structure` → `ms-new-project-outputs` → `ms-cicd-standards` → `ms-security-first`
- **Security Audit**: `ms-security-first` → `ms-cloud-security` → `ms-self-check`
- **SaaS Launch**: `ms-saas-factory` → `ms-saas-business` → `ms-observability` → `ms-enterprise-docs`
- **Code Review**: `ms-engineering-standards` → `ms-multi-domain-validation` → `ms-response-quality`

## Execution Model

When `master-system` is invoked, all 26 plugins are activated as the operating context. Every response thereafter is validated against:

1. Security-first (plugin 6)
2. Multi-domain validation (plugin 3)
3. Self-check (plugin 22)
4. Never operate blindly (plugin 26)

## Vault Links

- [[../../rules/architecture|Architecture Rules]]
- [[../../rules/security|Security Rules]]
- [[../../rules/testing|Testing Rules]]
- [[../../rules/guardrails|Guardrails Rules]]
- [[../../rules/devops|DevOps Rules]]
- [[../../rules/monitoring|Monitoring Rules]]
