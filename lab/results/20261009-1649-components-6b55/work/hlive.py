#!/usr/bin/env python3
"""H_live for a belt population: bits of live distinguishing information per body
per unit simulated time, from mutual-encounter impulses, against reabsorption.

Model (shearing-sheet, doll units: G*M_star = 1, a = 1, one orbit = one time unit,
v_k = 2*pi per orbit):
  - partners: radial density nu = N/dA (a in [1, 1.5]); conjunctions of a pair with
    radial offset x happen 1.5*|x| times per orbit (Kepler shear dn/da = -3*pi).
  - miss distance at conjunction b = |x + (epi1 - epi2)|; for b << sigma_e the
    conditional density is ~ flat -> p(b) ~ b (sample b = rho*sqrt(u)).
  - impulse (exact 2D hyperbolic, v_rel ~ const at conjunction):
    dv = 2*m/(b*v_rel), v_rel from shear+epicyclic at x ~ sigma_e scale.
  - element changes (Gauss, near-circular): da/a = 2*dv_t/v_k ; de ~ dv_r/v_k.
  - law grid: element quantum Q_e (relative). Each impulse lands as an integer
    step round(change / Q_e); offsets accumulate exactly (r2 lesson).
  - scar: |integer offset| >= 1 in any component. Bits for a scarred body:
    log2(mean |offset|) per live component + Elias-Fano ordinal
    (~2 + log2(N/k), shipmem program.rs).

Controls: (1) calibration vs r8 v2 belt-0 (N=1e4, 20 orbits, 427 encounters);
(2) a heavy belt MUST scar (instrument sensitivity); (3) MC walk sigma vs the
analytic diffusive sigma within 25%.
"""
import json
import sys
import numpy as np

VK = 2.0 * np.pi


def conjunction_rate(nu, sigma_e, rho):
    """Rate per body per orbit of conjunctions with miss < rho."""
    xs = np.linspace(1e-12, 6 * sigma_e, 24001)
    f0 = 2.0 * rho / (np.sqrt(2.0 * np.pi) * sigma_e)  # p(miss<rho | x), flat approx
    integrand = nu * 2.0 * 1.5 * xs * np.minimum(f0, 1.0)
    return float(np.trapz(integrand, xs))


def vrel_at_conjunction(sigma_e):
    shear = 1.5 * sigma_e * VK / np.sqrt(2.0)   # tangential shear, x ~ sigma_e/sqrt2
    epicy = sigma_e * VK / np.sqrt(2.0)         # radial epicyclic relative speed
    return float(np.hypot(shear, epicy))


def run_cohort(n_bodies, T_orbits, Gamma, m, rho, v_rel, Q_e, seed):
    """Per-body flyby streams; returns exact integer offsets at grid Q_e."""
    rng = np.random.default_rng(seed)
    ne = rng.poisson(Gamma * T_orbits, size=n_bodies)
    total = int(ne.sum())
    if total == 0:
        return np.zeros((n_bodies, 2), dtype=np.int64), 0
    b = rho * np.sqrt(rng.random(total))                  # flux-uniform miss
    dv = 2.0 * m / (np.maximum(b, 1e-30) * v_rel)         # v_k units
    theta = rng.random(total) * 2.0 * np.pi
    dvt, dvr = np.abs(dv * np.cos(theta)), np.abs(dv * np.sin(theta))
    da = 2.0 * dvt / VK                                    # relative da/a
    de = dvr / VK
    which = np.repeat(np.arange(n_bodies), ne)
    off_a = np.bincount(which, weights=np.round(da / Q_e).astype(np.int64),
                        minlength=n_bodies)
    off_e = np.bincount(which, weights=np.round(de / Q_e).astype(np.int64),
                        minlength=n_bodies)
    return np.stack([off_a, off_e], axis=1).astype(np.int64), total


