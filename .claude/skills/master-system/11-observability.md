---
name: ms-observability
description: Observability requirements — structured logging, distributed tracing, metrics, dashboards, alerting, uptime monitoring. OpenTelemetry + Prometheus + Grafana + Loki + Tempo + Sentry stack.
type: standard
priority: 11
---

# Observability Requirements

## Core Rule

All systems must support full observability from day one. No service goes to production without logging, metrics, tracing, and alerting.

## Required Capabilities

### Structured Logging
- JSON format with correlation IDs
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL
- PII redaction in all log output
- Request/response logging (sanitized)
- Structured context (user_id, tenant_id, trace_id)

### Distributed Tracing
- Trace propagation across all service boundaries
- Span attributes for business context
- Sampling strategy (100% errors, 10% success)
- Parent-child span relationships

### Metrics
- RED method: Rate, Errors, Duration
- USE method: Utilization, Saturation, Errors (infrastructure)
- Business metrics: signups, conversions, revenue events
- Custom metrics for domain-specific KPIs

### Dashboards
- Service overview (health, traffic, errors, latency)
- Infrastructure (CPU, memory, disk, network)
- Business metrics (funnel, revenue, churn)
- On-call dashboard (active alerts, recent incidents)

### Alerting
- Thresholds: >1% error rate, >500ms p95 latency
- Multi-window alerts (5min + 1hr burn rate)
- PagerDuty/Slack integration
- Escalation policies
- Runbook links in every alert

### Uptime Monitoring
- Synthetic checks from multiple regions
- SSL certificate expiry monitoring
- DNS resolution monitoring
- API endpoint health checks

## Preferred Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Instrumentation | OpenTelemetry | Unified traces, metrics, logs |
| Metrics | Prometheus | Time-series metrics store |
| Dashboards | Grafana | Visualization and alerting |
| Logs | Loki | Log aggregation and query |
| Traces | Tempo | Distributed trace storage |
| Errors | Sentry | Error tracking and grouping |
| Uptime | Uptime Robot / Checkly | Synthetic monitoring |

## Observability Maturity Levels

| Level | Capabilities |
|-------|-------------|
| L0 | Console logs, no metrics |
| L1 | Structured logs, basic metrics, manual dashboards |
| L2 | Distributed tracing, automated alerts, SLO tracking |
| L3 | Anomaly detection, auto-remediation, business metric correlation |

**Minimum for production: L2**

## Alert Design Rules

```yaml
good_alert:
  - Actionable (human knows what to do)
  - Linked to runbook
  - Low false-positive rate (<5%)
  - Multi-signal (not single metric)
  - Severity-appropriate routing

bad_alert:
  - "CPU is high" (no context)
  - No runbook link
  - Fires 10x/day with no action needed
  - Single metric threshold only
```
