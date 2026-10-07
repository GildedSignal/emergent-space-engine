#!/usr/bin/env python3
"""Whole-system probe: is the law's Catalogue key (quantized (p, 1/(1+e)), 12+12 bits)
already the encounter tier? One sorted key list must serve:
  (a) the candidate window (annulus overlap over KEY cells, not bodies),
  (b) formation/phase blocks (bodies under one key, phase-ordered by mean longitude),
with zero missed encounters against brute-force sampled truth.

Scenes: S2 dense belt, S3 formation, S4 high-e belt, S5 = S2 + precession 0.3 rad/orbit,
S6 moderate-e belt + precession, S7 high-e belt + strong precession 0.9 rad/orbit.
Controls: window without R-widening (A), without quantum-widening (B), Kepler cone with
stale periapsis under precession (C) plus its verdict-flip rate (the per-cycle expiry of
any periapsis-based certificate). Work scene: S1 sparse belt N=2e5. Kick maintenance on S1.
Floats explore; decisions (miss counts, recalls) are integer comparisons on the sampled oracle.
"""
import json, time
from collections import defaultdict
import numpy as np

rng = np.random.default_rng(9690)
TAU = 2 * np.pi
R = 5e-4          # encounter radius (reach)
SAMPLES = 128     # truth sampling per interval
SCALE_BITS = 12   # law's MEMO_SCALE_BITS (p mantissa)
SHAPE_BITS = 12   # law's MEMO_SHAPE_BITS (gap (1-e)/(1+e))

def scene(kind, n):
    if kind == "S1":
        a = rng.uniform(0.7, 1.3, n); e = rng.rayleigh(0.05, n)
    elif kind == "S2":
        a = rng.uniform(0.99, 1.01, n); e = rng.rayleigh(0.02, n)
    elif kind == "S3":
        a = 1 + rng.uniform(-1e-5, 1e-5, n); e = 0.001 + rng.uniform(-1e-6, 1e-6, n)
    elif kind == "S4":
        a = rng.uniform(0.99, 1.01, n); e = rng.uniform(0.7, 0.9, n)
    elif kind == "S5":
        a = rng.uniform(0.99, 1.01, n); e = rng.rayleigh(0.02, n)
    elif kind == "S6":
        a = rng.uniform(0.99, 1.01, n); e = np.clip(rng.rayleigh(0.15, n), 0.05, 0.4)
    elif kind == "S8":   # radially spread belt: annuli mostly disjoint, edge gaps exist
        a = rng.uniform(0.7, 1.3, n); e = rng.rayleigh(0.05, n)
    elif kind == "S7":
        a = rng.uniform(0.99, 1.01, n); e = rng.uniform(0.25, 0.35, n)
    else:
        raise ValueError(kind)
    pom = rng.uniform(0, TAU, n); M0 = rng.uniform(0, TAU, n)
    return a, e, pom, M0

def positions(a, e, pom, M0, t, prec=0.0):
    n_ = a ** -1.5
    M = M0[None, :] + n_[None, :] * t[:, None]
    E = M.copy()
    for _ in range(6):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    r = a * (1 - e * np.cos(E))
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    phi = nu + pom[None, :] + prec * t[:, None]
    return np.stack([r * np.cos(phi), r * np.sin(phi)], axis=-1)

def truth_pairs(a, e, pom, M0, prec=0.0, samples=SAMPLES):
    n = len(a); t = np.linspace(0, TAU, samples, endpoint=False)
    pos = positions(a, e, pom, M0, t, prec)
    out = []
    for i in range(n - 1):
        d = pos[:, i + 1:, :] - pos[:, i, :][:, None, :]
        d2 = np.einsum("tsd,tsd->ts", d, d).min(axis=0)
        hit = np.nonzero(d2 < R * R)[0]
        out.extend((i, i + 1 + j) for j in hit)
    return out

# ---------- the unified store: keys are the law's own integers ----------
def key_cells(a, e):
    p = a * (1 - e * e)
    g = (1 - e) / (1 + e)                       # 2k-1, the law's shape gap
    m, ex = np.frexp(p)
    mq = np.round(m * (1 << SCALE_BITS)).astype(np.int64)
    key_p = ex.astype(np.int64) * (1 << SCALE_BITS) + mq
    gq = np.clip(np.round(g * (1 << SHAPE_BITS)), 1, 1 << SHAPE_BITS).astype(np.int64)
    p_q = mq * 2.0 ** (ex - SCALE_BITS)
    g_q = gq / (1 << SHAPE_BITS)
    k_q = (1 + g_q) / 2
    r_peri = p_q * k_q
    r_apo = p_q * k_q / g_q
    return key_p, gq, r_peri, r_apo

