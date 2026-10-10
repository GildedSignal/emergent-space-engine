#!/usr/bin/env python3
"""Probe: e-domain of the phase-neighbour encounter certificate.

Fleet of n coplanar bodies on one orbit (a~1 AU), spreads in (a, e, varpi),
mean anomalies uniform. Truth: all pairs ever within R_enc over T, found by
KD-tree per sampled epoch (proximity episodes last >> the sample step, checked
below). Metric: partner rank in mean-anomaly order at t=0 (the order is fixed:
mean motions differ by <= 3*da/a ~ 3e-4, drift over T << one spacing in family A).

Units: AU, yr, mu = 4*pi^2 (a=1 -> P=1 yr, mean motion nn=2pi).
"""
import json, sys, time
import numpy as np
from scipy.spatial import cKDTree

MU = 4 * np.pi**2

def make_fleet(n, e0, da, de, dw, seed):
    r = np.random.default_rng(seed)
    a = 1.0 + r.uniform(-da, da, n)
    e = np.clip(e0 + r.uniform(-de, de, n), 0.0, 0.999)
    w = r.uniform(-dw, dw, n)
    M0 = r.uniform(0, 2 * np.pi, n)
    return a, e, w, M0

def positions(a, e, w, M):
    # Kepler: E from M (Newton, robust start), then rotate by varpi
    E = M + e * np.sin(M)
    for _ in range(30):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    xo = a * (np.cos(E) - e)
    yo = a * np.sqrt(1 - e**2) * np.sin(E)
    c, s = np.cos(w), np.sin(w)
    return xo * c - yo * s, xo * s + yo * c

def sweep(cfg):
    n, e0, da, de, dw, R, T, K, seed = cfg["n"], cfg["e0"], cfg["da"], cfg["de"], cfg["dw"], cfg["R"], cfg["T"], cfg["K"], cfg["seed"]
    a, e, w, M0 = make_fleet(n, e0, da, de, dw, seed)
    nn = np.sqrt(MU / a**3)
    order = np.argsort(M0)              # M-order at t0; drift << one spacing (family A)
    pos_in_order = np.empty(n, dtype=int)
    pos_in_order[order] = np.arange(n)
    pairs = set()
    where = []                          # (r_mid, v_mid) at first detection, for locus stats
    t0 = time.time()
    for k in range(K):
        t = T * k / K
        M = (M0 + nn * t) % (2 * np.pi)
        x, y = positions(a, e, w, M)
        tree = cKDTree(np.column_stack([x, y]))
        found = tree.query_pairs(R)
        if found:
            pairs.update(found)
            if not where and k > 0:     # first epoch with contacts: record locus
                ii = np.array([i for i, j in found]); jj = np.array([j for i, j in found])
                r = np.hypot(0.5 * (x[ii] + x[jj]), 0.5 * (y[ii] + y[jj]))
                where = r.tolist()
    if pairs:
        ii = np.array([i for i, j in pairs]); jj = np.array([j for i, j in pairs])
        d = np.abs(pos_in_order[ii] - pos_in_order[jj])
        ranks = np.minimum(d, n - d)      # circular rank in mean-anomaly order
    else:
        ranks = np.array([0])
    return {
        "cfg": {k: v for k, v in cfg.items()},
        "n_pairs": len(pairs),
        "enc_per_body": 2 * len(pairs) / n,
        "p999_rank": float(np.quantile(ranks, 0.999)),
        "max_rank": int(ranks.max()),
        "aphelion_frac": (float(np.mean([rr / (1 + e0) > 0.9 for rr in where])) if where else None),
        "mean_rank": float(ranks.mean()),
        "first_contact_r_aphelion_frac": ([float(rr / (1 + e0)) for rr in where][:50] if where else []),
        "wall_s": round(time.time() - t0, 2),
    }

def famA(e0, seed, n=3000, R=3e-3, da=1e-6, de=1e-6, dw=1e-6, T=2.0, K=240):
    return dict(n=n, e0=e0, da=da, de=de, dw=dw, R=R, T=T, K=K, seed=seed)

def famB(e0, seed, n=3000, R=1.5e-4, da=1e-4, de=1e-4, dw=1e-4, T=10.0, K=2000):
    return dict(n=n, e0=e0, da=da, de=de, dw=dw, R=R, T=T, K=K, seed=seed)

runs = []
# Family A main sweep, 3 seeds each (report max over seeds: worst case rules)
for e0 in [0.0, 0.3, 0.6, 0.77, 0.9]:
    for seed in [11, 12, 13]:
        runs.append(("A", famA(e0, seed)))
# Held-out: H3 e=0.95; H1 R doubled at e=0.9; H2 n doubled at e=0; negative R=0.02
for seed in [11, 12, 13]:
    runs.append(("H3", famA(0.95, seed)))
    runs.append(("H1", famA(0.9, seed, R=6e-3)))
    runs.append(("H2", famA(0.0, seed, n=6000)))
    runs.append(("NEG", famA(0.9, seed, R=2e-2)))
# Family B: drift regime (the gold's), circular reproduce + e check
for e0 in [0.0, 0.6, 0.9]:
    for seed in [21, 22, 23]:
        runs.append(("B", famB(e0, seed)))

out = []
for tag, cfg in runs:
    res = sweep(cfg); res["family"] = tag
    out.append(res)
    print(tag, "e=", cfg["e0"], "R=", cfg["R"], "n=", cfg["n"], "seed=", cfg["seed"],
          "-> pairs", res["n_pairs"], "max_rank", res["max_rank"],
          "p999", round(res["p999_rank"], 2), "enc/body", round(res["enc_per_body"], 3),
          "wall", res["wall_s"], flush=True)

with open(sys.argv[1] if len(sys.argv) > 1 else "probe_out.json", "w") as f:
    json.dump(out, f, indent=1)
print("done")
