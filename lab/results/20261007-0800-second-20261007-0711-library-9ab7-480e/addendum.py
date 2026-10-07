#!/usr/bin/env python3
"""Addendum: (1) Gaussian moment extrapolation vs the real hour's worst frame (the
probe's 27x-under claim, on the shipped stream); (2) per-seed frame-work anchors on
items_us (robust to descheduling between items); (3) alpha-hat jackknife over seeds;
(4) bench-window p99.9 spread (min/median/max); (5) the deep tail's census."""
import glob
import json

import numpy as np
from analysis import DT, load

def seeds_json(prefixes, field):
    return [load(p)[field].astype(float) for p in prefixes]

A = [f"data/A_s{s}" for s in range(1, 16)]
H = load("data/H_s99")
B = [f"data/B_s{s}" for s in range(1, 4 + 1)]
C = [f"data/C_s{s}" for s in range(1, 4 + 1)]
out = {}

# 1. Gaussian vs truth on the hour run (demand and per-frame work)
for field, name in (("ev", "demand"), ("items_us", "items_us")):
    x = H[field][300:].astype(float)
    mu, sd = x.mean(), x.std()
    q = mu + sd * np.sqrt(2) * __import__("scipy.special", fromlist=["erfcinv"]).erfcinv(2 / len(x))
    # erfcinv may be absent; fall back to the normal quantile via numpy's standard normal
    try:
        z = np.quantile(np.random.default_rng(0).standard_normal(10_000_000), 1 - 1 / len(x))
    except Exception:
        z = 4.8
    q = mu + sd * z
    out[f"gauss_vs_truth_{name}"] = {
        "mean": round(float(mu), 3), "sd": round(float(sd), 3),
        "gauss_1_in_n": round(float(q), 1), "truth_max": float(x.max()),
        "truth_over_gauss": round(float(x.max() / max(q, 1e-9)), 2),
    }

# 2. Per-seed frame-work anchors (items_us: sum of item times; descheduling-robust)
for name, ps in (("A", A), ("B", B), ("C", C)):
    per = [load(p)["items_us"][300:].astype(float) for p in ps]
    per = [x[x > 0] for x in per]
    out[f"{name}_items_us_per_seed_max_over_p99"] = [round(float(x.max() / max(np.quantile(x, 0.99), 1e-9)), 1) for x in per]
    out[f"{name}_items_us_per_seed_max_us"] = [round(float(x.max()), 0) for x in per]

# 3. alpha-hat jackknife over seeds (cost stream, k = top 1%)
def hill_at(x, f=0.01):
    xs = np.sort(x)
    n = len(xs)
    k = int(f * n)
    ln = np.log(xs)
    s = ln[n - k:].sum() - k * ln[n - k - 1]
    return k / s

tops = [load(p)["top1_us"][300:].astype(float) for p in A]
tops = [t[t > 0] for t in tops]
full = np.concatenate(tops)
out["A_cost_alpha_k1pct_full"] = round(hill_at(full), 3)
out["A_cost_alpha_k1pct_jackknife"] = sorted(round(hill_at(np.concatenate([t for i, t in enumerate(tops) if i != j])), 3) for j in range(len(tops)))

# 4. Bench-window p99.9 spread
for name, ps in (("A", A), ("B", B), ("C", C)):
    evs = np.concatenate([load(p)["ev"][300:].astype(float) for p in ps])
    w = 3300
    wp = np.array([np.quantile(evs[i * w:(i + 1) * w], 0.999) for i in range(len(evs) // w)])
    out[f"{name}_bench_p999_windows"] = {"n": int(len(wp)), "min": float(wp.min()), "median": round(float(np.median(wp)), 1), "max": float(wp.max())}

# 5. Deep-tail census (config A)
t = np.concatenate([load(p)["top1_us"][300:] for p in A])
tk = np.concatenate([load(p)["kind"][300:] for p in A])
m = t > 0
t, tk = t[m].astype(float), tk[m]
names = ["planet", "moon", "ship", "player", "fleet", "?"]
out["A_deep_tail"] = {}
for thr in (438, 1000, 3000):
    sel = tk[t >= thr]
    out["A_deep_tail"][f">={thr}us"] = {"count": int(len(sel)), "kinds": {names[k]: int((sel == k).sum()) for k in np.unique(sel)}}

print(json.dumps(out, indent=1))
json.dump(out, open("addendum.json", "w"), indent=1)
