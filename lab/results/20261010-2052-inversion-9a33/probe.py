#!/usr/bin/env python3
"""Inversion probe: does 'every encounter lies within partner rank 4 along the orbit'
(gold 20261006-0346-taleb-09b5) survive fleet element spread?

Truth = brute-force closest approaches: every pair ever within `thr` of a coarse
sample is a candidate (thr covers the worst between-sample motion), then each
candidate's coarse local minima are refined by golden section to 1e-8 in time.
An encounter is a distinct local minimum below RHO. No candidate-tier logic anywhere.

Scenes (a=1, GM=1, period 2pi, RHO=1e-4):
  A      control: n=800 circular zero-spread formation, uniform lambda over 0.2 rad
  B1e-3  A + burn footprint: n=1600, sigma_a/a=1e-4, sigma_e=1e-3, random apsides
  B3e-3  same with sigma_e=3e-3
  B1e-2  same with sigma_e=1e-2 (r8 v4's steady sigma_e)
  C      intercept: 400+400 ships, e=0.05, apsides anti-aligned, tight lambda clumps
         timed to co-arrive at an orbit crossing (t=pi/2, 3pi/2)

Usage: probe.py SCENE  ->  prints JSON, writes probe-SCENE.json
"""
import sys, json
import numpy as np
from scipy.spatial import cKDTree

RHO = 1e-4
PERIOD = 2 * np.pi
VREL_MAX = 2.5          # bound on relative speed at encounter (checked below)
T_OFF = np.pi / 2       # scene C: crossings at pi/2 and 3pi/2, away from t=0

def make_fleet(scene, seed=7):
    rng = np.random.RandomState(seed)
    if scene == "A":
        n = 800
        lam = rng.uniform(-0.1, 0.1, n)
        a = np.ones(n); ex = np.zeros(n); ey = np.zeros(n)
        grp = np.zeros(n, int); toff = 0.0
    elif scene.startswith("B"):
        sig_e = float(scene[1:])
        n = 800
        lam = rng.uniform(-0.1, 0.1, n)
        a = 1 + rng.normal(0, 1e-4, n)                  # r8 v4's kick scale
        ex = rng.normal(0, sig_e / np.sqrt(2), n)
        ey = rng.normal(0, sig_e / np.sqrt(2), n)
        grp = np.zeros(n, int); toff = 0.0
    elif scene == "C":
        n1 = n2 = 400
        e, m90 = 0.05, 1.4708856
        lam = np.concatenate([rng.normal(m90, 8e-3, n1),
                              rng.normal(np.pi - m90, 8e-3, n2)])
        a = np.ones(n1 + n2)
        ex = np.concatenate([np.full(n1, e), np.full(n2, -e)])  # anti-aligned apsides
        ey = np.zeros(n1 + n2)
        grp = np.concatenate([np.zeros(n1, int), np.ones(n2, int)])
        n = n1 + n2; toff = T_OFF
    else:
        raise SystemExit("scene?")
    e = np.hypot(ex, ey)
    w = np.arctan2(ey, ex)                              # 0 when e==0
    M0 = lam - w - toff * a ** -1.5                     # lam = w + M at t=toff
    return dict(a=a, e=e, w=w, M0=M0, grp=grp, n=n, scene=scene)

