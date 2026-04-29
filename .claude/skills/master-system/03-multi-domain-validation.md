---
name: ms-multi-domain-validation
description: Before producing results, internally validate across architecture, security, networking, DevOps, SRE, IAM, observability, scalability, API design, database, frontend, cost, and compliance. Resolve conflicts between domains.
type: directive
priority: 3
---

# Multi-Domain Validation

## Core Rule

Before producing any technical result, validate the design across **all relevant engineering domains**. Resolve conflicts between domains before responding. Explicitly identify trade-offs.

## Validation Domains

### Infrastructure & Platform
- **Architecture** — clean boundaries, dependency direction, coupling
- **Networking** — DNS, load balancing, service mesh, firewall rules
- **DevOps** — CI/CD feasibility, deployment strategy, GitOps compatibility
- **SRE** — reliability targets, error budgets, SLOs/SLIs
- **Cloud Engineering** — provider limits, quotas, managed service trade-offs

### Security & Compliance
- **Security** — attack surface, input validation, encryption
- **IAM** — least privilege, role boundaries, token lifetimes
- **Compliance** — regulatory requirements, data residency, audit trails

### Data & Performance
- **Database** — query performance, indexing, connection limits, consistency
- **Scalability** — horizontal scaling, bottlenecks, caching strategy
- **Observability** — metric coverage, trace propagation, alert quality

### Application
- **API Design** — REST conventions, versioning, rate limiting, pagination
- **Frontend UX** — performance budgets, accessibility, responsive design
- **Reliability** — failure modes, retry logic, graceful degradation

### Business
- **Cost Optimization** — right-sizing, reserved capacity, data transfer
- **Business Feasibility** — time-to-market, maintenance burden, staffing

## Conflict Resolution Protocol

When domains conflict:

1. **Identify the conflict** — state both requirements clearly
2. **Assess priority** — use execution priority order (security > stability > reliability > ...)
3. **Propose resolution** — concrete recommendation with rationale
4. **Document trade-off** — what is sacrificed, what is gained, what are the risks

## Output Format

When multi-domain validation reveals issues:

```markdown
## Domain Validation Results

### Conflicts Identified
- [Domain A] vs [Domain B]: <description>
  - Resolution: <chosen approach>
  - Trade-off: <what is sacrificed>

### Limitations
- <constraint that cannot be fully resolved>

### Risk Areas
- <identified risk with mitigation>
```

## Common Conflict Patterns

| Domain A | Domain B | Typical Resolution |
|----------|----------|-------------------|
| Security (encryption) | Performance (latency) | Encrypt at rest, TLS in transit, cache decrypted |
| Scalability (stateless) | UX (session state) | External session store (Redis) |
| Cost (minimal infra) | Reliability (redundancy) | Scale tier-appropriate redundancy |
| Speed (feature velocity) | Quality (test coverage) | TDD for critical paths, lighter for CRUD |
| Simplicity | Flexibility | Start simple, design for extension |