def simulate(Gamma, m, rho, v_rel, Q_e, nb, T_target, seed, budget=4_000_000):
    """Largest affordable window; CLT holds for many small steps.
    Cohort shrinks when the rate is huge, so events stay within budget."""
    nb_eff = int(max(50, min(nb, budget / max(Gamma, 1.0))))
    T = min(T_target, max(1e-6, budget / max(Gamma * nb_eff, 1.0)))
    offs, tot = run_cohort(nb_eff, T, Gamma, m, rho, v_rel, Q_e, seed)
    return offs, tot, T


def bits_per_body(offsets, N):
    """Live bits: scarred bodies pay offset payload + Elias-Fano ordinal."""
    scarred = np.any(np.abs(offsets) >= 1, axis=1)
    k = int(scarred.sum())
    n = offsets.shape[0]
    if k == 0:
        return 0.0, 0.0, 0
    mags = np.abs(offsets[scarred])
    payload = float(np.mean(np.sum(np.log2(np.maximum(mags, 1.0)), axis=1)))
    addr = 2.0 + np.log2(max(N / k, 2.0))
    return float(k / n * (payload + addr)), float(k / n), k


def sigma_walk_analytic(Gamma, m, rho, v_rel, T):
    """Diffusive walk scale (relative da/a) after T orbits; log-regularised
    at b_min = min(1 km physical, rho/10)."""
    b_min = min(6.7e-9, rho / 10.0)
    # da = 2*dv_t/v_k with dv = 2m/(b v_rel): <da^2> = (4m/(v_rel VK))^2 *
    # <cos^2> * <1/b^2>,  <1/b^2> = (2/rho^2) ln(rho/b_min) for p(b) ~ b
    ms_per_event = (4.0 * m / (v_rel * VK)) ** 2 * 0.5 * 2.0 / rho**2 * np.log(rho / b_min)
    return float(np.sqrt(Gamma * T * ms_per_event))


def crossing_time(Gamma, m, rho, v_rel, Q):
    s1 = sigma_walk_analytic(Gamma, m, rho, v_rel, 1.0)
    return float((Q / s1) ** 2) if s1 > 0 else float("inf")


def session_bits(Gamma, m, rho, v_rel, Q, N, T):
    """Post-reabsorption live bits/body at T orbits (Gaussian walk; a body
    whose offset is below one quantum reabsorbs into the program)."""
    import math
    s = sigma_walk_analytic(Gamma, m, rho, v_rel, T)
    if s <= 0:
        return 0.0, 0.0, s
    p1 = math.erfc(0.5 * Q / (s * math.sqrt(2.0)))          # 2*(1-Phi(z))
    p1 = min(max(p1, 0.0), 1.0)
    frac = 1.0 - (1.0 - p1) ** 2                             # two components
    payload = max(0.0, np.log2(max(1.5 * s / Q, 1.0)))
    addr = 2.0 + np.log2(max(N / max(frac * N, 2.0), 2.0))
    return float(frac * (2.0 * payload + addr)), float(frac), s


