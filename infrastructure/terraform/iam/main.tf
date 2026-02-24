# =============================================================================
# IAM — IRSA Roles (Least Privilege Per Pod)
# LESSON (Issue #10): AI data pod had s3:* on Resource:"*" — full account access.
# Found in SOC2 audit. Every pod gets ONLY what it needs, scoped to exact ARNs.
# =============================================================================

# AI Inference — read model artifacts from specific S3 prefix ONLY
resource "aws_iam_role" "inference" {
  name               = "${var.project_name}-inference-irsa"
  assume_role_policy = data.aws_iam_policy_document.inference_assume.json
}

data "aws_iam_policy_document" "inference_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }
    condition {
      test     = "StringEquals"
      variable = "${var.oidc_provider}:sub"
      values   = ["system:serviceaccount:inference:ai-inference"]
    }
  }
}

data "aws_iam_policy_document" "inference_permissions" {
  statement {
    sid     = "ReadModelArtifacts"
    effect  = "Allow"
    actions = ["s3:GetObject", "s3:GetObjectVersion"]
    # ONLY specific bucket and prefix — not s3:* on Resource:* (Issue #10 fix)
    resources = [
      "arn:aws:s3:::${var.model_artifacts_bucket}/models/*",
      "arn:aws:s3:::${var.model_artifacts_bucket}/checkpoints/*",
    ]
  }
}

resource "aws_iam_policy" "inference" {
  name   = "${var.project_name}-inference-policy"
  policy = data.aws_iam_policy_document.inference_permissions.json
}

resource "aws_iam_role_policy_attachment" "inference" {
  role       = aws_iam_role.inference.name
  policy_arn = aws_iam_policy.inference.arn
}

# GitHub Actions OIDC role — no static credentials (Issue #3 fix)
data "aws_iam_policy_document" "github_actions_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:kumarrajapuvvalla-bit/aws-ai-saas-devops:*"]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "${var.project_name}-github-actions"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume.json
}

data "aws_caller_identity" "current" {}

output "inference_role_arn"      { value = aws_iam_role.inference.arn }
output "github_actions_role_arn" { value = aws_iam_role.github_actions.arn }
