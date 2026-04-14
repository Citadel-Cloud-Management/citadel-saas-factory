# Platform Stack Module — Deploy platform services via Helm
# ArgoCD, Linkerd, Traefik, Prometheus, Grafana, Loki, Vault, Keycloak

variable "kubeconfig_path" {
  description = "Path to kubeconfig"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

# Platform services are deployed via ArgoCD ApplicationSets
# This module bootstraps ArgoCD itself

# TODO: Use helm_release resources or kubectl_manifest
# resource "helm_release" "argocd" {
#   name       = "argocd"
#   repository = "https://argoproj.github.io/argo-helm"
#   chart      = "argo-cd"
#   namespace  = "argocd"
# }

output "argocd_url" {
  description = "ArgoCD dashboard URL"
  value       = "https://argocd.${var.environment}.local"
}
