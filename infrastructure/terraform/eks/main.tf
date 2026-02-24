# =============================================================================
# EKS Cluster — Cloud Native AI SaaS Platform
# LESSON (Issue #1): Provider pinned EXACTLY — never use ~> in production.
# azurerm ~> 3.0 auto-upgraded to 3.44.0 and destroyed 6 production subnets.
# =============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 5.31.0"  # Pinned exactly — NEVER ~>
    }
  }

  backend "s3" {
    bucket         = "ai-saas-terraform-state"
    key            = "eks/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"  # Prevents concurrent apply (Issue #1)
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "ai-saas-platform"
      ManagedBy   = "terraform"
      Environment = var.environment
      Owner       = "devops-team"
    }
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.2.1"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = var.kubernetes_version
  vpc_id          = var.vpc_id
  subnet_ids      = var.private_subnet_ids

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = false
  enable_irsa                     = true  # Required for least-privilege pod IAM (Issue #10)
}

# System node group — monitoring pods go HERE (not on GPU nodes)
# LESSON (Issue #5): Prometheus/Fluent Bit were evicted from GPU nodes under
# memory pressure because they had no PriorityClass and no dedicated pool.
resource "aws_eks_node_group" "system" {
  cluster_name    = module.eks.cluster_name
  node_group_name = "${var.project_name}-system"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = var.private_subnet_ids
  instance_types  = ["m5.xlarge"]

  scaling_config {
    desired_size = 2
    min_size     = 2
    max_size     = 4
  }

  taint {
    key    = "dedicated"
    value  = "system"
    effect = "NO_SCHEDULE"
  }

  labels = { role = "system" }
}

# GPU node group — AI inference
# LESSON (Issue #2): Always set max — unbounded autoscaling caused quota breach.
resource "aws_eks_node_group" "gpu_inference" {
  cluster_name    = module.eks.cluster_name
  node_group_name = "${var.project_name}-gpu"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = var.private_subnet_ids
  instance_types  = ["g4dn.2xlarge"]
  capacity_type   = "ON_DEMAND"

  scaling_config {
    desired_size = 2
    min_size     = 1
    max_size     = 10  # Hard cap — prevents runaway GPU cost (Issue #11)
  }

  taint {
    key    = "nvidia.com/gpu"
    value  = "true"
    effect = "NO_SCHEDULE"
  }

  labels = { role = "gpu-inference", node-type = "gpu" }
}

# GPU quota alarm at 70% — fires BEFORE hitting the limit
# LESSON (Issue #2): We hit the quota wall during enterprise onboarding.
# 12,000 inference requests queued. 70% alarm gives weeks to act.
resource "aws_cloudwatch_metric_alarm" "gpu_vcpu_quota" {
  alarm_name          = "${var.project_name}-gpu-vcpu-quota-70pct"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ResourceCount"
  namespace           = "AWS/ServiceQuotas"
  period              = 3600
  statistic           = "Maximum"
  threshold           = var.gpu_vcpu_quota_limit * 0.70
  alarm_description   = "GPU vCPU quota >70% — request increase now, not during incident"
  alarm_actions       = [var.sns_ops_topic_arn]

  dimensions = {
    Service  = "Amazon Elastic Compute Cloud - Compute"
    Resource = "Running On-Demand P instances"
  }
}

output "cluster_name" { value = module.eks.cluster_name }
output "oidc_provider_arn" { value = module.eks.oidc_provider_arn }
