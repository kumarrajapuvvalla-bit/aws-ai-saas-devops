# =============================================================================
# variables.tf — EKS Module Input Variables
# =============================================================================

variable "aws_region" {
  description = "AWS region where the EKS cluster is deployed"
  type        = string
  default     = "eu-west-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "Must be a valid AWS region identifier (e.g. eu-west-1)."
  }
}

variable "project_name" {
  description = "Short project identifier used as a prefix for all resource names"
  type        = string
  default     = "ai-saas"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,20}$", var.project_name))
    error_message = "project_name must be lowercase alphanumeric with hyphens, 3-20 chars."
  }
}

variable "environment" {
  description = "Deployment environment: prod | staging | dev"
  type        = string

  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "environment must be one of: prod, staging, dev."
  }
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version. Must be explicitly set — never use 'latest'."
  type        = string
  default     = "1.28"
}

variable "vpc_id" {
  description = "ID of the VPC where the EKS cluster will be deployed"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for EKS node groups (spread across AZs)"
  type        = list(string)

  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "At least 2 private subnets required for multi-AZ node group placement."
  }
}

variable "system_node_instance_type" {
  description = "EC2 instance type for the system node group (Prometheus, Grafana, Fluent Bit)"
  type        = string
  default     = "m5.xlarge"
}

variable "system_node_desired" {
  description = "Desired number of system nodes. Minimum 2 for HA."
  type        = number
  default     = 2

  validation {
    condition     = var.system_node_desired >= 2
    error_message = "system_node_desired must be >= 2 for high availability."
  }
}

variable "gpu_node_instance_type" {
  description = "EC2 GPU instance type for the inference node group"
  type        = string
  default     = "g4dn.2xlarge"
}

variable "gpu_node_desired" {
  description = "Desired number of GPU inference nodes"
  type        = number
  default     = 2
}

variable "gpu_node_max" {
  description = "Hard cap on GPU node autoscaling to prevent runaway cost. See postmortem INC-002."
  type        = number
  default     = 10
}

variable "gpu_vcpu_quota_limit" {
  description = "Current AWS service quota for running on-demand GPU vCPUs. Used to calculate 70% alarm threshold."
  type        = number
  default     = 96
}

variable "cpu_spot_node_instance_types" {
  description = "EC2 instance types for CPU SPOT node group. Multiple types improve SPOT availability and reduce interruptions."
  type        = list(string)
  default     = ["m5.2xlarge", "m5a.2xlarge", "m5d.2xlarge"]
}

variable "sns_ops_topic_arn" {
  description = "SNS topic ARN for operational alerts (GPU quota breaches, cluster health warnings)"
  type        = string
}

variable "cluster_log_types" {
  description = "EKS control plane log types to send to CloudWatch Logs"
  type        = list(string)
  default     = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

variable "tags" {
  description = "Additional tags to merge with default resource tags (owner, environment, expires_on)"
  type        = map(string)
  default     = {}
}
