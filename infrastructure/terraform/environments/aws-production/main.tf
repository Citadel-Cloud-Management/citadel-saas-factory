# Citadel SaaS Factory — AWS Production Environment
# Orchestrates all modules for production Fintech deployment

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "citadel-production-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "citadel-production-terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "citadel"
      Environment = "production"
      ManagedBy   = "terraform"
      Team        = "platform"
    }
  }
}

locals {
  project      = "citadel"
  environment  = "production"
  cluster_name = "${local.project}-${local.environment}-eks"

  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

# --- Secrets & KMS (must be first — other modules depend on KMS key) ---
module "secrets" {
  source      = "../../modules/aws-secrets"
  project     = local.project
  environment = local.environment
  tags        = local.tags
}

# --- VPC ---
module "vpc" {
  source             = "../../modules/aws-vpc"
  project            = local.project
  environment        = local.environment
  vpc_cidr           = var.vpc_cidr
  cluster_name       = local.cluster_name
  single_nat_gateway = false  # HA in production
  tags               = local.tags
}

# --- EKS ---
module "eks" {
  source              = "../../modules/aws-eks"
  cluster_name        = local.cluster_name
  cluster_version     = "1.29"
  environment         = local.environment
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  public_subnet_ids   = module.vpc.public_subnet_ids
  kms_key_arn         = module.secrets.kms_key_arn
  node_instance_types = ["t3.large"]
  capacity_type       = "ON_DEMAND"
  node_desired_size   = 3
  node_min_size       = 3
  node_max_size       = 15
  tags                = local.tags
}

# --- RDS Aurora PostgreSQL ---
module "rds" {
  source                     = "../../modules/aws-rds"
  project                    = local.project
  environment                = local.environment
  vpc_id                     = module.vpc.vpc_id
  database_subnet_ids        = module.vpc.database_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  master_password            = var.db_master_password
  kms_key_arn                = module.secrets.kms_key_arn
  instance_count             = 2
  min_capacity               = 2
  max_capacity               = 32
  backup_retention_days      = 30
  deletion_protection        = true
  tags                       = local.tags
}

# --- ElastiCache Redis ---
module "elasticache" {
  source                     = "../../modules/aws-elasticache"
  project                    = local.project
  environment                = local.environment
  vpc_id                     = module.vpc.vpc_id
  database_subnet_ids        = module.vpc.database_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  node_type                  = "cache.r7g.large"
  num_cache_clusters         = 3
  auth_token                 = var.redis_auth_token
  kms_key_arn                = module.secrets.kms_key_arn
  snapshot_retention_days    = 7
  tags                       = local.tags
}

# --- ECR ---
module "ecr" {
  source      = "../../modules/aws-ecr"
  project     = local.project
  kms_key_arn = module.secrets.kms_key_arn
  tags        = local.tags
}

# --- S3 ---
module "s3" {
  source      = "../../modules/aws-s3"
  project     = local.project
  environment = local.environment
  kms_key_arn = module.secrets.kms_key_arn
  tags        = local.tags
}
