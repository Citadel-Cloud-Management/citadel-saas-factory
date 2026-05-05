variable "project" {
  type    = string
  default = "citadel"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name for subnet tagging"
}

variable "single_nat_gateway" {
  type        = bool
  default     = true
  description = "Use single NAT gateway (cost savings for non-prod)"
}

variable "tags" {
  type    = map(string)
  default = {}
}
