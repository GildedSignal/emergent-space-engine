#!/usr/bin/env python3
"""Falsifier for representation.md thesis 2's shadowing clause.

"Even chaos has invariant statistics, and by the shadowing lemma a deterministic law
with the right statistics is a true orbit of nearby initial conditions."

Model: standard map (area-preserving; KAM islands + chaotic sea + sticky layers), the
universal mixed-phase-space Hamiltonian case. The engine analogue: the dense order is
chaos "the normal case"; sticky orbits are temporary captures / resonant trappings
(co-orbital fleets live on islands in the rotating frame).

Law: exact float64 map. Quantized law (the doc's error model, one floor unit per
event): state rounded to a Q-grid every step. Shadowing proxy (Sauer-Yorke noise
test): i.i.d. +/-Q/2 noise each step; saturation of the ensemble deviation at a
bounded multiple of Q = shadowable; unbounded growth = shadowing breakdown.

Runtime budget: < 60 s, float64, numpy-vectorized over ensembles.
"""
import json
import time

import numpy as np

K = 1.2
TWO_PI = 2.0 * np.pi
CX, CP = np.pi, 0.0          # elliptic fixed point for K>0
R_DET = 1.1                  # dwell disk radius around the island (scan arm)
R_NEAR = 1.6                 # "near the island" for classification
RNG = np.random.default_rng(20261014)


def smap(x, p):
    p = p + K * np.sin(x)
    x = np.mod(x + p, TWO_PI)
    return x, np.mod(p, TWO_PI)


def torus_d(a, b):
    d = np.abs(a - b)
    return np.minimum(d, TWO_PI - d)


def rad(x, p):
    return np.sqrt(torus_d(x, CX) ** 2 + torus_d(p, CP) ** 2)


def orbit(x0, p0, n, quant=0.0):
    x = np.asarray(x0, dtype=np.float64).copy()
    p = np.asarray(p0, dtype=np.float64).copy()
    out_x = np.empty((n,) + x.shape)
    out_p = np.empty((n,) + p.shape)
    for i in range(n):
        x, p = smap(x, p)
        if quant > 0.0:
            x = np.round(x / quant) * quant
            p = np.round(p / quant) * quant
        out_x[i] = x
        out_p[i] = p
    return out_x, out_p


def lyap(x0, p0, n, d0=1e-9):
    x = np.asarray(x0, float).copy(); p = np.asarray(p0, float).copy()
    dx = np.full_like(x, d0 / np.sqrt(2)); dp = np.full_like(p, d0 / np.sqrt(2))
    s = 0.0
    for _ in range(n):
        x2, p2 = smap(x + dx, p + dp)
        x, p = smap(x, p)
        ex = torus_d(x2, x); ep = torus_d(p2, p)
        d = np.sqrt(ex**2 + ep**2)
        s += np.log(d / d0)
        dx = ex * (d0 / d); dp = ep * (d0 / d)
    return s / n


def dwell(x0, p0, n, quant=0.0, rng=None, noise=0.0, r_det=R_DET):
    """First-escape time from the disk r<r_det around the island (n if never)."""
    x = np.asarray(x0, float).copy(); p = np.asarray(p0, float).copy()
    esc = np.full(x.shape, -1, dtype=np.int64)
    alive = np.ones(x.shape, dtype=bool)
    for i in range(n):
        x, p = smap(x, p)
        if quant > 0.0:
            x = np.round(x / quant) * quant
            p = np.round(p / quant) * quant
        if noise > 0.0:
            x = np.mod(x + rng.uniform(-noise / 2, noise / 2, x.shape), TWO_PI)
            p = np.mod(p + rng.uniform(-noise / 2, noise / 2, p.shape), TWO_PI)
        gone = alive & (rad(x, p) > r_det)
        esc[gone] = i
        alive &= ~gone
        if not alive.any():
            break
    esc[alive] = n
    return esc


t0 = time.time()
rep = {"K": K, "island_centre": [CX, CP], "r_det": R_DET}