def widened_u(r_peri, r_apo, with_R=True, with_quantum=True):
    """Key-cell interval in u = 1/r: the quantized annulus pushed OUT by one quantum at
    each end (soundness vs the body's true annulus) and by R. Returns (u_lo, u_hi)."""
    qp = 2.0 ** -SCALE_BITS
    lo_r, hi_r = r_peri.copy(), r_apo.copy()    # inner, outer radius
    if with_quantum:
        g = r_peri / r_apo
        pad = r_apo * (qp + qp / g) + r_peri * qp
        lo_r, hi_r = lo_r - pad, hi_r + pad
    if with_R:
        lo_r, hi_r = lo_r - R, hi_r + R
    return 1.0 / hi_r, 1.0 / lo_r

def interval_pairs(u_lo, u_hi):
    """Every overlapping pair of the N u-intervals (sweep by u_lo, two-sided)."""
    n = len(u_lo)
    order = np.argsort(u_lo)
    lo_s, hi_s = u_lo[order], u_hi[order]
    pairs = []
    for rk in range(n - 1):
        stop = np.searchsorted(lo_s, hi_s[rk], side="right")
        for o in range(rk + 1, stop):
            if hi_s[o] >= lo_s[rk]:
                i, j = int(order[rk]), int(order[o])
                pairs.append((i, j) if i < j else (j, i))
    return pairs

def recall(cand, truth):
    cs = set(cand)
    return sum(1 for p in truth if p not in cs), len(truth), len(cs)

def cone_pairs(a, e, pom):
    """Kepler Binet cone (orientation-aware), periapsis as given."""
    U = 1.0 / (a * (1 - e * e))
    V = e * np.cos(pom) / (a * (1 - e * e))
    W = e * np.sin(pom) / (a * (1 - e * e))
    out = []
    for i in range(len(a) - 1):
        dU = U[i] - U[i + 1:]; dV = V[i] - V[i + 1:]; dW = W[i] - W[i + 1:]
        hit = np.nonzero(dU * dU <= dV * dV + dW * dW)[0]
        out.extend((i, i + 1 + j) for j in hit)
    return out

t0 = time.time(); out = {"R": R, "samples": SAMPLES}
log = lambda *s: print(f"[{time.time()-t0:6.1f}s]", *s, flush=True)

