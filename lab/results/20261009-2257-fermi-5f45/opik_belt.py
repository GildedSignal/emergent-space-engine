# Öpik–Arnold-style conjunction Monte Carlo for a flat shearing belt.
# Units: a=1, GM*=1, n=1, v_k=1. 2D belt (no inclination), r8-v4 regime:
# e Rayleigh(sigma_e), a uniform in [1-w, 1+w], encounter radius rho (fraction of a).
# Per-body encounter rate per orbit = E_neighbor[ 1.5*|da| * 1{miss < rho} ]
# (conjunctions per orbit with a neighbor at da ~ 1.5|da|; miss at conjunction from
# epicyclic phases). Fresh harness; shares no code with crates/encounters or r8.

import numpy as np

rng = np.random.default_rng(20261009)
QUANTUM = 1e-6  # the law's ~1e-6 relative floor (law.md jet discussion)

def belt(N, surface_density, sigma_e):
    """N bodies at fixed surface density (bodies per unit da): width w = N/(2*sd)."""
    w = N / (2 * surface_density)
    a = rng.uniform(1 - w, 1 + w, N)
    e = rng.rayleigh(sigma_e, N)
    return a, e, w

def encounter_stats(N, surface_density, sigma_e, rho, mu, n_samples=5_000_000):
    """Monte Carlo over (body, neighbor) conjunctions. Returns rate per body per
    orbit, kick-fraction distribution for encounters, and bits per outcome."""
    a, e, w = belt(N, surface_density, sigma_e)
    # sample neighbors: two independent bodies' da -> triangular pair separation
    da = rng.triangular(-2 * w, 0, 2 * w, n_samples)
    ei = rng.rayleigh(sigma_e, n_samples)
    ej = rng.rayleigh(sigma_e, n_samples)
    ui = rng.uniform(0, 2 * np.pi, n_samples)
    uj = rng.uniform(0, 2 * np.pi, n_samples)
    # miss distance at conjunction: radial offset of the two epicyclic positions
    miss = np.abs(da + ei * np.cos(ui) - ej * np.cos(uj))
    hit = miss < rho
    # conjunctions per orbit with that neighbor = 1.5|da| (shear, e<<1)
    rate = np.mean(1.5 * np.abs(da) * hit)  # per body per orbit
    # relative speed at conjunction (v_k units), epicyclic + shear
    vrel = np.sqrt((1.5 * da + ei * np.sin(ui) - ej * np.sin(uj)) ** 2
                   + (ei * np.cos(ui) - ej * np.cos(uj)) ** 2)
    vrel = np.maximum(vrel, 1e-12)
    # impulse kick fraction for the encounters that happened (b = miss, with
    # gravitational focusing folded into b_eff = sqrt(b^2 + b90^2), b90 = mu/vrel^2)
    b = miss[hit]
    v = vrel[hit]
    b90 = mu / v**2
    beff = np.sqrt(b**2 + b90**2)
    f = 2 * mu / (beff * v)          # delta-v / v_k
    f = np.minimum(f, 1.0)
    # distinguishable outcome cells: 3 independent impulse components + timing;
    # conservative bits = 3 * log2(spread / quantum) + log2(rho/quantum) timing
    if f.size > 100:
        f_lo, f_hi = np.percentile(f, [2, 98])
        bits = 3 * np.log2(max(f_hi - f_lo, QUANTUM) / QUANTUM) + np.log2(rho / QUANTUM)
    else:
        bits = float("nan")
    return dict(rate=rate, n_hits=int(hit.sum()), f_med=float(np.median(f)) if f.size else float("nan"),
                bits=float(bits), w=w)

def main():
    import json, time
    t0 = time.time()
    out = {"machine_load": open("/proc/loadavg").read().strip()}
    sd = 37_500          # bodies per unit da  (N=1500 in w=0.02, r8-v4-like)
    sigma_e = 1e-2
    mu = 1e-9            # m/M* per belt body -> belt of 1e6 bodies = 1.25e-3 M*
    for rho in (1e-4, 1e-3):
        for N in (1500, 15000):   # 10x N at fixed surface density
            s = encounter_stats(N, sd, sigma_e, rho, mu)
            out[f"rho={rho:g} N={N}"] = {k: (round(v, 6) if isinstance(v, float) else v)
                                          for k, v in s.items() if k != "w"}
            print(f"rho={rho:g} N={N:6d} w={s['w']:.4f} rate/body/orbit={s['rate']:.3e} "
                  f"hits={s['n_hits']} f_med={s['f_med']:.2e} bits/enc={s['bits']:.0f}")
    # H_live stock: rate x bits per body per orbit -> per 3h session at RTF 100
    r = out["rho=0.0001 N=1500"]
    per_orbit_bits = r["rate"] * r["bits"]
    out["bits_per_body_per_orbit"] = per_orbit_bits
    for T_orb_game_s, label in ((3.15e7, "1yr orbit"), (8.64e4, "1day orbit"), (3.6e3, "1hour orbit")):
        session_orbits = 3 * 3600 * 100 / T_orb_game_s     # 3h play at RTF 100
        out[label] = dict(orbits_per_session=session_orbits,
                          bits_per_body_per_session=per_orbit_bits * session_orbits)
        print(f"{label}: {session_orbits:.1e} orbits/session -> "
              f"{per_orbit_bits * session_orbits:.2e} bits/body/session")
    out["seconds"] = round(time.time() - t0, 1)
    import os
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opik_out.json")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
if __name__ == "__main__":
    main()
