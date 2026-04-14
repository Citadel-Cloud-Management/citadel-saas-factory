# Deployment Rollback Runbook

Procedures for rolling back deployments across all environments.

## When to Rollback

Rollback immediately when any of these conditions are met after a deployment:

- Error rate exceeds 1% for more than 5 minutes
- P95 latency exceeds 500ms for more than 5 minutes
- Health probes are failing on new pods
- Critical functionality is broken (auth, payments, data access)
- Security vulnerability discovered in the deployed code

## ArgoCD Rollback (Staging and Production)

### Rollback to Previous Revision

```bash
# List recent revisions
argocd app history citadel-production

# Rollback to the previous revision
argocd app rollback citadel-production

# Rollback to a specific revision number
argocd app rollback citadel-production --revision 42
```

### Verify Rollback

```bash
# Check sync status
argocd app get citadel-production

# Verify pods are running the correct image
kubectl get pods -n production -o jsonpath='{.items[*].spec.containers[*].image}'

# Check pod health
kubectl get pods -n production

# Verify service is responding
curl -s https://api.citadelcloudmanagement.com/health
```

### Canary Abort

If a canary deployment is in progress and metrics are degrading:

```bash
# Abort the canary rollout (reverts to stable)
kubectl argo rollouts abort citadel-backend -n production

# Verify stable version is serving all traffic
kubectl argo rollouts get rollout citadel-backend -n production
```

### Disable Auto-Sync (Emergency)

If ArgoCD keeps re-deploying the broken version:

```bash
# Disable auto-sync temporarily
argocd app set citadel-production --sync-policy none

# After fixing, re-enable
argocd app set citadel-production --sync-policy automated
```

## Docker Compose Rollback (Local/Dev)

### Rollback to Previous Version

```bash
# Stop current services
docker-compose down

# Check out the previous working version
git log --oneline -10  # find the last known good commit
git checkout <good-commit-hash> -- docker-compose.yml

# Restart with the previous configuration
docker-compose up -d

# Verify
docker-compose ps
curl http://localhost:8000/health
```

### Rollback Using Image Tags

If using explicit image tags in `docker-compose.yml`:

```bash
# Edit docker-compose.yml to use the previous image tag
# e.g., change citadel-backend:v1.2.3 to citadel-backend:v1.2.2

docker-compose up -d --force-recreate
```

### Full Reset (Last Resort)

```bash
# Remove all containers and volumes
docker-compose down -v

# Pull fresh images
docker-compose pull

# Start clean
docker-compose up -d
```

## Database Migration Rollback

### Identify Current Migration

```bash
# Check current migration head
alembic current

# List migration history
alembic history --verbose
```

### Rollback One Migration

```bash
# Downgrade by one revision
alembic downgrade -1

# Verify
alembic current
```

### Rollback to Specific Revision

```bash
# Downgrade to a specific revision
alembic downgrade abc123def456

# Verify
alembic current
```

### Rollback in Kubernetes

For staging/production, run the migration rollback as a Kubernetes Job:

```bash
# Create a one-off migration rollback job
kubectl run db-rollback \
  --image=citadel-backend:latest \
  --restart=Never \
  --rm -it \
  -n production \
  -- alembic downgrade -1
```

### Important Notes on Database Rollbacks

- **Data loss risk**: Downgrade migrations may drop columns or tables. Always check the downgrade function before running.
- **Backup first**: Take a database snapshot before any migration rollback in production.
- **Test in staging**: Always test the downgrade path in staging before running in production.
- **Coordinate with application rollback**: Roll back the application code first, then the database migration.

```bash
# Create a backup before rollback
pg_dump -h $DB_HOST -U $DB_USER -d citadel > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Rollback Verification Checklist

After completing any rollback:

- [ ] All pods/containers are running and healthy
- [ ] Health endpoints return 200 OK
- [ ] Error rate has returned to baseline (< 0.1%)
- [ ] P95 latency has returned to baseline (< 200ms)
- [ ] Authentication and authorization are working
- [ ] Key user flows are functional (test manually or via E2E)
- [ ] Linkerd metrics show healthy traffic (production)
- [ ] No Kyverno policy violations
- [ ] Status page updated (if it was a public incident)
- [ ] Incident channel updated with rollback confirmation

## Rollback Decision Tree

```
Deployment completed
  |
  +--> Metrics healthy for 10 min?
        |
        YES --> Deployment successful, monitor for 1 hour
        |
        NO  --> Is it a canary?
               |
               YES --> Abort canary: kubectl argo rollouts abort ...
               |
               NO  --> Is ArgoCD managing it?
                      |
                      YES --> argocd app rollback citadel-production
                      |
                      NO  --> Docker Compose rollback (git checkout + up -d)
                      |
                      +--> Database migration involved?
                            |
                            YES --> Backup DB, then: alembic downgrade -1
                            |
                            NO  --> Application rollback is sufficient
```

## Post-Rollback Actions

1. **Communicate**: Notify the team in the incident Slack channel
2. **Investigate**: Determine why the deployment failed
3. **Fix forward**: Create a fix branch, test thoroughly, and redeploy
4. **Postmortem**: If SEV1/SEV2, schedule a postmortem within 48 hours
5. **Re-enable auto-sync**: If ArgoCD auto-sync was disabled, re-enable after fixing
