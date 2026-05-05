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
  type        = list(string)
  description = "Security groups allowed to connect (EKS nodes)"
}

variable "database_name" {
  type    = string
  default = "citadel"
}

variable "master_username" {
  type    = string
  default = "citadel_admin"
}

variable "master_password" {
  type      = string
  sensitive = true
}

variable "engine_version" {
  type    = string
  default = "16.1"
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "min_capacity" {
  type    = number
  default = 0.5
}

variable "max_capacity" {
  type    = number
  default = 16
}

variable "backup_retention_days" {
  type    = number
  default = 30
}

variable "deletion_protection" {
  type    = bool
  default = true
}

variable "kms_key_arn" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
