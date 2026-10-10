#!/usr/bin/env python3
"""Inversion run 20261010-0100-inversion-b063.

Falsifies or defends the gold 20261006-0346-taleb-09b5 claim adopted into the encounters
design: under co-orbital concentration every real encounter lies within partner rank 4
along the orbit, so a phase-neighbour certificate at O(n*k), k~4, triggered by a
concentration number, replaces the quadratic pairwise tier.

Scenes (mu=1, a=1, P=2*pi, encounter radius rho):
  S0/S0b: one stream (gold's scene class), n and rho swept. Truth: analytic conjunction
          times (shared e, wp => conjunction == same point on the same curve), verified
          by Kepler distance.
  S1: two co-orbital streams, same a, same e, wp_A=0, wp_B=pi/2; curves cross at
      lam*=pi/4, 5pi/4. Truth: exact pass-time matching at each crossing + Kepler-refined
      closest approach (parabola on d^2).

Floats explore; no canonical outcome is decided here.
"""
import json
import numpy as np

P = 2.0 * np.pi


def wrap_pm(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def body_state(M, e, wp):
    """x, y, r, true longitude. e and wp scalar or array (broadcast against M)."""
    E = kepler_E(M, e)
    xo = np.cos(E) - e
    yo = np.sqrt(1.0 - e * e) * np.sin(E)
    c, s = np.cos(wp), np.sin(wp)
    x = xo * c - yo * s
    y = xo * s + yo * c
    return x, y, np.hypot(x, y), np.arctan2(y, x)


def vel_at_M(M, e, wp):
    """Velocity d(pos)/dM with mean motion 1."""
    E = kepler_E(np.atleast_1d(M), e)
    den = 1.0 - e * np.cos(E)
    dxo = -np.sin(E) / den
    dyo = np.sqrt(1.0 - e * e) * np.cos(E) / den
    c, s = np.cos(wp), np.sin(wp)
    return np.stack([dxo * c - dyo * s, dxo * s + dyo * c], axis=-1)


def nu_to_M(nu, e):
    E = 2.0 * np.arctan(np.sqrt((1.0 - e) / (1.0 + e)) * np.tan(nu / 2.0))
    return E - e * np.sin(E)


def ranks_at(order_key, i_idx, j_idx):
    """Circular rank distance in the ordering given by order_key."""
    order = np.argsort(order_key)
    pos = np.empty(len(order_key), dtype=np.int64)
    pos[order] = np.arange(len(order_key))
    r = np.abs(pos[i_idx] - pos[j_idx]).astype(float)
    n = len(order_key)
    return np.minimum(r, n - r)


def summarize_rank(rk):
    if len(rk) == 0:
        return None
    return {"count": int(len(rk)), "median_rank": float(np.median(rk)),
            "p99_rank": float(np.quantile(rk, 0.99)), "max_rank": int(rk.max()),
            "catch@4": float(np.mean(rk <= 4)), "catch@8": float(np.mean(rk <= 8)),
            "catch@16": float(np.mean(rk <= 16))}


def scene_S0(n, rho, T_orbits=None, seed=7, rank_sample=2000):
    """ONE stream: e=0.01, wp=0 shared; da ~ U(+-rho/2); M0 uniform."""
    rng = np.random.default_rng(seed)
    e, wp = 0.01, 0.0
    if T_orbits is None:
        T_orbits = 200 if rho <= 1e-4 else 20
    a = 1.0 + rng.uniform(-rho / 2, rho / 2, n)
    M0 = rng.uniform(0, 2 * np.pi, n)
    nmm = a ** -1.5
    T = T_orbits * P
    ei, ej, et = [], [], []
    CH = 250_000
    for lo in range(0, n, CH):
        i1 = min(lo + CH, n)
        rows = np.arange(lo, i1)
        dM0 = wrap_pm(M0[lo:i1, None] - M0[None, :])
        delta = nmm[lo:i1, None] - nmm[None, :]
        ii, jj = np.meshgrid(rows, np.arange(n), indexing="ij")
        m = ii < jj
        dM0, delta = dM0[m], delta[m]
        ii, jj = ii[m], jj[m]
        pos_d = delta > 0
        ad = np.abs(delta)
        t = np.where(pos_d & (dM0 < 0), -dM0 / np.where(pos_d, delta, 1),
                     np.where(pos_d & (dM0 >= 0), (2 * np.pi - dM0) / np.where(pos_d, delta, 1),
                              np.where(~pos_d & (dM0 > 0), dM0 / ad,
                                       (dM0 + 2 * np.pi) / np.where(ad > 0, ad, 1))))
        ok = (t > 1e-9) & (t < T) & (ad > 0)
        if ok.any():
            ei.append(ii[ok]); ej.append(jj[ok]); et.append(t[ok])
    ei = np.concatenate(ei); ej = np.concatenate(ej); et = np.concatenate(et)
    # verify real encounter at the analytic conjunction (same curve, radial diff only)
    xi, yi = body_state(M0[ei] + nmm[ei] * et, e, wp)[:2]
    xj, yj = body_state(M0[ej] + nmm[ej] * et, e, wp)[:2]
    d = np.hypot(xi - xj, yi - yj)
    keep = d < rho
    ei, ej, et = ei[keep], ej[keep], et[keep]
    out = {"n": n, "rho": rho, "T_orbits": T_orbits, "encounters": int(len(ei)),
           "per_orbit": len(ei) / T_orbits,
           "max_d_at_conjunction": float(d[keep].max()) if keep.any() else None}
    if len(ei) == 0:
        out["error"] = "no encounters"
        return out
    smp = rng.choice(len(ei), size=min(rank_sample, len(ei)), replace=False)
    ei, ej, et = ei[smp], ej[smp], et[smp]
    res = {}
    for lead in P * np.array([1 / 32, 1 / 8, 1 / 4, 1 / 2, 1.0]):
        rk = np.empty(len(et))
        for k, t in enumerate(et):
            Mk = (M0 + nmm * (t - lead)) % (2 * np.pi)
            rk[k] = ranks_at(Mk, np.array([ei[k]]), np.array([ej[k]]))[0]
        res[f"lead={lead/P:.4f}P"] = summarize_rank(rk)
    out["M_ranks"] = res
    out["candidates_per_encounter"] = (n * (n - 1) / 2) / out["per_orbit"]
    return out


def scene_S1(n_per, e=0.2, rho=1e-4, seed=11):
    """TWO streams: same a=1, same e; wp_A=0, wp_B=pi/2; M0 uniform per fleet."""
    rng = np.random.default_rng(seed)
    wpA, wpB = 0.0, np.pi / 2
    n = 2 * n_per
    M0A = rng.uniform(0, 2 * np.pi, n_per)
    M0B = rng.uniform(0, 2 * np.pi, n_per)
    M0 = np.concatenate([M0A, M0B])
    earr = np.full(n, e)
    warr = np.concatenate([np.full(n_per, wpA), np.full(n_per, wpB)])
    out = {"n": n, "n_per_fleet": n_per, "rho": rho, "e": e}
    ei, ej, et, ed, elam = [], [], [], [], []
    for lam in (np.pi / 4, 5 * np.pi / 4):
        tA = (nu_to_M(wrap_pm(lam - wpA), e) - M0A) % P
        tB = (nu_to_M(wrap_pm(lam - wpB), e) - M0B) % P
        vA = vel_at_M(nu_to_M(wrap_pm(lam - wpA), e), e, wpA)[0]
        vB = vel_at_M(nu_to_M(wrap_pm(lam - wpB), e), e, wpB)[0]
        vrel = float(np.linalg.norm(vA - vB))
        win = 12 * rho / vrel
        dt = wrap_pm(tA[:, None] - tB[None, :])
        ii, jj = np.meshgrid(np.arange(n_per), np.arange(n_per), indexing="ij")
        m = np.abs(dt) < win
        ii, jj, dt = ii[m], jj[m], dt[m]
        tc = 0.5 * (tA[ii] + tB[jj])
        w = np.abs(dt) / 2 + 5 * rho / vrel
        ts = tc[:, None] + np.linspace(-1, 1, 9)[None, :] * w[:, None]
        MA = M0A[ii][:, None] + ts
        MB = M0B[jj][:, None] + ts
        d2 = np.empty(ts.shape)
        for sl in range(9):
            xA, yA = body_state(MA[:, sl], e, wpA)[:2]
            xB, yB = body_state(MB[:, sl], e, wpB)[:2]
            d2[:, sl] = (xA - xB) ** 2 + (yA - yB) ** 2
        # parabola through points 3,4,5 (centered) -> min
        t0, h = ts[:, 4], ts[:, 5] - ts[:, 4]
        c0, c1, c2 = d2[:, 4], (d2[:, 5] - d2[:, 3]) / (2 * h), (d2[:, 5] - 2 * d2[:, 4] + d2[:, 3]) / (2 * h * h)
        disc = np.maximum(c2, 1e-300)
        tmin = t0 - c1 / (2 * disc)
        d2min = c0 - c1 * c1 / (4 * disc)
        good = (tmin > ts[:, 0]) & (tmin < ts[:, 8]) & (d2min < rho * rho)
        out[f"vrel@lam={lam:.3f}"] = vrel
        ei.append(ii[good]); ej.append(n_per + jj[good])
        et.append(tmin[good] % P); ed.append(np.sqrt(np.maximum(d2min[good], 0)))
        elam.append(np.full(int(good.sum()), lam))
    ei = np.concatenate(ei); ej = np.concatenate(ej)
    et = np.concatenate(et); ed = np.concatenate(ed)
    per_orbit = len(ei)  # exactly periodic: one period = one orbit's worth
    out.update({"encounters_per_orbit": int(per_orbit),
                "min_d": float(ed.min()) if per_orbit else None,
                "same_fleet_encounters": 0})
    if per_orbit == 0:
        out["error"] = "no encounters"
        return out
    # M-ordering rank at encounter time (constant in time: same a => dM const)
    rk_enc = ranks_at(M0 % (2 * np.pi), ei, ej)
    out["M_rank_at_encounter"] = {"median": float(np.median(rk_enc)),
                                  "max": int(rk_enc.max()),
                                  "frac_over_n/8": float(np.mean(rk_enc > n / 8))}
    resM, resL = {}, {}
    for lead in P * np.array([1 / 32, 1 / 8, 1 / 4, 1 / 2, 1.0]):
        rkM = np.empty(len(et)); rkL = np.empty(len(et))
        for k, t in enumerate(et):
            Mk = (M0 + (t - lead)) % (2 * np.pi)
            rkM[k] = ranks_at(Mk, np.array([ei[k]]), np.array([ej[k]]))[0]
            lk = body_state(Mk, earr, warr)[3]
            rkL[k] = ranks_at(lk, np.array([ei[k]]), np.array([ej[k]]))[0]
        tag = f"lead={lead/P:.4f}P"
        resM[tag] = summarize_rank(rkM)
        resL[tag] = summarize_rank(rkL)
    out["M_ranks"] = resM
    out["lambda_ranks"] = resL
    out["candidates_per_encounter"] = (n * (n - 1) / 2) / per_orbit
    return out


def main():
    metrics = {}
    print("== S0 control (gold scene class: ONE stream), n=2000, rho=1e-4 ==", flush=True)
    metrics["S0_control"] = scene_S0(2000, 1e-4)
    print(json.dumps(metrics["S0_control"], indent=1), flush=True)

    print("== S0b scaling probe (ONE stream; max/median M-rank at lead=P vs n, rho) ==", flush=True)
    scan = []
    for rho in (1e-4, 1e-3):
        for n in (500, 1000, 2000, 4000):
            o = scene_S0(n, rho)
            r = o.get("M_ranks", {}).get("lead=1.0000P")
            scan.append({"rho": rho, "n": n, "enc_per_orbit": round(o["per_orbit"], 1),
                         "max_rank": r["max_rank"] if r else None,
                         "median_rank": r["median_rank"] if r else None,
                         "k99": r["p99_rank"] if r else None})
            print(scan[-1], flush=True)
    metrics["S0b_scaling"] = scan

    print("== S1 KILL SCENE (TWO co-orbital streams), n_per=1000 ==", flush=True)
    metrics["S1_crossing"] = scene_S1(1000)
    print(json.dumps(metrics["S1_crossing"], indent=1), flush=True)

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=1)
    print("wrote metrics.json", flush=True)


if __name__ == "__main__":
    main()
