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

> **Recruiter summary:** Production DevOps portfolio rebuilt from 1.5 years of hands-on experience running an enterprise AI SaaS platform on AWS EKS — covering Terraform IaC, Kubernetes GPU workloads, GitOps CI/CD with ArgoCD, and full-stack observability. All architecture patterns and incident resolutions are drawn from live production systems.

---

## 🎯 What This Project Demonstrates

- **Production AWS EKS infrastructure** — multi-node-group cluster with GPU, CPU SPOT, and system pools
- **Terraform infrastructure-as-code** — modular, exact-pinned, remote state with S3 backend and DynamoDB locking
- **Kubernetes GPU workloads** — NVIDIA T4 inference serving, PriorityClass scheduling, PodDisruptionBudgets
- **GitOps CI/CD pipelines** — GitHub Actions for CI, ArgoCD for GitOps delivery, OIDC-based zero-key authentication
- **Observability and incident response** — Prometheus, Grafana, CloudWatch, PagerDuty; alert noise reduced 87%
- **Security and cost optimization** — IRSA least-privilege IAM, OPA Gatekeeper guardrails, automated zombie resource cleanup saving $8.2k/month

---

## 🏆 Key DevOps Achievements

| Achievement | Impact |
|---|---|
| Redesigned 340-alert monitoring system | Reduced alert volume 85/week → 11/week; MTTA 22 min → 4 min |
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
| 1 | Terraform state corruption destroys subnets | Concurrent `terraform apply` without state lock | Exact provider pinning + DynamoDB state locking enforced | Zero recurrence for 14 months |
| 2 | AWS GPU quota breach during enterprise onboarding | No proactive quota visibility | Proactive CloudWatch alarm at 70% quota threshold + onboarding runbook | Prevented future breaches |
| 3 | OIDC thumbprint drift freezes all GitHub Actions pipelines | AWS rotated OIDC thumbprint silently | Weekly Lambda drift detector auto-reconciles thumbprint | 12-min MTTR → automated prevention |
| 4 | Helm chart schema rename breaks production rollout | No schema validation in CI | kubeval gate added to CI pipeline + values migration checklist | Schema regressions caught in 90 sec |
| 5 | GPU OOMKill cascade evicts Prometheus and Fluent Bit | No pod priority separation | PriorityClass for system pods + dedicated system node group | Zero cascade evictions |
| 6 | etcd overloaded by 28,000 uncleaned CronJob pods | No TTL on CronJob completion | OPA Gatekeeper enforces `ttlSecondsAfterFinished` on all CronJobs | API latency 9s → 300ms |
| 7 | PyTorch GPU memory leak — OOMKill every 110 minutes | CUDA memory not released between requests | Memory profiling + explicit `torch.cuda.empty_cache()` + limits tuned for CUDA overhead | Zero OOMKills for 7+ months |
| 8 | Silent model version mismatch serving wrong AI outputs | No validation gate on model artifact promotion | Golden dataset validation gate added to CI; mismatch fails build | Caught in 90 sec, before production |
| 9 | 340 noisy alerts caused missed P0 payment outage | Cause-based alerts, no severity triage | Rebuilt alert strategy: symptom-based, severity-tiered | Alerts 85/wk → 11/wk, MTTA 22→4 min |
| 10 | Over-permissive pod IAM (`s3:*` on `*`) flagged in SOC2 audit | Wildcard IAM roles on pods | IRSA least-privilege per-service-account; blast radius reduced 95% | SOC2 audit passed |
| 11 | $98,400/year in zombie AWS resources | No resource lifecycle policy | Auto-expiry Lambda tags resources at creation; cleans up on schedule | $8,200/month saved |

---

## 🧰 DevOps Skills Demonstrated

### Infrastructure as Code
Terraform modules with exact version pinning (no `~>` wildcards), remote S3 backend with DynamoDB locking, reusable EKS node group modules, Helm 3 chart management.

### Container Platforms
Amazon EKS 1.28, multi-pool node groups (GPU g4dn/p3, CPU SPOT m5.2xl, system m5.xl), Karpenter autoscaling, PodDisruptionBudgets, PriorityClass scheduling, resource limits accounting for CUDA overhead.

### CI/CD
GitHub Actions pipelines with OIDC authentication (zero static keys), multi-stage build → test → scan → push workflows, ArgoCD GitOps delivery, kubeval and Trivy gates in CI, Helm schema validation.

### Observability
Prometheus + Grafana dashboards, CloudWatch custom metrics, PagerDuty alerting, Fluent Bit log shipping, symptom-based alert design, alert noise reduction from 85/week to 11/week.

### Security
IRSA (IAM Roles for Service Accounts) with least-privilege per workload, OIDC-based CI/CD authentication, OPA Gatekeeper policy enforcement, Trivy image scanning, AWS Config compliance rules, SOC2 audit support.

