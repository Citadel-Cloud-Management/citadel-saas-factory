# Incident Response Runbook

## Severity Levels

| Level | Definition | Response Time | Examples |
|-------|-----------|---------------|----------|
| SEV1 | Critical: Service fully down or data breach | 15 minutes | Production outage, security breach, data loss |
| SEV2 | Major: Significant feature degraded | 30 minutes | High error rate, major API failures, auth down |
| SEV3 | Minor: Non-critical feature impacted | 4 hours | Slow queries, minor UI bugs, single agent failures |
| SEV4 | Low: Cosmetic or informational | Next business day | Typos, non-blocking warnings, documentation gaps |

## Incident Lifecycle

### 1. Detection

Incidents are detected through:

- **Automated alerts**: Prometheus/Grafana OnCall firing on threshold breach
- **User reports**: Customer support tickets or direct reports
- **Internal discovery**: Team member notices an issue during development or testing

### 2. Triage

The on-call engineer performs initial triage:

1. **Acknowledge** the alert in Grafana OnCall
2. **Assess severity** using the table above
3. **Create incident channel** in Slack: `#incident-YYYY-MM-DD-brief-description`
4. **Assign Incident Commander (IC)** -- the on-call engineer by default

### 3. Escalation

| Severity | Escalation Path |
|----------|----------------|
| SEV1 | On-call --> Engineering Lead --> CTO (within 15 min) |
| SEV2 | On-call --> Engineering Lead (within 30 min) |
| SEV3 | On-call handles, notify team lead |
| SEV4 | On-call handles, create ticket for follow-up |

For SEV1 incidents, immediately:

- Page secondary on-call
- Notify Engineering Lead
- Prepare to update status page

### 4. Communication

#### Internal Communication

- All updates go to the incident Slack channel
- IC posts updates every **15 minutes** for SEV1, **30 minutes** for SEV2
- Use the format: `[HH:MM UTC] STATUS: <update>`

#### External Communication (SEV1/SEV2)

- Update the status page within **30 minutes** of detection
- Provide estimated time to resolution if known
- Update status page when resolved
- Send post-incident summary to affected customers within 24 hours

#### Status Page Update Template

```
Title: [Service Name] Degraded Performance / Outage
Status: Investigating / Identified / Monitoring / Resolved

Body:
We are currently experiencing [description of impact].
Our team is actively investigating and working on a resolution.
Next update in [time].

Impact: [List affected services and user-facing impact]
```

### 5. Mitigation

Common mitigation strategies by issue type:

| Issue | Mitigation |
|-------|-----------|
| Bad deployment | Rollback via ArgoCD: `argocd app rollback citadel-production` |
| High error rate | Scale up replicas, enable circuit breaker |
| Database overload | Kill long-running queries, add read replicas |
| Memory leak | Restart affected pods: `kubectl rollout restart deploy/<name> -n production` |
| Security breach | Isolate affected service, rotate credentials, engage security team |
| DDoS | Enable rate limiting, engage CDN/WAF |
| Feature bug | Disable via feature flag (Flagsmith) |

### 6. Resolution

1. Confirm the fix resolves the issue
2. Monitor for recurrence (minimum 30 minutes)
3. Update status page to "Resolved"
4. Post final update in incident Slack channel
5. Schedule postmortem within 48 hours

## Postmortem Process

### Timeline

- **Within 48 hours**: Postmortem meeting held
- **Within 5 business days**: Postmortem document published
- **Within 2 weeks**: Action items assigned and tracked

### Postmortem Template

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Duration**: HH:MM - HH:MM UTC (X hours Y minutes)
**Severity**: SEV[1-4]
**Incident Commander**: [Name]
**Authors**: [Names]

## Summary

[1-2 sentence summary of what happened and the impact]

## Impact

- **Users affected**: [number or percentage]
- **Duration**: [time]
- **Revenue impact**: [if applicable]
- **Data impact**: [if applicable]

## Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | [First detection or alert] |
| HH:MM | [Triage and severity assignment] |
| HH:MM | [Key investigation steps] |
| HH:MM | [Mitigation applied] |
| HH:MM | [Resolution confirmed] |

## Root Cause

[Detailed description of the root cause. Be specific and technical.]

## Contributing Factors

- [Factor 1]
- [Factor 2]

## What Went Well

- [Positive aspect of the response]
- [Positive aspect of the response]

## What Could Be Improved

- [Area for improvement]
- [Area for improvement]

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| [Action description] | [Name] | YYYY-MM-DD | P1/P2/P3 |
| [Action description] | [Name] | YYYY-MM-DD | P1/P2/P3 |

## Lessons Learned

[Key takeaways for the team]
```

### Postmortem Principles

- **Blameless**: Focus on systems and processes, not individuals
- **Thorough**: Trace the full chain of events
- **Actionable**: Every "what could be improved" must have a corresponding action item
- **Shared**: Publish to the team for collective learning

## On-Call Checklist

When starting an on-call shift:

- [ ] Verify access to Grafana, ArgoCD, kubectl, and Vault
- [ ] Review open alerts and recent incidents
- [ ] Confirm notification settings (phone, Slack, email)
- [ ] Check the handoff notes from the previous on-call
- [ ] Verify VPN/access to production infrastructure

## Quick Reference Commands

```bash
# Check system health
kubectl get pods -n production
argocd app get citadel-production
linkerd viz stat deploy -n production

# Rollback deployment
argocd app rollback citadel-production

# Restart a service
kubectl rollout restart deploy/citadel-backend -n production

# Check logs
kubectl logs -f deploy/citadel-backend -n production --tail=100

# Scale up
kubectl scale deploy/citadel-backend -n production --replicas=5
```
