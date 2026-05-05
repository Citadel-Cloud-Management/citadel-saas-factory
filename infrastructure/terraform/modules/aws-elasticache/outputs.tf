output "primary_endpoint" {
  value = aws_elasticache_replication_group.main.primary_endpoint_address
}

output "reader_endpoint" {
  value = aws_elasticache_replication_group.main.reader_endpoint_address
}

output "port" {
  value = 6379
}

output "connection_string" {
  value     = "rediss://:${var.auth_token}@${aws_elasticache_replication_group.main.primary_endpoint_address}:6379/0"
  sensitive = true
}

output "security_group_id" {
  value = aws_security_group.redis.id
}