def main():
    out = {"calibration": {}, "controls": {}, "sweep": [], "player_cone": {}, "notes": {}}
    dA = 0.5  # belt width, a in [1, 1.5]

    # --- calibration to r8 v2 belt-0 (427 encounters, N=1e4, 20 orbits) ---
    for name, sig, rho in [("median-draw", 5.5e-3, 5.5e-5),
                           ("low-draw", 2.0e-3, 1.5e-5)]:
        G = conjunction_rate(1e4 / dA, sig, rho)
        out["calibration"][name] = {
            "sigma_e": sig, "rho": rho, "rate_per_body_orbit": G,
            "expected_encounters_20orbits": G * 1e4 * 20, "measured_belt0": 427}

    # main-sweep belt parameters (r8 steady case)
    sig, rho = 1e-2, 1e-4
    v_rel = vrel_at_conjunction(sig)
    out["notes"]["v_rel_at_conjunction"] = v_rel

    # --- controls ---
    # C1 heavy belt must scar
    N = 1e6; Mb = 1e-3; Q = 1e-9
    G = conjunction_rate(N / dA, sig, rho)
    offs, tot, T_used = simulate(G, Mb / N, rho, v_rel, Q, 500, 1e2, 7)
    bpb, frac, k = bits_per_body(offs, N)
    out["controls"]["heavy_must_scar"] = {"bits_per_body": bpb, "scarred_frac": frac,
                                          "orbits_simulated": T_used}
    # C2 MC vs analytic diffusion (tiny Q so offsets are unsaturated)
    Gc = conjunction_rate(1e4 / dA, sig, rho)
    offs2, tot2, T2 = simulate(Gc, 1e-3 / 1e4, rho, v_rel, 1e-15, 4000, 1e3, 11)
    mc = float(np.std(offs2[:, 0].astype(float))) * 1e-15
    an = sigma_walk_analytic(Gc, 1e-3 / 1e4, rho, v_rel, T2)
    out["controls"]["diffusion"] = {"mc_sigma": mc, "analytic_sigma": an,
                                    "ratio": mc / an if an > 0 else None,
                                    "orbits": T2}

    # --- decisive sweep ---
    T_session = 1e4  # orbits; a long session at a=1 AU is 1e4 years
    for N in [1e4, 1e6, 1e9]:
        for Mb in [1e-9, 1e-7, 1e-5, 1e-3]:
            for Q in [1e-9, 1e-7, 1e-5]:
                for regime, r_eff in [("fixed-rho", rho),
                                      ("rho-1/N", rho * 1e4 / N)]:
                    G = conjunction_rate(N / dA, sig, r_eff)
                    offs, tot, T = simulate(G, Mb / N, r_eff, v_rel, Q, 4000,
                                            T_session, 3)
                    bpb, frac, k = bits_per_body(offs, N)
                    an = sigma_walk_analytic(G, Mb / N, r_eff, v_rel, T_session)
                    sb, sfrac, s_sig = session_bits(G, Mb / N, r_eff, v_rel, Q,
                                                    N, T_session)
                    out["sweep"].append({
                        "N": N, "M_belt": Mb, "Q_e": Q, "regime": regime,
                        "rate_per_body_orbit": G,
                        "orbits_simulated": T, "bits_per_body_measured": bpb,
                        "scarred_frac_measured": frac,
                        "analytic_sigma_rel_1e4orbits": an,
                        "session_bits_per_body": sb,
                        "session_scarred_frac": sfrac,
                        "crossing_time_orbits": crossing_time(G, Mb / N, r_eff,
                                                              v_rel, Q),
                        "crossed_in_session": bool(an > Q),
                        "events_simulated": tot})

    # bits at the analytic session scale (Gaussian tail beyond |offset|>=1)
    # reported per row via crossed_in_session + crossing_time_orbits.

    # --- player light-cone bound (real units; c = 1 AU / 499 s) ---
    sigma_2d = 1e9 / (np.pi * (1.5**2 - 1.0**2))
    r_cone = 1.0 / 499.0
    n_touched = sigma_2d * np.pi * r_cone**2
    out["player_cone"] = {
        "bodies_per_AU2": sigma_2d, "light_second_AU": r_cone,
        "bodies_in_cone_per_game_second": float(n_touched),
        "bits_per_game_second_at_32_bits_each": float(n_touched * 32),
        "budget_bits_per_s_for_4GiB_over_1h": 4 * 2**30 / 3600.0}

    path = sys.argv[1] if len(sys.argv) > 1 else "metrics.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"calibration": out["calibration"],
                      "controls": out["controls"],
                      "player_cone": out["player_cone"]}, indent=1))
    for row in out["sweep"]:
        print(f"N={row['N']:.0e} Mb={row['M_belt']:.0e} Q={row['Q_e']:.0e} "
              f"{row['regime']:9s} rate={row['rate_per_body_orbit']:.2e} "
              f"bits/body={row['bits_per_body_measured']:.3e} "
              f"scarred={row['scarred_frac_measured']:.3e} "
              f"tau_cross={row['crossing_time_orbits']:.2e} "
              f"crossed={row['crossed_in_session']}")


if __name__ == "__main__":
    main()
