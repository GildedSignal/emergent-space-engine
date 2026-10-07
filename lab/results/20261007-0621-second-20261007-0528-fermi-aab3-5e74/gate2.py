#!/usr/bin/env python3
"""Final gate accounting on top of enc3.py's measurements.

Loads the measured kick law (enc3-out.json) and re-derives the rate curve to b = 0.5
(belt-wide saturation), then computes:
  A. b_bits / b_strong per perturber mass, with saturation handled explicitly
     (a level never crossed inside the belt = every conjunction qualifies).
  B. creation bits/s and tube materialization per TOTAL perturber mass M_pert
     (M_sun units, per 1e9-rock belt at belt-0 local density) — the f_emb x mu
     degeneracy removed: per-rock rate = R(b_bits) * f_emb, f_emb = M_pert/(mu*N_rock).
  C. the worst case over the perturber mass split at fixed M_pert (max over mu of
     R(b_bits(mu))/mu), using the shear law b_bits = sqrt(4 mu / (3 q)) above the
     epicyclic transition mu* = 3 q (e a)^2 / 4 (validated: measured slope -2.0,
     normalization 1.7x) and the epicyclic impulse b_bits = 2 mu / (q v_ep) below it
     (v_ep = 0.0175, the checker's conjunction median, valid in that regime).
"""
import json
import numpy as np

RNG = np.random.default_rng(4242)
MSUN = 1.989e30
YR_S = 3.156e7
Q = 1e-6
E_A = 0.01 * 1.25          # epicyclic radial scale (sigma_e * a)
MU_STAR = 3 * Q * E_A**2 / 4          # transition perturber mass, M_sun
V_EP = 0.0175              # median conjunction relative speed (author's own sample)

def rate_curve_wide():
    n = 3_000_000
    a1 = RNG.uniform(1, 1.5, n); a2 = RNG.uniform(1, 1.5, n)
    e1 = np.minimum(0.01 * np.sqrt(-2 * np.log(1 - RNG.random(n))), 0.5)
    e2 = np.minimum(0.01 * np.sqrt(-2 * np.log(1 - RNG.random(n))), 0.5)
    w1 = RNG.uniform(0, 2 * np.pi, n); w2 = RNG.uniform(0, 2 * np.pi, n)
    th = RNG.uniform(0, 2 * np.pi, n)
    p1 = a1 * (1 - e1**2); p2 = a2 * (1 - e2**2)
    f1 = th - w1; f2 = th - w2
    c1 = 1 + e1 * np.cos(f1); c2 = 1 + e2 * np.cos(f2)
    dvr = e1 * np.sin(f1) / np.sqrt(p1) - e2 * np.sin(f2) / np.sqrt(p2)
    dvt = c1 / np.sqrt(p1) - c2 / np.sqrt(p2)
    v = np.hypot(dvr, dvt)
    bmin = np.abs(p1 / c1 - p2 / c2) * np.abs(dvt) / np.maximum(v, 1e-30)
    dn = np.abs(a1**-1.5 - a2**-1.5)
    grid = np.logspace(-6, np.log10(0.5), 27)
    rate = [float(np.mean(dn * (bmin < g)) * 10_000) for g in grid]
    return grid, np.array(rate)

