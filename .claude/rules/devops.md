# DevOps Rules
- GitOps: all infrastructure as code, all changes via git
- Immutable infrastructure: never patch in place, rebuild
- Health probes: liveness, readiness, startup on all services
- Resource limits on all containers (CPU + memory)
- Rolling deployments with automatic rollback on failure
- Infrastructure-agnostic: no cloud vendor lock-in
