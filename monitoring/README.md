# Monitoring

Observability stack: metrics, dashboards, logs, and alerting.

| Tool | Directory | Purpose |
|------|-----------|---------|
| Prometheus | `prometheus/` | Metrics collection and alerting rules |
| Grafana | `grafana/` | Dashboard definitions |
| Loki | `loki/` | Log aggregation configuration |
| AlertManager | `alertmanager/` | Alert routing and notification |

## Setup

```bash
docker compose --profile monitoring up -d
```

| Service | URL |
|---------|-----|
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 (admin/admin) |

## Alert Thresholds

- Error rate > 1% triggers alert
- p95 latency > 500ms triggers alert
- Dashboard for every service (RED method: Rate, Errors, Duration)
