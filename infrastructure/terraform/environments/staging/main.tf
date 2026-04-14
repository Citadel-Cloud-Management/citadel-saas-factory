terraform {
  required_version = ">= 1.5.0"
}

module "network" {
  source      = "../../modules/network"
  environment = "staging"
  region      = var.region
}

module "compute" {
  source         = "../../modules/compute"
  environment    = "staging"
  instance_count = 2
  instance_type  = var.instance_type
  ssh_key_id     = var.ssh_key_id
}
