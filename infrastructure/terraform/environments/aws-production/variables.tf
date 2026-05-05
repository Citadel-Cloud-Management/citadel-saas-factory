variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "db_master_password" {
  type      = string
  sensitive = true
}

variable "redis_auth_token" {
  type      = string
  sensitive = true
}

variable "domain" {
  type    = string
  default = "app.citadelcloudmanagement.com"
}
