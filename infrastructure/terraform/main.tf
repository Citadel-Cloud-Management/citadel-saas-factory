# Citadel SaaS Factory — Infrastructure
# Cloud-agnostic: swap the provider block for any cloud or bare metal.
# Default uses null_resource as a placeholder — replace with your provider.

terraform {
  required_version = ">= 1.5.0"
}

variable "server_count" {
  type    = number
  default = 1
}

variable "ssh_public_key" {
  type    = string
  default = "~/.ssh/id_rsa.pub"
}

variable "domain" {
  type    = string
  default = "app.example.com"
}

variable "environment" {
  type    = string
  default = "staging"
}

module "server" {
  source   = "./modules/server"
  count    = var.server_count
  name     = "citadel-${var.environment}-${count.index}"
  ssh_key  = var.ssh_public_key
}

output "server_ids" {
  value = module.server[*].server_id
}
