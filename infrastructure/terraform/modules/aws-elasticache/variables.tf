variable "project" {
  type    = string
  default = "citadel"
}

variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "database_subnet_ids" {
  type = list(string)
}

variable "allowed_security_group_ids" {
  type = list(string)
}

variable "node_type" {
  type    = string
  default = "cache.t4g.medium"
}

variable "num_cache_clusters" {
  type    = number
  default = 2
}

variable "auth_token" {
  type      = string
  sensitive = true
}

variable "kms_key_arn" {
  type = string
}

variable "snapshot_retention_days" {
  type    = number
  default = 7
}

variable "tags" {
  type    = map(string)
  default = {}
}
