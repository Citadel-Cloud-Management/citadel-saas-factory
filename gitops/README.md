# GitOps — ArgoCD Deployment

Declarative, auditable, self-healing deployments via ArgoCD and Kustomize.

## Structure

```
gitops/
├── argocd/              ArgoCD application definitions
├── base/                Base Kustomize resources (deployment, service)
└── overlays/
    ├── staging/         Staging-specific configuration
    └── production/      Production-specific configuration
```

## Deploy

```bash
# Apply staging
kubectl apply -k gitops/overlays/staging

# ArgoCD auto-syncs from git — push to trigger deployment
git push origin main
```

## Rollback

```bash
argocd app rollback citadel-production
# or
bash scripts/rollback.sh production
```

## Principles

- Git is the single source of truth
- No imperative `kubectl apply` in production
- Self-healing: manual cluster changes are automatically reverted
- Every deployment traced to a git commit
