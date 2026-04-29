---
name: ms-enterprise-docs
description: Enterprise documentation standards — auto-generate ADRs, runbooks, SOPs, onboarding docs, architecture docs, API docs, operational guides, DR procedures, incident response playbooks, compliance mapping, IAM documentation. Always synchronized with implementation.
type: standard
priority: 25
---

# Enterprise Documentation Standards

## Core Rule

Automatically generate and maintain comprehensive documentation. Documentation must remain synchronized with implementation — stale docs are worse than no docs.

## Required Document Types

### 1. Architecture Decision Records (ADRs)
```markdown
Location: docs/adr/
Format: ADR-NNN-title.md
Trigger: Any architectural decision

Template:
# ADR-NNN: [Title]
## Status: [Proposed|Accepted|Deprecated|Superseded]
## Context: [Problem being solved]
## Decision: [What we decided]
## Consequences: [Positive, negative, neutral outcomes]
## Alternatives: [What else was considered]
```

### 2. Runbooks
```markdown
Location: docs/runbooks/
Format: runbook-[service]-[scenario].md
Trigger: Any operational procedure

Sections:
- Overview (what this covers)
- Prerequisites (access, tools)
- Steps (numbered, copy-pasteable commands)
- Verification (how to confirm success)
- Rollback (how to undo)
- Escalation (who to contact if stuck)
```

### 3. Standard Operating Procedures (SOPs)
```markdown
Location: docs/sops/
Format: sop-[process].md
Trigger: Any repeatable process

Sections:
- Purpose
- Scope
- Roles and responsibilities
- Procedure steps
- Frequency
- Compliance references
```

### 4. Onboarding Documentation
```markdown
Location: docs/onboarding/
Format: onboard-[role].md

Required guides:
- Developer setup (clone → env → run in <15 min)
- Architecture overview (system context diagram)
- Key decisions (link to ADRs)
- Common tasks (how to add feature, fix bug, deploy)
- Team conventions (git, code review, testing)
```

### 5. Architecture Documentation
```markdown
Location: docs/architecture/
Format: arch-[system].md

Required diagrams:
- System context (C4 level 1)
- Container view (C4 level 2)
- Component view (C4 level 3, critical services)
- Data flow diagram
- Network topology
- Deployment architecture
```

### 6. API Documentation
```markdown
Location: Auto-generated from OpenAPI spec
Format: Swagger UI + Redoc

Requirements:
- Every endpoint documented
- Request/response examples
- Error response catalog
- Authentication instructions
- Rate limiting documentation
- Changelog per version
```

### 7. Operational Guides
```markdown
Location: docs/operations/
Format: ops-[topic].md

Topics:
- Deployment process
- Monitoring and alerting
- Scaling procedures
- Backup and restore
- Log access and analysis
- Performance tuning
```

### 8. Disaster Recovery Procedures
```markdown
Location: docs/dr/
Format: dr-[scenario].md

Required scenarios:
- Database failure and recovery
- Region outage failover
- Data corruption recovery
- Complete system rebuild
- Credential compromise response
```

### 9. Incident Response Playbooks
```markdown
Location: docs/incidents/
Format: incident-[type].md

Required playbooks:
- Service outage
- Data breach
- Performance degradation
- Security vulnerability discovered
- Dependency failure
- DNS issues
```

### 10. Compliance Mapping
```markdown
Location: docs/compliance/
Format: compliance-[framework].md

Frameworks:
- SOC 2 Type II controls mapping
- GDPR data processing records
- HIPAA safeguards (if applicable)
- PCI-DSS requirements (if applicable)
- ISO 27001 controls
```

### 11. IAM Documentation
```markdown
Location: docs/iam/
Format: iam-[topic].md

Required docs:
- Role definitions and permissions matrix
- Service account inventory
- Access request process
- Emergency access procedure
- Audit and review schedule
```

## Synchronization Rules

```
Code change → Check if docs need updating
Schema change → Update API docs + data flow
Infra change → Update architecture + runbooks
Process change → Update SOPs + onboarding
Security change → Update IAM docs + compliance mapping
```

## Documentation Quality Standards

- **Testable**: Commands in docs should work when run
- **Current**: Updated within 24 hours of implementation change
- **Discoverable**: Linked from README and vault index
- **Reviewed**: Docs PRs required for significant changes
- **Versioned**: Documentation versioned alongside code
