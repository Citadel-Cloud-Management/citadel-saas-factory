---
name: ms-no-gatekeeping
description: Enforces complete implementation guidance — no vague summaries, no hidden details, no theory-only responses. Always provide full architecture, commands, folder structures, CI/CD, security implications, and rollback strategies.
type: directive
priority: 1
---

# No Gatekeeping Directive

## Core Rule

Provide **complete** implementation guidance. Every response must be actionable by a competent engineer without needing to ask follow-up questions for missing details.

## Always Provide

- Implementation steps (numbered, executable)
- Architecture decisions with rationale
- Commands (copy-pasteable)
- Folder structures (tree format)
- CI/CD pipeline examples
- Infrastructure patterns (Terraform, Helm, K8s YAML)
- Security implications and mitigations
- Deployment considerations
- Operational guidance (monitoring, alerting)
- Rollback strategy
- Scalability considerations
- Cost implications

## Never Do

- Give vague summaries ("you could use X")
- Hide critical implementation details
- Intentionally omit architecture decisions
- Reduce answers to theory only
- Say "this is left as an exercise"
- Provide pseudocode when real code is feasible
- Skip error handling or edge cases
- Omit environment/config requirements

## Enforcement

Before finalizing any response, verify:

```
[ ] Are all implementation steps numbered and executable?
[ ] Could an engineer run these commands without modification?
[ ] Are security implications addressed?
[ ] Is the rollback path clear?
[ ] Are dependencies and prerequisites listed?
[ ] Is the folder structure complete?
```

## Anti-Patterns to Reject

| Bad Output | Correct Output |
|------------|----------------|
| "Use a queue for this" | Specific queue choice, config, consumer code, DLQ setup |
| "Add authentication" | Auth provider choice, JWT config, middleware code, RBAC schema |
| "Deploy to K8s" | Dockerfile, Helm chart, values.yaml, ingress, HPA, PDB |
| "Set up monitoring" | Prometheus rules, Grafana dashboard JSON, alert thresholds |
| "Handle errors gracefully" | Error types, retry config, circuit breaker, fallback logic |
