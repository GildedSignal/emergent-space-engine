#!/usr/bin/env python3
"""Synodic return map of a belt pair: representation check, tails, drift crossover.

Two coplanar Kepler orbits about one primary (mu=1, a2=1). At a longitude
conjunction both bodies sit on the same ray, so the conjunction miss distance is
purely radial: b(L) = |p1/(1+e1 cos(L-w1)) - p2/(1+e2 cos(L-w2))| at conjunction
longitude L. Conjunction longitudes advance by alpha per conjunction
(alpha = 2pi/(1-r^1.5) mod 2pi, r=a1/a2), so {b_k} is a circle rotation observed
through f. Part A validates against full Kepler (and measures the
conjunction-less leak); B/C iterate the rotation.

Usage: conjmap.py [ABC]  (writes results_<parts>.json, hit_B.npy, pairs_B.npy)
"""
import json
import sys
import time

import numpy as np

rng = np.random.default_rng(20261007)
OUT = {}
R_GRID = (0.02, 0.05)


def kepler_E(M, e):
    E = M.copy()
    for _ in range(7):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def lon_r(t, a, e, w, M0, n):
    """Longitude and radius; arrays broadcast over t."""
    M = M0 + n * t
    E = kepler_E(M, e)
    f = E + 2.0 * np.arctan2(e * np.sin(E), 1.0 - e * np.cos(E))
    return w + f, a * (1.0 - e * np.cos(E))


def miss_f(th, a1, e1, w1, a2, e2, w2):
    p1 = a1 * (1.0 - e1**2)
    p2 = a2 * (1.0 - e2**2)
    return np.abs(
        p1 / (1.0 + e1 * np.cos(th - w1)) - p2 / (1.0 + e2 * np.cos(th - w2))
    )


def state_at_L(L, a, e, w):
    """Closed-form radius and velocity at true longitude L (mu=1)."""
    f = L - w
    p = a * (1.0 - e**2)
    r = p / (1.0 + e * np.cos(f))
    v_t = (1.0 + e * np.cos(f)) / np.sqrt(p)
    v_r = (e * np.sin(f)) / np.sqrt(p)
    return r, v_r, v_t


def b_tilde(th, a1, e1, w1, a2, e2, w2):
    """Oepik perpendicular distance of the relative pass at conjunction L."""
    r1, vr1, vt1 = state_at_L(th, a1, e1, w1)
    r2, vr2, vt2 = state_at_L(th, a2, e2, w2)
    dr = r1 - r2
    dvt = vt1 - vt2
    dvr = vr1 - vr2
    return np.abs(dr * dvt) / np.sqrt(dvr**2 + dvt**2)


