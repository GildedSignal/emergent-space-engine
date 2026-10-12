#!/usr/bin/env python3
"""Decisive cross-checks, standalone. (1) dense brute-force time scan vs the
conjunction+Newton machinery on ONE hot belt — the two share only the Kepler
solver; the encounter-finding logic is independent. (2) planet SOI transits,
planet-vs-belt only (the earlier run wrongly reused all-pairs machinery, which
counted belt-belt encounters at R_SOI scale). (3) P2 re-run."""
import json
import math

import numpy as np


def make_belt(n, sigma_e, a_lo, a_hi, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(n))), 0.5)
    pom = rng.uniform(0, 2 * np.pi, n)
    lam = rng.uniform(0, 2 * np.pi, n)
    return a, e, pom, lam


def kepler_pos(a, e, pom, lam, n, t):
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(3):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    r = a * (1 - e * np.cos(E))
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    nu = np.arctan2(fac * np.sin(E), np.cos(E) - e)
    th = nu + pom
    return r * np.cos(th), r * np.sin(th)


def true_long(a, e, pom, lam, n, t):
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(3):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    return np.arctan2(fac * np.sin(E), np.cos(E) - e) + pom


def encounter_rate(a, e, pom, lam, rho, horizon):
    """conjunction + Newton on the true-longitude crossing (as in the main run)."""
    n = a ** -1.5
    N = len(a)
    per_lo = a * (1 - e) - rho
    per_hi = a * (1 + e) + rho
    i, j = np.triu_indices(N, k=1)
    ov = (per_lo[i] <= per_hi[j]) & (per_lo[j] <= per_hi[i])
    i, j = i[ov], j[ov]
    cand = len(i)
    dn = n[i] - n[j]
    dl = (lam[j] - lam[i]) % (2 * np.pi)
    hits = 0
    K = int(np.ceil(np.abs(dn).max() * horizon / (2 * np.pi))) + 1
    for k in range(-1, K + 1):
        with np.errstate(divide="ignore", invalid="ignore"):
            tk = (dl + 2 * np.pi * k) / dn
        good = np.isfinite(tk) & (tk > 0) & (tk <= horizon)
        if not good.any():
            continue
        ii, jj, tkk, dng = i[good], j[good], tk[good], dn[good]
        t = tkk.copy()
        for _ in range(3):
            dth = true_long(a[ii], e[ii], pom[ii], lam[ii], n[ii], t) - \
                true_long(a[jj], e[jj], pom[jj], lam[jj], n[jj], t)
            dth = (dth + np.pi) % (2 * np.pi) - np.pi
            t = t - dth / np.where(dng != 0, dng, 1.0)
        t = np.clip(t, 0.0, horizon)
        x1, y1 = kepler_pos(a[ii], e[ii], pom[ii], lam[ii], n[ii], t)
        x2, y2 = kepler_pos(a[jj], e[jj], pom[jj], lam[jj], n[jj], t)
        best = np.hypot(x1 - x2, y1 - y2)
        xm, ym = kepler_pos(a[ii], e[ii], pom[ii], lam[ii], n[ii], tkk)
        xp, yp = kepler_pos(a[jj], e[jj], pom[jj], lam[jj], n[jj], tkk)
        best = np.minimum(best, np.hypot(xm - xp, ym - yp))
        hits += int((best < rho).sum())
    return hits, hits / (N * horizon / (2 * np.pi)), cand


R = {}
# ---------- (1) dense scan vs conjunction machinery, one hot belt -------------
N, SIGMA_E, RHO, HOR = 200, 0.05, 1e-3, 20 * 2 * math.pi
a, e, pom, lam = make_belt(N, SIGMA_E, 1.0, 1.5, 99)
n = a ** -1.5
per_lo = a * (1 - e) - RHO
per_hi = a * (1 + e) + RHO
i, j = np.triu_indices(N, k=1)
ov = (per_lo[i] <= per_hi[j]) & (per_lo[j] <= per_hi[i])
i, j = i[ov], j[ov]
n_ov = len(i)
sel = np.random.default_rng(1).choice(n_ov, min(n_ov, 8000), replace=False)
ii, jj, scale = i[sel], j[sel], n_ov / len(sel)
print(f"dense: {n_ov} overlapping pairs ({len(ii)} tracked, scale x{scale:.2f})")
vrel = math.sqrt(2) * SIGMA_E
dt = RHO / (2.0 * vrel)
steps = int(HOR / dt)
print(f"dense: dt={dt:.2e}, {steps} steps")
ai, ei, pi_, li_, ni_ = a[ii], e[ii], pom[ii], lam[ii], n[ii]
aj, ej, pj, lj, nj = a[jj], e[jj], pom[jj], lam[jj], n[jj]
best = np.full(len(ii), np.inf)
for s in range(steps):
    t = (s + 0.5) * dt
    x1, y1 = kepler_pos(ai, ei, pi_, li_, ni_, t)
    x2, y2 = kepler_pos(aj, ej, pj, lj, nj, t)
    np.minimum(best, np.hypot(x1 - x2, y1 - y2), out=best)
