# Network Module — Cloud-agnostic network configuration
# Adapt to your cloud provider (AWS VPC, GCP VPC, Hetzner Network, etc.)

variable "network_cidr" {
  description = "CIDR block for the network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

# TODO: Replace with provider-specific resources
# Example for a generic network setup:
# resource "provider_network" "main" {
#   cidr_block = var.network_cidr
#   name       = "citadel-${var.environment}"
# }

output "network_id" {
  description = "Network identifier"
  value       = "placeholder"
}

output "subnet_ids" {
  description = "Subnet identifiers"
  value       = []
}
