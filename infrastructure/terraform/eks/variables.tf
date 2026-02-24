variable "aws_region"           { type = string; default = "eu-west-1" }
variable "project_name"         { type = string; default = "ai-saas" }
variable "environment"          { type = string }
variable "kubernetes_version"   { type = string; default = "1.28" }
variable "vpc_id"               { type = string }
variable "private_subnet_ids"   { type = list(string) }
variable "gpu_vcpu_quota_limit" { type = number; default = 96 }
variable "sns_ops_topic_arn"    { type = string }
