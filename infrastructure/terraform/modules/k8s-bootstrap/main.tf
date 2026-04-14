# K3s Bootstrap Module — Install and configure K3s cluster

variable "server_ip" {
  description = "IP address of the K3s server node"
  type        = string
}

variable "agent_ips" {
  description = "IP addresses of K3s agent nodes"
  type        = list(string)
  default     = []
}

variable "k3s_version" {
  description = "K3s version to install"
  type        = string
  default     = "v1.29.0+k3s1"
}

# K3s is installed via Ansible (see playbooks/bootstrap-node.yml)
# This module manages the cluster state after provisioning

output "kubeconfig_path" {
  description = "Path to the kubeconfig file"
  value       = "/etc/rancher/k3s/k3s.yaml"
}

output "cluster_endpoint" {
  description = "K3s API server endpoint"
  value       = "https://${var.server_ip}:6443"
}
