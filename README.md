<div align="center">

# ☁️ AWS Cloud Native AI SaaS — DevOps Engineering Portfolio

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

## 📌 About This Repository

This repository is a **personal portfolio reference** rebuilt from 1.5 years of hands-on production
experience as a DevOps Engineer on a Cloud Native AI SaaS platform running entirely on AWS.

The platform served enterprise clients with AI-powered features — inference services, model training
pipelines, data processing workflows — all running on Amazon EKS with GPU node groups, managed
through GitHub Actions and ArgoCD using GitOps principles.

> All code is rebuilt as an open-source reference. Production credentials, client data, and
> proprietary logic have been replaced with safe example values. The architecture patterns,
> issue resolutions, and engineering decisions are real — drawn from live production systems.

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AWS Cloud (eu-west-1)                         │
│                                                                         │
│   Developer Push                                                        │
│        │                                                                │
│        ▼                                                                │
│  ┌──────────────┐   CI: Build → Test → Scan → Push                     │
│  │   GitHub     │─────────────────────────────────▶  Amazon ECR        │
│  │   Repo       │   CD: ArgoCD GitOps                                  │
│  └──────────────┘         │                                             │
│                           ▼                                             │
│                    ┌─────────────┐                                      │
│                    │   ArgoCD    │  (GitOps — pulls from Git)           │
│                    └──────┬──────┘                                      │
│                           │                                             │
│                           ▼                                             │
│      ┌────────────────────────────────────────────┐                    │
│      │              Amazon EKS Cluster             │                    │
│      │                                             │                    │
│      │  ┌──────────────┐   ┌───────────────────┐  │                    │
│      │  │ System Pool  │   │  CPU Workload Pool │  │                    │
│      │  │ (m5.xlarge)  │   │  (m5.2xl SPOT)    │  │                    │
│      │  │ Prometheus   │   │  API Gateway       │  │                    │
│      │  │ Grafana      │   │  Data Processor    │  │                    │
│      │  │ Fluent Bit   │   │  Auth Service      │  │                    │
│      │  └──────────────┘   └───────────────────┘  │                    │
│      │                                             │                    │
│      │  ┌─────────────────────────────────────┐   │                    │
│      │  │   GPU Inference Pool                │   │                    │
│      │  │   g4dn.2xlarge — NVIDIA T4          │   │                    │
│      │  │   AI Model Serving (PyTorch)         │   │                    │
│      │  └─────────────────────────────────────┘   │                    │
│      └────────────────────────────────────────────┘                    │
│                          │                                              │
│          ┌───────────────┼────────────────────┐                        │
│          ▼               ▼                    ▼                        │
│      Amazon S3       Amazon RDS           Amazon SQS                   │
│      (Model          (PostgreSQL)         (Job Queue + DLQ)            │
│       Artifacts)                                                        │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │         Prometheus + Grafana + CloudWatch + PagerDuty            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔥 Production Issues Solved

| # | Issue | Category | MTTR | Outcome |
|---|-------|----------|------|---------|
| 1 | Terraform state corruption — concurrent apply destroys subnets | Infra | 45 min | Exact provider pinning, zero recurrence 14 months |
| 2 | AWS GPU quota breach during enterprise onboarding | Infra | 8 hrs | Proactive quota alarm at 70%, onboarding runbook |
| 3 | OIDC thumbprint drift freezes all GitHub Actions pipelines | CI/CD | 12 min | Weekly Lambda drift detector |
| 4 | Helm chart schema rename breaks production rollout | CI/CD | 90 sec | kubeval gate in CI, values migration checklist |
| 5 | GPU OOMKill cascade evicts Prometheus and Fluent Bit | Kubernetes | 35 min | PriorityClass + dedicated system node group |
| 6 | etcd overloaded by 28,000 uncleaned CronJob pods | Kubernetes | 2 hrs | API latency 9s → 300ms, OPA TTL enforcement |
| 7 | PyTorch GPU memory leak — OOMKill every 110 minutes | AI/ML | 2 weeks | Zero OOMKills for 7+ months |
| 8 | Silent model version mismatch serving wrong AI outputs | AI/ML | 90 sec | Golden dataset validation gate in CI |
| 9 | 340 noisy alerts caused missed P0 payment outage | Monitoring | 3 days | Alerts 85/wk → 11/wk, MTTA 22min → 4min |
| 10 | Over-permissive pod IAM (s3:* on *) in SOC2 audit | Security | 9 days | Blast radius -95%, SOC2 passed |
| 11 | $98,400/yr in zombie AWS resources | Cost | 72 hrs | Auto-expiry Lambda, $8,200/month saved |

---

## 🧰 Tech Stack

| Category | Tools |
|----------|-------|
| Cloud | AWS — EKS, EC2, S3, RDS, ECR, IAM, SQS, Lambda, CloudWatch |
| IaC | Terraform (exact pinning), Helm 3 |
| CI/CD | GitHub Actions, ArgoCD (GitOps), OIDC auth |
| Containers | Docker (BuildKit layer caching), Kubernetes 1.28 |
| AI/ML Infra | GPU node groups (g4dn/p3), Karpenter, PyTorch serving |
| Monitoring | Prometheus, Grafana, CloudWatch, PagerDuty, Fluent Bit |
| Security | Trivy, OPA Gatekeeper, IRSA (least-privilege), AWS Config |
| Languages | Python 3.11, Bash, YAML, HCL |

---

## 🏆 Engineering Principles Applied

```
✅  Provider versions pinned exactly — no ~> wildcards ever
✅  Every pod has a PodDisruptionBudget — OPA enforced
✅  Every CronJob has ttlSecondsAfterFinished — OPA enforced
✅  IRSA for pod IAM — no wildcard permissions anywhere
✅  OIDC for CI/CD auth — zero static AWS access keys
✅  Alerts are symptom-based not cause-based
✅  Blue-green standby scale-down is automated
✅  GPU memory limits account for CUDA overhead
✅  Every resource tagged: owner, environment, expires_on
```

---

## ⚠️ Disclaimer

Personal portfolio project. All code rebuilt from engineering knowledge as open-source reference.
No proprietary code, client data, or confidential information included.

---

<div align="center">

**[@kumarrajapuvvalla-bit](https://github.com/kumarrajapuvvalla-bit)**

*If this helped you — ⭐ Star it!*

</div>
