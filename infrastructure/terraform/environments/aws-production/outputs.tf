output "vpc_id" {
  value = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "rds_endpoint" {
  value = module.rds.cluster_endpoint
}

output "redis_endpoint" {
  value = module.elasticache.primary_endpoint
}

output "ecr_backend_url" {
  value = module.ecr.backend_repository_url
}

output "ecr_frontend_url" {
  value = module.ecr.frontend_repository_url
}

output "s3_assets_bucket" {
  value = module.s3.assets_bucket_name
}

output "kms_key_arn" {
  value = module.secrets.kms_key_arn
}
