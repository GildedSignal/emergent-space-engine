#!/usr/bin/env python3
"""H_live Fermi estimate: which physical term creates live distinctions at 1e9 bodies?

All internal units are the doll's: GM_star = 1, a = 1 (=> v_K = 1, T_orbit = 2*pi).
Physical anchor for the table: a = 3 AU, M_star = 1 M_sun, T_orbit = 1.64e8 s.
"""
import json
import math
import random

import numpy as np

R = {"meta": {"units": "doll: GM=1, a=1, v_K=1, T=2pi; anchor a=3AU M_sun"}}

# ---------------------------------------------------------------- belt sampler
# replicates crates/encounters/src/belt.rs (continuous a branch)


def make_belt(n, sigma_e, a_lo, a_hi, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log(1.0 - rng.random(n))), 0.5)
    pom = rng.uniform(0, 2 * np.pi, n)          # periapsis angle varpi
    lam = rng.uniform(0, 2 * np.pi, n)          # mean longitude at t=0
    return a, e, pom, lam


def kepler_pos(a, e, pom, lam, n, t):
    """Position at time t. M = lam + n t - pom; Newton on E - e sinE = M."""
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(4):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    r = a * (1 - e * np.cos(E))
    c, s = np.cos(E), np.sin(E)
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    nu = np.arctan2(fac * s, c - e)
    th = nu + pom
    return r * np.cos(th), r * np.sin(th)

def true_long(a, e, pom, lam, n, t):
    M = (lam + n * t - pom) % (2 * np.pi)
    E = M.copy()
    for _ in range(3):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    fac = np.sqrt(np.maximum(1.0 - e * e, 1e-18))
    return np.arctan2(fac * np.sin(E), np.cos(E) - e) + pom


def encounter_rate(a, e, pom, lam, rho, horizon, refine_pts=5):
    """r8-v2-reference-lite: pairs whose radial ranges overlap within rho;
    distance at the true-longitude crossing (Newton from the mean-longitude
    crossing: the two differ by ~2(e1+e2)/dn >> rho/v_rel; missing that shift
    biased the first version low by ~30x)."""
    n = a ** -1.5
    N = len(a)
    per_lo = a * (1 - e) - rho
    per_hi = a * (1 + e) + rho
    i, j = np.triu_indices(N, k=1)
    ov = (per_lo[i] <= per_hi[j]) & (per_lo[j] <= per_hi[i])
    i, j = i[ov], j[ov]
    cand_pairs = len(i)
    dn = n[i] - n[j]
    dl = (lam[j] - lam[i]) % (2 * np.pi)
    hits = 0
    # conjunction times t_k = (dl + 2 pi k)/dn, k = 0..K
    K = int(np.ceil(np.abs(dn).max() * horizon / (2 * np.pi))) + 1
    for k in range(-1, K + 1):
        with np.errstate(divide="ignore", invalid="ignore"):
            tk = (dl + 2 * np.pi * k) / dn
        good = np.isfinite(tk) & (tk > 0) & (tk <= horizon)
        if not good.any():
            continue
        ii, jj, tkk, dng = i[good], j[good], tk[good], dn[good]
        # Newton to the true-longitude crossing (slope ~ dn) ...
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
        # ... and the mean-longitude time itself, as a fallback root.
        xm, ym = kepler_pos(a[ii], e[ii], pom[ii], lam[ii], n[ii], tkk)
        xp, yp = kepler_pos(a[jj], e[jj], pom[jj], lam[jj], n[jj], tkk)
        best = np.minimum(best, np.hypot(xm - xp, ym - yp))
        hits += int((best < rho).sum())
    body_orbits = N * horizon / (2 * np.pi)
    return hits, hits / body_orbits, cand_pairs


# ---- P1: r8-v2-style belts, 16 draws, N = 1e4, 20 orbits --------------------
pyrng = random.Random(20261012)
belts = []
for b in range(8):
    sigma_e = 10 ** pyrng.uniform(-3, math.log10(3e-2))
    rho = 10 ** pyrng.uniform(-5, math.log10(3e-4))
    belts.append((sigma_e, rho))
