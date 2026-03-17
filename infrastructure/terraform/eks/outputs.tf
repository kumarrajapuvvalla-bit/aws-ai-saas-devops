# =============================================================================
# outputs.tf — EKS Module Outputs
# Consumed by: IAM module (OIDC ARN), monitoring module, CD pipeline
# =============================================================================

output "cluster_name" {
  description = "EKS cluster name — used by CI/CD to run aws eks update-kubeconfig"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS API server endpoint — used by kubectl and Helm"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "cluster_certificate_authority_data" {
  description = "Base64-encoded certificate authority data for the cluster"
  value       = module.eks.cluster_certificate_authority_data
  sensitive   = true
}

output "oidc_provider_arn" {
  description = "ARN of the OIDC provider — required for IRSA IAM role trust policies"
  value       = module.eks.oidc_provider_arn
}

output "oidc_provider_url" {
  description = "URL of the OIDC provider (without https://) — used in IAM condition keys"
  value       = module.eks.cluster_oidc_issuer_url
}

output "node_group_system_arn" {
  description = "ARN of the system node group (hosts Prometheus, Grafana, Fluent Bit)"
  value       = aws_eks_node_group.system.arn
}

output "node_group_gpu_arn" {
  description = "ARN of the GPU inference node group"
  value       = aws_eks_node_group.gpu_inference.arn
}

output "node_role_arn" {
  description = "IAM role ARN for EKS worker nodes — referenced in Karpenter provisioner"
  value       = aws_iam_role.node_role.arn
}

output "gpu_quota_alarm_arn" {
  description = "CloudWatch alarm ARN for GPU vCPU quota at 70% — fires before limit is hit"
  value       = aws_cloudwatch_metric_alarm.gpu_vcpu_quota.arn
}

output "cluster_version" {
  description = "Kubernetes version running on the cluster"
  value       = module.eks.cluster_version
}