for kind, prec in [("S2", 0.0), ("S3", 0.0), ("S4", 0.0), ("S5", 0.3), ("S6", 0.3), ("S7", 0.9), ("S8", 0.3)]:
    a, e, pom, M0 = scene(kind, 1000)
    tr = truth_pairs(a, e, pom, M0, prec, samples=384 if kind in ("S4", "S7") else (256 if kind == "S8" else SAMPLES))
    key_p, gq, r_peri, r_apo = key_cells(a, e)
    res = {"truth_pairs": len(tr), "distinct_keys": len(set(zip(key_p.tolist(), gq.tolist())))}

    u_lo, u_hi = widened_u(r_peri, r_apo, True, True)
    cand = interval_pairs(u_lo, u_hi)
    miss, ntr, ncand = recall(cand, tr)
    res["window_misses"] = miss
    res["cand_per_truth"] = round(len(cand) / max(1, len(tr)), 1)

    u_lo, u_hi = widened_u(r_peri, r_apo, False, True)
    res["ctrlA_noR_misses"] = recall(interval_pairs(u_lo, u_hi), tr)[0]
    u_lo, u_hi = widened_u(r_peri, r_apo, True, False)
    res["ctrlB_noQuantum_misses"] = recall(interval_pairs(u_lo, u_hi), tr)[0]

    if prec:
        res["ctrlC_stale_cone_misses"] = recall(cone_pairs(a, e, pom), tr)[0]
        U = 1.0 / (a * (1 - e * e)); V = e * np.cos(pom) / (a * (1 - e * e)); W = e * np.sin(pom) / (a * (1 - e * e))
        pom2 = (pom + prec * TAU) % TAU
        V2 = e * np.cos(pom2) / (a * (1 - e * e)); W2 = e * np.sin(pom2) / (a * (1 - e * e))
        iu, ju = np.triu_indices(len(a), 1)
        v1 = (U[iu] - U[ju]) ** 2 <= (V[iu] - V[ju]) ** 2 + (W[iu] - W[ju]) ** 2
        v2 = (U[iu] - U[ju]) ** 2 <= (V2[iu] - V2[ju]) ** 2 + (W2[iu] - W2[ju]) ** 2
        res["cone_verdict_flips"] = int((v1 != v2).sum())
        res["cone_pairs_t0"] = int(v1.sum())

    if kind == "S3":
        lam = (M0 + pom) % TAU
        cell = defaultdict(list)
        for i in range(len(a)):
            cell[(int(key_p[i]), int(gq[i]))].append(i)
        def crank(members, i, j):
            ms = sorted(members, key=lambda q: lam[q])
            ii, jj = ms.index(i), ms.index(j)
            d = abs(ii - jj)
            return min(d, len(ms) - d)
        ranks, ranks_win = [], []
        for i, j in tr:
            same = (key_p[i] == key_p[j]) and (gq[i] == gq[j])
            ranks.append(crank(cell[(int(key_p[i]), int(gq[i]))], i, j) if same else -1)
            ranks_win.append(crank(range(len(a)), i, j))
        rs = np.array(ranks); rw = np.array(ranks_win)
        res["block"] = {
            "same_cell_true_pairs": int((rs >= 0).sum()),
            "cross_cell_true_pairs": int((rs < 0).sum()),
            "median_rank_same_cell": float(np.median(rs[rs >= 0])) if (rs >= 0).any() else None,
            "max_rank_same_cell": int(rs.max()) if (rs >= 0).any() else None,
            "median_rank_whole_scene": float(np.median(rw)),
            "max_rank_whole_scene": int(rw.max()),
            "max_block_size": max(len(v) for v in cell.values()),
        }
    out[kind] = res
    log(kind, json.dumps(res))

# --- work scene S1 ---
a, e, pom, M0 = scene("S1", 200_000)
key_p, gq, r_peri, r_apo = key_cells(a, e)
u_lo, u_hi = widened_u(r_peri, r_apo, True, True)
cells = defaultdict(list)
for i, q in enumerate(zip(key_p.tolist(), gq.tolist())):
    cells[q].append(i)
keys = sorted(cells)
klo_arr = np.array([u_lo[cells[q]][0] for q in keys])
khi_arr = np.array([u_hi[cells[q]][0] for q in keys])
cell_size = np.array([len(cells[q]) for q in keys])
order = np.argsort(klo_arr)
klo_s, khi_s, size_s = klo_arr[order], khi_arr[order], cell_size[order]
qs = rng.choice(len(a), 100, replace=False)
cand_counts, cell_visits = [], []
for i in qs:
    hi_cut = np.searchsorted(klo_s, u_hi[i], side="right")
    ok = khi_s[:hi_cut] >= u_lo[i]
    cand_counts.append(int(size_s[:hi_cut][ok].sum()))
    cell_visits.append(int(hi_cut))
out["S1"] = {
    "N": len(a), "distinct_keys": len(keys),
    "median_candidates_per_query": int(np.median(cand_counts)),
    "p99_candidates_per_query": int(np.percentile(cand_counts, 99)),
    "median_cells_visited": int(np.median(cell_visits)),
    "plane_evals_per_query": len(a),
}
log("S1", json.dumps(out["S1"]))

# --- kick maintenance ---
nk = 2000
sel = rng.choice(len(a), nk, replace=False)
a2 = a.copy(); a2[sel] *= (1 + rng.normal(0, 1e-3, nk))
kp2, kg2, _, _ = key_cells(a2, e)
same_sel = ((kp2 == key_p) & (kg2 == gq))[sel]
moved = np.abs(kp2 - key_p)[sel]
out["kick"] = {
    "kicked": nk,
    "key_unchanged_frac_of_kicked": round(float(same_sel.mean()), 4),
    "median_key_move_cells": int(np.median(moved[~same_sel])) if (~same_sel).any() else 0,
    "p99_key_move_cells": int(np.percentile(moved[~same_sel], 99)) if (~same_sel).any() else 0,
}
log("kick", json.dumps(out["kick"]))

with open(__file__.replace(".py", ".json"), "w") as f:
    json.dump(out, f, indent=1)
log("done")
