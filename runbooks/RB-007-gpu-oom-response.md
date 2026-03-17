# RB-007 — Runbook: GPU Inference OOMKill Response

| Field | Value |
|---|---|
| **Alert** | `GPUMemoryLeakDetected` (P1) or pod `OOMKilled` events |
| **Service** | `inference/ai-inference` |
| **On-call rotation** | Platform DevOps |
| **Postmortem reference** | [INC-007](../postmortems/INC-007-gpu-oom-pytorch-memory-leak.md) |
| **Last reviewed** | 2025-04-01 |

---

## When to use this runbook

- PagerDuty alert: `GPUMemoryLeakDetected` (GPU memory growing >500MB in 30 min)
- PagerDuty alert: `InferenceServiceRestartingFrequently` (restart count > 3 in 1h)
- Manual observation: `kubectl get pods -n inference` shows `OOMKilled` status

**Estimated time to mitigate: 5–15 minutes**
**Root cause investigation: 30–120 minutes**

---

## Step 1 — Confirm the alert is real (2 min)

```bash
# Check current pod status
kubectl get pods -n inference -l app=ai-inference

# Look for OOMKilled in recent events
kubectl describe pods -n inference -l app=ai-inference | grep -A5 "OOMKilled\|Killed\|OOM"

# Check restart counts
kubectl get pods -n inference -o wide

# Check GPU memory usage RIGHT NOW
kubectl exec -n inference -it $(kubectl get pod -n inference -l app=ai-inference -o name | head -1) \
  -- nvidia-smi --query-gpu=memory.used,memory.free,memory.total --format=csv
```

Expected healthy output:
```
memory.used [MiB], memory.free [MiB], memory.total [MiB]
8192 MiB, 7808 MiB, 16160 MiB
```

If memory.used is >14,000 MiB and growing, the leak is active. Proceed to Step 2.

---

## Step 2 — Immediate mitigation: rolling restart (3 min)

A rolling restart will clear GPU memory. This causes ~45 seconds of degraded
capacity per pod (model reload time). With 2 replicas, full capacity returns
in ~90 seconds.

```bash
# Rolling restart — triggers one pod at a time, respects PDB (minAvailable: 2 is set, so
# this will wait for each new pod to be Ready before killing the old one)
kubectl rollout restart deployment/ai-inference -n inference

# Watch the rollout progress
kubectl rollout status deployment/ai-inference -n inference --timeout=5m

# Confirm new pods are healthy
kubectl get pods -n inference -l app=ai-inference -w
```

**After restart, monitor GPU memory for 30 minutes.** If it grows again, the
memory leak is still present in the current image. Proceed to Step 3.

---

## Step 3 — Identify if current image has the leak (10 min)

```bash
# Get the current image tag
kubectl get deployment ai-inference -n inference \
  -o jsonpath='{.spec.template.spec.containers[0].image}'

# Stream GPU memory metrics to terminal (watch for growth)
# Run this in a separate terminal and leave it open
kubectl exec -n inference -it \
  $(kubectl get pod -n inference -l app=ai-inference -o name | head -1) \
  -- watch -n 10 'nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader'

# Send a batch of test requests and watch memory
# If memory grows by >100MB per 100 requests, the leak is present
curl -s -X POST http://ai-inference.inference.svc/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test input"}' | jq .

# Check application logs for CUDA OOM errors
kubectl logs -n inference -l app=ai-inference --tail=100 | grep -i "oom\|cuda\|memory\|killed"
```

---

## Step 4 — If leak is confirmed: rollback to last stable image (5 min)

```bash
# Find the last stable image tag from deployment history
kubectl rollout history deployment/ai-inference -n inference

# Roll back to the previous revision
kubectl rollout undo deployment/ai-inference -n inference

# Confirm rollback succeeded
kubectl rollout status deployment/ai-inference -n inference --timeout=5m

# Verify the reverted image tag
kubectl get deployment ai-inference -n inference \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

After rollback, check GPU memory again. If stable, the leak was introduced
in the latest image. File a P1 issue with the application team and link INC-007.

---

## Step 5 — If rollback doesn't help: check memory limits

Sometimes the issue is not a leak but an under-provisioned memory limit
(e.g., model was updated with more parameters).

```bash
# Check current limits
kubectl get deployment ai-inference -n inference \
  -o jsonpath='{.spec.template.spec.containers[0].resources}' | jq .

# Check actual GPU memory required by running model
kubectl exec -n inference -it \
  $(kubectl get pod -n inference -l app=ai-inference -o name | head -1) \
  -- python3 -c "
import torch
print(f'Allocated: {torch.cuda.memory_allocated()/1024**3:.1f} GB')
print(f'Reserved:  {torch.cuda.memory_reserved()/1024**3:.1f} GB')
print(f'Max alloc: {torch.cuda.max_memory_allocated()/1024**3:.1f} GB')
"
```

If reserved > (limit - 4GB CUDA overhead), you need to increase limits.
Edit the deployment and increase `limits.memory` — remember: model size + 4GB CUDA + 2GB buffer.

---

## Step 6 — Escalation

If none of the above resolves the issue within 30 minutes:

1. Page the application team lead (PagerDuty: `app-team-oncall`)
2. Scale the deployment to 4 replicas (increases restart frequency but reduces
   per-restart impact)
3. Open a P0 incident if error rate > 5%

```bash
# Emergency scale-up to absorb restart churn
kubectl scale deployment ai-inference --replicas=4 -n inference
```

---

## Step 7 — Post-incident

After the incident is resolved:

- [ ] Confirm zero OOMKills for 30 minutes
- [ ] Update PagerDuty alert to resolved
- [ ] File a post-mortem if MTTR > 30 minutes or if a new root cause was found
- [ ] Update the [INC-007 postmortem](../postmortems/INC-007-gpu-oom-pytorch-memory-leak.md) if new information was discovered
- [ ] Verify the `GPUMemoryLeakDetected` alert is firing correctly for future incidents

---

## Quick Reference

| Command | Purpose |
|---|---|
| `kubectl get pods -n inference` | Check pod status and restart counts |
| `kubectl rollout restart deployment/ai-inference -n inference` | Rolling restart to clear GPU memory |
| `kubectl rollout undo deployment/ai-inference -n inference` | Roll back to previous image |
| `nvidia-smi` (inside pod) | Real-time GPU memory stats |
| `kubectl scale deployment ai-inference --replicas=4 -n inference` | Emergency scale-up |