hits_dense = int(round((best < RHO).sum() * scale))
rate_dense = hits_dense / (N * HOR / (2 * np.pi))
h_new, r_new, _ = encounter_rate(a, e, pom, lam, RHO, HOR)
ana = 3 * math.pi * (N / (math.pi * 1.25)) * RHO * 2 * SIGMA_E
print(f"dense={hits_dense} hits ({rate_dense:.2e}/body/orbit) | "
      f"newton={h_new} ({r_new:.2e}) | epicyclic analytic={ana:.2e}")
R["dense_scan"] = {"rate_dense": rate_dense, "rate_newton": r_new,
                   "hits_dense": hits_dense, "hits_newton": h_new,
                   "analytic_epicyclic": ana, "pairs_tracked": int(len(ii)),
                   "scale": scale}

# ---------- (2) planet SOI transits, planet-vs-belt only ----------------------
MU_P, A_P = 1e-3, 1.25
R_SOI = A_P * (MU_P / 3.0) ** (1 / 3)
a, e, pom, lam = make_belt(10_000, 5.5e-3, 1.0, 1.5, 42)
nb = a ** -1.5
npp = A_P ** -1.5
dn = npp - nb
dl = lam % (2 * np.pi)
hits = 0
K = int(np.ceil(np.abs(dn).max() * HOR / (2 * np.pi))) + 1
for k in range(-1, K + 1):
    with np.errstate(divide="ignore", invalid="ignore"):
        tk = (dl + 2 * np.pi * k) / dn
    good = np.isfinite(tk) & (tk > 0) & (tk <= HOR)
    if not good.any():
        continue
    t = tk[good]
    dng = dn[good]
    for _ in range(3):
        dth = true_long(a[good], e[good], pom[good], lam[good], nb[good], t) - t * npp
        dth = (dth + np.pi) % (2 * np.pi) - np.pi
        t = t - dth / np.where(dng != 0, dng, 1.0)
    t = np.clip(t, 0.0, HOR)
    x, y = kepler_pos(a[good], e[good], pom[good], lam[good], nb[good], t)
    xp, yp = A_P * np.cos(t * npp), A_P * np.sin(t * npp)
    hits += int((np.hypot(x - xp, y - yp) < R_SOI).sum())
rate_soi = hits / (10_000 * 20)
R["soi"] = {"R_SOI": R_SOI, "hits": hits,
            "transits_per_body_per_orbit": rate_soi,
            "saturation_orbits": 1.0 / max(rate_soi, 1e-12)}
print(f"SOI: hits={hits} rate={rate_soi:.2e}/body/orbit "
      f"(1 body in {1/max(rate_soi,1e-12):.0f} orbits)")

# ---------- (3) P2 ------------------------------------------------------------
x = np.linspace(0.2, 6.0, 200000)
theta = 2 * np.arctan(1.0 / x)
dv_ex = 2 * 0.03 / np.sqrt(x * x + 1)
dv_im = 2 * 0.03 / x
R["P2"] = {"small": float(np.median(dv_im[theta < 0.5] / dv_ex[theta < 0.5])),
           "big": float(np.median(dv_im[theta > 2.0] / dv_ex[theta > 2.0]))}
print("P2 small %.3f big %.2f" % (R["P2"]["small"], R["P2"]["big"]))

with open("crosscheck_results.json", "w") as f:
    json.dump(R, f, indent=1)
print("wrote crosscheck_results.json")
