#!/usr/bin/env python3
"""Conjunction return map for candidate pairs (dynamics lens). v2 (slice fixed).

Model: two bodies on fixed decoupled Kepler ellipses about one primary
(r8 v2's encounter-search model). Conjunctions are exact:
lambda_1(t)-lambda_2(t) = u t + dlam0, u = n1-n2 > 0, so conjunction k is at
t_k = (2 pi k - dlam0)/u; the inner body's mean anomaly there advances by
exactly delta = 2 pi n1/u per conjunction: a circle rotation.
At conjunction M1 + varpi1 = M2 + varpi2, so the conjunction miss distance is
g(theta) = |r1(theta; e1,w1) - r2(theta + w1 - w2; e2,w2)|, a fixed function
on the circle, and the miss at conjunction k is g(theta_0 + k delta).
(v1 sampled the wrong slice — equal-time instead of conjunction — caught by
an independent time sweep, not by the shared-harness control.)

Stages:
  A  control: conjunction-slice g vs time-propagated distances at t_k
  B  window fractions (candidate-set shrinkage), three-gap integer check,
     waiting-time law and per-pair equidistribution predictor
  D  near-rational (resonance) structure: censoring vs ||q alpha||
  E  conjunction-less leak vs eccentricity (dense time sampling)
  F  drift horizon: window drifting at rate eta
"""
import json
import sys

import numpy as np

TWO_PI = 2.0 * np.pi
RNG = np.random.default_rng(20261008)


def kepler_E(M, e, iters=30):
    M = np.mod(M, TWO_PI)
    E = M + e * np.sin(M)
    for _ in range(iters):
        f = E - e * np.sin(E) - M
        E = E - f / (1.0 - e * np.cos(E))
    return E


def pos(a, e, varpi, M):
    """2D position about the focus, rotated by varpi."""
    E = kepler_E(M, e)
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1.0 - e * e) * np.sin(E)
    c, s = np.cos(varpi), np.sin(varpi)
    return x * c - y * s, x * s + y * c


def finish(p):
    p["n1"] = p["a1"] ** -1.5
    p["n2"] = p["a2"] ** -1.5
    p["u"] = p["n1"] - p["n2"]
    dlam0 = p["varpi1"] + p["M01"] - p["varpi2"] - p["M02"]
    t0 = (0.0 - dlam0) / p["u"]
    p["th0"] = np.mod(p["M01"] + p["n1"] * t0, TWO_PI)
    p["alpha"] = np.mod(p["n1"] / p["u"], 1.0)
    return p


def sample_pairs(n, sigma_e=0.1, dmin=0.005, dmax=0.05, rng=RNG):
    p = dict(
        a1=np.ones(n),
        e1=rng.rayleigh(sigma_e, n).clip(0.0, 0.9),
        e2=rng.rayleigh(sigma_e, n).clip(0.0, 0.9),
        dlt=rng.uniform(dmin, dmax, n),
        varpi1=rng.uniform(0, TWO_PI, n),
        varpi2=rng.uniform(0, TWO_PI, n),
        M01=rng.uniform(0, TWO_PI, n),
        M02=rng.uniform(0, TWO_PI, n),
    )
    p["a2"] = p["a1"] + p["dlt"]
    return finish(p)


def g_slice(p, theta):
    """Conjunction miss distance with body-1 mean anomaly = theta (vector)."""
    M1 = theta
    M2 = theta + p["varpi1"] - p["varpi2"]
    x1, y1 = pos(p["a1"], p["e1"], p["varpi1"], M1)
    x2, y2 = pos(p["a2"], p["e2"], p["varpi2"], M2)
    return np.hypot(x1 - x2, y1 - y2)


def time_dist(p, t):
    """Distance at absolute time t (independent path: pure time propagation)."""
    M1 = p["M01"] + p["n1"] * t
    M2 = p["M02"] + p["n2"] * t
    x1, y1 = pos(p["a1"], p["e1"], p["varpi1"], M1)
    x2, y2 = pos(p["a2"], p["e2"], p["varpi2"], M2)
    return np.hypot(x1 - x2, y1 - y2)


def conj_times(p, ks):
    dlam0 = p["varpi1"] + p["M01"] - p["varpi2"] - p["M02"]
    return (TWO_PI * ks - dlam0) / p["u"]


def g_grid(p, G=4096):
    th = np.linspace(0.0, TWO_PI, G, endpoint=False)
    out = np.empty((len(p["a1"]), G))
    for i in range(len(p["a1"])):
        pi_ = {k: v[i: i + 1] for k, v in p.items()}
        out[i] = g_slice(pi_, th)
    return th, out


