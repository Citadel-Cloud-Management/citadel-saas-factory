terraform {
  required_version = ">= 1.5.0"
}

module "network" {
  source      = "../../modules/network"
  environment = "production"
  region      = var.region
}

module "compute" {
  source         = "../../modules/compute"
  environment    = "production"
  instance_count = 3
  instance_type  = var.instance_type
  ssh_key_id     = var.ssh_key_id
}
