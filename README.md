<div align="center">

# ☁️ AWS Cloud Native AI SaaS Platform — DevOps Engineering Portfolio

[![AWS](https://img.shields.io/badge/AWS-EKS%20%7C%20EC2%20%7C%20S3%20%7C%20RDS%20%7C%20ECR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://terraform.io)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS%20%7C%20GPU%20Nodes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20ArgoCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io)

**Role:** DevOps Engineer · Cloud Native AI SaaS Platform · AWS
**Duration:** 1 Year 6 Months · Full-Time
**GitHub:** [@kumarrajapuvvalla-bit](https://github.com/kumarrajapuvvalla-bit)

</div>

---

> **Recruiter summary:** Production DevOps portfolio rebuilt from 1.5 years of hands-on experience running an enterprise AI SaaS platform on AWS EKS — covering Terraform IaC, Kubernetes GPU workloads, GitOps CI/CD with ArgoCD, and full-stack observability. All architecture patterns, scripts, and incident resolutions are drawn from live production systems.

---

## 🎯 What This Project Demonstrates

- **Production AWS EKS infrastructure** — multi-node-group cluster with GPU, CPU SPOT, and system pools
- **Terraform infrastructure-as-code** — modular, exact-pinned, typed variables with validation, remote S3 backend with DynamoDB locking
- **Kubernetes GPU workloads** — NVIDIA T4 inference serving, PriorityClass scheduling, CUDA-aware memory limits, IRSA service accounts
- **GitOps CI/CD pipelines** — GitHub Actions for CI + Terraform, ArgoCD for GitOps delivery, OIDC-based zero-key authentication
- **Observability and incident response** — Prometheus, Grafana, CloudWatch, PagerDuty; alert noise reduced 87%; post-mortems and runbooks
- **Security and cost optimization** — IRSA least-privilege IAM, OPA Gatekeeper guardrails, automated zombie resource cleanup saving $8.2k/month

---

## 🏆 Key DevOps Achievements

| Achievement | Impact |
|---|---|
| Redesigned 340-alert monitoring system | Alert volume 85/week → 11/week; MTTA 22 min → 4 min |
| Eliminated GPU OOMKill cascade | Zero OOMKill incidents for 7+ months |
| Automated zombie AWS resource cleanup | Saved $8,200/month ($98,400/year) |
| Implemented GitOps deployment model via ArgoCD | Deterministic, auditable deployments with Git as source of truth |
| Enforced infrastructure guardrails with OPA Gatekeeper | Every pod has PDB + TTL; blast radius reduced 95% on IAM audit |
| Introduced kubeval schema gate in CI | Helm schema regressions caught in 90 seconds before reaching production |
| Built proactive GPU quota alarm at 70% threshold | Prevented quota breach recurrence during enterprise onboarding |
| OIDC-based CI/CD authentication | Eliminated all static AWS access keys from pipelines |

---

## 🔥 Incident Engineering — Production Issues Solved

| # | Incident | Root Cause | Resolution | Impact |
|---|---|---|---|---|
| 1 | Terraform state corruption destroys subnets | Concurrent `terraform apply` without state lock | Exact provider pinning + DynamoDB state locking | Zero recurrence for 14 months |
| 2 | AWS GPU quota breach during enterprise onboarding | No proactive quota visibility | CloudWatch alarm at 70% quota threshold + onboarding runbook | Prevented future breaches |
| 3 | OIDC thumbprint drift freezes all GitHub Actions pipelines | AWS rotated OIDC thumbprint silently | Weekly Lambda drift detector auto-reconciles thumbprint | 12-min MTTR → automated prevention |
| 4 | Helm chart schema rename breaks production rollout | No schema validation in CI | kubeval gate in CI + values migration checklist | Schema regressions caught in 90 sec |
| 5 | GPU OOMKill cascade evicts Prometheus and Fluent Bit | No pod priority separation | PriorityClass for system pods + dedicated system node group | Zero cascade evictions |
| 6 | etcd overloaded by 28,000 uncleaned CronJob pods | No TTL on CronJob completion | OPA Gatekeeper enforces `ttlSecondsAfterFinished` | API latency 9s → 300ms |
| 7 | PyTorch GPU memory leak — OOMKill every 110 minutes | CUDA memory not released between requests | `torch.cuda.empty_cache()` + CUDA-aware limits | Zero OOMKills for 7+ months — [postmortem](postmortems/INC-007-gpu-oom-pytorch-memory-leak.md) |
| 8 | Silent model version mismatch serving wrong AI outputs | No validation gate on model artifact promotion | Golden dataset validation gate added to CI | Caught in 90 sec before production |
| 9 | 340 noisy alerts caused missed P0 payment outage | Cause-based alerts, no severity triage | Rebuilt alert strategy: symptom-based, severity-tiered | Alerts 85/wk → 11/wk, MTTA 22→4 min |
| 10 | Over-permissive pod IAM (`s3:*` on `*`) in SOC2 audit | Wildcard IAM roles on pods | IRSA least-privilege per service account | Blast radius -95%, SOC2 passed |
| 11 | $98,400/year in zombie AWS resources | No resource lifecycle policy | Auto-expiry Lambda + weekly audit script | $8,200/month saved |

---

## 🧰 DevOps Skills Demonstrated

### Infrastructure as Code
Terraform modules with exact version pinning (no `~>` wildcards), typed variables with `validation` blocks, remote S3 backend with DynamoDB locking, reusable EKS node group modules, `outputs.tf` consumed by downstream modules, `terraform.tfvars.example` for onboarding.

### Container Platforms
Amazon EKS 1.28, multi-pool node groups (GPU g4dn/p3, CPU SPOT m5.2xl, system m5.xl), Karpenter autoscaling, PodDisruptionBudgets, PriorityClass scheduling, CUDA-aware resource limits, init containers for model pre-loading, ArgoCD GitOps delivery with AppProject isolation.

### CI/CD
GitHub Actions pipelines with OIDC authentication (zero static keys), multi-stage build → test → scan → push workflows, Terraform plan/apply with PR plan comments, ArgoCD GitOps delivery, kubeval and Trivy gates in CI, Helm schema validation, concurrency locks to prevent parallel applies.

### Observability
Prometheus + Grafana dashboards, CloudWatch custom metrics, PagerDuty alerting with 3-tier severity model (P0/P1/P2), Fluent Bit log shipping, symptom-based alert design, alert noise reduction from 85/week to 11/week.

### Security
IRSA (IAM Roles for Service Accounts) with least-privilege per workload, OIDC-based CI/CD authentication, OPA Gatekeeper policy enforcement, Trivy image scanning, AWS Config compliance rules, SOC2 audit support, pod security context with non-root and read-only root filesystem.

### Cost Optimization
Automated zombie resource cleanup (RDS, EBS, Elastic IPs), SPOT instance node pools for non-critical workloads, blue-green standby scale-down automation, resource tagging policy (`owner`, `environment`, `expires_on`) enforced via OPA, GPU node hard cap to prevent runaway scaling.

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AWS Cloud (eu-west-1)                          │
│                                                                         │
│  Developer Push                                                         │
│       │                                                                 │
│       ▼                                                                 │
│  ┌──────────────┐   CI: Build → Test → Scan → Push                     │
│  │    GitHub    │─────────────────────────────────▶  Amazon ECR        │
│  │     Repo     │   CD: ArgoCD GitOps                                  │
│  └──────────────┘                                                       │
│                                │                                        │
│                                ▼                                        │
│                       ┌─────────────┐                                  │
│                       │   ArgoCD    │  (GitOps — pulls from Git)       │
│                       └──────┬──────┘                                  │
│                              │                                          │
│                              ▼                                          │
│  ┌────────────────────────────────────────────────┐                    │
│  │               Amazon EKS Cluster               │                    │
│  │                                                │                    │
│  │  ┌──────────────┐   ┌───────────────────────┐ │                    │
│  │  │ System Pool  │   │   CPU Workload Pool    │ │                    │
│  │  │ (m5.xlarge)  │   │  (m5.2xl SPOT)        │ │                    │
│  │  │  Prometheus  │   │   API Gateway          │ │                    │
│  │  │  Grafana     │   │   Data Processor       │ │                    │
│  │  │  Fluent Bit  │   │   Auth Service         │ │                    │
│  │  └──────────────┘   └───────────────────────┘ │                    │
│  │                                                │                    │
│  │  ┌─────────────────────────────────────────┐  │                    │
│  │  │           GPU Inference Pool             │  │                    │
│  │  │      g4dn.2xlarge — NVIDIA T4            │  │                    │
│  │  │      AI Model Serving (PyTorch)          │  │                    │
│  │  └─────────────────────────────────────────┘  │                    │
│  └────────────────────────────────────────────────┘                    │
│                                                                         │
│        ┌───────────────┬────────────────────┐                          │
│        ▼               ▼                    ▼                          │
│   Amazon S3       Amazon RDS           Amazon SQS                      │
│  (Model Artifacts) (PostgreSQL)    (Job Queue + DLQ)                   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │        Prometheus + Grafana + CloudWatch + PagerDuty             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Request flow:** Client request → API Gateway (EKS CPU pool) → Auth Service validates JWT → SQS job queue for async workloads → GPU Inference Pool processes AI requests → results persisted to S3/RDS → response returned. All deployments flow through GitHub Actions CI (build/test/scan/push to ECR) then ArgoCD pulls and applies manifests to EKS via GitOps.

---

## 📁 Repository Structure

```
aws-ai-saas-devops/
├── .github/
│   └── workflows/
│       └── terraform.yml              # Terraform plan (PR) + apply (merge) with OIDC auth
│
├── infrastructure/terraform/
│   ├── eks/
│   │   ├── main.tf                    # EKS cluster, node groups, GPU quota alarm
│   │   ├── variables.tf               # Typed inputs with descriptions and validation blocks
│   │   ├── outputs.tf                 # Cluster endpoint, OIDC ARN, node group ARNs
│   │   └── terraform.tfvars.example   # Annotated example values — copy to terraform.tfvars
│   └── iam/
│       └── main.tf                    # IRSA roles (least-privilege), GitHub Actions OIDC role
│
├── kubernetes/
│   ├── argocd/applications/
│   │   └── ai-inference-app.yaml      # ArgoCD Application + AppProject with RBAC isolation
│   ├── manifests/
│   │   ├── ai-inference-deployment.yaml  # GPU Deployment, Service, HPA, ServiceAccount
│   │   └── pdb-priority-network.yaml     # PodDisruptionBudgets, PriorityClass definitions
│   └── policies/
│       └── opa-constraints.yaml       # OPA Gatekeeper: enforce PDB, TTL, resource limits
│
├── monitoring/prometheus/
│   └── alerting-rules.yaml            # P0/P1/P2 symptom-based alert rules (85/wk → 11/wk)
│
├── pipelines/github-actions/
│   ├── ci-build.yml                   # Build → test → Trivy scan → push to ECR
│   └── cd-deploy.yml                  # Blue-green deploy via ArgoCD with auto standby cleanup
│
├── postmortems/
│   ├── INC-001-terraform-state-corruption.md
│   └── INC-007-gpu-oom-pytorch-memory-leak.md  # Full RCA with timeline, code diffs, lessons
│
├── runbooks/
│   ├── gpu-oomkill-troubleshooting.md
│   └── RB-007-gpu-oom-response.md     # Step-by-step on-call response with kubectl commands
│
└── scripts/
    └── zombie-resource-audit.py       # RDS/EBS/EIP scanner, Slack report, CI mode exit codes
```

### What each folder contains

**`.github/workflows/`** — GitHub Actions workflow files. `terraform.yml` runs `terraform plan` on every PR (posts output as a PR comment), and `terraform apply` only on merge to main — with OIDC authentication and DynamoDB concurrency locking.

**`infrastructure/terraform/eks/`** — EKS cluster Terraform module with typed, validated variables, full outputs file, exact provider pinning, system/GPU/SPOT node groups, and GPU quota alarm at 70%. Copy `terraform.tfvars.example` to get started.

**`infrastructure/terraform/iam/`** — IRSA role definitions scoped to exact S3 prefixes (fix for INC-010), plus the GitHub Actions OIDC trust policy that eliminated all static AWS keys.

**`kubernetes/argocd/`** — ArgoCD Application manifests defining GitOps sync configuration with automated prune, selfHeal, retry, and AppProject resource whitelisting for production isolation.

**`kubernetes/manifests/`** — Production Kubernetes workload definitions. The GPU inference deployment includes: init container for model download, CUDA-aware memory limits (model + 4GB overhead), node affinity, pod anti-affinity across AZs, liveness/readiness/startup probes, preStop lifecycle hook, and IRSA ServiceAccount.

**`kubernetes/policies/`** — OPA Gatekeeper constraint templates enforcing: every pod has a PDB, every CronJob has `ttlSecondsAfterFinished`, no wildcard IAM annotations.

**`monitoring/prometheus/`** — Prometheus alerting rules using 3-tier severity model. All alerts are symptom-based (not cause-based). Redesigned after INC-009 where 340 noisy alerts caused a missed P0 payment outage.

**`pipelines/github-actions/`** — CI/CD pipeline YAMLs. `ci-build.yml` runs lint → unit tests → Helm validation → Docker build → Trivy scan → ECR push. `cd-deploy.yml` implements blue-green deployment with automated standby scale-down.

**`postmortems/`** — Structured post-mortem documents with incident metadata, minute-by-minute timelines, root cause analysis, before/after code diffs, impact metrics, and action item tracking.

**`runbooks/`** — On-call runbooks with step-by-step diagnosis procedures, exact `kubectl` and `aws` CLI commands, escalation paths, and post-incident checklists.

**`scripts/`** — Python automation scripts. `zombie-resource-audit.py` scans for idle RDS instances, unattached EBS volumes, and unassociated Elastic IPs — posts a Slack report and exits non-zero in CI mode for automated alerting.

---

## ⚙️ Example DevOps Workflows

### CI Pipeline — `.github/workflows/` + `pipelines/github-actions/ci-build.yml`
```yaml
# On every PR: lint → test → Helm validate → build → Trivy scan → push to ECR
on: [pull_request]
jobs:
  lint-and-test:
    steps:
      - run: ruff check . && pytest tests/unit/ --cov-fail-under=80
  helm-validate:
    steps:
      - run: helm lint && helm template | kubeval --strict
  build-and-push:
    needs: [lint-and-test, helm-validate]
    permissions:
      id-token: write   # OIDC — zero static AWS keys
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: "${{ secrets.AWS_GITHUB_ACTIONS_ROLE_ARN }}" }
      - uses: docker/build-push-action@v5
        with: { cache-from: "type=s3,bucket=ai-saas-build-cache", push: true }
  security-scan:
    needs: [build-and-push]
    steps:
      - uses: aquasecurity/trivy-action@master
        with: { severity: "CRITICAL,HIGH", exit-code: "1" }
```

### Terraform Plan/Apply — `.github/workflows/terraform.yml`
```yaml
# Plan on PR (posts output as comment), apply on merge to main
jobs:
  plan:
    steps:
      - run: terraform init -backend-config="dynamodb_table=terraform-state-lock"
      - run: terraform plan -out=tfplan.binary -detailed-exitcode
      - uses: actions/github-script@v7   # Post plan output to PR as comment
  apply:
    if: github.ref == 'refs/heads/main'
    environment: production              # Requires manual approval gate
    steps:
      - run: terraform apply -auto-approve tfplan.binary
```

### GitOps Deployment — `kubernetes/argocd/applications/ai-inference-app.yaml`
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ai-inference
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/kumarrajapuvvalla-bit/aws-ai-saas-devops
    path: kubernetes/manifests
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: inference
  syncPolicy:
    automated:
      prune: true       # Remove resources deleted from Git
      selfHeal: true    # Re-apply if someone manually edits the cluster
```

### Zombie Resource Audit — `scripts/zombie-resource-audit.py`
```bash
# Weekly scheduled run — posts Slack report, exits non-zero if zombies found
python scripts/zombie-resource-audit.py \
  --region eu-west-1 \
  --idle-days 7 \
  --slack-webhook $SLACK_WEBHOOK \
  --output-json results.json \
  --ci-mode
```

---

## 👀 What Recruiters Should Look At

| Area | File / Folder | What it shows |
|---|---|---|
| **Terraform IaC** | [`infrastructure/terraform/eks/`](infrastructure/terraform/eks/) | Typed variables with validation, outputs, tfvars.example, exact pinning |
| **Kubernetes GPU workload** | [`kubernetes/manifests/ai-inference-deployment.yaml`](kubernetes/manifests/ai-inference-deployment.yaml) | CUDA limits, IRSA, init container, probes, anti-affinity, HPA |
| **ArgoCD GitOps** | [`kubernetes/argocd/applications/`](kubernetes/argocd/applications/) | Application + AppProject with production RBAC isolation |
| **CI/CD pipelines** | [`pipelines/github-actions/`](pipelines/github-actions/) | OIDC auth, Trivy scan, kubeval gate, blue-green deploy |
| **Terraform workflow** | [`.github/workflows/terraform.yml`](.github/workflows/terraform.yml) | Plan on PR, apply on merge, PR comment, concurrency lock |
| **Monitoring config** | [`monitoring/prometheus/alerting-rules.yaml`](monitoring/prometheus/alerting-rules.yaml) | P0/P1/P2 symptom-based alert rules |
| **Incident engineering** | [`postmortems/INC-007-gpu-oom-pytorch-memory-leak.md`](postmortems/INC-007-gpu-oom-pytorch-memory-leak.md) | Full RCA with timeline, code diffs, memory breakdown |
| **On-call runbook** | [`runbooks/RB-007-gpu-oom-response.md`](runbooks/RB-007-gpu-oom-response.md) | Step-by-step diagnosis with exact kubectl commands |
| **Automation scripts** | [`scripts/zombie-resource-audit.py`](scripts/zombie-resource-audit.py) | Multi-resource scanner, Slack integration, CI mode |
| **OPA policies** | [`kubernetes/policies/opa-constraints.yaml`](kubernetes/policies/opa-constraints.yaml) | Guardrails: PDB + TTL enforcement |

---

## 🧱 Tech Stack

| Category | Tools |
|---|---|
| Cloud | AWS — EKS, EC2, S3, RDS, ECR, IAM, SQS, Lambda, CloudWatch |
| IaC | Terraform (exact pinning), Helm 3 |
| CI/CD | GitHub Actions, ArgoCD (GitOps), OIDC authentication |
| Containers | Docker (BuildKit layer caching), Kubernetes 1.28 |
| AI/ML Infra | GPU node groups (g4dn/p3), Karpenter, PyTorch serving |
| Monitoring | Prometheus, Grafana, CloudWatch, PagerDuty, Fluent Bit |
| Security | Trivy, OPA Gatekeeper, IRSA (least-privilege), AWS Config |
| Languages | Python 3.11, Bash, YAML, HCL |

---

## 🏆 Engineering Principles Applied

```
✅ Provider versions pinned exactly — no ~> wildcards ever
✅ All Terraform variables have descriptions, types, and validation blocks
✅ Every pod has a PodDisruptionBudget — OPA enforced
✅ Every CronJob has ttlSecondsAfterFinished — OPA enforced
✅ IRSA for pod IAM — no wildcard permissions anywhere
✅ OIDC for CI/CD auth — zero static AWS access keys
✅ Alerts are symptom-based not cause-based
✅ Blue-green standby scale-down is automated
✅ GPU memory limits account for CUDA overhead (model + 4GB)
✅ Every resource tagged: owner, environment, expires_on
✅ Post-mortems written for every P1+ incident
✅ Runbooks linked from every monitoring alert
```

---

## ⚠️ Disclaimer

Personal portfolio project. All code rebuilt from engineering knowledge as open-source reference. No proprietary code, client data, or confidential information included.

[@kumarrajapuvvalla-bit](https://github.com/kumarrajapuvvalla-bit)

*If this helped you — ⭐ Star it!*