rates, totals, cands = [], [], []
N_BELT, HOR = 5_000, 20 * 2 * math.pi
for idx, (sigma_e, rho) in enumerate(belts):
    a, e, pom, lam = make_belt(N_BELT, sigma_e, 1.0, 1.5, 1000 + idx)
    hits, rate, cp = encounter_rate(a, e, pom, lam, rho, HOR)
    rates.append(rate)
    totals.append(hits)
    cands.append(cp)
    print(f"belt {idx:2d}: sigma_e={sigma_e:.2e} rho={rho:.2e} "
          f"encounters={hits:5d} rate/body/orbit={rate:.2e} cand_pairs={cp}")
med = float(np.median(rates))
R["P1_r8_belts"] = {
    "per_body_orbit_rates": rates, "median": med,
    "totals": totals, "median_total": float(np.median(totals)),
    "analytic_median": float((N_BELT / (math.pi * (1.5**2 - 1.0))) * 2 * 5.5e-5
                             * math.sqrt(2) * 5.5e-3 * 2 * math.pi),
    "r8_v2_anchor_belt0": 427 / (1e4 * 20),
    "cand_pairs_median": float(np.median(cands)),
}
print("P1 median rate %.2e /body/orbit; analytic %.2e; r8 belt0 %.2e"
      % (med, R["P1_r8_belts"]["analytic_median"],
         R["P1_r8_belts"]["r8_v2_anchor_belt0"]))

# ---- P2: impulse vs exact hyperbolic scattering -----------------------------


def p2():
    m = 1.0
    v = np.full(200000, 0.03)                     # typical relative speed
    u = np.random.default_rng(7).random(200000)
    b = np.linspace(0.2, 6.0, 200000) * (m / v**2)  # b in units of b_90 = Gm/v^2
    theta_exact = 2 * np.arctan(m / (b * v**2))
    dv_exact = 2 * v * np.sin(theta_exact / 2)
    dv_imp = 2 * m / (b * v)
    ok = theta_exact < 0.5
    big = theta_exact > 2.0
    return {
        "ratio_median_small": float(np.median(dv_imp[ok] / dv_exact[ok])),
        "ratio_median_big": float(np.median(dv_imp[big] / dv_exact[big])),
    }


R["P2_impulse"] = p2()
print("P2 impulse/exact: small defl %.3f, big defl %.2f"
      % (R["P2_impulse"]["ratio_median_small"],
         R["P2_impulse"]["ratio_median_big"]))

# ---- P3: SOI transits of a planet embedded in the belt ----------------------
MU_P = 1e-3
A_P = 1.25
R_SOI = A_P * (MU_P / 3.0) ** (1.0 / 3.0)
a, e, pom, lam = make_belt(10_000, 5.5e-3, 1.0, 1.5, 42)
ap = np.array([A_P]); ep = np.array([0.0])
pomp = np.array([0.0]); lamp = np.array([0.0])
# pairs: planet vs every body (treat planet as body 0)
full_a = np.concatenate([ap, a]); full_e = np.concatenate([ep, e])
full_pom = np.concatenate([pomp, pom]); full_lam = np.concatenate([lamp, lam])
hits, rate, _ = encounter_rate(full_a, full_e, full_pom, full_lam, R_SOI, HOR)
# deflection at the SOI edge (v_inf ~ shear + e)
v_inf = 0.5 * abs(1.25 - 1.1)  # conservative shear-only estimate ~ 0.075
dv_soi_edge = 2 * MU_P / (R_SOI * v_inf)
R["P3_soi"] = {
    "R_SOI": R_SOI, "transits_per_body_per_orbit": rate,
    "overlap_fraction": float(np.mean(
        (a * (1 - e) - R_SOI <= A_P) & (A_P <= a * (1 + e) + R_SOI))),
    "dv_at_soi_edge": dv_soi_edge,
    "singleton_saturation_orbits": 1.0 / max(rate, 1e-12),
}
print("P3 SOI transits %.2e /body/orbit; overlap frac %.2f; "
      "delta-v at SOI edge %.2f v_K; saturation ~%.0f orbits"
      % (rate, R["P3_soi"]["overlap_fraction"], dv_soi_edge,
         R["P3_soi"]["singleton_saturation_orbits"]))

