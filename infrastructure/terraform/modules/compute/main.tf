# Compute Module — Cloud-agnostic compute instances
# Adapt to your provider (AWS EC2, GCP GCE, Hetzner Cloud, DigitalOcean, etc.)

variable "instance_count" {
  description = "Number of compute instances"
  type        = number
  default     = 3
}

variable "instance_type" {
  description = "Instance size/type"
  type        = string
  default     = "cx21" # Hetzner example; change per provider
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "ssh_key_id" {
  description = "SSH key identifier for instance access"
  type        = string
}

# TODO: Replace with provider-specific resources
# resource "provider_instance" "node" {
#   count       = var.instance_count
#   type        = var.instance_type
#   name        = "citadel-${var.environment}-${count.index}"
#   ssh_keys    = [var.ssh_key_id]
# }

output "instance_ips" {
  description = "Public IP addresses of compute instances"
  value       = []
}