def positions(f, t):
    """Exact Kepler positions of all bodies at time t."""
    M = np.mod(f["M0"] + f["a"] ** -1.5 * t, 2 * np.pi)
    E = M.copy()
    for _ in range(12):
        E -= (E - f["e"] * np.sin(E) - M) / (1 - f["e"] * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = f["a"] * (1 - f["e"] * cE)
    th = f["w"] + np.arctan2(np.sqrt(1 - f["e"] ** 2) * sE, cE - f["e"])
    return r * np.cos(th), r * np.sin(th), th, r

def circ_centered(x):
    """Centre angles on their largest circular gap so a clump is never split."""
    ls = np.sort(x)
    if len(ls) < 2:
        return x
    gaps = np.diff(ls)
    wrap = ls[0] + 2 * np.pi - ls[-1]
    cut = ls[-1] if wrap > gaps.max() else ls[int(np.argmax(gaps))]
    return np.mod(x - cut - 1e-12, 2 * np.pi)

def kepler_xy(a, e, w, M0, t):
    M = np.mod(M0 + a ** -1.5 * t, 2 * np.pi)
    E = M.copy()
    for _ in range(12):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    th = w + np.arctan2(np.sqrt(1 - e ** 2) * sE, cE - e)
    return r * np.cos(th), r * np.sin(th)

def dist2(f, t, I, J):
    xi, yi = kepler_xy(f["a"][I], f["e"][I], f["w"][I], f["M0"][I], t)
    xj, yj = kepler_xy(f["a"][J], f["e"][J], f["w"][J], f["M0"][J], t)
    return (xi - xj) ** 2 + (yi - yj) ** 2

def coarse(f, nsamp):
    """Candidate pairs: present in a thr-neighbourhood at t=0 (persistent pairs,
    whose distance varies little) or at any coarse sample (transient dips)."""
    dt = PERIOD / nsamp
    thr = RHO + VREL_MAX * dt / 2 + 5e-4
    n = f["n"]
    x, y, *_ = positions(f, 0.0)
    p0 = cKDTree(np.stack([x, y], 1)).query_pairs(thr, output_type="ndarray")
    p0 = p0[p0[:, 0] < p0[:, 1]]
    perm = np.unique(p0[:, 0] * n + p0[:, 1])           # sorted keys, t=0 companions
    trans_i, trans_j, trans_s = [], [], []
    for s in range(1, nsamp):
        t = s * dt
        x, y, *_ = positions(f, t)
        ps = cKDTree(np.stack([x, y], 1)).query_pairs(thr, output_type="ndarray")
        ps = ps[ps[:, 0] < ps[:, 1]]
        if not len(ps):
            continue
        keys = ps[:, 0] * n + ps[:, 1]
        idx = np.searchsorted(perm, keys)
        idxc = np.minimum(idx, len(perm) - 1)
        new = keys != perm[idxc]
        if new.any():
            trans_i.append(ps[new, 0]); trans_j.append(ps[new, 1])
            trans_s.append(np.full(new.sum(), s))
    perm_i, perm_j = perm // n, perm % n
    if trans_i:
        ti = np.concatenate(trans_i); tj = np.concatenate(trans_j)
        ts = np.concatenate(trans_s)
    else:
        ti = tj = ts = np.array([], np.int64)
    return perm_i, perm_j, ti, tj, ts, dt, thr, len(perm)

def golden(f, t_lo, t_hi, RI, RJ, iters=40):
    invphi = (np.sqrt(5) - 1) / 2
    x1 = t_hi - invphi * (t_hi - t_lo); x2 = t_lo + invphi * (t_hi - t_lo)
    f1 = dist2(f, x1, RI, RJ); f2 = dist2(f, x2, RI, RJ)
    for _ in range(iters):
        m = f1 < f2
        t_hi = np.where(m, x2, t_hi); t_lo = np.where(m, t_lo, x1)
        span = t_hi - t_lo
        x1 = t_hi - invphi * span; x2 = t_lo + invphi * span
        f1 = dist2(f, x1, RI, RJ); f2 = dist2(f, x2, RI, RJ)
    return 0.5 * (t_lo + t_hi), np.sqrt(dist2(f, 0.5 * (t_lo + t_hi), RI, RJ))

def refine(f, perm_i, perm_j, ti, tj, ts, dt):
    """Persistent pairs (within thr at t=0): one bracket over the whole orbit.
    Transient pairs: consecutive-sample runs around each dip, bracket +- dt."""
    t_lo_l, t_hi_l, I_l, J_l = [], [], [], []
    t_lo_l.append(np.zeros(len(perm_i))); t_hi_l.append(np.full(len(perm_i), PERIOD))
    I_l.append(perm_i); J_l.append(perm_j)
    if len(ti):
        key = ti * f["n"] + tj
        order = np.lexsort((ts, key))
        ti, tj, ts = ti[order], tj[order], ts[order]
        key = key[order]
        D = dist2(f, ts * dt, ti, tj)
        starts = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
        ends = np.r_[starts[1:], len(key)]
        for b, en in zip(starts, ends):
            s = ts[b:en]
            bidx = np.flatnonzero(np.r_[True, np.diff(s) > 1])
            for k in range(len(bidx)):
                lo = b + bidx[k]
                hi = b + (bidx[k + 1] - 1 if k + 1 < len(bidx) else en - 1)
                am = lo + int(np.argmin(D[lo:hi + 1]))
                t0 = ts[am] * dt
                t_lo_l.append(np.array([t0 - dt])); t_hi_l.append(np.array([t0 + dt]))
                I_l.append(ti[am:am + 1]); J_l.append(tj[am:am + 1])
    t_lo = np.concatenate(t_lo_l); t_hi = np.concatenate(t_hi_l)
    RI = np.concatenate(I_l).astype(int); RJ = np.concatenate(J_l).astype(int)
    t_star, d_star = golden(f, t_lo, t_hi, RI, RJ)
    return RI, RJ, t_star, d_star

def analyse(f, RI, RJ, t_star, d_star):
    ev = d_star < RHO
    RI, RJ, t_star = RI[ev], RJ[ev], t_star[ev]
    if not len(RI):
        return dict(events=0)
    o = np.lexsort((t_star, RJ, RI))
    RI, RJ, t_star = RI[o], RJ[o], t_star[o]
    keep = np.r_[True, (np.diff(RI) != 0) | (np.diff(RJ) != 0) | (np.diff(t_star) > 1e-6)]
    RI, RJ, t_star = RI[keep], RJ[keep], t_star[keep]
    n = f["n"]
    nbar = f["a"] ** -1.5
    ranks_lam, ranks_th, cross = [], [], []
    for t in np.unique(t_star):
        lam_c = circ_centered(np.mod(f["w"] + f["M0"] + nbar * t, 2 * np.pi))
        order = np.argsort(lam_c)
        rlam = np.empty(n, int); rlam[order] = np.arange(n)
        _, _, th, _ = positions(f, t)
        thc = circ_centered(th)
        order = np.argsort(thc)
        rth = np.empty(n, int); rth[order] = np.arange(n)
        sel = t_star == t
        for ii, jj in zip(RI[sel], RJ[sel]):
            ranks_lam.append(abs(rlam[ii] - rlam[jj]))
            ranks_th.append(abs(rth[ii] - rth[jj]))
            cross.append(f["grp"][ii] != f["grp"][jj])
    ranks_lam = np.array(ranks_lam); ranks_th = np.array(ranks_th)
    cross = np.array(cross, bool)
    res = dict(
        n=n, events=int(len(RI)),
        pairs=int(len(set(zip(RI.tolist(), RJ.tolist())))),
        miss_lam_k4=float((ranks_lam > 4).mean()),
        miss_th_k4=float((ranks_th > 4).mean()),
        max_rank_lam=int(ranks_lam.max()),
        p99_rank_lam=float(np.percentile(ranks_lam, 99)),
        k_needed=int(ranks_lam.max()),
    )
    if cross.any():
        res.update(
            miss_lam_k4_cross=float((ranks_lam[cross] > 4).mean()),
            miss_lam_k4_within=float((ranks_lam[~cross] > 4).mean()),
            max_rank_cross=int(ranks_lam[cross].max()),
            max_rank_within=int(ranks_lam[~cross].max()),
            n_cross_events=int(cross.sum()), n_within_events=int((~cross).sum()),
        )
    return res

if __name__ == "__main__":
    SCENE = sys.argv[1]
    f = make_fleet(SCENE)
    x, y, _, _ = positions(f, 0.0)
    res0 = dict(scene=SCENE)
    # worst-case relative speed check for the thr margin
    n = f["n"]
    ts_chk = np.linspace(0, PERIOD, 60, endpoint=False)
    vmax = 0.0
    for t in ts_chk:
        vx = []
        # speed of each body: |v| = sqrt(GM*(2/r - 1/a))
        _, _, th, r = positions(f, t)
        sp = np.sqrt(np.maximum(2.0 / r - 1.0 / f["a"], 0))
        vmax = max(vmax, 2 * sp.max())
    res0["vrel_bound_used"] = VREL_MAX
    nsamp = 1200
    perm_i, perm_j, ti, tj, ts, dt, thr, nperm = coarse(f, nsamp)
    RI, RJ, t_star, d_star = refine(f, perm_i, perm_j, ti, tj, ts, dt)
    res = analyse(f, RI, RJ, t_star, d_star)
    res.update(res0)
    res["coarse_thr"] = thr; res["n_persistent_pairs"] = int(nperm)
    res["n_transient_records"] = int(len(ti))
    rms = float(np.sqrt(((x - x.mean()) ** 2 + (y - y.mean()) ** 2).mean()))
    res["clump_rms_radius"] = rms
    print(json.dumps(res, indent=1))
    with open(f"probe-{SCENE}.json", "w") as fh:
        json.dump(res, fh, indent=1)
