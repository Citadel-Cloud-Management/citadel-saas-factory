variable "region" {
  description = "Deployment region"
  type        = string
}

variable "instance_type" {
  description = "Instance size for staging"
  type        = string
  default     = "cx21"
}

variable "ssh_key_id" {
  description = "SSH key identifier"
  type        = string
}
