---
title: Incident Response Runbook
type: runbook
source-doc: docs/runbooks/incident-response.md
tags: [runbook, ops, incident, security]
---

# Incident Response Runbook

> Source: [`docs/runbooks/incident-response.md`](../../runbooks/incident-response.md)

## Trigger

Production incident — outage, security event, data integrity issue, or SLA breach.

## Owning Agents

- [[../agents/security/sec-incident|Incident Responder]]
- [[../agents/security/sec-threat|Threat Hunter]]
- [[../agents/security/sec-runtime|Runtime Monitor]]
- [[../agents/devops/devops-debugger|K8s Debugger]]
- [[../agents/devops/devops-rollback|Rollback Agent]]
- [[../agents/content/content-status|Status Writer]]
- [[../agents/legal/legal-incident|Incident Notifier]]

## Affected Components

- [[../architecture/component-backend]]
- [[../architecture/component-database]]
- [[../architecture/component-orchestration]]
- [[../architecture/component-mesh]]

## Related Memory

- [[../memory/error-patterns]]
- [[../memory/deployment-history]]

## Vault Links

- [[_index|Runbooks Index]]
- [[deployment-rollback]]
- [[../_index|Vault Home]]

## Linked Notes

<!-- linked-notes:start -->
<!-- linked-notes:end -->
