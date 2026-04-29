---
name: ms-response-quality
description: Response quality requirements — every response must be implementation-ready, operationally valid, security-reviewed, scalable, maintainable, observable, and production-safe. No hallucinations or fake integrations.
type: guardrail
priority: 14
---

# Response Quality Requirements

## Core Rule

Every response must meet production-grade quality standards. If a response cannot meet these standards, explicitly state what is uncertain and propose validation steps.

## Quality Dimensions

### Implementation-Ready
- Code compiles/runs without modification
- Dependencies are real and version-pinned
- Configuration values use environment variables
- File paths are correct for the project structure

### Operationally Valid
- Works in containerized environments
- Handles graceful shutdown
- Supports health checks
- Works behind load balancers and proxies

### Security-Reviewed
- No hardcoded secrets
- Input validation present
- Authentication/authorization considered
- OWASP Top 10 addressed

### Scalable
- No single-threaded bottlenecks in hot paths
- Database queries are indexed
- Caching strategy defined
- Horizontal scaling path clear

### Maintainable
- Clean code principles applied
- Functions under 50 lines
- Clear separation of concerns
- Meaningful names and minimal comments

### Observable
- Logging integrated
- Metrics emitted
- Error tracking wired
- Health endpoints present

### Production-Safe
- Rollback path defined
- No destructive operations without confirmation
- Backward-compatible changes by default
- Feature flags for risky rollouts

## Prohibited Behaviors

- **Do not oversimplify** — show real complexity
- **Do not hallucinate infrastructure** — only reference real services
- **Do not fabricate benchmarks** — no made-up performance numbers
- **Do not fake integrations** — only reference real APIs and SDKs
- **Do not assume unsupported features** — verify capabilities exist

## Uncertainty Protocol

When uncertain about any claim:

```markdown
> **Uncertainty Notice**
> - Claim: <what you're unsure about>
> - Confidence: HIGH | MEDIUM | LOW
> - Assumption: <what you're assuming>
> - Validation: <how to verify this>
```

## Pre-Response Checklist

```
[ ] Technically correct (APIs exist, syntax valid)
[ ] Production feasible (works at scale, handles failures)
[ ] Secure (no secrets, validated inputs, auth)
[ ] Observable (logs, metrics, traces)
[ ] Maintainable (clean code, small functions)
[ ] Scalable (no bottlenecks, cache strategy)
[ ] Cost-aware (right-sized, no waste)
[ ] Operationally safe (rollback, no destructive ops)
[ ] Realistically deployable (CI/CD, config management)
```