# ---------------------------------------------------------------- classification
n_scan = 2048
ang = RNG.uniform(0, TWO_PI, n_scan)
rad0 = np.concatenate([RNG.uniform(0.55, 1.5, n_scan - 256),
                       RNG.uniform(2.2, 4.4, 256)])
sx = np.mod(CX + rad0 * np.cos(ang), TWO_PI)
sp = np.mod(CP + rad0 * np.sin(ang), TWO_PI)

x, p = sx.copy(), sp.copy()
r_max = np.zeros(n_scan); near_cnt = np.zeros(n_scan)
dwell_scan = np.full(n_scan, 20000, dtype=np.int64); alive = np.ones(n_scan, bool)
for i in range(20000):
    x, p = smap(x, p)
    r = rad(x, p)
    np.maximum(r_max, r, out=r_max)
    near_cnt += r < R_NEAR
    gone = alive & (r > R_DET)
    dwell_scan[gone] = i; alive &= ~gone
frac_near = near_cnt / 20000
lam = lyap(sx, sp, 4000)

# KAM islands (fate-based, robust to stuck-phase lambda ~ 0); the sticky band is
# handled by dwell_tail.py with a per-angle calibrated region.
regular = (dwell_scan >= 20000) & (r_max < R_DET)
sticky = (lam > 1e-3) & (frac_near > 0.95)
sea = (lam > 1e-2) & (frac_near < 0.01)
rep["scan"] = {"n": n_scan, "regular": int(regular.sum()),
               "sticky": int(sticky.sum()), "sea": int(sea.sum()),
               "dwell_scan_sticky": ([int(np.percentile(dwell_scan[sticky], q)) for q in (50, 90, 99)] if sticky.any() else [])}
print(f"[scan] regular={regular.sum()} sticky={sticky.sum()} sea={sea.sum()} "
      f"(sea lambda range {lam[sea].min():.3f}..{lam[sea].max():.3f})")

reg_ic = int(np.argmax(regular))
sticky_idx = np.where(sticky)[0]
sea_idx = np.where(sea)[0][:3]

# ---------------------------------------------------------------- noise test
CHECKS = [100, 1000, 10000, 30000, 100000]
T_NOISE = 100000
N_COPIES = 64
cases = [("regular", reg_ic)]
cases += [("sticky", int(i)) for i in sticky_idx[:3]]
cases += [("sea", int(i)) for i in sea_idx]

noise_tbl = {}
for j, (cls, ii) in enumerate(cases):
    tag = f"{cls}{j}"
    x0, p0 = float(sx[ii]), float(sp[ii])
    rx, rp = orbit(x0, p0, T_NOISE)
    for Q in (1e-4, 1e-3):
        nx = np.full(N_COPIES, x0); npp = np.full(N_COPIES, p0)
        rows = []
        for i in range(1, T_NOISE + 1):
            nx, npp = smap(nx, npp)
            nx = np.mod(nx + RNG.uniform(-Q / 2, Q / 2, N_COPIES), TWO_PI)
            npp = np.mod(npp + RNG.uniform(-Q / 2, Q / 2, N_COPIES), TWO_PI)
            if i in CHECKS:
                d = np.sqrt(torus_d(nx, rx[i - 1])**2 + torus_d(npp, rp[i - 1])**2)
                rows.append((i, float(np.median(d)), float(np.percentile(d, 90))))
        noise_tbl[f"{tag}_Q{Q:.0e}"] = rows
    qx, qp = orbit(x0, p0, T_NOISE, quant=1e-3)
    qd = np.sqrt(torus_d(qx, rx)**2 + torus_d(qp, rp)**2)
    noise_tbl[f"{tag}_quant"] = [(c, float(np.percentile(qd[:c], 90)))
                                 for c in CHECKS]

print("\n[noise test] median(noisy dev from reference) at checkpoints "
      "(Q=quantized p90); torus diag = %.2f" % (np.pi * np.sqrt(2)))
for k, rows in noise_tbl.items():
    if k.endswith("_quant"):
        print(f"  {k:15s} " + "  ".join(f"t{c}:{v:.2e}" for c, v in rows))
    else:
        print(f"  {k:15s} " + "  ".join(f"t{c}:{m:.2e}" for c, m, _ in rows))
