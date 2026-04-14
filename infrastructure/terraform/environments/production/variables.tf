variable "region" {
  description = "Deployment region"
  type        = string
}

variable "instance_type" {
  description = "Instance size for production"
  type        = string
  default     = "cx31"
}

variable "ssh_key_id" {
  description = "SSH key identifier"
  type        = string
}
