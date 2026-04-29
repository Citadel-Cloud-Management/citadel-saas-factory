---
name: ms-context-engineering
description: Context engineering — maintain long-term memory, project context, architecture history, decision logs, changelogs, ADRs, deployment records. Preserve consistency across APIs, naming, infra, folder structures, and environments.
type: framework
priority: 13
---

# Context Engineering Rules

## Core Rule

Maintain persistent context across sessions. Every decision, deployment, and architectural change must be recorded and retrievable.

## Required Context Stores

### Long-Term Memory
- Project goals and constraints
- User preferences and working style
- Architectural decisions and rationale
- Known issues and workarounds
- Team conventions and patterns

### Architecture History
- ADRs (Architecture Decision Records) in `docs/adr/`
- Schema evolution log
- API version changelog
- Infrastructure topology changes
- Dependency audit trail

### Decision Logs
- Why this tech stack was chosen
- Why this pattern was preferred
- Trade-offs considered and rejected alternatives
- Business constraints that drove technical decisions
- Compliance requirements that shaped architecture

### Changelogs
- Feature additions with context
- Breaking changes with migration guides
- Deprecation notices with timelines
- Security patches with CVE references

### Deployment Records
- What was deployed, when, by whom
- Rollback events and root causes
- Performance impact of deployments
- Feature flag states at deployment time

## Consistency Requirements

### Across APIs
- Same response envelope format everywhere
- Consistent error codes and messages
- Uniform pagination, filtering, sorting
- Versioning strategy applied uniformly

### Across Naming
- File naming: kebab-case
- Python: snake_case functions, PascalCase classes
- TypeScript: camelCase functions, PascalCase types
- Database: snake_case tables, plural names
- Environment: UPPER_SNAKE_CASE

### Across Infrastructure
- Same networking patterns (VPC, subnets, security groups)
- Same container base images
- Same health check patterns
- Same logging format
- Same secret access pattern

### Across Environments
- dev, staging, production parity
- Same IaC for all environments (different values)
- Feature flags for environment-specific behavior
- No environment-specific code paths

## ADR Template

```markdown
# ADR-NNN: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue we're deciding on?

## Decision
What did we decide?

## Consequences
What are the positive, negative, and neutral outcomes?

## Alternatives Considered
What else did we evaluate and why was it rejected?
```

## Context Refresh Protocol

At the start of each session:
1. Check memory for relevant project context
2. Read recent git log for changes since last session
3. Check for open issues/PRs that affect current work
4. Verify infrastructure state matches expectations
5. Review any ADRs or decisions made since last session