def part_a():
    """Full Kepler: rotation residual (e=0.1) + conjunction-less leak vs chi."""
    res = {}
    P, K = 256, 240
    e_levels = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5]
    leak = {}
    # first: single e=0.1 draw for the rotation-residual checks
    sweep = [(0.1, dA) for dA in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2)]
    sweep += [(eL, round(0.85 * 2 * eL, 3)) for eL in (0.05, 0.1, 0.2, 0.4)]
    sweep += [(0.05, round(0.6 * 2 * 0.05, 3)), (0.2, round(0.6 * 2 * 0.2, 3))]
    for eL, dA in sweep:
        if dA > 0.9 * 2 * eL:
            continue
        a1 = 1.0 + dA + rng.uniform(-0.002, 0.002, P)
        a2 = np.ones(P)
        e1 = np.full(P, eL)
        e2 = np.full(P, eL)
        w1 = rng.uniform(0, 2 * np.pi, P)
        w2 = rng.uniform(0, 2 * np.pi, P)
        M10 = rng.uniform(0, 2 * np.pi, P)
        M20 = rng.uniform(0, 2 * np.pi, P)
        n1 = a1**-1.5
        s = n1 - 1.0
        kk = np.arange(1, K + 1)[:, None]
        tgt = 2 * np.pi * kk + (w1 + M10 - w2 - M20)
        t = tgt / s
        h = 0.05 * (2 * np.pi / np.abs(s))
        for _ in range(8):  # vectorized secant on lam1(t)-lam2(t)=tgt
            la1, _ = lon_r(t, a1, e1, w1, M10, n1)
            la2, _ = lon_r(t, a2, e2, w2, M20, 1.0)
            G0 = (la1 - la2 - tgt).astype(float)
            la1h, _ = lon_r(t + h, a1, e1, w1, M10, n1)
            la2h, _ = lon_r(t + h, a2, e2, w2, M20, 1.0)
            G1 = (la1h - la2h - tgt).astype(float)
            t = t - G0 * h / (G1 - G0)
        la1, r1_ = lon_r(t, a1, e1, w1, M10, n1)
        la2, r2_ = lon_r(t, a2, e2, w2, M20, 1.0)
        b_conj = np.abs(r1_ - r2_)  # same ray: radial difference
        L = la1 % (2 * np.pi)
        dL = np.diff(L, axis=0)
        dL_std = float(np.median(np.std(dL - dL.mean(axis=0), axis=0)))
        # closed-form Oepik perpendicular distance at each conjunction
        bt = b_tilde(L, a1, e1, w1, a2, e2, w2)
        # window minimum (true closest approach near each conjunction):
        # full 2-D distance, warm-started Kepler on a subsample
        Psyn = 2 * np.pi / np.abs(s)
        ntau = 161
        tau = np.linspace(-0.25, 0.25, ntau)[None, :, None] * Psyn
        KW = 48
        tw = t[:KW]
        Mk10 = M10[None, :] + n1[None, :] * tw
        Mk20 = M20[None, :] + tw
        E1w = kepler_E(Mk10, e1)
        E2w = kepler_E(Mk20, e2)
        bmin = np.full((KW, P), np.inf)
        for i0 in range(0, ntau, 40):
            dtau = tau[:, i0 : i0 + 40, :]
            shp = (dtau.shape[1], KW, P)
            M1g = (Mk10[None, :, :] + n1[None, None, :] * dtau[0][:, None, :]).reshape(-1)
            M2g = (Mk20[None, :, :] + dtau[0][:, None, :]).reshape(-1)
            E1 = np.broadcast_to(E1w, shp).reshape(-1).copy()
            E2 = np.broadcast_to(E2w, shp).reshape(-1).copy()
            e1g = np.broadcast_to(e1, shp).reshape(-1)
            e2g = np.broadcast_to(e2, shp).reshape(-1)
            for _ in range(3):
                E1 -= (E1 - e1g * np.sin(E1) - M1g) / (1.0 - e1g * np.cos(E1))
                E2 -= (E2 - e2g * np.sin(E2) - M2g) / (1.0 - e2g * np.cos(E2))
            f1 = E1 + 2.0 * np.arctan2(e1g * np.sin(E1), 1.0 - e1g * np.cos(E1))
            f2 = E2 + 2.0 * np.arctan2(e2g * np.sin(E2), 1.0 - e2g * np.cos(E2))
            lam1 = f1 + np.broadcast_to(w1, shp).reshape(-1)
            lam2 = f2 + np.broadcast_to(w2, shp).reshape(-1)
            r1g = np.broadcast_to(a1, shp).reshape(-1) * (1.0 - e1g * np.cos(E1))
            r2g = np.broadcast_to(a2, shp).reshape(-1) * (1.0 - e2g * np.cos(E2))
            dx = r1g * np.cos(lam1) - r2g * np.cos(lam2)
            dy = r1g * np.sin(lam1) - r2g * np.sin(lam2)
            bmin = np.minimum(bmin, np.hypot(dx, dy).reshape(shp).min(axis=0))
        chi = dA / (eL if eL > 0 else 1.0)
        for R in R_GRID:
            n_true = int((bmin < R).sum())
            key = f"e={eL},da={dA},chi={chi:.2f},R={R}"
            leak[key] = {
                "n_true": n_true,
                "dL_std_rad": dL_std,
                "leak_conj": float(((bmin < R) & (b_conj[:KW] >= R)).sum())
                / max(n_true, 1),
                "leak_oepik": float(((bmin < R) & (bt[:KW] >= R)).sum())
                / max(n_true, 1),
            }
        ratio = bmin / np.maximum(bt[:KW], 1e-12)
        res.setdefault("bmin_over_btilde_p10_med_p90", []).append(
            [f"e={eL},da={dA}",
             float(np.percentile(ratio, 10)),
             float(np.median(ratio)),
             float(np.percentile(ratio, 90))]
        )
    res["leak_table"] = leak
    OUT["A"] = res


def sample_pairs(M, R):
    """Crossing belt pairs (Binet-cone population) with rotation parameters."""
    a1 = 1.0 + rng.uniform(0.005, 0.25, 4 * M)
    e1 = np.minimum(rng.rayleigh(0.1, 4 * M), 0.35)
    e2 = np.minimum(rng.rayleigh(0.1, 4 * M), 0.35)
    w1 = rng.uniform(0, 2 * np.pi, 4 * M)
    w2 = rng.uniform(0, 2 * np.pi, 4 * M)
    cross = (a1 * (1 - e1) < 1 + e2) & (1 - e2 < a1 * (1 + e1))
    a1, e1, e2, w1, w2 = (v[cross][:M] for v in (a1, e1, e2, w1, w2))
    M = len(a1)
    alpha = (2 * np.pi / (1.0 - a1**1.5)) % (2 * np.pi)
    th0 = rng.uniform(0, 2 * np.pi, M)
    g = np.linspace(0, 2 * np.pi, 8192, endpoint=False)
    eps = (miss_f(g[:, None], a1, e1, w1, 1.0, e2, w2) < R).mean(axis=0)
    return a1, e1, e2, w1, w2, alpha, th0, eps


