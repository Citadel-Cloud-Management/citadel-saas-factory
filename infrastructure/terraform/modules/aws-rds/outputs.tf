output "cluster_endpoint" {
  value = aws_rds_cluster.main.endpoint
}

output "cluster_reader_endpoint" {
  value = aws_rds_cluster.main.reader_endpoint
}

output "cluster_port" {
  value = aws_rds_cluster.main.port
}

output "database_name" {
  value = aws_rds_cluster.main.database_name
}

output "security_group_id" {
  value = aws_security_group.rds.id
}

output "connection_string" {
  value     = "postgresql://${var.master_username}:${var.master_password}@${aws_rds_cluster.main.endpoint}:${aws_rds_cluster.main.port}/${aws_rds_cluster.main.database_name}"
  sensitive = true
}