def windows_below(th, Frow, mstar):
    """Windows {theta: g(theta) < mstar} as circle-fraction intervals."""
    G = len(th)
    below = Frow < mstar
    if not below.any():
        return 0.0, []
    dth = th[1] - th[0]
    rot = int(np.argmin(below))
    b2 = np.roll(below, -rot)
    d = np.diff(np.concatenate(([0], b2.astype(np.int8), [0])))
    starts = np.nonzero(d == 1)[0]
    ends = np.nonzero(d == -1)[0] - 1
    intervals = []
    w = 0.0
    for s0, e0 in zip(starts, ends):
        j_in = (s0 + rot) % G
        j_out = (s0 - 1 + rot) % G
        f_in, f_out = Frow[j_in], Frow[j_out]
        t = 0.0 if f_out <= mstar else (f_out - mstar) / (f_out - f_in)
        lo = (th[j_out] + t * dth) / TWO_PI
        j_in = (e0 + rot) % G
        j_out = (e0 + 1 + rot) % G
        f_in, f_out = Frow[j_in], Frow[j_out]
        t = 1.0 if f_out <= mstar else (f_in - mstar) / (f_in - f_out)
        hi = (th[j_in] + t * dth) / TWO_PI
        lo %= 1.0
        hi %= 1.0
        width = hi - lo
        if width <= 0:
            width += 1.0
        w += width
        intervals.append((lo, hi))
    return w, intervals


def first_hit_scan(alpha, th0_frac, intervals, kmax, block=2048):
    n = len(alpha)
    kstar = np.full(n, -1)
    k = 1
    alive = np.arange(n)
    while k <= kmax and len(alive):
        kk = np.arange(k, min(k + block, kmax + 1))
        th = np.mod(th0_frac[alive][:, None] + kk[None, :] * alpha[alive][:, None], 1.0)
        hit = np.zeros(th.shape, bool)
        for j, i in enumerate(alive):
            for (lo, hi) in intervals[i]:
                hit[j] |= (th[j] >= lo) & (th[j] <= hi)
        found = hit.any(1)
        if found.any():
            first = hit.argmax(1)
            kstar[alive[found]] = kk[first[found]]
            alive = alive[~found]
        k += block
    return kstar


def stage_a(out):
    p = sample_pairs(384)
    G = 4096
    th, F = g_grid(p, G)
    K = 512
    ks = np.arange(1, K + 1)
    # g(theta_k) vs time-propagated distance at t_k (independent paths)
    maxrel = 0.0
    for chunk in np.array_split(ks, 8):
        t_k = conj_times(p, chunk[:, None])
        d_time = time_dist(p, t_k)
        th_k = np.mod(TWO_PI * chunk[:, None] * p["alpha"][None, :] + p["th0"][None, :], TWO_PI)
        d_grd = np.empty_like(d_time)
        for i in range(len(p["a1"])):
            d_grd[:, i] = np.interp(th_k[:, i], th, F[i])
        rel = np.abs(d_grd - d_time) / np.maximum(d_time, 1e-9)
        maxrel = max(maxrel, float(np.percentile(rel, 99)))
    # exact-slice check (no interpolation), worst pair
    i = 0
    pi_ = {k: v[i: i + 1] for k, v in p.items()}
    th_ex = np.mod(p["th0"][i] + TWO_PI * ks * p["alpha"][i], TWO_PI)
    d_ex = g_slice(pi_, th_ex)
    t_ex = conj_times(pi_, ks)
    d_tex = time_dist(pi_, t_ex)
    out["control"] = dict(pairs=len(p["a1"]), K=K, grid=G,
                          p99_rel_grid_vs_time=float(maxrel),
                          max_rel_exact_vs_time=float(np.max(np.abs(d_ex - d_tex) / np.maximum(d_tex, 1e-9))))


