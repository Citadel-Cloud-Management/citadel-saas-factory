# ADR-004: ArgoCD for GitOps Continuous Delivery

## Status

Accepted

## Context

Citadel SaaS Factory requires a continuous delivery system that:

- Implements GitOps: git is the single source of truth for all deployments
- Supports declarative configuration (no imperative `kubectl apply` in production)
- Provides automatic drift detection and self-healing
- Maintains a full audit trail of all deployments
- Integrates with K3s and Helm charts

The primary candidates evaluated were ArgoCD, Flux CD, and Jenkins CD.

## Decision

We chose **ArgoCD** as the GitOps continuous delivery tool.

### Key Reasons

1. **GitOps native**: ArgoCD continuously monitors git repositories and synchronizes the desired state (in git) with the actual state (in the cluster). Any manual change to the cluster is automatically reverted, enforcing GitOps discipline.

2. **Declarative configuration**: All application definitions, environment configurations, and deployment strategies are declared in YAML and stored in git. No imperative commands are needed for deployments.

   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: citadel-production
   spec:
     source:
       repoURL: https://github.com/Citadel-Cloud-Management/citadel-saas-factory
       targetRevision: main
       path: infrastructure/k8s/overlays/production
     destination:
       server: https://kubernetes.default.svc
       namespace: production
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```

3. **Self-healing**: When `selfHeal: true` is enabled, ArgoCD automatically corrects drift. If someone manually deletes a pod or modifies a ConfigMap, ArgoCD restores the desired state from git within seconds.

4. **Audit trail**: Every sync operation is recorded with the git commit hash, author, timestamp, and sync result. This provides a complete audit trail for compliance (SOC 2, GDPR) without additional tooling.

5. **Web UI and CLI**: ArgoCD provides a rich web dashboard for visualizing application topology, sync status, and resource health, plus a CLI for automation and scripting.

6. **Rollback support**: ArgoCD maintains a history of deployed revisions, enabling one-command rollback to any previous state.

## Consequences

### Positive

- All deployments are traceable to a specific git commit
- Drift detection prevents configuration drift in production
- Self-healing reduces manual intervention for operational issues
- Web UI improves visibility for the entire team (not just operators)
- Supports Helm, Kustomize, plain YAML, and Jsonnet
- Rollback is a single command: `argocd app rollback`

### Negative

- Adds operational complexity (ArgoCD itself needs to be deployed and maintained)
- Learning curve for teams unfamiliar with GitOps workflows
- Secrets management requires integration with external tools (Vault, sealed-secrets) since secrets should not be stored in git
- Multi-cluster management requires ArgoCD ApplicationSets or multiple ArgoCD instances

### Mitigations

- Deploy ArgoCD via its own Helm chart with HA mode for production reliability
- Use HashiCorp Vault with the ArgoCD Vault Plugin for secret injection
- Provide team training on GitOps workflows and ArgoCD usage
- Start with a single cluster and add ApplicationSets when multi-cluster is needed
