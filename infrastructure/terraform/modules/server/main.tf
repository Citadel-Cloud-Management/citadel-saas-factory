variable "name" { type = string }
variable "ssh_key" { type = string; default = "" }

resource "null_resource" "server" {
  triggers = {
    name = var.name
  }

  # Replace with actual provisioner for your infrastructure:
  # - Hetzner: hcloud_server
  # - DigitalOcean: digitalocean_droplet
  # - AWS: aws_instance
  # - Bare metal: use remote-exec provisioner with SSH

  provisioner "local-exec" {
    command = "echo 'Server ${var.name} provisioned (placeholder)'"
  }
}

output "server_id" {
  value = null_resource.server.id
}
