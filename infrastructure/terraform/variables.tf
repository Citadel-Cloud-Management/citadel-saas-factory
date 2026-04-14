variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Deployment region (provider-specific)"
}

variable "server_size" {
  type        = string
  default     = "medium"
  description = "Server size: small, medium, large"
}
