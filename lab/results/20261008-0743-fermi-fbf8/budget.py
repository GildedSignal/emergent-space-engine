#!/usr/bin/env python3
"""Verification of the N-scaling and the analytic kick model; budget table."""
import json
import numpy as np
import h_live_fermi as H

# 1) N-scaling of R (fixed width 0.5): R per body must scale linearly with N.
scal = {}
for n in (1000, 4000, 8000):
    a = H.anchor(n=n, orbits=40)
    scal[n] = {"R": a["R_per_body_per_orbit"],
               "cand_pairs_per_body": a["cand_pairs_per_body"],
               "conj_per_body_per_orbit": a["conjunctions_per_body_per_orbit"],
               "encounters": a["encounters"]}
r41 = scal[4000]["R"] / scal[1000]["R"]
r84 = scal[8000]["R"] / scal[4000]["R"]

# 2) Analytic kick model validated against the anchor's encounter sample:
#    de = C/d per unit encounter mass (C measured), focused cutoff d0,
#    sigma_de(m) = C*sqrt(2*ln(rho/d0))/rho with p(d) ~ d on [d0, rho].
A = H.anchor(n=4000, orbits=60)
rho = 1e-3
C = A["de_median_per_m"] * A["d_median"]


def sigma_de(m, vrel=0.03, rphys=5e-9):
    d0 = min(max(4.0 * m / vrel ** 2, rphys), rho / 2)  # focus cutoff, clamped
    return m * C * np.sqrt(2.0 * np.log(rho / d0)) / rho

def solve_m(target_sigma):
    lo, hi = 1e-12, 1e-3
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if sigma_de(mid) < target_sigma:
            lo = mid
        else:
            hi = mid
    return float(np.sqrt(lo * hi))


# 3) Budget at N=1e9, M1 constants.
N = 1e9
R = A["R_per_body_per_orbit"]
TORB_S = 3.156e7                                # 1 AU orbit in game-seconds
CAMPAIGN_ORBITS = 100 * 3600 * 100 / TORB_S     # 100 real h at RTF 100
q = 1e-3                                        # element quantum (generous)
GEN_MB = 0.126 * N / 8 / 1e6
scar_MB = N * R * CAMPAIGN_ORBITS * 8 / 1e6     # first-encounter scars only
t_first = 1.0 / R
R_pack = R * (N / 4000.0)                       # same width, 2.5e5x density
enc_s_fixed = R * N / TORB_S
enc_s_pack = R_pack * N / TORB_S
setup_s_st = [128.3 * N * r for r in (2.5e-6, 24e-6)]
ops_orbit = N * 500 * 200                       # pre-pivot: 500 steps x 200 ops
n_k10 = 10.0 * R_pack
sigma10 = q / np.sqrt(n_k10)
m_star_packed = solve_m(sigma10) if n_k10 > 1 else None

out = {
  "scaling": {str(k): v for k, v in scal.items()},
  "R_ratio_4k_1k": r41, "R_ratio_8k_4k": r84,
  "C_measured": C,
  "de_rms_measured_per_m": A["de_rms_per_m"],
  "budget": {
    "N": N,
    "generator_MB": GEN_MB,
    "campaign_orbits_at_RTF100_100h": CAMPAIGN_ORBITS,
    "scars_MB_fixed_density_100h": scar_MB,
    "first_encounter_orbits": t_first,
    "m_one_kick_equals_q": solve_m(q),
    "packed_same_width": {
      "R_per_body_per_orbit": R_pack,
      "orbits_to_all_distinguished": 1.0 / R_pack,
      "scar_MB_at_saturation": N * 8 / 1e6,
      "m_star_t_d_10orbits": m_star_packed,
      "aggregate_MSun_at_m_star": m_star_packed * N if m_star_packed else None},
    "encounters_per_game_s_fixed": enc_s_fixed,
    "encounters_per_game_s_packed": enc_s_pack,
    "setup_s_single_thread": setup_s_st,
    "setup_s_8cores": [x / 8 for x in setup_s_st],
    "cores_pre_pivot_at_rtf1": ops_orbit / TORB_S / 1e10,
    "cores_pre_pivot_at_rtf1e6": ops_orbit * 1e6 / TORB_S / 1e10,
    "rtf_max_m1_pre_pivot": 1e10 / (ops_orbit / TORB_S),
    "H_live_bits_per_game_s_fixed": enc_s_fixed * 64,
  },
}
print(json.dumps(out, indent=1))
with open("budget.json", "w") as f:
    json.dump(out, f, indent=1)
