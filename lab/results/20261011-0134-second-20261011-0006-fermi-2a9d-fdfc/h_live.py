#!/usr/bin/env python3
"""H_live Monte Carlo: bits of live distinguishing information per body for a kicked belt.

Two store policies on ONE trajectory (policies are codes for the same state; the
dynamics never depend on them):
  A. frozen birth program  -> scar entropy of (x - x0)
  B. re-fit generator      -> residuals of the sorted ensemble against an m-knot
                              quantile bijection (sorted matching)
plus the label permutation cost (rank displacement of birth ordinals), the per-orbit
information birth H(delta) (claim check vs law.md's "+62 bits per kick"), and the
ever-encountered fraction.

Grounded constants: close-encounter rate r = 427/(1e4*20) = 2.135e-3 per body per orbit
(r8 v2 belt 0, lab/board.md 30 Sept), jump std J = 100 cells (10 in one holdout),
diffusion s cells/orbit (ladder), N = 2^20 (B18 belt scale), W cells of belt span.

Run: python3 h_live.py            (~6 min, < 1 GB)
"""
import json
import numpy as np

N = 1 << 20          # bodies (B18 belt scale)
T_MAIN = 1 << 13     # orbits, main run
T_HOLD = 1 << 12     # orbits, held-out runs
M_KNOTS = 256        # quantile-program knots (re-fit policy)
rng = np.random.default_rng(20261011)

def H(counts):
    c = counts[counts > 0].astype(np.float64)
    n = c.sum()
    return float(np.log2(n) - (c * np.log2(c)).sum() / n)

def ent_of(v):
    v = np.asarray(v, dtype=np.int64)
    return H(np.bincount(v - v.min()))

def knots_program(xs, m):
    """m-knot piecewise quantile program; returns P(rank) for ranks 0..N-1."""
    idx = (np.arange(m + 1) * (len(xs) - 1)) // m
    ranks = np.arange(len(xs), dtype=np.float64)
    return np.rint(np.interp(ranks, idx.astype(np.float64),
                             xs[idx].astype(np.float64))).astype(np.int64)

def measure(x0, x, m):
    out = {}
    out["frozen_scar_bits"] = ent_of(x.astype(np.int64) - x0.astype(np.int64))
    order = np.argsort(x, kind="stable")
    xs = x[order].astype(np.int64)
    P = knots_program(xs, m)
    out["refit_resid_bits"] = ent_of(xs - P)
    ranks = np.empty(N, dtype=np.int64)
    ranks[order] = np.arange(N, dtype=np.int64)
    out["label_perm_bits"] = ent_of(ranks - np.arange(N, dtype=np.int64))
    return out
def run(s, lam, J, r, T):
    W = N // lam
    x0 = ((np.arange(N, dtype=np.float64) + 0.5) * (W / N)).astype(np.int32)
    x = x0.copy()
    ever_hit = np.zeros(N, dtype=bool)
    snaps = {}
    B = 32
    t = 1
    while t <= T:
        nb = min(B, T - t + 1)
        d = np.rint(rng.standard_normal((nb, N), dtype=np.float32) * s)
        hit = rng.random((nb, N)) < r
        ever_hit |= hit.any(axis=0)
        fi = np.nonzero(hit.ravel())[0]
        if fi.size:
            d.ravel()[fi] += np.rint(rng.standard_normal(fi.size,
                                                         dtype=np.float32) * J)
        for i in range(nb):
            x += d[i].astype(np.int32)
            if (t + i) & -(t + i) == t + i:
                snaps[t + i] = x.copy()
        t += nb
    res = {"s": s, "lam": lam, "J": J, "r": r, "T": T,
           "ever_hit_frac": float(ever_hit.mean()), "points": []}
    for tt in sorted(snaps):
        m = measure(x0, snaps[tt], M_KNOTS)
        m["t"] = tt
        res["points"].append(m)
    d1 = np.rint(rng.normal(0.0, s, N))
    dj = d1.copy()
    hit = rng.random(N) < r
    dj[hit] += np.rint(rng.normal(0.0, J, int(hit.sum())))
    res["H_delta_bits"] = ent_of(d1)
    res["H_delta_with_jumps_bits"] = ent_of(dj)
    res["H_jump_bits"] = ent_of(np.rint(rng.normal(0.0, J, N)))
    return res

R_ENC = 427.0 / (1e4 * 20.0)   # 2.135e-3 per body per orbit (r8 v2 belt 0)
out = {"N": N, "m_knots": M_KNOTS, "r_enc": R_ENC, "runs": []}
for cfg in [(1.0, 1, 100.0, T_MAIN), (0.1, 1, 100.0, T_HOLD),
            (10.0, 1, 100.0, T_HOLD), (1.0, 32, 10.0, T_HOLD)]:
    s, lam, J, T = cfg
    print(f"running s={s} lam={lam} J={J} T={T}", flush=True)
    out["runs"].append(run(s, lam, J, R_ENC, T))

with open("results.json", "w") as f:
    json.dump(out, f, indent=1)

for res in out["runs"]:
    print(f"\n== s={res['s']} lam={res['lam']} J={res['J']} r={res['r']:.2e} "
          f"T={res['T']} ever_hit={res['ever_hit_frac']:.3f}")
    print(f"   H(delta)={res['H_delta_bits']:.2f} bits/orbit "
          f"(with jumps {res['H_delta_with_jumps_bits']:.2f}; jump alone {res['H_jump_bits']:.2f})")
    print("   t      frozen_scar  refit_resid  label_perm")
    for p in res["points"]:
        print(f"   {p['t']:6d}  {p['frozen_scar_bits']:10.2f}  "
              f"{p['refit_resid_bits']:10.2f}  {p['label_perm_bits']:10.2f}")
