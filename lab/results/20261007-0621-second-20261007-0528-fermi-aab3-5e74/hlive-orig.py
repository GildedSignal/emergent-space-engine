#!/usr/bin/env python3
"""H_live Fermi anchor: belt-0 conjunction geometry -> encounter rate and impulse bits.

Game units: G = M_star = 1, time in radians (a=1 orbit = 2*pi).
Belt 0 geometry from crates/encounters/src/belt.rs: a ~ U[1, 1.5], e ~ Rayleigh(sigma_e)
capped at 0.5, random omega, coplanar.

Method (exact 2-body, no integration): a conjunction happens when the two bodies share a
polar angle theta. At conjunction the separation is purely radial; relative motion over the
pass is straight-line to first order in (pass duration / orbit), so the closest approach is
b_min = |b x v| / |v| with the exact Kepler velocities evaluated at theta.

Outputs:
  A. crossing fraction of all pairs -> candidate-pair count vs r8's 1.7M on belt 0 (N=1e4)
  B. encounters vs threshold rho (belt 0, 20 orbits) vs r8's 427  -> infer r8's rho
  C. per-body per-orbit encounter rate at N=1e9 in the SAME annulus (optical depth check)
  D. impulse bits per encounter for ship/rock/embryo masses at the r8 threshold and at
     physical-contact scale; individualization clock (orbits to 1 rad phase drift)
  E. the 8 GB gate table: f_ind (fraction needing a 16-byte tube) vs memory
"""
import json
import numpy as np

RNG = np.random.default_rng(20261007)
AU_STAR_MASS = 1.989e30  # kg, solar

def draw_belt(n, sigma_e, a_lo=1.0, a_hi=1.5):
    a = RNG.uniform(a_lo, a_hi, n)
    e = np.minimum(sigma_e * np.sqrt(-2.0 * np.log1p(-RNG.random(n))), 0.5)
    w = RNG.uniform(0, 2 * np.pi, n)
    return a, e, w

def conj_sample(a1, e1, w1, a2, e2, w2):
    """One random conjunction per pair: returns b_min and relative speed at conjunction."""
    th = RNG.uniform(0, 2 * np.pi, a1.size)
    p1 = a1 * (1 - e1**2); p2 = a2 * (1 - e2**2)
    f1 = th - w1; f2 = th - w2
    c1 = 1 + e1 * np.cos(f1); c2 = 1 + e2 * np.cos(f2)
    r1 = p1 / c1; r2 = p2 / c2
    b_r = np.abs(r1 - r2)                       # separation at conjunction (radial)
    h1 = np.sqrt(p1); h2 = np.sqrt(p2)          # specific ang. momentum (G M = 1)
    vr1 = e1 * np.sin(f1) / h1; vr2 = e2 * np.sin(f2) / h2
    vt1 = c1 / h1;            vt2 = c2 / h2
    dvr = vr1 - vr2; dvt = vt1 - vt2            # rel. velocity (radial, tangential)
    v = np.hypot(dvr, dvt)
    bmin = b_r * np.abs(dvt) / np.maximum(v, 1e-30)
    return bmin, v, np.abs(a1 - a2)