### Cost Optimization
Automated zombie resource cleanup Lambda, SPOT instance node pools for non-critical workloads, blue-green standby scale-down automation, resource tagging policy (`owner`, `environment`, `expires_on`) enforced via OPA.

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
├── infrastructure/terraform/    # Terraform modules: EKS cluster, node groups, VPC, IAM, S3, RDS
├── kubernetes/                  # Kubernetes manifests: Deployments, Services, HPA, PDB, PriorityClass
├── monitoring/prometheus/       # Prometheus rules, Grafana dashboards, alerting configuration
├── pipelines/github-actions/    # GitHub Actions CI workflows: build, test, scan, push, deploy
├── postmortems/                 # Post-mortem documents for production incidents
├── runbooks/                    # Operational runbooks for on-call engineers
└── scripts/                     # Automation scripts: cleanup Lambda, drift detection, quota alarms
```

- **`infrastructure/terraform/`** — Modular Terraform with exact version pinning, S3 remote backend, DynamoDB locking, EKS node group configurations for GPU/CPU/system pools.
- **`kubernetes/`** — Production Kubernetes manifests including GPU workload deployments, PodDisruptionBudgets, PriorityClass definitions, HPA configs, and CronJob TTL policies.
- **`monitoring/prometheus/`** — Prometheus alerting rules (symptom-based, severity-tiered), Grafana dashboard definitions, PagerDuty integration config.
- **`pipelines/github-actions/`** — CI pipelines using OIDC auth (no static keys), multi-stage build/test/Trivy scan/ECR push workflows, kubeval schema gates.
- **`postmortems/`** — Structured post-mortem documents covering root cause analysis, timeline, and corrective actions for each production incident.
- **`runbooks/`** — Step-by-step operational runbooks for GPU quota management, OOMKill response, ArgoCD sync failures, and more.
- **`scripts/`** — Python/Bash automation: zombie resource cleanup Lambda, OIDC thumbprint drift detector, GPU quota alarm configuration.

---

## ⚙️ Example DevOps Workflows

### CI Pipeline (GitHub Actions)
```yaml
# On every PR: lint → unit test → Trivy security scan → kubeval schema check
on: [pull_request]
jobs:
  ci:
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: pytest tests/
      - name: Trivy image scan
        uses: aquasecurity/trivy-action@master
      - name: kubeval schema validation
        run: kubeval kubernetes/**/*.yaml
```

### Container Build Pipeline
```yaml
# On merge to main: build with BuildKit layer caching → push to ECR via OIDC
jobs:
  build-push:
    permissions:
      id-token: write   # OIDC — zero static AWS keys
    steps:
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/github-actions-ecr
      - name: Build and push to ECR
        uses: docker/build-push-action@v5
        with:
          cache-from: type=registry,ref=$ECR_URI:cache
          push: true
```

### Terraform Plan and Apply
```bash
# Remote backend with DynamoDB locking — prevents concurrent state corruption
terraform init -backend-config="bucket=tf-state-prod" \
               -backend-config="dynamodb_table=tf-locks"
terraform plan  -out=tfplan
terraform apply tfplan
```

### GitOps Deployment (ArgoCD)
```yaml
# ArgoCD Application manifest — Git is the single source of truth
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ai-inference-service
spec:
  source:
    repoURL: https://github.com/kumarrajapuvvalla-bit/aws-ai-saas-devops
    path: kubernetes/inference
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: inference
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 👀 What Recruiters Should Look At

| Area | Where to look | What it shows |
|---|---|---|
| **Terraform IaC** | `infrastructure/terraform/` | Modular design, exact pinning, remote state, EKS/VPC/IAM modules |
| **Kubernetes manifests** | `kubernetes/` | GPU workloads, PDB, PriorityClass, HPA, CronJob TTL policies |
| **CI/CD pipelines** | `pipelines/github-actions/` | OIDC auth, multi-stage CI, Trivy scan, kubeval gate |
| **Monitoring config** | `monitoring/prometheus/` | Symptom-based alert rules, Grafana dashboards, PagerDuty routing |
| **Incident engineering** | `postmortems/` | Structured RCA, corrective actions, runbook references |
| **Operational runbooks** | `runbooks/` | On-call procedures, GPU quota management, OOMKill response |
| **Automation scripts** | `scripts/` | Zombie cleanup Lambda, OIDC drift detector, quota alarms |

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
✅ Every pod has a PodDisruptionBudget — OPA enforced
✅ Every CronJob has ttlSecondsAfterFinished — OPA enforced
✅ IRSA for pod IAM — no wildcard permissions anywhere
✅ OIDC for CI/CD auth — zero static AWS access keys
✅ Alerts are symptom-based not cause-based
✅ Blue-green standby scale-down is automated
✅ GPU memory limits account for CUDA overhead
✅ Every resource tagged: owner, environment, expires_on
```

---

## ⚠️ Disclaimer

Personal portfolio project. All code rebuilt from engineering knowledge as open-source reference. No proprietary code, client data, or confidential information included.

[@kumarrajapuvvalla-bit](https://github.com/kumarrajapuvvalla-bit)

*If this helped you — ⭐ Star it!*
