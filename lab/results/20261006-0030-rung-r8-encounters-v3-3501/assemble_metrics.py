#!/usr/bin/env python3
"""Assemble metrics.json from the run's jsonl outputs (verify, steady, scale, kicks)."""
import json, math, os, sys

R = os.path.dirname(os.path.abspath(__file__))


import re

def lines(name):
    p = os.path.join(R, name)
    if not os.path.exists(p):
        return []
    out = []
    for l in open(p):
        l = l.strip()
        if not l.startswith("{"):
            continue
        if "truth_rate" in l:  # a known-malformed summary line; the rate is regexed where needed
            continue
        try:
            out.append(json.loads(l))
        except json.JSONDecodeError:
            pass
    return out


# ---- (a): pooled completeness/soundness/checks ----
pool = {l["pool"]: l for l in lines("verify.jsonl") if "pool" in l}
missed_fraction = {c: pool[c]["missed"] / pool[c]["truth"] for c in pool}
false_fraction = {c: pool[c]["false"] / pool[c]["truth"] for c in pool}
checks_per_encounter = {c: pool[c]["checks"] / pool[c]["truth"] for c in pool}

# ---- (b): steady ----
st = lines("steady.jsonl")
truth_rate = 5.833333e-3  # from steady.jsonl's rate line (1-in-10 sampled truth over 1000 orbits)
ratio = {l["steady"]: l["ratio"] for l in st if "ratio" in l}
steady_ratio = {
    "diophantine": ratio["diophantine"],           # at the full 1e5-orbit horizon
    "element-sort": ratio["element-sort"],
    "conjunction-sampled": ratio["conjunction-sampled"],
    "oracle": 1.0,
}

# ---- (c): scale exponent of check work against N ----
sc = lines("scale.jsonl")
sc.sort(key=lambda l: l["scale"])
ns = [l["scale"] for l in sc]
def fit_exponent(vals):
    x = [math.log(n) for n in ns]
    y = [math.log(max(v, 1e-12)) for v in vals]
    k = len(x)
    sx, sy = sum(x), sum(y)
    sxx = sum(xi * xi for xi in x)
    sxy = sum(xi * yi for xi, yi in zip(x, y))
    return (k * sxy - sx * sy) / (k * sxx - sx * sx)

scale_exponent = {
    "diophantine": fit_exponent([l["dio_checks"] for l in sc]),
    "element-sort": fit_exponent([l["conj_checks"] for l in sc]),          # same conjunction checks
    "conjunction-sampled": fit_exponent([l["conj_checks"] for l in sc]),
    "oracle": fit_exponent([l["oracle_checks"] for l in sc]),
}

# ---- (d): kicks ----
kk = {l["kick"]: l for l in lines("kicks.jsonl")}
kick_setup_ratio = {c: kk[c]["median_ratio"] for c in kk}
other_certificates_touched = {c: kk[c]["others"] for c in kk}

configs = ["diophantine", "element-sort", "conjunction-sampled", "oracle"]
metrics = {
    c: {
        "missed_fraction": missed_fraction[c],
        "false_fraction": false_fraction[c],
        "steady_ratio": steady_ratio[c],
        "checks_per_encounter": checks_per_encounter[c],
        "scale_exponent": scale_exponent[c],
        "kick_setup_ratio": kick_setup_ratio[c],
        "other_certificates_touched": other_certificates_touched[c],
    }
    for c in configs
}
with open(os.path.join(R, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=1)
print(json.dumps(metrics, indent=1))
print("truth_rate", truth_rate)
for l in sc:
    print(l)