def stage_b(out):
    p = sample_pairs(512)
    G = 4096
    th, F = g_grid(p, G)
    gmin = F.min(1)
    out["gmin_pct"] = [float(x) for x in np.percentile(gmin, [1, 10, 25, 50, 75, 90, 99])]
    mstars = [3e-3, 1e-3, 3e-4, 1e-4]
    kmax = 262144
    res = {}
    for m in mstars:
        haswin = gmin < m
        intervals = []
        wfrac = np.zeros(len(p["a1"]))
        for i in range(len(p["a1"])):
            wf, iv = windows_below(th, F[i], m)
            wfrac[i] = wf
            intervals.append(iv)
        ks = first_hit_scan(p["alpha"], p["th0"] / TWO_PI, intervals, kmax)
        unc = ks >= 0
        pred = 1.0 / np.maximum(wfrac, 1e-12)
        r = ks[unc] / pred[unc] if unc.any() else np.array([])
        res["%g" % m] = dict(
            n=len(ks), with_window=int(haswin.sum()),
            window_frac=float(haswin.mean()),
            censored_of_windows=int(unc.sum() and (~unc[haswin]).sum() or ((~unc) & haswin).sum()),
            median_kstar=float(np.median(ks[unc])) if unc.any() else None,
            frac_within2=float(np.mean((r > 0.5) & (r < 2.0))) if len(r) else None,
            median_ratio=float(np.median(r)) if len(r) else None)
    out["waiting"] = res
    mm, kk = [], []
    for k, v in res.items():
        if v["median_kstar"]:
            mm.append(float(k))
            kk.append(v["median_kstar"])
    if len(mm) >= 2:
        out["waiting_slope"] = float(np.polyfit(np.log(mm), np.log(kk), 1)[0])
    # three-gap integer check at the median-friendly threshold
    m = 1e-3 if (gmin < 1e-3).mean() > 0.3 else 3e-3
    ng, agree = [], []
    K3 = 65536
    kk3 = np.arange(1, K3 + 1)
    for i in range(len(p["a1"])):
        _, iv = windows_below(th, F[i], m)
        if not iv:
            continue
        thk = np.mod(p["th0"][i] / TWO_PI + kk3 * p["alpha"][i], 1.0)
        hit = np.zeros(K3, bool)
        for (lo, hi) in iv:
            hit |= (thk >= lo) & (thk <= hi)
        idx = np.nonzero(hit)[0]
        if len(idx) >= 8:
            ng.append(len(np.unique(np.diff(idx))))
        if len(idx):
            th_k = p["th0"][i] + TWO_PI * idx * p["alpha"][i]
            d = g_slice({k: v[i: i + 1] for k, v in p.items()}, th_k)
            t_ = conj_times({k: v[i: i + 1] for k, v in p.items()}, idx)
            dt = time_dist({k: v[i: i + 1] for k, v in p.items()}, t_)
            agree.append(float(np.mean(dt < m)))
    ng = np.array(ng)
    out["three_gap"] = dict(threshold=m, pairs_checked=int(len(ng)),
                            frac_le3=float(np.mean(ng <= 3)) if len(ng) else None,
                            max_distinct=int(ng.max()) if len(ng) else None,
                            time_path_agree=float(np.mean(agree)) if agree else None)


def stage_d(out):
    p = sample_pairs(4096, sigma_e=0.1)
    G = 2048
    th, F = g_grid(p, G)
    m = 1e-3
    intervals = []
    for i in range(len(p["a1"])):
        _, iv = windows_below(th, F[i], m)
        intervals.append(iv)
    haswin = np.array([bool(iv) for iv in intervals])
    kmax = 32768
    ks = first_hit_scan(p["alpha"], p["th0"] / TWO_PI, intervals, kmax)
    qs = np.arange(1, 65)
    dist = np.abs(p["alpha"][:, None] * qs[None, :]
                  - np.round(p["alpha"][:, None] * qs[None, :])).min(1)
    buckets = [(0.0, 1e-4), (1e-4, 1e-3), (1e-3, 1e-2), (1e-2, 1.01)]
    bstats = []
    for lo, hi in buckets:
        sel = haswin & (dist >= lo) & (dist < hi)
        if sel.sum() == 0:
            continue
        unc = ks[sel] >= 0
        bstats.append(dict(beta_lo=lo, beta_hi=hi, n=int(sel.sum()),
                           censored_frac=float(1 - unc.mean()) if sel.sum() else None,
                           median_kstar=float(np.median(ks[sel][unc])) if unc.any() else None))
    out["near_rational"] = bstats
    out["window_frac_1e-3"] = float(haswin.mean())
    np.savetxt("staircase.csv", np.column_stack([p["dlt"], p["alpha"], ks, dist, haswin]),
               delimiter=",", header="delta,alpha,kstar,beta_min,has_window", comments="")


