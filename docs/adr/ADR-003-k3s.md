# ADR-003: K3s as Kubernetes Distribution

## Status

Accepted

## Context

Citadel SaaS Factory requires a container orchestration platform that:

- Runs on any infrastructure (VPS, bare metal, on-prem, edge, home lab)
- Has no cloud vendor lock-in or proprietary dependencies
- Is lightweight enough for single-node deployments but scales to multi-node clusters
- Is Kubernetes-compatible (standard API, Helm charts, CRDs)
- Has zero licensing cost

The primary candidates evaluated were K3s, standard Kubernetes (kubeadm), K0s, and MicroK8s.

## Decision

We chose **K3s** as the Kubernetes distribution.

### Key Reasons

1. **Lightweight**: K3s is packaged as a single binary under 100MB. It replaces etcd with SQLite (single-node) or embedded etcd (multi-node), reducing memory footprint by approximately 50% compared to standard Kubernetes.

2. **Single binary installation**: Install and run with a single command:

   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```

   This simplifies deployment on any Linux server with SSH access, aligned with the "any infrastructure" requirement.

3. **Edge-friendly**: K3s is designed for resource-constrained environments (ARM64, low-memory VPS, edge devices). It runs comfortably on a 2GB RAM VPS, making it accessible for small teams and development environments.

4. **CNCF certified**: K3s is a CNCF-certified Kubernetes distribution, meaning all standard Kubernetes APIs, tools (kubectl, Helm, Kustomize), and CRDs work without modification. There is no migration risk.

5. **Infrastructure-agnostic**: K3s runs on any Linux system with SSH. No cloud-specific dependencies, no proprietary node pools, no managed service lock-in.

6. **Built-in components**: K3s includes Traefik as the default ingress controller, CoreDNS, and Flannel networking out of the box, reducing initial setup complexity.

## Consequences

### Positive

- Minimal resource requirements enable deployment on low-cost VPS ($5-10/month)
- Single-command installation reduces operational complexity
- Full Kubernetes API compatibility means all Helm charts and operators work
- Easy to set up HA clusters with embedded etcd (3+ server nodes)
- Active community and Rancher/SUSE backing for long-term support

### Negative

- SQLite backend (single-node) is not suitable for high-availability production without switching to embedded etcd or external datastore
- Fewer pre-configured monitoring/logging integrations compared to managed Kubernetes (EKS, GKE, AKS)
- Some advanced Kubernetes features may require manual configuration (e.g., PodSecurityPolicies replaced by Pod Security Standards)
- Community support is smaller than mainstream Kubernetes distributions

### Mitigations

- Use embedded etcd mode for production clusters (3+ server nodes for HA)
- Deploy Prometheus, Grafana, and Loki via Helm charts for monitoring/logging
- Use Kyverno for policy enforcement (replacing deprecated PodSecurityPolicies)
- Follow K3s documentation for production hardening (CIS benchmarks)
