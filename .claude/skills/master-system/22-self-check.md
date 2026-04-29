---
name: ms-self-check
description: Final self-check before responding — validate technically correct, production feasible, secure, observable, maintainable, scalable, cost-aware, operationally safe, and realistically deployable.
type: guardrail
priority: 22
---

# Final Self-Check Before Responding

## Core Rule

Before finalizing any technical response, run through this validation checklist. If any critical check fails, revise the response before delivering.

## Validation Checklist

### Critical (Must Pass)

```
[ ] TECHNICALLY CORRECT
    - APIs referenced actually exist
    - Syntax is valid for the language/framework
    - Dependencies are real and compatible
    - Configuration values are valid
    - Commands would actually work if run

[ ] PRODUCTION FEASIBLE
    - Works in containerized environments
    - Handles concurrent users
    - No single points of failure
    - Resource requirements are reasonable
    - No blocking operations on hot paths

[ ] SECURE
    - No hardcoded secrets
    - Input validation present
    - Auth/authz considered
    - No SQL injection, XSS, SSRF vectors
    - Secrets use proper management (env vars, vault)
    - OWASP Top 10 addressed

[ ] OPERATIONALLY SAFE
    - Rollback path is clear
    - No destructive operations without confirmation
    - Backward-compatible changes
    - Migration is reversible
    - No data loss scenarios
```

### Important (Should Pass)

```
[ ] OBSERVABLE
    - Logging integrated at appropriate levels
    - Metrics emitted for key operations
    - Error tracking wired up
    - Health endpoints present
    - Correlation IDs propagated

[ ] MAINTAINABLE
    - Clean code principles applied
    - Functions are small and focused
    - Clear separation of concerns
    - Naming is descriptive
    - No unnecessary complexity

[ ] SCALABLE
    - No obvious bottlenecks
    - Database queries are indexed
    - Caching strategy defined where needed
    - Horizontal scaling path exists
    - No N+1 query patterns

[ ] COST-AWARE
    - Resources right-sized
    - No unnecessary always-on compute
    - Storage tier appropriate
    - Transfer costs considered
    - Third-party API costs estimated
```

### Informational (Nice to Pass)

```
[ ] REALISTICALLY DEPLOYABLE
    - CI/CD compatible
    - Environment variables documented
    - Docker/K8s compatible
    - Config management approach defined
    - No manual steps required
```

## Failure Response Protocol

If a check fails:

| Severity | Action |
|----------|--------|
| Critical fails | Fix before responding. No exceptions. |
| Important fails | Fix if possible, note as known limitation if not |
| Informational fails | Note as future improvement |

## Common Self-Check Failures

| Issue | How to Catch | Fix |
|-------|-------------|-----|
| Hallucinated API | Check docs exist | Use verified APIs only |
| Missing error handling | No try/catch | Add error handling |
| Hardcoded config | Literal values in code | Extract to env vars |
| No timeout | HTTP calls without timeout | Add explicit timeouts |
| No rollback | Destructive migration | Make backward-compatible |
| Over-engineering | 100 lines for 10-line problem | Simplify |

## Speed vs Quality Trade-off

- Quick fix / hotfix: Critical checks only (security + correctness)
- Standard feature: Critical + Important checks
- Architecture / infrastructure: All checks required
- Production deployment: All checks + peer review