def stage_e(out):
    m = 1e-3
    D_tol = 0.2
    es = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    rows = []
    for e in es:
        n = 48
        p = sample_pairs(n, sigma_e=0.05)
        p["e1"] = np.full(n, 0.05)
        p["e2"] = np.full(n, e)
        p["dlt"] = np.full(n, 0.02)
        p["a2"] = p["a1"] + p["dlt"]
        finish(p)
        tsyn = TWO_PI / p["u"][0]
        nper, sps = 16, 2048
        ts = np.linspace(0.0, nper * tsyn, nper * sps, endpoint=False)
        total_events = 0
        con_detected = 0
        for i0 in range(0, n, 12):
            i1 = min(i0 + 12, n)
            pp = {k: v[i0:i1] for k, v in p.items()}
            m_ = i1 - i0
            T = np.repeat(ts[None, :], m_, 0)
            M1 = pp["M01"][:, None] + pp["n1"][:, None] * T
            M2 = pp["M02"][:, None] + pp["n2"][:, None] * T
            x1, y1 = pos(np.repeat(pp["a1"][:, None], T.shape[1], 1),
                         np.repeat(pp["e1"][:, None], T.shape[1], 1),
                         np.repeat(pp["varpi1"][:, None], T.shape[1], 1), M1)
            x2, y2 = pos(np.repeat(pp["a2"][:, None], T.shape[1], 1),
                         np.repeat(pp["e2"][:, None], T.shape[1], 1),
                         np.repeat(pp["varpi2"][:, None], T.shape[1], 1), M2)
            d = np.hypot(x1 - x2, y1 - y2)
            dlam = np.mod(M1 + pp["varpi1"][:, None] - M2 - pp["varpi2"][:, None], TWO_PI)
            dlam = np.minimum(dlam, TWO_PI - dlam)
            dm = d[:, 1:-1]
            loc = (dm < m) & (dm < d[:, :-2]) & (dm <= d[:, 2:])
            for i in range(m_):
                idx = np.nonzero(loc[i])[0] + 1
                total_events += len(idx)
                con_detected += int(np.sum(dlam[i][idx] < D_tol))
        rows.append(dict(e2=e, events=total_events,
                         leak_frac=float(1 - con_detected / max(total_events, 1))))
    out["leak"] = rows


def stage_f(out):
    p = sample_pairs(1024)
    G = 2048
    th, F = g_grid(p, G)
    gmin = F.min(1)
    m = float(np.percentile(gmin, 30)) * 3  # ~70% of pairs have windows
    centers, widths = [], []
    for i in range(len(p["a1"])):
        _, iv = windows_below(th, F[i], m)
        if not iv:
            centers.append(None)
            widths.append(0.0)
            continue
        widths.append(sum(hi - lo for lo, hi in iv))
        big = max(iv, key=lambda z: z[1] - z[0])
        centers.append(((big[0] + big[1]) / 2.0) % 1.0)
    keep = np.array([c is not None for c in centers])
    idx = np.nonzero(keep)[0]
    cen = np.array([centers[i] for i in idx])
    wid = np.array([widths[i] for i in idx])
    al = p["alpha"][idx]
    t0f = p["th0"][idx] / TWO_PI
    etas = [0.0, 1e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3]
    kmax = 262144
    rows = []
    for eta in etas:
        ks = np.full(len(idx), -1)
        found = np.zeros(len(idx), bool)
        x = t0f.copy()
        c = cen.copy()
        for k in range(1, kmax + 1):
            x += al
            x -= np.floor(x)
            if eta:
                c += eta
                c -= np.floor(c)
            dd = np.abs(x - c)
            np.minimum(dd, 1.0 - dd, out=dd)
            hit = (~found) & (dd <= wid / 2)
            if hit.any():
                ks[hit] = k
                found |= hit
            if eta and k * eta > 3.0:
                break
            if found.all():
                break
        rows.append(dict(eta=eta, n=int(len(idx)), median_w=float(np.median(wid)),
                         frac_hit=float(found.mean()),
                         median_kstar=float(np.median(ks[found])) if found.any() else None,
                         p90_kstar=float(np.percentile(ks[found], 90)) if found.any() else None))
    out["drift"] = rows
    out["drift_threshold"] = m


if __name__ == "__main__":
    stages = sys.argv[1:] or ["a", "b", "d", "e", "f"]
    out = {}
    for s in stages:
        {"a": stage_a, "b": stage_b, "d": stage_d, "e": stage_e, "f": stage_f}[s](out)
        print(f"stage {s} done", flush=True)
    with open("enc_results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))