def runs_and_gaps(hit):
    M, T = hit.shape
    clusters, gaps = [], []
    for i in range(M):
        x = hit[i]
        if not x.any():
            continue
        z = np.diff(np.r_[0, x.astype(np.int8), 0])
        si = np.flatnonzero(z == 1)
        ei = np.flatnonzero(z == -1)
        clusters.append(ei - si)
        if len(si) > 1:
            gaps.append(si[1:] - ei[:-1])
    cl = np.concatenate(clusters) if clusters else np.array([], int)
    gp = np.concatenate(gaps) if gaps else np.array([], int)
    return cl, gp


def ccdf_slope(gp, qs=(2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000)):
    qs = np.array([q for q in qs if q < np.percentile(gp, 99.5)], dtype=float)
    if len(qs) < 3:
        return None, None
    cc = np.array([np.mean(gp > q) for q in qs])
    ok = cc > 0
    if ok.sum() < 3:
        return None, None
    sl = float(np.polyfit(np.log(qs[ok]), np.log(cc[ok]), 1)[0])
    return sl, {int(q): float(c) for q, c in zip(qs, cc) if c > 0}


def part_b(R=0.05, M=1500, T=65536, keep_eps=3e-4):
    a1, e1, e2, w1, w2, alpha, th0, eps = sample_pairs(M, R)
    sel = eps > keep_eps
    a1, e1, e2, w1, w2, alpha, th0, eps = (
        v[sel] for v in (a1, e1, e2, w1, w2, alpha, th0, eps)
    )
    M = len(a1)
    hit = np.zeros((M, T), dtype=bool)
    hit2 = np.zeros((M, T), dtype=bool)
    th = th0.copy()
    for k in range(T):
        hit[:, k] = miss_f(th, a1, e1, w1, 1.0, e2, w2) < R
        hit2[:, k] = b_tilde(th, a1, e1, w1, 1.0, e2, w2) < R
        th = th + alpha
    cl, gp = runs_and_gaps(hit)
    res = {
        "R": R,
        "M_crossing_pairs": M,
        "epsilon_median": float(np.median(eps)),
        "hit_rate_per_conj_median": float(np.median(hit.mean(axis=1))),
        "cluster_mean": float(cl.mean()),
        "cluster_p99": float(np.percentile(cl, 99)),
        "P_cluster_ge4": float(np.mean(cl >= 4)),
        "P_cluster_ge10": float(np.mean(cl >= 10)),
        "gap_median": float(np.median(gp)),
        "gap_p99_over_p50": float(np.percentile(gp, 99) / np.median(gp)),
        "gap_p999": float(np.percentile(gp, 99.9)),
    }
    res["gap_ccdf_loglog_slope"], res["gap_ccdf_points"] = ccdf_slope(gp)
    per_maxc = np.zeros(M, int)
    for i in range(M):
        z = np.diff(np.r_[0, hit[i].astype(np.int8), 0])
        if (z == 1).any():
            per_maxc[i] = (
                np.flatnonzero(z == -1) - np.flatnonzero(z == 1)
            ).max()
    sticky = per_maxc >= 4
    av = alpha / (2 * np.pi)
    best_d = np.full(M, 9.0)
    best_q = np.zeros(M, int)
    for q in range(1, 51):
        d = np.abs(av - np.round(av * q) / q)
        upd = d < best_d
        best_d[upd] = d[upd]
        best_q[upd] = q
    res["per_pair_max_cluster_ge10_share"] = float(np.mean(per_maxc >= 10))
    if sticky.sum() > 3:
        res["sticky_share"] = float(sticky.mean())
        res["sticky_bestq_le8_share"] = float(np.mean(best_q[sticky] <= 8))
        res["nonsticky_bestq_le8_share"] = float(np.mean(best_q[~sticky] <= 8))
        res["sticky_bestd_median"] = float(np.median(best_d[sticky]))
        res["nonsticky_bestd_median"] = float(np.median(best_d[~sticky]))
    maxwin = np.zeros(M, int)
    for i in range(M):
        W = max(int(round(abs(alpha[i]) / (2 * np.pi))), 1)
        c = np.convolve(hit[i].astype(np.int32), np.ones(W, int), "valid")
        maxwin[i] = int(c.max()) if len(c) else 0
    res["events_per_orbit_window_p50_p99_max"] = [
        float(np.median(maxwin)),
        float(np.percentile(maxwin, 99)),
        int(maxwin.max()),
    ]
    cl2, gp2 = runs_and_gaps(hit2)
    res["oepik"] = {
        "hit_rate_per_conj_median": float(np.median(hit2.mean(axis=1))),
        "cluster_mean": float(cl2.mean()) if len(cl2) else None,
        "P_cluster_ge4": float(np.mean(cl2 >= 4)) if len(cl2) else None,
        "gap_median": float(np.median(gp2)) if len(gp2) else None,
        "gap_p99_over_p50": float(np.percentile(gp2, 99) / np.median(gp2))
        if len(gp2)
        else None,
    }
    if len(gp2) > 500:
        res["oepik"]["gap_ccdf_loglog_slope"], _ = ccdf_slope(gp2)
    OUT["B"] = res
    np.save("hit_B.npy", hit[:64, :4096])
    np.save(
        "pairs_B.npy", np.column_stack([a1, e1, e2, w1, w2, alpha, th0, eps])[:64]
    )


