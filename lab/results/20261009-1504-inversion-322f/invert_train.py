#!/usr/bin/env python3
"""Inversion of the train certificate (gold 20261006-0346-taleb-09b5).

Independent instrument: 2D Kepler fleets (analytic propagation), encounters by
brute fine sampling (formation scenes) or analytic crossing/beat search (debris
pinwheel). For every encounter we measure:
  - distance-rank of the partner at closest approach, min over both directions
    (exactly the gold's instrument), and
  - lambda-rank: |index gap| in the mean-longitude sort at encounter time
    (what the adopted "sort by longitude, watch k neighbours" train watches),
plus how many mean-longitude order swaps (overtakes) happen over the horizon.

Self-checks: Kepler M->E->f->M roundtrip; pinwheel crossing radius identity.
"""
import json
import sys

import numpy as np

TAU = 2.0 * np.pi
RHO = 1e-4


def rng_of(seed):
    return np.random.default_rng(seed)


def kepler_E(M, e):
    E = M.copy()
    for _ in range(16):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def inv_kepler_M(f, e):
    """true anomaly -> mean anomaly"""
    E = 2.0 * np.arctan2(np.sqrt((1.0 - e) / (1.0 + e)) * np.tan(f / 2.0), 1.0)
    return E - e * np.sin(E)


