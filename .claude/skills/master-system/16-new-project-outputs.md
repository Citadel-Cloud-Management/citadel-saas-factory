---
name: ms-new-project-outputs
description: Required outputs for new projects — architecture diagram, service map, data flow, threat model, CI/CD pipeline, infrastructure design, IAM design, deployment workflow, rollback strategy, observability stack, secrets management, scaling model, DR strategy.
type: checklist
priority: 16
---

# Required Outputs for New Projects

## Core Rule

When creating a new system, automatically generate all required artifacts. No system goes to production without these documents and configurations.

## Required Artifacts

### 1. Architecture Diagram
```
- System components and boundaries
- Data flow directions
- External integrations
- Network boundaries (public, private, DMZ)
- Format: ASCII diagram or Mermaid
```

### 2. Service Map
```
- All services with ports and protocols
- Dependencies between services
- External service dependencies
- Health check endpoints
- SLA/SLO targets per service
```

### 3. Data Flow Diagram
```
- Data sources and sinks
- Processing stages
- Encryption points (in-transit, at-rest)
- PII data paths (highlighted)
- Data retention policies
```

### 4. Threat Model
```
- STRIDE analysis per component
- Attack surface inventory
- Trust boundaries
- Data classification (public, internal, confidential, restricted)
- Mitigation controls per threat
```

### 5. CI/CD Pipeline
```
- Pipeline stages (lint, test, scan, build, deploy)
- Approval gates
- Environment promotion strategy
- Artifact management
- Rollback triggers
```

### 6. Infrastructure Design
```
- Cloud resource inventory
- Network topology (VPC, subnets, security groups)
- Compute sizing (CPU, memory, storage)
- Auto-scaling policies
- Cost estimate
```

### 7. IAM Design
```
- Role definitions (admin, operator, developer, viewer)
- Service account permissions
- API key management
- Token lifecycle (creation, rotation, revocation)
- Audit logging scope
```

### 8. Deployment Workflow
```
- Deployment strategy (blue/green, canary, rolling)
- Pre-deployment checks
- Post-deployment verification
- Smoke test suite
- Notification channels
```

### 9. Rollback Strategy
```
- Automated rollback triggers (error rate, latency)
- Manual rollback procedure
- Database rollback approach
- Feature flag fallbacks
- Communication plan
```

### 10. Observability Stack
```
- Metrics collection and storage
- Log aggregation pipeline
- Distributed tracing setup
- Dashboard definitions
- Alert rules and escalation
```

### 11. Secrets Management
```
- Secret storage (Vault, K8s Secrets, cloud KMS)
- Rotation schedule
- Access control policies
- Emergency rotation procedure
- Audit trail configuration
```

### 12. Scaling Model
```
- Expected traffic patterns
- Scaling triggers and thresholds
- Horizontal vs vertical scaling decisions
- Database scaling strategy
- Cost at 1x, 10x, 100x traffic
```

### 13. Disaster Recovery Strategy
```
- RTO (Recovery Time Objective)
- RPO (Recovery Point Objective)
- Backup schedule and retention
- Cross-region failover procedure
- DR test schedule (quarterly)
```

## Generation Workflow

```
New Project Request
    → Generate folder structure (plugin 15)
    → Generate all 13 artifacts above
    → Create initial CI/CD pipeline
    → Create initial Terraform/Helm configs
    → Create initial test suite scaffolding
    → Create README with setup instructions
    → Create .env.example with all required variables
```
