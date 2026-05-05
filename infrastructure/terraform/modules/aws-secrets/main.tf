# AWS Secrets Manager + KMS — Secrets and encryption for Fintech compliance

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# KMS key for all encryption (RDS, ElastiCache, ECR, Secrets, EKS)
resource "aws_kms_key" "main" {
  description             = "Citadel ${var.environment} encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow EKS to use the key"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = merge(var.tags, {
    Name = "${var.project}-${var.environment}-kms"
  })
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.project}-${var.environment}"
  target_key_id = aws_kms_key.main.key_id
}

data "aws_caller_identity" "current" {}

# Application secrets
resource "aws_secretsmanager_secret" "database_url" {
  name       = "${var.project}/${var.environment}/database-url"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

resource "aws_secretsmanager_secret" "redis_url" {
  name       = "${var.project}/${var.environment}/redis-url"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

resource "aws_secretsmanager_secret" "stripe_secret_key" {
  name       = "${var.project}/${var.environment}/stripe-secret-key"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

resource "aws_secretsmanager_secret" "stripe_webhook_secret" {
  name       = "${var.project}/${var.environment}/stripe-webhook-secret"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

resource "aws_secretsmanager_secret" "jwt_secret" {
  name       = "${var.project}/${var.environment}/jwt-secret"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

resource "aws_secretsmanager_secret" "anthropic_api_key" {
  name       = "${var.project}/${var.environment}/anthropic-api-key"
  kms_key_id = aws_kms_key.main.arn

  tags = var.tags
}

output "kms_key_arn" {
  value = aws_kms_key.main.arn
}

output "kms_key_id" {
  value = aws_kms_key.main.key_id
}

output "secret_arns" {
  value = {
    database_url          = aws_secretsmanager_secret.database_url.arn
    redis_url             = aws_secretsmanager_secret.redis_url.arn
    stripe_secret_key     = aws_secretsmanager_secret.stripe_secret_key.arn
    stripe_webhook_secret = aws_secretsmanager_secret.stripe_webhook_secret.arn
    jwt_secret            = aws_secretsmanager_secret.jwt_secret.arn
    anthropic_api_key     = aws_secretsmanager_secret.anthropic_api_key.arn
  }
}

variable "project" {
  type    = string
  default = "citadel"
}

variable "environment" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
