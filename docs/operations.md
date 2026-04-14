# Operations Guide

Monitoring, alerting, logging, and incident response for Citadel SaaS Factory.

## Monitoring Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Metrics | Prometheus | Time-series metrics collection |
| Dashboards | Grafana | Visualization and alerting |
| Logging | Loki | Log aggregation and search |
| Tracing | Linkerd viz | Distributed request tracing |
| Alerting | Grafana OnCall | Alert routing and escalation |
| Uptime | Health probes | Liveness, readiness, startup |

## Metrics (Prometheus)

### RED Method

All services expose metrics following the RED method:

- **Rate**: Requests per second
- **Errors**: Error count and error rate (percentage)
- **Duration**: Request latency (p50, p95, p99)

### Key Metrics

```promql
# Request rate per service
rate(http_requests_total[5m])

# Error rate percentage
rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m]) * 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Agent execution success rate
rate(agent_executions_total{status="success"}[5m])
  / rate(agent_executions_total[5m]) * 100
```

### Service-Level Indicators (SLIs)

| SLI | Target | Measurement |
|-----|--------|-------------|
| Availability | 99.9% | Successful requests / total requests |
| Latency (p95) | < 500ms | 95th percentile response time |
| Error rate | < 1% | 5xx responses / total responses |
| Agent success rate | > 95% | Successful agent executions / total executions |

### Custom Metrics

Applications expose custom metrics via `/metrics` endpoint:

```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)
```

## Dashboards (Grafana)

### Pre-Built Dashboards

| Dashboard | URL Path | Shows |
|-----------|----------|-------|
| Platform Overview | `/d/overview` | All services health at a glance |
| Backend API | `/d/backend` | FastAPI request rate, latency, errors |
| Frontend | `/d/frontend` | Next.js Core Web Vitals, asset loading |
| Database | `/d/database` | PostgreSQL connections, query performance |
| Cache | `/d/cache` | Redis hit rate, memory usage, evictions |
| Agent System | `/d/agents` | Per-domain and per-agent execution metrics |
| Security | `/d/security` | Falco alerts, Kyverno violations, scan results |
| Infrastructure | `/d/infra` | K3s node health, pod status, resource usage |

### Dashboard as Code

All dashboards are version-controlled in `infrastructure/grafana/dashboards/` and deployed via ArgoCD. Manual dashboard changes are overwritten on sync.

## Alerting

### Alert Rules

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High Error Rate | > 1% for 5 min | SEV2 | Page on-call engineer |
| High Latency | p95 > 500ms for 5 min | SEV2 | Page on-call engineer |
| Service Down | 0 healthy pods for 2 min | SEV1 | Page on-call + escalate |
| Database Connection Pool | > 80% utilized for 10 min | SEV3 | Notify channel |
| Disk Usage | > 85% for 15 min | SEV3 | Notify channel |
| Certificate Expiry | < 14 days | SEV3 | Notify channel |
| Falco Critical Alert | Any critical rule triggered | SEV1 | Page on-call + security |
| Agent Failure Rate | > 5% for 10 min | SEV3 | Notify channel |

### Alert Routing (Grafana OnCall)

```
Alert fires
  --> Grafana OnCall
    --> Route by severity:
      SEV1: Page primary on-call (phone + Slack)
            Auto-escalate to secondary after 5 min
      SEV2: Page primary on-call (Slack + email)
            Auto-escalate after 15 min
      SEV3: Notify #ops-alerts Slack channel
      SEV4: Log to #ops-info Slack channel
```

### On-Call Schedule

- Primary and secondary on-call rotation
- Weekly rotation, handoff on Monday 09:00 UTC
- Escalation chain: Primary --> Secondary --> Engineering Lead --> CTO

## Logging (Loki)

### Log Format

All services emit structured JSON logs:

```json
{
  "timestamp": "2026-04-11T10:00:00.000Z",
  "level": "INFO",
  "service": "citadel-backend",
  "correlation_id": "abc-123-def",
  "tenant_id": "tenant-456",
  "message": "User created successfully",
  "user_id": "user-789",
  "duration_ms": 42
}
```

### Log Levels

| Level | Usage | Retention |
|-------|-------|-----------|
| ERROR | Unexpected failures requiring investigation | 90 days |
| WARN | Degraded but recoverable conditions | 30 days |
| INFO | Business-significant events | 14 days |
| DEBUG | Detailed diagnostic information | 3 days (staging only) |

### PII Redaction

All logs are processed through a redaction filter before storage:

- Email addresses are masked: `u***@example.com`
- IP addresses are masked in non-security logs
- Authentication tokens are never logged
- Request bodies with sensitive fields are redacted

### Querying Logs

```bash
# Via Grafana Explore (Loki)
{service="citadel-backend"} |= "error" | json | level="ERROR"

# Filter by correlation ID
{service=~"citadel-.*"} | json | correlation_id="abc-123-def"

# Filter by tenant
{service="citadel-backend"} | json | tenant_id="tenant-456"
```

## Health Probes

All services implement three probe types:

### Liveness Probe

Indicates whether the process is alive. Failure triggers a pod restart.

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  failureThreshold: 3
```

### Readiness Probe

Indicates whether the service can accept traffic. Failure removes the pod from the load balancer.

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
```

### Startup Probe

Allows slow-starting containers to initialize before liveness checks begin.

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 30
```

## Incident Response

See [Incident Response Runbook](runbooks/incident-response.md) for the full procedure.

### Quick Reference

1. **Detect**: Alert fires or user report received
2. **Triage**: Assess severity (SEV1-4)
3. **Communicate**: Update status page, notify stakeholders
4. **Mitigate**: Contain the impact (rollback, feature flag, scaling)
5. **Resolve**: Fix the root cause
6. **Postmortem**: Blameless review within 48 hours

## Runbooks

| Runbook | Purpose |
|---------|---------|
| [Incident Response](runbooks/incident-response.md) | SEV1-4 handling, escalation, postmortem |
| [Deployment Rollback](runbooks/deployment-rollback.md) | ArgoCD, Docker Compose, database rollback |

## Backup and Recovery

### Velero Backups

Kubernetes resources and persistent volumes are backed up via Velero:

```bash
# Create on-demand backup
velero backup create citadel-backup-$(date +%Y%m%d)

# Schedule daily backups
velero schedule create daily-backup --schedule="0 2 * * *" --ttl 720h

# Restore from backup
velero restore create --from-backup citadel-backup-20260411
```

### Database Backups

PostgreSQL backups run on a schedule:

- **Continuous**: WAL archiving for point-in-time recovery
- **Daily**: Full `pg_dump` at 02:00 UTC, retained for 30 days
- **Weekly**: Full backup retained for 90 days

### Recovery Time Objectives

| Component | RTO | RPO |
|-----------|-----|-----|
| Application | 15 minutes | 0 (stateless, redeploy) |
| Database | 30 minutes | 5 minutes (WAL archiving) |
| Object Storage | 1 hour | 24 hours (daily replication) |
| Full Platform | 2 hours | 5 minutes |