def crossing_pairs(sigma_e, rho_max, n_pairs, chunk=400_000):
    """Draw pairs from the belt, keep orbit-crossing ones; also mean synodic rate."""
    kept = {"bmin": [], "v": [], "dn": [], "cross": 0, "tot": 0}
    for _ in range(max(1, n_pairs // chunk)):
        a1, e1, w1 = draw_belt(chunk, sigma_e)
        a2, e2, w2 = draw_belt(chunk, sigma_e)
        cross = np.abs(a1 - a2) < 0.5 * (a1 * (1 + e1) - a1 * (1 - e1) + a2 * (1 + e2) - a2 * (1 - e2)) + rho_max
        kept["cross"] += int(cross.sum()); kept["tot"] += chunk
        if cross.any():
            b, v, _ = conj_sample(a1[cross], e1[cross], w1[cross], a2[cross], e2[cross], w2[cross])
            kept["bmin"].append(b); kept["v"].append(v)
            n1 = a1[cross] ** -1.5; n2 = a2[cross] ** -1.5
            kept["dn"].append(np.abs(n1 - n2))
    return (np.concatenate(kept["bmin"]), np.concatenate(kept["v"]),
            np.concatenate(kept["dn"]), kept["cross"] / kept["tot"])

def main():
    sigma_e = 0.01
    rho_max = 1e-3
    N0 = 10_000                # belt-0 scale (r8 v2: 1.7M candidate pairs, 427 enc / 20 orbits)
    T20 = 20 * 2 * np.pi       # 20 orbits of a=1
    out = {}

    bmin, vrel, dn, xfrac = crossing_pairs(sigma_e, rho_max, 2_000_000)
    n_cross_pairs = xfrac * N0 * (N0 - 1) / 2
    out["crossing_fraction"] = xfrac
    out["candidate_pairs_N1e4"] = n_cross_pairs
    rhos = np.array([1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2])
    # B: encounters in 20 orbits vs rho (belt-wide): sum over crossing pairs of dn * T * P(bmin<rho)
    # encounters over time T: each pair: (dn/2pi) conjunctions per unit time -> x T
    enc20 = [float((dn * (bmin < r)).mean() * n_cross_pairs * T20 / (2 * np.pi)) for r in rhos]
    enc = np.array(enc20)
    out["rho_grid"] = rhos.tolist()
    out["encounters_20orbits_N1e4"] = enc20

    # per-body per-orbit rate at N in the same annulus (rate ~ n ~ N at fixed volume)
    per_body_orbit_1e4 = [e / (20 * N0) for e in enc20]
    out["per_body_per_orbit_N1e4"] = per_body_orbit_1e4
    out["per_body_per_orbit_N1e9_sameannulus"] = [p * (1e9 / N0) for p in per_body_orbit_1e4]

    # D: impulse bits. delta v/v = 2 mu a / b (tangential impulse, GM=1, v_K^2 = 1/a)
    rho_star = float(rhos[int(np.argmin(np.abs(enc - 427)))])
    masses_kg = {"ship_1e6": 1e6, "rock_1e12": 1e12, "rock_1e15": 1e15, "embryo_1e22": 1e22}
    bits_tbl = {}
    for name, m in masses_kg.items():
        mu = m / AU_STAR_MASS
        for b_au, tag in [(rho_star, "r8rho"), (1e-4, "1e-4AU"), (1e-7, "15km")]:
            dv_v = 2 * mu * 1.0 / b_au           # a=1 AU
            q = 1e-6                              # program quantum (relative)
            bits = min(128.0, max(0.0, np.log2(max(dv_v / q, 1.0))))  # ~1 significant element
            bits_tbl[f"{name}@{tag}"] = {"dv_over_v": dv_v, "bits_q1e-6": bits}
    out["impulse"] = {"rho_matching_427": rho_star, "table": bits_tbl}

    # individualization clock: delta n/n = 1.5 delta a/a ~ 1.5 dv_v/v; orbits to 1 rad
    clocks = {}
    for k, d in bits_tbl.items():
        dn_n = 1.5 * d["dv_over_v"]
        clocks[k] = 1.0 / max(dn_n, 1e-300) if dn_n > 0 else np.inf   # orbits per rad of phase drift
    out["orbits_per_rad_drift"] = clocks

    # E: the 8 GB gate
    tube_bytes = 16
    for f in [0.01, 0.05, 0.1, 0.3, 0.375]:
        out[f"mem_f{f}"] = f * 1e9 * tube_bytes / 1e9  # GB

    # F: joint fit to r8 v2 belt 0 (1.7M candidate pairs, 427 encounters / 20 orbits):
    # find (N, rho) consistent with both, given measured crossing fraction and enc(N=1e4, rho).
    enc_n1e4 = np.array(enc20)
    fit = None
    for r_i, r in enumerate(rhos):
        for N in range(3000, 12000, 50):
            cand = xfrac * N * (N - 1) / 2
            e = enc_n1e4[r_i] * (N / N0) ** 2
            if abs(cand - 1.7e6) / 1.7e6 < 0.35 and abs(e - 427) / 427 < 0.35:
                fit = {"N": N, "rho": float(r), "candidates": cand, "enc20": e}
                break
        if fit:
            break
    out["r8_joint_fit"] = fit

    # G: creation rate and materialization at 1e9, population SPREAD (per-doll density fixed):
    # per-body per-orbit encounter rate at each rho, then game seconds (a=1 <-> 1 yr).
    yr_s = 3.156e7
    pbo = np.array(per_body_orbit_1e4)          # per body per orbit, belt-0 density
    mu_emb = 1e22 / AU_STAR_MASS
    # bit-crossing threshold for embryo kicks: dv/v = 2 mu / b > q  ->  b < 2 mu / q
    q = 1e-6
    b_bits = 2 * mu_emb / q                     # AU (a=1 AU); ~1e-2 AU
    # strong-scatter (materializing) threshold: dv/v > 1e-3
    b_strong = 2 * mu_emb / 1e-3                 # AU
    def rate_at(b):
        return float(10 ** np.interp(np.log10(b), np.log10(rhos), np.log10(pbo)))
    r_bits = rate_at(b_bits)                    # per rock per orbit, >=1-bit embryo kicks
    r_strong = rate_at(b_strong)
    bits_per_cross = 3.0                        # ~log2(delta/q) averaged over 1/b kick sizes
    out["creation_1e9_spread"] = {
        "b_bits_AU": b_bits, "b_strong_AU": b_strong,
        "rock_embryo_bitkicks_per_orbit": r_bits,
        "creation_bits_per_game_s": 1e9 * r_bits / yr_s * bits_per_cross,
        "materialize_per_game_s": 1e9 * r_strong / yr_s,
        "materialized_after_1e5_game_s_GB": 1e9 * r_strong / yr_s * 1e5 * tube_bytes / 1e9,
        "encounters_per_game_s_at_rho1e-5": 1e9 * rate_at(1e-5) / yr_s,
    }
    # creation-rate terms, bits/s game-time, at N=1e9 spread (per-doll density fixed)
    out["gate"] = {
        "f_ind_max_at_6GB": 6e9 / (1e9 * tube_bytes),
        "fleet_1e6_fully_individual_GB": 1e6 * tube_bytes / 1e9,
    }
    print(json.dumps(out, indent=1, default=float))

if __name__ == "__main__":
    main()
