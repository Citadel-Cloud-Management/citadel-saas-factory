# Architecture Decision Records

## ADR-001: Infrastructure Agnostic
- Decision: No cloud vendor lock-in. All infrastructure runs on any Linux server with SSH and Docker.
- Rationale: Maximum portability — VPS, bare metal, on-prem, edge, home lab.
- Consequence: No AWS/GCP/Azure-specific services. Use open-source alternatives (MinIO for S3, Keycloak for Cognito, etc.).

## ADR-002: Free Toolchain
- Decision: $0/month software cost using open-source tools.
- Tools: K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy, ZAP, Flagsmith.

## ADR-003: 265-Agent Architecture
- Decision: 265 specialized autonomous agents across 15 business domains.
- Rationale: Each agent has a focused responsibility, enabling parallel execution and domain expertise.

## ADR-004: GitOps Deployment
- Decision: ArgoCD with Kustomize overlays for staging and production.
- Rationale: Declarative, auditable, and self-healing deployments.
