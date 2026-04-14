---
title: Deployment Rollback Runbook
type: runbook
source-doc: docs/runbooks/deployment-rollback.md
tags: [runbook, ops, deployment]
---

# Deployment Rollback Runbook

> Source: [`docs/runbooks/deployment-rollback.md`](../../runbooks/deployment-rollback.md)

## Trigger

A deployment to staging or production has failed health checks, introduced a regression, or breached SLO thresholds.

## Owning Agents

- [[../agents/devops/devops-rollback|Rollback Agent]]
- [[../agents/devops/devops-cd|CD Deployer]]
- [[../agents/devops/devops-canary|Canary Manager]]
- [[../agents/devops/devops-gitops|GitOps Sync]]
- [[../agents/security/sec-incident|Incident Responder]]

## Affected Components

- [[../architecture/component-orchestration|K3s + ArgoCD]]
- [[../architecture/component-backend|Backend (FastAPI)]]
- [[../architecture/component-frontend|Frontend (Next.js)]]

## Vault Links

- [[_index|Runbooks Index]]
- [[../_index|Vault Home]]
- [[incident-response]]

## Linked Notes

<!-- linked-notes:start -->
<!-- linked-notes:end -->
