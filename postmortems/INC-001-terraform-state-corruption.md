# Postmortem: INC-001 — Terraform State Corruption

**Date:** Month 4 | **Severity:** P0 | **Duration:** 22 minutes | **Status:** Resolved ✅

## Summary
Two engineers ran `terraform apply` simultaneously. DynamoDB lock race condition allowed
a Terraform run with auto-upgraded `azurerm 3.44.0` provider to execute. Breaking schema
change in `azurerm_subnet` destroyed and recreated 6 production subnets. AKS nodes lost
network connectivity for 22 minutes during UK business hours.

## Timeline
| Time  | Event |
|-------|-------|
| 14:02 | Engineer A begins terraform apply for VPC peering |
| 14:07 | Engineer A session crashes — stale DynamoDB lock left |
| 14:08 | Engineer B apply proceeds — picks up azurerm 3.44.0 auto-upgrade |
| 14:11 | 6 subnets destroyed — AKS CNI loses subnet association |
| 14:12 | All pods Unknown — P0 alert fires |
| 14:19 | Corrected terraform apply runs — subnets recreated |
| 14:34 | AKS nodes recover — services restored |

## Root Cause
Provider pinned with `~> 3.0` — silently auto-accepted breaking minor version bump.

## Action Items
| Action | Status |
|--------|--------|
| Pin all providers to exact versions (= x.y.z) | ✅ Done |
| Enforce pipeline-only terraform applies | ✅ Done |
| Lambda alert if DynamoDB lock > 30 minutes | ✅ Done |
| Provider Upgrade Runbook | ✅ Done |

## Lessons Learned
- `~>` version constraints are dangerous — treat providers like app dependencies: pin exactly
- Local terraform apply in production is an org risk — automate it out of existence
- Stale state locks need monitoring
