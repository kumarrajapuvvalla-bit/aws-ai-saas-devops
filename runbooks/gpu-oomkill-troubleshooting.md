# Runbook: GPU OOMKill Troubleshooting

**Severity:** P0/P1 | **Related:** INC-005 — GPU OOMKill cascade

---

## Symptoms
- Pods in `OOMKilled` state in inference namespace
- Regular crash/restart cycle every ~110 minutes (= memory leak pattern)
- `Exit Code: 137` in pod events
- Monitoring pods evicted from GPU nodes

---

## Step 1 — Confirm OOMKill
```bash
kubectl describe pod <pod-name> -n inference | grep -A5 "Last State"
# Expected: Reason: OOMKilled, Exit Code: 137
```

## Step 2 — Is it cyclic (leak) or one-off (limit too low)?
```bash
kubectl get pods -n inference  # High restart count + regular interval = leak
kubectl exec -n inference <pod> -- python3 -c "
import torch
print(f'Allocated: {torch.cuda.memory_allocated()/1e9:.2f}GB')
print(f'Max: {torch.cuda.max_memory_allocated()/1e9:.2f}GB')
"
```

## Step 3 — Memory limit too low?
Rule of thumb: `limit = model_size_gb + 4GB CUDA overhead + 20% buffer`
Example: 12GB model → 12 + 4 + 3.2 = 19.2 → round to **20Gi**

## Step 4 — Fix memory leak (with ML team)
```python
# WRONG — tensors accumulate across requests
def inference(input_data):
    with torch.no_grad():
        return model(input_data)

# CORRECT — explicit cleanup after each request
def inference(input_data):
    try:
        with torch.no_grad():
            return model(input_data)
    finally:
        del input_data
        torch.cuda.empty_cache()  # Release CUDA cache
```

## Step 5 — Update Helm values permanently
```yaml
resources:
  limits:
    memory: "20Gi"       # Was 14Gi — didn't account for CUDA overhead
    nvidia.com/gpu: "1"
  requests:
    memory: "14Gi"
```

## Prevention Checklist
- [ ] GPU limits = model size + CUDA overhead (not just model size)
- [ ] Monitoring pods have `priorityClassName: system-critical`
- [ ] Monitoring DaemonSets target system node group (not GPU nodes)
- [ ] GPU memory growth rate alert active (>500MB in 30 min)