def states(a, e, pom, lam0, t):
    """positions/velocities of all bodies at scalar time t (n = a^-1.5)."""
    n = a ** -1.5
    M = (lam0 - pom + n * t) % TAU
    E = kepler_E(M, e)
    r = a * (1.0 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    fac = np.sqrt(1.0 - e * e)
    th = (pom + np.arctan2(fac * sE, cE - e)) % TAU
    x, y = r * np.cos(th), r * np.sin(th)
    mu = n * n * a * a * a
    h = np.sqrt(mu * a * (1.0 - e * e))
    vr = (n * a * e * np.sin(E)) / (1.0 - e * np.cos(E))
    vth = h / r
    vx = vr * np.cos(th) - vth * np.sin(th)
    vy = vr * np.sin(th) + vth * np.cos(th)
    return x, y, vx, vy, th, r


def mean_longs(a, lam0, t):
    return (lam0 + a ** -1.5 * t) % TAU


def binet_diameter(e, pom, a):
    """max over pairs of sup_phi |u_i - u_j|, u=(1+e cos(phi-pom))/p (a~1)."""
    best = 0.0
    for i in range(len(e)):
        A = np.hypot(e[i] - e * np.cos(pom[i] - pom), e * np.sin(pom[i] - pom)) / (a * (1 - e * e))
        A[i] = 0.0
        best = max(best, float(A.max()))
    return best


def ranks_at(t, i, j, a, e, pom, lam0):
    """distance-rank (gold's instrument, min over directions), lambda-rank
    (mean-longitude sort gap: the cheap element) and theta-rank (true-longitude
    sort gap: the spatial reading of 'sort by longitude')."""
    x, y, _, _, th, _ = states(a, e, pom, lam0, t)
    di = np.hypot(x - x[i], y - y[i])
    ri = int(np.where(np.argsort(di, kind="stable") == j)[0][0])
    dj = np.hypot(x - x[j], y - y[j])
    rj = int(np.where(np.argsort(dj, kind="stable") == i)[0][0])
    lam = mean_longs(a, lam0, t)
    li = int(np.where(np.argsort(lam, kind="stable") == i)[0][0])
    lj = int(np.where(np.argsort(lam, kind="stable") == j)[0][0])
    oi = int(np.where(np.argsort(th, kind="stable") == i)[0][0])
    oj = int(np.where(np.argsort(th, kind="stable") == j)[0][0])
    N = len(a)
    lg, tg = abs(li - lj), abs(oi - oj)
    return min(ri, rj), min(lg, N - lg), min(tg, N - tg)


def summarize(encs, label, extra=None):
    if not encs:
        print(json.dumps({"scene": label, "encounters": 0, **(extra or {})}))
        return
    dr = np.array([q[0] for q in encs])
    lr = np.array([q[1] for q in encs])
    tr = np.array([q[2] for q in encs])
    out = {
        "scene": label,
        "encounters_ranked": len(encs),
        "dist_rank": {"p50": int(np.median(dr)), "p99": int(np.percentile(dr, 99)), "max": int(dr.max()),
                      "le4": float((dr <= 4).mean())},
        "lam_rank": {"p50": int(np.median(lr)), "p99": int(np.percentile(lr, 99)), "max": int(lr.max()),
                     "le4": float((lr <= 4).mean())},
        "theta_rank": {"p50": int(np.median(tr)), "p99": int(np.percentile(tr, 99)), "max": int(tr.max()),
                       "le4": float((tr <= 4).mean())},
        "watch_k4_catches_lambda_sort": float((lr <= 4).mean()),
        "watch_k4_catches_theta_sort": float((tr <= 4).mean()),
    }
    if extra:
        out.update(extra)
    print(json.dumps(out), flush=True)


def swaps_over_horizon(a, lam0, T):
    """count of mean-longitude order swaps (overtakes) fleet-wide over [0,T]."""
    n = a ** -1.5
    d0 = lam0[:, None] - lam0[None, :]              # unwrapped difference
    d1 = d0 + (n[:, None] - n[None, :]) * T
    iu = np.triu_indices(len(a), 1)
    return int(np.sum(np.floor(d0[iu] / TAU) != np.floor(d1[iu] / TAU)))


# ---------------------------------------------------------------- formation scenes

def fleet(nc, a_hw, sig_lam, seed, sig_e=1e-3, pom_half=0.1):
    r = rng_of(seed)
    a = 1.0 + (2 * r.random(nc) - 1) * a_hw
    e = np.clip(r.rayleigh(sig_e, nc), None, 1e-2)
    pom = TAU * r.random() + (2 * r.random(nc) - 1) * pom_half
    if sig_lam > 0:
        lam = (TAU * r.random() + sig_lam * r.standard_normal(nc)) % TAU
    else:
        lam = TAU * r.random(nc)
    return a, e, pom, lam


def formation_scene(label, nc, a_hw, sig_lam, seed, orbits=10.0, dt=1e-3, rank_cap=400):
    a, e, pom, lam = fleet(nc, a_hw, sig_lam, seed)
    T = orbits * TAU
    steps = int(T / dt)
    best = {}
    for s in range(steps):
        t = s * dt
        x, y, _, _, th, _ = states(a, e, pom, lam, t)
        o = np.argsort(th)
        ths = th[o]
        gaps = np.append(np.diff(ths), ths[0] + TAU - ths[-1])
        small = gaps < 3 * RHO * 1.05
        for p in np.where(small)[0]:
            q = (p + 1) % nc
            u, v = int(o[p]), int(o[q])
            key = (min(u, v), max(u, v))
            dd = float(np.hypot(x[u] - x[v], y[u] - y[v]))
            if dd < 40 * RHO and (key not in best or dd < best[key][0]):
                best[key] = (dd, t)
            if p + 2 < nc and small[p + 1]:
                w = int(o[p + 2])
                key = (min(u, w), max(u, w))
                dd = float(np.hypot(x[u] - x[w], y[u] - y[w]))
                if dd < 40 * RHO and (key not in best or dd < best[key][0]):
                    best[key] = (dd, t)
    encs = [(k, v) for k, v in best.items() if v[0] < RHO]
    rr = []
    for (i, j), (d, t) in encs[:rank_cap]:
        dr, lr, tr = ranks_at(t, i, j, a, e, pom, lam)
        rr.append((dr, lr, tr))
    x, y, _, _, th, r = states(a, e, pom, lam, T / 2)
    o = np.argsort(th)
    ths = th[o]
    gaps = np.append(np.diff(ths), ths[0] + TAU - ths[-1])
    spacing = float(np.median(gaps * r[o]))
    summarize(rr, label, extra={
        "spacing_over_rho": round(spacing / RHO, 3),
        "encounters_total": len(encs),
        "swaps": swaps_over_horizon(a, lam, T),
        "binet_diam": float(binet_diameter(e, pom, a)),
    })


# ---------------------------------------------------------------- pinwheel debris

def pinwheel_scene(label, nc, seed, ecc=0.05, a_hw=1e-5, orbits=20.0, rank_cap=150):
    r = rng_of(seed)
    a = 1.0 + (2 * r.random(nc) - 1) * a_hw
    e = np.full(nc, ecc) + r.rayleigh(1e-3, nc)
    pom = TAU * r.random(nc)
    lam0 = TAU * r.random(nc)
    n = a ** -1.5
    T = orbits * TAU
    ks = np.arange(0, int(orbits) + 4)

    def cross_enc(i, j):
        dp = (pom[i] - pom[j] + np.pi) % TAU - np.pi
        if abs(dp) < 1e-6:
            return []
        out = []
        for half in (0.0, np.pi):
            thc = (pom[i] + pom[j]) / 2.0 + half
            fi = (thc - pom[i] + np.pi) % TAU - np.pi
            fj = (thc - pom[j] + np.pi) % TAU - np.pi
            Mi, Mj = inv_kepler_M(fi, e[i]), inv_kepler_M(fj, e[j])
            ti = (pom[i] + Mi - lam0[i]) / n[i] + ks * (TAU / n[i])
            tj = (pom[j] + Mj - lam0[j]) / n[j] + ks * (TAU / n[j])
            ti = ti[(ti > TAU) & (ti < T - TAU)]
            tj = tj[(tj > 0) & (tj < T)]
            if len(ti) == 0 or len(tj) == 0:
                continue
            dtm = np.abs(ti[:, None] - tj[None, :])
            p, q = np.unravel_index(np.argmin(dtm), dtm.shape)
            D = ti[p] - tj[q]
            if abs(D) > 0.3:
                continue
            tm = 0.5 * (ti[p] + tj[q])
            p_c = a[i] * (1 - e[i] ** 2)
            rc = p_c / (1 + e[i] * np.cos(fi))
            Eci = kepler_E(np.array([Mi]), e[i])[0]
            Ecj = kepler_E(np.array([Mj]), e[j])[0]
            vri = (n[i] * a[i] * e[i] * np.sin(Eci)) / (1 - e[i] * np.cos(Eci))
            vrj = (n[j] * a[j] * e[j] * np.sin(Ecj)) / (1 - e[j] * np.cos(Ecj))
            vthi = n[i] * a[i] * a[i] * np.sqrt(1 - e[i] ** 2) / rc
            vthj = n[j] * a[j] * a[j] * np.sqrt(1 - e[j] ** 2) / rc
            vi = np.array([vri * np.cos(thc) - vthi * np.sin(thc), vri * np.sin(thc) + vthi * np.cos(thc)])
            vj = np.array([vrj * np.cos(thc) - vthj * np.sin(thc), vrj * np.sin(thc) + vthj * np.cos(thc)])
            dv, sv = vi - vj, vi + vj
            u = -(dv @ sv) * D / 2.0 / (dv @ dv)
            w = dv * u + sv * D / 2.0
            out.append((float(np.hypot(*w)), tm))
        return out

    encs = []
    for i in range(nc):
        for j in range(i + 1, nc):
            for dmin, tm in cross_enc(i, j):
                if dmin < RHO:
                    encs.append(((i, j), dmin, tm))
    rr = []
    sel = rng_of(seed ^ 0xabc)
    if encs:
        take = sel.choice(len(encs), size=min(rank_cap, len(encs)), replace=False)
        for k in take:
            (i, j), d, t = encs[k]
            dr, lr, tr = ranks_at(t, i, j, a, e, pom, lam0)
            rr.append((dr, lr, tr))
    summarize(rr, label, extra={
        "pairs": nc * (nc - 1) // 2,
        "encounters_total": len(encs),
        "enc_per_ship_per_orbit": round(len(encs) / nc / orbits, 4),
        "swaps": swaps_over_horizon(a, lam0, T),
        "binet_diam": float(binet_diameter(e, pom, a)),
    })


def selfcheck():
    M = np.linspace(0.01, TAU - 0.01, 2001)
    err = 0.0
    for e in (0.001, 0.05, 0.2):
        E = kepler_E(M, e)
        f = 2 * np.arctan2(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2), 1.0)
        M2 = inv_kepler_M(f, e)
        err = max(err, float(np.abs((M2 - M + np.pi) % TAU - np.pi).max()))
        assert err < 1e-11, (e, err)
    a, e, pom, lam = fleet(50, 1e-5, 0.0, 7)
    e[:] = 0.05
    p = a[0] * (1 - e[0] ** 2)
    thc = (pom[0] + pom[1]) / 2
    f0 = (thc - pom[0] + np.pi) % TAU - np.pi
    rc = p / (1 + e[0] * np.cos(f0))
    E0 = kepler_E(np.array([inv_kepler_M(f0, e[0])]), e[0])[0]
    r0 = a[0] * (1 - e[0] * np.cos(E0))
    assert abs(r0 - rc) < 1e-12, (r0, rc)
    print(json.dumps({"selfcheck": "ok", "kepler_roundtrip_max_err": err}), flush=True)


if __name__ == "__main__":
    selfcheck()
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "s0"):
        formation_scene("S0-control gold-fleet", 200, 1e-5, 0.01, 27)
    if mode in ("all", "s2"):
        for s in (3e-3, 1e-3, 5e-4, 3e-4):
            formation_scene(f"S2-jam sig_lam={s}", 200, 1e-5, s, 27 + int(s * 1e5))
    if mode in ("all", "s1"):
        pinwheel_scene("S1-pinwheel-debris seed11", 400, 11)
        pinwheel_scene("S1-pinwheel-debris seed12", 400, 12)
