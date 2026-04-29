---
name: ms-execution-ready-output
description: Standardized response format for all technical outputs — includes objective, assumptions, architecture, implementation, infrastructure, security, CI/CD, observability, risks, rollback, scaling, cost, and future improvements.
type: template
priority: 5
---

# Execution-Ready Output Format

## Core Rule

All technical responses follow a structured format that ensures completeness and actionability.

## Default Response Template

```markdown
## Objective
<What we're building/fixing/deploying and why>

## Assumptions
<What we're assuming about the environment, constraints, and requirements>

## Architecture
<System design, component diagram, data flow>

## Implementation Steps
<Numbered, executable steps with actual code/commands>

## Folder Structure
<Tree diagram of files created/modified>

## Infrastructure
<Terraform, Helm, K8s manifests, Docker configs>

## Security Controls
<Auth, encryption, secrets, RBAC, network policies>

## CI/CD
<Pipeline definition, stages, gates, deployment strategy>

## Observability
<Logging, metrics, tracing, dashboards, alerts>

## Risks
<Known risks, mitigations, unresolved concerns>

## Rollback Plan
<How to revert if something goes wrong>

## Scaling Strategy
<Horizontal/vertical scaling, bottlenecks, capacity planning>

## Cost Considerations
<Estimated costs, optimization opportunities>

## Future Improvements
<What to do next, tech debt created, enhancement opportunities>
```

## Section Usage Rules

| Context | Required Sections | Optional Sections |
|---------|-------------------|-------------------|
| New feature | All | — |
| Bug fix | Objective, Assumptions, Implementation, Risks, Rollback | Others as relevant |
| Architecture review | Objective, Architecture, Security, Scaling, Risks | Implementation |
| Security audit | Objective, Security Controls, Risks, Rollback | Others |
| Infrastructure change | All except Frontend-specific | — |
| Quick utility | Objective, Implementation, Folder Structure | Others as needed |

## Code Artifact Requirements

When including code, always provide:

- **Terraform** — for infrastructure resources
- **Helm values** — for K8s deployments
- **Kubernetes YAML** — for custom resources, CRDs
- **Dockerfiles** — for containerized services
- **GitHub Actions** — for CI/CD pipelines
- **Shell scripts** — for automation, deployment, setup
- **Python/TypeScript** — for application code
- **SQL migrations** — for schema changes
- **API schemas** — OpenAPI/JSON Schema
- **IAM policies** — for cloud permissions
- **Threat models** — for security-critical systems

## Quality Bar

Every output section must be:
- Copy-pasteable (commands work as-is)
- Environment-aware (uses variables, not hardcoded values)
- Idempotent where possible
- Documented with inline comments for non-obvious logic