# ---- P4: mutual-encounter diffusion vs quantum ------------------------------
# 2D thin belt: d<dv^2>/dt = 8 G^2 m^2 Sigma lnL / v_rel, doll units (G M=1).
SIGMA0 = 1e4 / (math.pi * (1.5**2 - 1.0))     # 2546 bodies per area


def crossing_time(mu, sigma_bodies, q_v, v_rel=math.sqrt(2) * 5.5e-3,
                  lnL=math.log(1e5 / 1e-9)):
    D = 8 * mu**2 * sigma_bodies * lnL / v_rel
    return q_v**2 / D                          # per in-plane dim ~ q^2/(2D)


T_ORBIT_S = 1.64e8  # a=3AU, M_sun
M_SUN = 1.989e30
table = []
for name, kg in [("ship 1e6 kg", 1e6), ("asteroid 1e13 kg", 1e13),
                 ("dwarf 1e18 kg", 1e18)]:
    mu = kg / M_SUN
    row = {"body": name, "mu": mu}
    for label, sig in [("N=1e4 (r8)", SIGMA0),
                       ("N=1e9 fixed annulus", SIGMA0 * 1e5)]:
        t = crossing_time(mu, sig, 1e-5)
        row[label + " t_cross(q=1e-5) [orbits]"] = t
        row[label + " t_cross [years]"] = t * T_ORBIT_S / 3.15e7
    table.append(row)
    print("P4 %-18s mu=%.1e  t_cross(N=1e9, q=1e-5): %.1e orbits = %.1e yr"
          % (name, mu, row["N=1e9 fixed annulus t_cross(q=1e-5) [orbits]"],
             row["N=1e9 fixed annulus t_cross [years]"]))
mu_crit = 1e-5 * 5.5e-5 * 5.5e-3 / 2
R["P4_diffusion"] = {"rows": table, "mu_crit_e encounter": mu_crit,
                     "m_crit_kg": mu_crit * M_SUN}
print("   critical mass for per-encounter scarring: %.1e kg" % (mu_crit * M_SUN))

# ---- P5 + the 1e9 table ------------------------------------------------------
# contact rate (physical radius 10 m) at N=1e9 fixed annulus; doll length = 3AU
AU = 4.49e11
rho_phys = 10.0 / (3 * AU)
v_rel = math.sqrt(2) * 5.5e-3
sig9 = SIGMA0 * 1e5
cont_rate_body_orbit = sig9 * 2 * rho_phys * v_rel * 2 * math.pi
cont_total_per_s = cont_rate_body_orbit * 1e9 / T_ORBIT_S
rebind_per_s = R["P3_soi"]["transits_per_body_per_orbit"] * 1e9 / T_ORBIT_S
R["P5_scale_table"] = {
    "contact_rate_per_body_per_orbit_N9": cont_rate_body_orbit,
    "contacts_per_game_second": cont_total_per_s,
    "rebinds_per_game_second": rebind_per_s,
    "H_live_rebind_bits_per_s": rebind_per_s * 128,   # 16 B tube
    "H_live_contact_bits_per_s": cont_total_per_s * 256,
    "birth_program_bytes_at_1e9": 0.126 / 8 * 1e9,
    "singleton_bytes_at_1e9": 16 * 1e9,
    "session_1h_bytes_from_rebinds": rebind_per_s * 3600 * 16,
    "singleton_saturation_orbits": R["P3_soi"]["singleton_saturation_orbits"],
    "saturation_years": (R["P3_soi"]["singleton_saturation_orbits"]
                         * T_ORBIT_S / 3.15e7),
}
for k, v in R["P5_scale_table"].items():
    print("table %-38s %.3e" % (k, v))

with open("h_live_results.json", "w") as f:
    json.dump(R, f, indent=1)
print("\nwrote h_live_results.json")
