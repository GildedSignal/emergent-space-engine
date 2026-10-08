#!/usr/bin/env python3
"""Taleb probe: does the phase-neighbour (rank-k) encounter certificate survive
lawful formation states it was not measured on?

Truth: time-sliced KD-tree min-distance with per-hit refinement (slice dt chosen
so a sub-rho window cannot fall between slices; controls on both sides).
Certificate: circular rank in mean longitude lambda = M0 + varpi at build time
(and at nearest rebuild before the encounter), pair found iff either side <= k.

Units: mu=1, a0=1, P=2pi. Encounter radius rho/a.
"""
import json, sys, time
import numpy as np
from scipy.spatial import cKDTree

TAU = 2 * np.pi

def kepler_E(M, e):
    E = M.copy()
    for _ in range(50):
        d = (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E -= d
        if np.abs(d).max() < 1e-14:
            break
    return E


def truth(a, e, w, M0, T, rho, slices_per_period):
    """All pairs with min distance < rho over [0,T]; dict pair -> (t*, dmin).
    Rigorous capture: any pair sub-rho at t_m is within rho + v_cap*dt of each
    other at the nearest slice (v_cap bounds all relative speeds), so a dilated
    query plus +-dt refinement cannot miss it."""
    n = len(a)
    v_cap = 2.0 * np.sqrt(np.maximum(2.0 / (a * (1.0 - e)) - 1.0 / a, 0.0)).max()
    n_sl = int(slices_per_period * T / TAU) + 1
    ts = np.linspace(0.0, T, n_sl)
    dt = ts[1] - ts[0]
    r_q = rho + v_cap * dt
    hits_i, hits_j, hits_t = [], [], []
    for t in ts:
        x, y, _, _ = states_all(a, e, w, M0, t)
        tree = cKDTree(np.column_stack([x, y]))
        for i, j in tree.query_pairs(r=r_q):
            hits_i.append(i); hits_j.append(j); hits_t.append(t)
    if not hits_i:
        return {}, dt, 0
    hi = np.array(hits_i); hj = np.array(hits_j); ht = np.array(hits_t)
    # keep every trough of each contiguous run: a run (pair within r_q) can hold
    # two sub-rho conjunctions separated by a local max that stays under r_q
    pid = np.minimum(hi, hj) * n + np.maximum(hi, hj)
    order = np.lexsort((ht, pid))
    pid, hi, hj, ht = pid[order], hi[order], hj[order], ht[order]
    d_hit = dist_t(a, e, w, M0, hi, hj, ht)
    starts = np.flatnonzero(np.r_[True, (pid[1:] != pid[:-1]) | (ht[1:] - ht[:-1] > 1.5 * dt)])
    ends = np.r_[starts[1:], len(pid)]
    sel = []
    for s0, e0 in zip(starts, ends):
        if e0 - s0 == 1:
            sel.append(s0)
            continue
        seg = d_hit[s0:e0]
        lm = np.r_[False, (seg[1:-1] < seg[:-2]) & (seg[1:-1] <= seg[2:]), False]
        if not lm.any():
            lm[np.argmin(seg)] = True
        else:
            lm[0] |= seg[0] < seg[1]
            lm[-1] |= seg[-1] < seg[-2]
        sel.extend((s0 + np.flatnonzero(lm)).tolist())
    sel = np.array(sel)
    hi, hj, ht = hi[sel], hj[sel], ht[sel]
    # refine: ternary on [t-dt, t+dt], fully vectorized over windows
    lo, hiB = ht - dt, ht + dt
    for _ in range(48):
        m1 = lo + (hiB - lo) / 3.0
        m2 = hiB - (hiB - lo) / 3.0
        d1 = dist_t(a, e, w, M0, hi, hj, m1)
        d2 = dist_t(a, e, w, M0, hi, hj, m2)
        take = d1 < d2
        hiB = np.where(take, m2, hiB)
        lo = np.where(take, lo, m1)
    tm = 0.5 * (lo + hiB)
    dm = dist_t(a, e, w, M0, hi, hj, tm)
    pid = np.minimum(hi, hj) * n + np.maximum(hi, hj)
    best = {}
    for P, D, Tm, I, J in zip(pid, dm, tm, hi, hj):
        key = (min(int(I), int(J)), max(int(I), int(J)))
        if D < rho and (key not in best or D < best[key][1]):
            best[key] = (float(Tm), float(D))
    return best, dt, len(hits_i)

def dist_t(a, e, w, M0, i, j, t):
    """Per-row times: positions of body i at t, body j at t (same t per row)."""
    aa_i, ee_i, ww_i, mm_i = a[i], e[i], w[i], M0[i]
    aa_j, ee_j, ww_j, mm_j = a[j], e[j], w[j], M0[j]
    xi, yi = pos_t(aa_i, ee_i, ww_i, mm_i, t)
    xj, yj = pos_t(aa_j, ee_j, ww_j, mm_j, t)
    return np.hypot(xi - xj, yi - yj)

def pos_t(a, e, w, M0, t):
    n = a ** -1.5
    M = (M0 + n * t) % TAU
    E = kepler_E(M, e)
    r = a * (1.0 - e * np.cos(E))
    f = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    th = f + w
    return r * np.cos(th), r * np.sin(th)

def states_all(a, e, w, M0, t):
    x, y = pos_t(a, e, w, M0, np.full_like(a, t))
    return x, y, None, None

def ranks_of_pairs(a, e, w, M0, pairs, rebuild_period=None):
    """Rank of each true pair at t=0 and at the nearest rebuild before t*.
    Rank from i = 1 + #{j: circ dlambda_i->j < dlambda_i->pair}; pair found if
    either side's rank <= k."""
    lam0 = (M0 + w) % TAU
    nn = a ** -1.5
    res = []
    for (i, j) in pairs:
        tstar, _ = pairs[(i, j)]
        variants = [("rank_t0", 0.0)]
        if rebuild_period:
            variants.append(("rank_rebuild", (tstar // rebuild_period) * rebuild_period))
        for label, t in variants:
            li = (lam0[i] + nn[i] * t) % TAU
            lj = (lam0[j] + nn[j] * t) % TAU
            dij_i = np.abs((lam0 + nn * t - li + np.pi) % TAU - np.pi)
            dij_j = np.abs((lam0 + nn * t - lj + np.pi) % TAU - np.pi)
            r_i = 1 + int((dij_i < dij_i[j]).sum())
            r_j = 1 + int((dij_j < dij_j[i]).sum())
            res.append((i, j, label, min(r_i, r_j), max(r_i, r_j)))
    return res

def run_case(name, N, T_periods, rho, slices_per_period, e_base, sig_e, w_mode, sig_a, lam_mode, seed):
    rng = np.random.default_rng(seed)
    a = 1.0 + sig_a * (rng.random(N) - 0.5)
    e = np.clip(np.full(N, e_base) + (sig_e * rng.standard_normal(N) if sig_e else 0.0), 0.0, 0.97)
    idx = np.arange(N)
    if w_mode == "aligned":
        w = np.zeros(N)
    elif w_mode == "uniform":
        w = rng.uniform(0, TAU, N)
    elif w_mode == "two_cluster":
        w = np.where(idx < N // 2, 0.0, np.pi)
    if lam_mode == "uniform":
        M0 = rng.uniform(0, TAU, N)
    elif lam_mode == "two_cluster":
        c = np.where(idx < N // 2, 0.0, np.pi) + rng.normal(0, 0.02, N)
        M0 = c - w
    T = T_periods * TAU
    t_start = time.time()
    enc, dt, nhits = truth(a, e, w, M0, T, rho, slices_per_period)
    wall = time.time() - t_start
    out = {"name": name, "N": N, "T_periods": T_periods, "rho": rho, "e": e_base,
           "sig_e": sig_e, "sig_a": sig_a, "w_mode": w_mode, "lam_mode": lam_mode,
           "seed": seed, "n_encounters": len(enc), "dt": round(float(dt), 6),
           "hits": nhits, "wall_s": round(wall, 1)}
    if enc:
        for label, rb in [("rank_t0", None), ("rank_rebuild", TAU / 4.0)]:
            rec = ranks_of_pairs(a, e, w, M0, enc, rb)
            ranks = np.array([minr for _, _, lab, minr, _ in rec if lab == label])
            out[label] = {
                "miss@4": round(float((ranks > 4).mean()), 4),
                "miss@16": round(float((ranks > 16).mean()), 4),
                "p50": int(np.percentile(ranks, 50)),
                "p99": int(np.percentile(ranks, 99)),
                "max": int(ranks.max()),
            }
        if w_mode == "two_cluster" or lam_mode == "two_cluster":
            inter = [p for p in enc if (p[0] < N // 2) != (p[1] < N // 2)]
            if inter:
                rec = ranks_of_pairs(a, e, w, M0, {p: enc[p] for p in inter}, None)
                ranks = np.array([minr for _, _, lab, minr, _ in rec if lab == "rank_t0"])
                out["inter_cluster"] = {"n": len(inter), "miss@4": round(float((ranks > 4).mean()), 4), "max_rank": int(ranks.max())}
            else:
                out["inter_cluster"] = {"n": 0}
    return out

def controls():
    # positive: same a,e,w; tiny da drifts body 2 into conjunction at t* ~ 2.5 P
    a = np.array([1.0, 1.0 + 2e-4]); e = np.zeros(2); w = np.zeros(2)
    M0 = np.array([0.0, 0.005])
    enc, _, _ = truth(a, e, w, M0, 4 * TAU, 1e-3, 2048)
    pos = len(enc) == 1 and enc[(0, 1)][1] < 1e-3
    # negative: circular orbits radially separated by 10 rho -> never within rho
    a2 = np.array([1.0, 1.0 + 1e-2])
    enc2, _, _ = truth(a2, np.zeros(2), np.zeros(2), np.array([0.0, 0.005]), 4 * TAU, 1e-3, 2048)
    neg = len(enc2) == 0
    return pos, neg

if __name__ == "__main__":
    t0 = time.time()
    pos, neg = controls()
    print(f"controls: positive={'PASS' if pos else 'FAIL'} negative={'PASS' if neg else 'FAIL'}")
    if not (pos and neg):
        sys.exit(2)
    cases = json.loads(sys.argv[1])
    results = []
    for c in cases:
        r = run_case(**c)
        print(json.dumps(r), flush=True)
        results.append(r)
    with open(sys.argv[2], "w") as f:
        json.dump(results, f, indent=1)
    print(f"total {time.time()-t0:.0f}s")
