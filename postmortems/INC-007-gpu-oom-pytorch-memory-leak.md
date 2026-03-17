# INC-007 — Post-Mortem: PyTorch GPU Memory Leak / OOMKill Every 110 Minutes

| Field | Value |
|---|---|
| **Incident ID** | INC-007 |
| **Severity** | P1 — Degraded (inference pods restarting every ~110 min) |
| **Duration** | 3 weeks (detected week 1, root cause found week 2, fixed week 3) |
| **Date Opened** | 2025-03-10 |
| **Date Resolved** | 2025-03-31 |
| **MTTR** | 2 weeks to root cause, 1 day to fix |
| **Services Affected** | `inference/ai-inference` (all replicas) |
| **On-Call Engineer** | Platform DevOps |

---

## Summary

The AI inference service was OOMKilled by Kubernetes every ~110 minutes.
Each restart caused ~45 seconds of unavailability while the model reloaded.
The root cause was a PyTorch CUDA memory leak: GPU memory was allocated
per-request but never released between requests. Memory accumulated steadily
until the pod exceeded its `limits.memory` and was killed.

The issue was compounded by a GPU memory limit that did not account for
CUDA's overhead allocation (4GB reserved on pod start). The effective usable
memory was 14GB - 4GB = 10GB — not the 14GB the team assumed.

---

## Timeline

| Time | Event |
|---|---|
| 2025-03-10 08:14 | PagerDuty alert: `InferenceServiceRestartingFrequently` — restart count > 5 in 24h |
| 2025-03-10 09:00 | On-call engineer acknowledges; assumes transient OOM, watches metrics |
| 2025-03-10 14:30 | Second restart cycle. OOMKill confirmed in pod events |
| 2025-03-11 | Increased memory limit from 14Gi → 16Gi. Restart interval extended to ~140 min |
| 2025-03-12 | Increased limit to 20Gi. Restart interval extended to ~180 min. Issue not resolved |
| 2025-03-14 | Escalated to senior DevOps. GPU memory profiling begins |
| 2025-03-17 | `nvidia-smi` captured inside running pod shows memory growing ~80MB/request |
| 2025-03-18 | Root cause confirmed: PyTorch not releasing CUDA tensors between requests |
| 2025-03-19 | Fix implemented: `torch.cuda.empty_cache()` after each request + CUDA alloc config |
| 2025-03-20 | Fix deployed to staging. No OOMKill for 72 hours |
| 2025-03-24 | Fix deployed to production. Monitoring period begins |
| 2025-03-31 | INC-007 closed. Zero OOMKills for 7 days in production |

---

## Root Cause Analysis

### Primary: PyTorch CUDA tensor leak

PyTorch keeps CUDA tensors in a memory pool by default. When using a
request-response serving pattern (not PyTorch Serve with built-in lifecycle),
tensors allocated during inference are not freed until the garbage collector
runs — which is infrequent for long-running processes.

```python
# BEFORE — memory leaked on every request
def predict(input_data: dict) -> dict:
    with torch.no_grad():
        inputs = tokenizer(input_data["text"], return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=512)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"output": result}
    # Problem: CUDA memory pool not returned to OS even after function returns
```

### Contributing: CUDA overhead not factored into memory limit

CUDA reserves ~4GB on the GPU when initialised. The pod limit was set to 14Gi
based on model size (12GB) alone. Effective usable memory was ~10GB, not 14GB.

| Component | Memory |
|---|---|
| Model weights (fp16) | ~6 GB |
| Model weights + inference state | ~12 GB |
| CUDA runtime overhead | ~4 GB |
| KV cache / attention buffers | ~2 GB |
| **Total required** | **~18 GB** |
| Limit at time of incident | 14 GB |

### Contributing: No GPU memory growth alert

There was no alert for sustained GPU memory growth rate. The OOMKill was the
first signal, by which time the pod was already dead.

---

## Fix

### Code fix — explicit cache clearing after each request

```python
# AFTER — memory released after every request
import gc
import torch

def predict(input_data: dict) -> dict:
    try:
        with torch.no_grad():
            inputs = tokenizer(input_data["text"], return_tensors="pt").to(device)
            outputs = model.generate(**inputs, max_new_tokens=512)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"output": result}
    finally:
        # Explicit cleanup — do not rely on GC timing for GPU memory
        del inputs
        del outputs
        torch.cuda.empty_cache()
        gc.collect()
```

### Environment fix — CUDA allocator config

Added to deployment manifest and container env:

```yaml
env:
  - name: PYTORCH_CUDA_ALLOC_CONF
    value: "max_split_size_mb:512"
```

### Infrastructure fix — correct memory limits

```yaml
resources:
  requests:
    memory: "14Gi"
    nvidia.com/gpu: "1"
  limits:
    memory: "20Gi"    # model(12GB) + CUDA(4GB) + buffer(4GB)
    nvidia.com/gpu: "1"
```

### Observability fix — GPU memory growth alert

Added to `monitoring/prometheus/alerting-rules.yaml`:

```yaml
- alert: GPUMemoryLeakDetected
  expr: increase(container_accelerator_memory_used_bytes{container="ai-inference"}[30m]) > 524288000
  for: 5m
  labels:
    severity: p1
  annotations:
    summary: "P1: GPU memory growing >500MB in 30min on {{ $labels.pod }}"
    description: "Likely memory leak. Pod will OOMKill in ~{{ $value | humanizeDuration }} without intervention."
```

---

## Impact

| Metric | Value |
|---|---|
| Duration of incidents | 3 weeks of recurring OOMKills |
| Restart interval before fix | ~110 minutes |
| Downtime per restart | ~45 seconds (model reload) |
| Estimated affected requests (3 weeks) | ~3,000+ interrupted inferences |
| OOMKills since fix | **0 in 7+ months** |

---

## Action Items

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Add `torch.cuda.empty_cache()` after every inference request | App team | ✅ Done (2025-03-19) |
| 2 | Set memory limits to account for CUDA overhead (model + 4GB + buffer) | DevOps | ✅ Done (2025-03-19) |
| 3 | Add GPU memory growth rate alert (>500MB/30min) | DevOps | ✅ Done (2025-03-20) |
| 4 | Add GPU memory headroom to deployment documentation | DevOps | ✅ Done |
| 5 | Add memory profiling step to CI before GPU deployment | App team | ⏳ In progress |
| 6 | Evaluate PyTorch Serve as managed serving runtime | Architecture | 🗒️ Backlog |

---

## Lessons Learned

1. **GPU memory ≠ requested memory.** CUDA always reserves overhead. Always
   add at least 4GB to your model's memory footprint when setting Kubernetes
   limits on GPU pods.

2. **OOMKill is a lagging indicator.** By the time Kubernetes OOMKills a pod,
   the user experience is already degraded. Alert on memory growth *rate*,
   not just on threshold breach.

3. **PyTorch CUDA memory pool is not GC-managed.** Long-running servers must
   explicitly call `torch.cuda.empty_cache()` or use context managers.

4. **"Increasing the limit fixed it" is not a root cause.** Three engineers
   increased memory limits during this incident without asking *why* it was
   leaking. Root cause analysis would have found the fix in day 1.

---

## References

- PyTorch CUDA memory management: https://pytorch.org/docs/stable/notes/cuda.html
- Kubernetes GPU resources: https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
- Fix commit: kubernetes/manifests/ai-inference-deployment.yaml (CUDA limits)
- Alert: monitoring/prometheus/alerting-rules.yaml (GPUMemoryLeakDetected)
- Runbook: runbooks/RB-007-gpu-oom-response.md
