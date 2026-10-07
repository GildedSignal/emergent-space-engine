#!/usr/bin/env python3
"""Follow-up: bench-max sampling noise, and RTF dip depth/duration vs rho."""
import json
import numpy as np

rng = np.random.default_rng(4242)
BASE, Q_BURST = 4.0, 0.005
MATCH = {"par15": None}

def draw(kind, alpha, k):
    if kind == "light":
        return rng.lognormal(np.log(6.0), 0.45, k)
    sc = MATCH.get(kind) or 1.0
    return sc * (1.0 - rng.random(k)) ** (-1.0 / alpha)

def stream(kind, alpha, n):
    w = BASE + rng.poisson(0.3, n) * 0.2
    hit = rng.random(n) < Q_BURST
    w[hit] += draw(kind, alpha, int(hit.sum()))
    return w

# calibrate par15 to the same bench p99.9 as light (as in probe_tail.py)
light = stream("light", None, 36_000)
ref = float(np.quantile(light, 0.999))
p0 = float(np.quantile(stream("par15", 1.5, 36_000), 0.999))
MATCH["par15"] = (ref - BASE) / (p0 - BASE)

out = {}
# (a) bench-max sampling noise over 30 replicate benches
for kind, alpha in [("light", None), ("par15", 1.5)]:
    mx = np.array([stream(kind, alpha, 36_000).max() for _ in range(30)])
    out[f"benchmax_{kind}"] = dict(mean=float(mx.mean()), sd=float(mx.std()),
                                   lo=float(mx.min()), hi=float(mx.max()))
    print(f"bench max {kind}: mean {mx.mean():6.1f}  sd {mx.std():6.1f} "
          f"range [{mx.min():.1f}, {mx.max():.1f}]")

# (b) RTF dip depth + duration at fixed budget policy
def rtf_run(kind, alpha, rho, n=200_000):
    B = float(stream(kind, alpha, 200_000).mean()) / rho
    backlog = 0.0
    rtfs, dips = [], []
    cur = 0
    for f in range(n):
        w = BASE + rng.poisson(0.3) * 0.2
        if rng.random() < Q_BURST:
            w += float(draw(kind, alpha, 1)[0])
        exec_ = min(B, backlog + w)
        backlog = backlog + w - exec_
        rtfs.append(exec_ / w if w > 0 else 1.0)          # delivered vs wanted
        if backlog > 1e-9:
            cur += 1
        elif cur:
            dips.append(cur); cur = 0
    rt = np.array(rtfs)
    return dict(rtf_p1=float(np.quantile(rt, 0.01)),
                rtf_p01=float(np.quantile(rt, 0.001)),
                dip_n=len(dips), dip_mean=float(np.mean(dips)) if dips else 0.0,
                dip_max=int(np.max(dips)) if dips else 0)

for kind, alpha in [("light", None), ("par15", 1.5)]:
    for rho in (0.5, 0.7, 0.9):
        r = rtf_run(kind, alpha, rho)
        out[f"rtf_{kind}_{rho}"] = r
        print(f"{kind:6s} rho={rho}  RTF p1={r['rtf_p1']:.3f} p0.1={r['rtf_p01']:.3f}  "
              f"dips={r['dip_n']} mean_len={r['dip_mean']:.1f} max_len={r['dip_max']}")

json.dump(out, open("probe_out2.json", "w"), indent=1)
