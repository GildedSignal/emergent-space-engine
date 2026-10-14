#!/usr/bin/env python3
"""Decisive arm: does the quantized law (one floor unit per event, per
representation.md thesis 2 / the error model) preserve sticky-trapping behaviour?

K = 1.2 standard map. Sticky ensemble: at 32 angles around the main island, the thin
chaotic band just outside the outermost KAM curve (found per angle by a capped-dwell
sweep), dwell measured as continuous stay within the enclosing disk r < 2.6 (the disk
contains the whole island including its diagonal bulges, so hovering orbits stay
counted). Cap 100k steps.
"""
import json
import time

import numpy as np

K = 1.2
TWO_PI = 2.0 * np.pi
CX, CP = np.pi, 0.0
R_DET = 2.6
CAP = 100000
RNG = np.random.default_rng(20261014)


def smap(x, p):
    p = p + K * np.sin(x)
    x = np.mod(x + p, TWO_PI)
    return x, np.mod(p, TWO_PI)


def td(a, b):
    d = np.abs(a - b)
    return np.minimum(d, TWO_PI - d)


def rad(x, p):
    return np.sqrt(td(x, CX) ** 2 + td(p, CP) ** 2)


def dwell(x0, p0, cap=CAP, quant=0.0, rng=None, noise=0.0):
    x = np.asarray(x0, float).copy(); p = np.asarray(p0, float).copy()
    esc = np.full(x.shape, -1, dtype=np.int64)
    alive = np.ones(x.shape, dtype=bool)
    for i in range(cap):
        x, p = smap(x, p)
        if quant > 0.0:
            x = np.round(x / quant) * quant
            p = np.round(p / quant) * quant
        if noise > 0.0:
            x = np.mod(x + rng.uniform(-noise / 2, noise / 2, x.shape), TWO_PI)
            p = np.mod(p + rng.uniform(-noise / 2, noise / 2, p.shape), TWO_PI)
        gone = alive & (rad(x, p) > R_DET)
        esc[gone] = i
        alive &= ~gone
        if not alive.any():
            break
    esc[alive] = cap
    return esc


t0 = time.time()
rep = {"K": K, "R_DET": R_DET, "cap": CAP}

# --- per-angle outermost KAM curve (capped dwell over 30k sweep), then the band
angles = np.linspace(0.05, TWO_PI - 0.05, 32)
band_x, band_y, band_dwell_scan = [], [], []
for th in angles:
    rs = np.linspace(1.0, R_DET - 0.01, 220)
    x = np.mod(CX + rs * np.cos(th), TWO_PI)
    p = np.mod(CP + rs * np.sin(th), TWO_PI)
    e = dwell(x, p, cap=30000)
    reg = e >= 30000
    if not reg.any():
        continue
    r_reg = rs[reg].max()
    sel = (rs > r_reg) & (rs <= r_reg + 0.06)
    band_x.append(x[sel]); band_y.append(p[sel])
    band_dwell_scan.append(e[sel])
bx = np.concatenate(band_x); by = np.concatenate(band_y)
print(f"[ensemble] n={len(bx)} ICs in the sticky bands beyond the outermost KAM curve")

# --- arms
d_true = dwell(bx, by)
arms = {"true": d_true}
for Q in (1e-4, 1e-3, 1e-2):
    arms[f"q{Q:.0e}"] = dwell(bx, by, quant=Q)
arms["noise1e-03"] = dwell(bx, by, noise=1e-3, rng=RNG)


def qrow(a):
    return {"p50": float(np.percentile(a, 50)), "p90": float(np.percentile(a, 90)),
            "p99": float(np.percentile(a, 99)), "max": float(a.max()),
            "capped": float((a >= CAP).mean())}


rep["dwell"] = {k: qrow(v) for k, v in arms.items()}
print("\n[dwell] continuous stay inside the island disk, cap %d" % CAP)
for k, v in rep["dwell"].items():
    print(f"  {k:10s} p50={v['p50']:7.0f} p90={v['p90']:7.0f} p99={v['p99']:7.0f} "
          f"max={v['max']:7.0f} capped={v['capped']:.3f}")

# --- shadow check: for ICs with a genuinely long TRUE dwell (>= p99 of true), is the
# quantized escape typical of true orbits started in the same Q-cell?
p99 = np.percentile(d_true, 99)
cand = np.where(d_true >= max(p99, 10 * np.median(d_true[d_true > 0]) if (d_true > 0).any() else 1))[0]
cand = cand[:80]
if len(cand) >= 5:
    dq = arms["q1e-03"][cand]
    rng2 = np.random.default_rng(7)
    mx = rng2.uniform(-5e-4, 5e-4, (len(cand), 32))
    mp = rng2.uniform(-5e-4, 5e-4, (len(cand), 32))
    d_cell = dwell(np.mod(bx[cand][:, None] + mx, TWO_PI),
                   np.mod(by[cand][:, None] + mp, TWO_PI))
    fracs = (d_cell > dq[:, None]).mean(axis=1)
    ratios = dq / np.median(d_cell, axis=1)
    rep["shadow"] = {"n": len(cand), "true_dwell_threshold": float(p99),
                     "median_frac_cell_dwell_longer": float(np.median(fracs)),
                     "median_ratio_quant_over_cell": float(np.median(ratios)),
                     "frac_orbits_ratio_lt_half": float((ratios < 0.5).mean()),
                     "frac_orbits_ratio_lt_0.1": float((ratios < 0.1).mean())}
    s = rep["shadow"]
    print(f"\n[shadow check] n={s['n']} (true dwell >= {s['true_dwell_threshold']:.0f})")
    print(f"  median fraction of same-cell true orbits dwelling longer than the "
          f"quantized law: {s['median_frac_cell_dwell_longer']:.3f}")
    print(f"  median ratio quantized/cell-median true dwell: "
          f"{s['median_ratio_quant_over_cell']:.4f}")
    print(f"  quantized escapes >=2x faster than cell median: "
          f"{s['frac_orbits_ratio_lt_half']:.3f}; >=10x faster: "
          f"{s['frac_orbits_ratio_lt_0.1']:.3f}")
else:
    print("\n[shadow check] too few long-dwell ICs (n=%d)" % len(cand))
    rep["shadow"] = {"n": len(cand)}

print(f"\nelapsed {time.time() - t0:.1f}s")
with open("dwell_out.json", "w") as f:
    json.dump(rep, f, indent=1)
