# AWS ElastiCache Redis — Session store and hot data cache

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project}-${var.environment}-redis"
  subnet_ids = var.database_subnet_ids

  tags = var.tags
}

resource "aws_security_group" "redis" {
  name_prefix = "${var.project}-${var.environment}-redis-"
  vpc_id      = var.vpc_id
  description = "ElastiCache Redis security group"

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = var.allowed_security_group_ids
    description     = "Redis from EKS nodes"
  }

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-redis-sg"
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_elasticache_replication_group" "main" {
  replication_group_id = "${var.project}-${var.environment}"
  description          = "Redis cluster for ${var.project} ${var.environment}"

  engine               = "redis"
  engine_version       = "7.1"
  node_type            = var.node_type
  num_cache_clusters   = var.num_cache_clusters
  port                 = 6379
  parameter_group_name = aws_elasticache_parameter_group.main.name

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  kms_key_id                 = var.kms_key_arn
  auth_token                 = var.auth_token

  automatic_failover_enabled = var.num_cache_clusters > 1
  multi_az_enabled           = var.num_cache_clusters > 1

  snapshot_retention_limit = var.snapshot_retention_days
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-redis"
  })
}

resource "aws_elasticache_parameter_group" "main" {
  family = "redis7"
  name   = "${var.project}-${var.environment}-redis7"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }

  tags = var.tags
}
