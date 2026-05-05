# Citadel SaaS Factory — AWS Staging Environment
# Cost-optimized staging with same architecture as production

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "citadel-staging-terraform-state"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "citadel-staging-terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "citadel"
      Environment = "staging"
      ManagedBy   = "terraform"
      Team        = "platform"
    }
  }
}

locals {
  project      = "citadel"
  environment  = "staging"
  cluster_name = "${local.project}-${local.environment}-eks"
  tags         = {
    Project     = local.project
    Environment = local.environment
  }
}

module "secrets" {
  source      = "../../modules/aws-secrets"
  project     = local.project
  environment = local.environment
  tags        = local.tags
}

module "vpc" {
  source             = "../../modules/aws-vpc"
  project            = local.project
  environment        = local.environment
  vpc_cidr           = "10.1.0.0/16"
  cluster_name       = local.cluster_name
  single_nat_gateway = true  # Cost savings for staging
  tags               = local.tags
}

module "eks" {
  source              = "../../modules/aws-eks"
  cluster_name        = local.cluster_name
  cluster_version     = "1.29"
  environment         = local.environment
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  public_subnet_ids   = module.vpc.public_subnet_ids
  kms_key_arn         = module.secrets.kms_key_arn
  node_instance_types = ["t3.medium"]
  capacity_type       = "SPOT"  # Cost savings
  node_desired_size   = 2
  node_min_size       = 1
  node_max_size       = 5
  tags                = local.tags
}

module "rds" {
  source                     = "../../modules/aws-rds"
  project                    = local.project
  environment                = local.environment
  vpc_id                     = module.vpc.vpc_id
  database_subnet_ids        = module.vpc.database_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  master_password            = var.db_master_password
  kms_key_arn                = module.secrets.kms_key_arn
  instance_count             = 1
  min_capacity               = 0.5
  max_capacity               = 8
  backup_retention_days      = 7
  deletion_protection        = false
  tags                       = local.tags
}

module "elasticache" {
  source                     = "../../modules/aws-elasticache"
  project                    = local.project
  environment                = local.environment
  vpc_id                     = module.vpc.vpc_id
  database_subnet_ids        = module.vpc.database_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  node_type                  = "cache.t4g.micro"
  num_cache_clusters         = 1
  auth_token                 = var.redis_auth_token
  kms_key_arn                = module.secrets.kms_key_arn
  snapshot_retention_days    = 1
  tags                       = local.tags
}

module "ecr" {
  source      = "../../modules/aws-ecr"
  project     = local.project
  kms_key_arn = module.secrets.kms_key_arn
  tags        = local.tags
}

module "s3" {
  source      = "../../modules/aws-s3"
  project     = local.project
  environment = local.environment
  kms_key_arn = module.secrets.kms_key_arn
  tags        = local.tags
}
