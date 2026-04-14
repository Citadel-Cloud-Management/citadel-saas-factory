---
description: Deploy to a target environment
argument-hint: "[staging|production]"
---

Deploy to the **$ARGUMENTS** environment.

## Pre-deploy Checklist
1. All tests pass
2. Security scan clean
3. Docker images built and pushed

## Steps
1. Build and tag images with current git SHA
2. Push to GHCR
3. Update `gitops/overlays/$ARGUMENTS/kustomization.yaml` with new image tag
4. Verify ArgoCD sync status
5. Run smoke tests against deployed environment
