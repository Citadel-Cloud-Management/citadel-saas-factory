variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "citadel"
}

variable "image" {
  description = "OS image for compute instances"
  type        = string
  default     = "ubuntu-22.04"
}