def main():
    meas = json.load(open("enc3-out.json"))
    grid, rate = rate_curve_wide()
    R1e6 = rate[int(np.argmin(np.abs(grid - 1e-6)))]
    def R(b):
        if b < 1e-6:               # measured exact R ~ b below the grid (epicyclic regime)
            return float(R1e6 * b / 1e-6)
        return float(10 ** np.interp(np.log10(min(b, 0.5)), np.log10(grid), np.log10(rate)))
    T_orb = 2 * np.pi * 1.25**1.5 / (2 * np.pi) * YR_S

    # A: crossings per mass, from the measured medians
    out = {"rate_grid_b": grid.tolist(), "rate_per_body_per_orbit": rate.tolist(),
           "T_orb_s": T_orb, "mu_star_Msun": MU_STAR, "mu_star_kg": MU_STAR * MSUN}
    kl = meas["kick_law"]
    rows = {}
    b_strong_24 = None
    for name in ["1e22", "1e24", "1e26"]:
        rl = kl[name]
        bs = np.array([r["b"] for r in rl]); dv = np.array([r["dv_v"] for r in rl])
        def cross(level):
            for i in range(len(dv) - 1):
                if dv[i] >= level > dv[i + 1]:
                    t = np.log(level / dv[i]) / np.log(dv[i + 1] / dv[i])
                    return float(np.exp(np.log(bs[i]) + t * (np.log(bs[i + 1]) - np.log(bs[i]))))
            if dv[-1] >= level:
                return "BELT-WIDE"      # never crossed: every conjunction qualifies
            return None
        b_bits, b_strong = cross(Q), cross(1e-3)
        mu = float(name) / MSUN
        r_H = (mu / 3)**(1/3) * 1.25
        if name == "1e24" and isinstance(b_strong, float):
            b_strong_24 = b_strong
        rows[name] = dict(mu=mu, r_H_AU=r_H, b_bits=b_bits, b_strong=b_strong,
                          R_bits=R(b_bits) if isinstance(b_bits, float) else R(0.5),
                          R_strong=None)
    # b_strong for 1e22: shear-scale the measured 1e24 crossing (dv ~ mu/b^2 => b ~ sqrt(mu))
    b_strong_22 = b_strong_24 * np.sqrt(1e22 / 1e24)
    rows["1e22"]["b_strong"] = float(b_strong_22)
    rows["1e22"]["b_strong_method"] = "shear-scaled from measured 1e24 crossing"
    for name in rows:
        rb = rows[name]["R_strong"] = R(rows[name]["b_strong"]) if isinstance(rows[name]["b_strong"], float) else R(0.5)

    # B: per total perturber mass. C = R(b_bits) * M_pert/mu * bits / T_orb (N cancels)
    BITS = 2.0
    mpert_pts = [("belt_all_rocks_5e-10", 5e-10), ("stated_1e25kg", 5e-6),
                 ("heavy_1e-4Msun", 1e-4), ("max_disk_1e-3", 1e-3), ("absurd_1e-2", 1e-2)]
    tab = {}
    for mpn, mp in mpert_pts:
        tab[mpn] = {}
        for name, v in rows.items():
            cre = v["R_bits"] / v["mu"] * mp * BITS / T_orb
            tub = v["R_strong"] / v["mu"] * mp / T_orb
            tab[mpn][name] = {"creation_bits_s": cre, "tubes_s": tub,
                              "fill_game_years": 0.375e9 / max(tub, 1e-30) / YR_S}
    out["per_mass"] = rows
    out["vs_Mpert"] = tab
    out["floor_tubes_per_s"] = 0.375e9 / 3.6e7   # 6 GB share over 3.6e7 game-s

    # C: worst case over the mass split at fixed M_pert, with f_emb <= 1 (mu >= M_pert/N_rock)
    N_ROCK = 1e9
    mus = np.logspace(np.log10(1e12 / MSUN), np.log10(1e27 / MSUN), 400)
    b_bits_mu = np.where(mus > MU_STAR, np.sqrt(4 * mus / (3 * Q)), 2 * mus / (Q * V_EP))
    b_strong_mu = np.where(mus > MU_STAR, np.sqrt(4 * mus / 3e-3), 2 * mus / (1e-3 * V_EP))
    eff_bits = np.array([R(b) for b in b_bits_mu]) / mus
    eff_strong = np.array([R(b) for b in b_strong_mu]) / mus
    wc = {}
    for mpn, mp in mpert_pts:
        ok = mus >= mp / N_ROCK                 # f_emb <= 1
        i = int(np.argmax(eff_bits * ok))
        j = int(np.argmax(eff_strong * ok))
        cre = eff_bits[i] * BITS / T_orb * mp
        tub = eff_strong[j] / T_orb * mp
        wc[mpn] = {
            "mu_opt_bits_kg": float(mus[i] * MSUN), "creation_bits_s": cre,
            "mu_opt_strong_kg": float(mus[j] * MSUN), "tubes_s": tub,
            "tube_fill_game_years": 0.375e9 / max(tub, 1e-30) / YR_S,
        }
    out["worst_case"] = wc
    json.dump(out, open("gate2-out.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ["floor_tubes_per_s", "worst_case"]}, indent=1, default=str))

if __name__ == "__main__":
    main()
