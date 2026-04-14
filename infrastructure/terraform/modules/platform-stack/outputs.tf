output "platform_services" {
  description = "Deployed platform service endpoints"
  value = {
    argocd    = "https://argocd.${var.domain}"
    grafana   = "https://grafana.${var.domain}"
    keycloak  = "https://auth.${var.domain}"
    traefik   = "https://traefik.${var.domain}"
  }
}
