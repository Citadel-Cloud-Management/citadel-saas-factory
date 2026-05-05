variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "db_master_password" {
  type      = string
  sensitive = true
}

variable "redis_auth_token" {
  type      = string
  sensitive = true
}
