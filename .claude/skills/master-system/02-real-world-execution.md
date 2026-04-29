---
name: ms-real-world-execution
description: All outputs must be production-oriented, technically feasible, operationally realistic, security-aware, and cloud-native. No toy examples or fake abstractions.
type: directive
priority: 2
---

# Real-World Execution First

## Core Rule

Every output must be deployable in a real production environment with real users, real infrastructure, real security risks, and real cost implications.

## All Outputs Must Be

- **Production-oriented** — designed for actual deployment, not demos
- **Technically feasible** — uses real APIs, real libraries, real infrastructure
- **Operationally realistic** — accounts for failure modes, maintenance, on-call
- **Security-aware** — threat model considered, attack surface minimized
- **Cloud-native where appropriate** — leverages managed services, auto-scaling, HA

## Avoid

- Toy examples that don't scale past 10 users
- Fake abstractions that hide real complexity
- Non-scalable recommendations (single-node, no replication)
- Academically correct but operationally weak solutions
- "Hello World" patterns presented as production patterns
- Ignoring cost at scale
- Assuming infinite resources

## Always Assume

- **Real users** — concurrent, distributed, adversarial
- **Real infrastructure** — failures happen, networks partition, disks fill
- **Real security risks** — bots, scrapers, DDoS, credential stuffing
- **Real deployment constraints** — CI/CD gates, approval flows, rollback needs
- **Real cost implications** — compute, storage, bandwidth, third-party APIs
- **Real compliance requirements** — GDPR, SOC2, HIPAA as applicable

## Production Realism Checklist

```
[ ] Would this survive 10x traffic spike?
[ ] What happens when the database is unavailable for 30 seconds?
[ ] What happens when a downstream API returns 500?
[ ] Is this cost-effective at 100K MAU? 1M MAU?
[ ] Can this be debugged at 3am during an incident?
[ ] Does this work behind a CDN/load balancer?
[ ] Is the data model correct for multi-tenancy?
[ ] Are secrets properly isolated?
```

## Scale Tiers to Consider

| Tier | MAU | Infra Assumptions |
|------|-----|-------------------|
| Startup | <10K | Single region, managed services |
| Growth | 10K-100K | Multi-AZ, read replicas, CDN |
| Scale | 100K-1M | Multi-region, sharding, edge |
| Enterprise | 1M+ | Global, custom infra, SLAs |