def part_c(R=0.05, M=400, T=16384, sigmas=(0.0, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2)):
    a1, e1, e2, w1, w2, alpha, th0, eps = sample_pairs(M, R)
    sel = eps > 1e-3
    a1, e1, e2, w1, w2, alpha, th0, eps = (
        v[sel] for v in (a1, e1, e2, w1, w2, alpha, th0, eps)
    )
    M = len(a1)
    out = {}
    for sg in sigmas:
        rng_c = np.random.default_rng(77)
        hit = np.zeros((M, T), dtype=bool)
        th = th0.copy()
        dth = alpha.copy()
        for k in range(T):
            hit[:, k] = b_tilde(th, a1, e1, w1, 1.0, e2, w2) < R
            th = th + dth
            if sg > 0:
                dth = dth + sg * rng_c.standard_normal(M)
        cl, gp = runs_and_gaps(hit)
        d = {
            "cluster_mean": float(cl.mean()) if len(cl) else None,
            "gap_median": float(np.median(gp)) if len(gp) else None,
            "gap_p99": float(np.percentile(gp, 99)) if len(gp) else None,
        }
        if len(gp) > 500:
            d["gap_p999_over_p50"] = float(np.percentile(gp, 99.9) / np.median(gp))
            d["gap_ccdf_loglog_slope"], _ = ccdf_slope(gp)
        out[sg] = d
    # certificate invalidation: frozen-alpha prediction vs drifting reality
    inv = {}
    for sg in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2):
        rng_i = np.random.default_rng(991)
        traj = np.empty((M, T))
        th = th0.copy()
        dth = alpha.copy()
        for k in range(T):
            traj[:, k] = th
            th = th + dth
            if sg > 0:
                dth = dth + sg * rng_i.standard_normal(M)
        hitm = b_tilde(traj % (2 * np.pi), a1[:, None], e1[:, None], w1[:, None], 1.0, e2[:, None], w2[:, None]) < R
        pairs = []
        for i in range(M):
            hi = np.flatnonzero(hitm[i])
            if len(hi) >= 3 and hi[-1] < T - 8:
                pairs.extend((i, a, b) for a, b in zip(hi[:-1], hi[1:]))
        rng_i.shuffle(pairs)
        pairs = pairs[:4000]
        i_arr = np.array([p[0] for p in pairs])
        a_arr = np.array([p[1] for p in pairs], dtype=float)
        b_arr = np.array([p[2] for p in pairs], dtype=float)
        tp = traj[i_arr, a_arr.astype(int)].copy()
        alive = np.ones(len(pairs), bool)
        Tpred = np.full(len(pairs), np.nan)
        for j in range(1, 8193):
            tp = tp + alpha[i_arr]
            h = b_tilde(
                tp % (2 * np.pi), a1[i_arr], e1[i_arr], w1[i_arr], 1.0, e2[i_arr], w2[i_arr]
            ) < R
            h &= alive
            Tpred[h] = j
            alive &= ~h
            if not alive.any():
                break
        ok = ~np.isnan(Tpred)
        if ok.sum() > 50:
            wrong = np.abs((b_arr - a_arr) - Tpred) >= 1
            med = float(np.median(Tpred[ok]))
            near_med = np.abs(Tpred[ok] - med) < 5
            inv[sg] = {
                "n": int(ok.sum()),
                "p_invalid_wrong_conjunction": float(wrong[ok].mean()),
                "median_horizon_conj": med,
                "p_invalid_at_median_horizon": float(wrong[ok][near_med].mean())
                if near_med.any()
                else None,
            }
    OUT["C"] = {
        "epsilon_median": float(np.median(eps)),
        "stats_by_sigma": out,
        "invalidation": inv,
    }

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "ABC"
    for part in which:
        t0 = time.time()
        {"A": part_a, "B": part_b, "C": part_c}[part]()
        print(f"part {part}: {time.time()-t0:.1f}s", file=sys.stderr)
    with open(f"results_{which}.json", "w") as f:
        json.dump(OUT, f, indent=1, default=str)
    print(json.dumps(OUT, indent=1, default=str)[:6000])
