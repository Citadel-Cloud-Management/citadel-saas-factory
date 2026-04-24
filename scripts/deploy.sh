#!/bin/bash
set -euo pipefail

ENVIRONMENT="${1:-staging}"
IMAGE_TAG="${2:-$(git rev-parse --short HEAD)}"
REGISTRY="ghcr.io/Citadel-Cloud-Management/citadel-saas-factory"

echo "Deploying to ${ENVIRONMENT} (tag: ${IMAGE_TAG})..."

# Build and push images
echo "Building backend image..."
docker build -t "${REGISTRY}/backend:${IMAGE_TAG}" -f backend/Dockerfile backend/
docker push "${REGISTRY}/backend:${IMAGE_TAG}"

echo "Building frontend image..."
docker build -t "${REGISTRY}/frontend:${IMAGE_TAG}" -f frontend/Dockerfile frontend/
docker push "${REGISTRY}/frontend:${IMAGE_TAG}"

# Apply GitOps manifests
echo "Applying GitOps manifests for ${ENVIRONMENT}..."
if command -v kubectl >/dev/null 2>&1; then
  kubectl apply -k "gitops/overlays/${ENVIRONMENT}"
  echo "Deployment applied. ArgoCD will sync automatically."
else
  echo "kubectl not found — apply manually or push to trigger ArgoCD sync"
fi

echo "Deploy to ${ENVIRONMENT} complete (${IMAGE_TAG})"
