# Deployment Guide

How to deploy Citadel SaaS Factory across local, staging, and production environments.

## Environments

| Environment | Orchestration | Purpose |
|-------------|--------------|---------|
| Local | Docker Compose | Development and testing |
| Staging | K3s + ArgoCD | Pre-production validation |
| Production | K3s + ArgoCD | Live workloads with canary deploys |

## Local Deployment (Docker Compose)

### Start All Services

```bash
docker-compose up -d
```

### Verify Services

```bash
docker-compose ps
curl http://localhost:8000/health
```

### Stop Services

```bash
docker-compose down
```

### Reset Data

```bash
docker-compose down -v  # removes volumes
docker-compose up -d
```

### Service Ports

| Service | Port |
|---------|------|
| Frontend | 3000 |
| Backend API | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Keycloak | 8080 |
| MinIO | 9000 (API), 9001 (Console) |
| RabbitMQ | 5672 (AMQP), 15672 (Management) |
| Grafana | 3001 |
| Prometheus | 9090 |

## Staging Deployment (ArgoCD)

Staging mirrors production configuration but runs on a smaller resource footprint.

### Prerequisites

- K3s cluster running with `kubectl` access
- ArgoCD installed and accessible
- Linkerd service mesh injected
- Vault configured with staging secrets

### Deploy to Staging

1. **Push to staging branch:**

```bash
git push origin feature-branch:staging
```

2. **ArgoCD auto-syncs** from the staging branch:

ArgoCD watches the `staging` branch and automatically applies changes to the `staging` namespace. No manual `kubectl apply` is needed.

3. **Verify deployment:**

```bash
kubectl get pods -n staging
kubectl get svc -n staging
argocd app get citadel-staging
```

4. **Check ArgoCD sync status:**

```bash
argocd app sync citadel-staging
argocd app wait citadel-staging --health
```

### Staging Health Checks

```bash
# Verify all pods are running
kubectl get pods -n staging --field-selector=status.phase!=Running

# Check service endpoints
kubectl get endpoints -n staging

# View Linkerd metrics
linkerd viz stat deploy -n staging
```

## Production Deployment (Canary)

Production deployments use canary releases to minimize risk.

### Canary Strategy

```
Phase 1: Deploy canary (5% traffic)
  --> Monitor error rate, latency for 10 minutes
Phase 2: Promote to 25% traffic
  --> Monitor for 10 minutes
Phase 3: Promote to 100% traffic
  --> Full rollout
```

### Deploy to Production

1. **Create a release tag:**

```bash
git tag v1.2.3
git push origin v1.2.3
```

2. **ArgoCD picks up the new tag** and starts the canary rollout.

3. **Monitor the canary:**

```bash
# Watch rollout status
kubectl argo rollouts get rollout citadel-backend -n production --watch

# Check canary metrics
kubectl argo rollouts status citadel-backend -n production
```

4. **Promote the canary** (if metrics are healthy):

```bash
kubectl argo rollouts promote citadel-backend -n production
```

5. **Abort the canary** (if metrics degrade):

```bash
kubectl argo rollouts abort citadel-backend -n production
```

### Automatic Rollback

Canary deployments automatically roll back when:

- Error rate exceeds 1% (measured by Prometheus)
- P95 latency exceeds 500ms
- Health probe failures exceed threshold
- Kyverno policy violations detected

### Production Health Checks

```bash
# Pod status
kubectl get pods -n production

# ArgoCD sync status
argocd app get citadel-production

# Linkerd golden metrics
linkerd viz stat deploy -n production

# Grafana dashboard
# Open: https://grafana.citadelcloudmanagement.com/d/production
```

## Database Migrations

Database migrations run via Alembic before application deployment.

### Local

```bash
alembic upgrade head
```

### Staging/Production

Migrations are applied as a Kubernetes Job that runs before the main deployment:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: citadel-backend:latest
          command: ["alembic", "upgrade", "head"]
      restartPolicy: Never
```

### Rollback Migrations

```bash
# Rollback one revision
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123
```

## Rollback Procedures

See [Deployment Rollback Runbook](runbooks/deployment-rollback.md) for detailed rollback procedures.

### Quick Rollback (ArgoCD)

```bash
# Rollback to previous revision
argocd app rollback citadel-production

# Rollback to specific revision
argocd app rollback citadel-production --revision 42
```

### Quick Rollback (Docker Compose)

```bash
# Roll back to previous image
docker-compose down
git checkout HEAD~1 -- docker-compose.yml
docker-compose up -d
```

## Infrastructure as Code

All infrastructure is defined in version control:

```
infrastructure/
  k8s/
    base/             # Base Kubernetes manifests
    overlays/
      staging/        # Staging-specific patches
      production/     # Production-specific patches
  helm/
    citadel/          # Helm chart for the full platform
  terraform/
    modules/          # Reusable Terraform modules
    environments/
      staging/
      production/
```

Changes to infrastructure follow the same GitOps flow: commit to git, ArgoCD syncs automatically.

## CI/CD Pipeline

The CI/CD pipeline runs on every push:

1. **Lint**: Code formatting and static analysis
2. **Test**: Unit, integration, and E2E tests
3. **Security Scan**: SAST (Semgrep), SCA (Trivy), secret scan (TruffleHog)
4. **Build**: Docker image build and push
5. **Deploy**: ArgoCD sync to target environment

See `.github/workflows/ci-cd.yml` for the full pipeline definition.