rep["noise"] = noise_tbl

# ---------------------------------------------------------------- dwell tails
T_DWELL = 200000
sub = sticky_idx[:300]
assert len(sub) > 0, "no sticky ensemble: classification failed"
d_true = dwell(sx[sub], sp[sub], T_DWELL)
tails = {"true": d_true}
for Q in (1e-4, 1e-3, 1e-2):
    tails[f"q{Q:.0e}"] = dwell(sx[sub], sp[sub], T_DWELL, quant=Q)
tails["noise1e-03"] = dwell(sx[sub], sp[sub], T_DWELL, noise=1e-3, rng=RNG)


def qrow(a):
    return {"p50": float(np.percentile(a, 50)), "p90": float(np.percentile(a, 90)),
            "p99": float(np.percentile(a, 99)), "capped": float((a >= T_DWELL).mean())}


rep["dwell"] = {k: qrow(v) for k, v in tails.items()}
print("\n[dwell] first escape from the island disk, sticky ensemble n=%d, cap %d"
      % (len(sub), T_DWELL))
for k, v in rep["dwell"].items():
    print(f"  {k:10s} p50={v['p50']:8.0f} p90={v['p90']:8.0f} p99={v['p99']:8.0f} "
          f"capped={v['capped']:.3f}")

# ---------------------------------------------------------------- shadow check
# Sticky ICs whose TRUE dwell >= 50k: is the quantized escape typical of true orbits
# from the same Q-cell? One batched call (candidates x 24 cell mates).
cand = np.where(d_true >= 50000)[0][:60]
if len(cand):
    dq = tails["q1e-03"][cand]
    rng2 = np.random.default_rng(7)
    mx = rng2.uniform(-5e-4, 5e-4, (len(cand), 24))
    mp = rng2.uniform(-5e-4, 5e-4, (len(cand), 24))
    d_cell = dwell(np.mod(sx[sub[cand]][:, None] + mx, TWO_PI),
                   np.mod(sp[sub[cand]][:, None] + mp, TWO_PI), T_DWELL)
    fracs = (d_cell > dq[:, None]).mean(axis=1)
    ratios = dq / np.median(d_cell, axis=1)
    rep["shadow"] = {"n": len(cand),
                     "median_frac_cell_dwell_longer": float(np.median(fracs)),
                     "median_ratio_quant_over_cell": float(np.median(ratios)),
                     "frac_orbits_ratio_lt_0.1": float((ratios < 0.1).mean())}
    print("\n[shadow check] quantized escape vs true dwells in the same Q-cell "
          "(n=%d)" % len(cand))
    print(f"  median fraction of same-cell true orbits dwelling longer than the "
          f"quantized law: {rep['shadow']['median_frac_cell_dwell_longer']:.3f}")
    print(f"  median ratio quantized/cell-median true dwell: "
          f"{rep['shadow']['median_ratio_quant_over_cell']:.4f}")
    print(f"  fraction of quantized orbits escaping >10x faster than the cell median: "
          f"{rep['shadow']['frac_orbits_ratio_lt_0.1']:.3f}")

# ---------------------------------------------------------------- controls
r_reg_t = dwell(sx[reg_ic:reg_ic + 1], sp[reg_ic:reg_ic + 1], 50000)
r_reg_q = dwell(sx[reg_ic:reg_ic + 1], sp[reg_ic:reg_ic + 1], 50000, quant=1e-2)
r_bigq = dwell(sx[sub[:100]], sp[sub[:100]], 50000, quant=1.0)
rep["controls"] = {
    "regular_true_dwell_capped": bool(r_reg_t[0] >= 50000),
    "regular_quantQ1e-2_dwell_capped": bool(r_reg_q[0] >= 50000),
    "sticky_bigQ1.0_capped_frac": float((r_bigq >= 50000).mean()),
}
print("\n[controls]", rep["controls"])
print(f"\nelapsed {time.time() - t0:.1f}s")

with open("shadow_out.json", "w") as f:
    json.dump(rep, f, indent=1)
