#!/usr/bin/env python3
"""Game-scale extrapolation of the scar layer (H_live) from measured belt constants.

Inputs (measured by scarwalk, run3.csv headers):
  physical belt mu=1e-4: encounter rate 319.62/orbit/body,
  rms/encounter da=3.130e-7 (a-units), combined de=3.372e-7 (per component 2.386e-7).
  per-orbit rms: da = 5.596e-6 (rate-weighted), de_per_component = 6.028e-6/sqrt(2).
Store model, calibrated on the shipped codec (within ~1-2 bits/column, G2/G3):
  bits/column = log2(sigma/quantum) + 2.05, plus ~2 bits/body Elias-Fano.
Grids (the law's model quanta): q_a = q_e = 2^-24 of a; q_phi = TAU/2^32.
"""
import math

RATE = 319.62
DA_ORB = 5.596e-6            # rms da accumulated per orbit (a-units)
DE_ORB = 6.028e-6 / math.sqrt(2)  # per e-component
QA = QE = 2.0**-24
QPHI = math.tau / 2.0**32
P_YR_S = 3.156e7             # 1 AU orbit in seconds


N_REF = 1_048_576  # the MC belt's body count; at fixed belt mass, Var/orbit ~ mu^2/N


def scar_bytes(n_orbits, mu_scale=1.0, n_bodies=N_REF):
    nscale = mu_scale * math.sqrt(N_REF / n_bodies)  # Var/orbit ~ mu^2/N
    sa = DA_ORB * math.sqrt(n_orbits) * nscale
    se = DE_ORB * math.sqrt(n_orbits) * nscale
    # phase: Var = (1.5*TAU)^2 * sigma_orbit^2 * sum_i i  (walk integrated per orbit)
    varphi = (1.5 * math.tau * DA_ORB * nscale) ** 2 * n_orbits * (n_orbits + 1) / 2
    sphi = math.sqrt(varphi)
    # below one quantum the scar layer is empty (most bodies round onto the program)
    col = lambda sig, q: max(0.0, math.log2(sig / q) + 2.05)
    bits = col(sa, QA) + 2 * col(se, QE) + col(sphi, QPHI)
    bits += 2  # EF ordinals
    return bits / 8, sa, sphi


print("play[h] @RTF100 | orbits | sig_da[a]  | sig_phi[rad] | bytes/body | 1e9 bodies")
for h in [1, 10, 100, 1000, 10000]:
    n = h * 3600 * 100 / P_YR_S
    b, sa, sphi = scar_bytes(n)
    print(f"{h:>10} | {n:8.1f} | {sa:.3e} | {sphi:.3e}  | {b:8.2f}    | {b:.1f} GB")

print("\nmu and N sensitivity (bytes/body at 10 h play, 1 AU):")
for mu, nb in [(1e-2, 2**20), (1e-4, 2**20), (1e-6, 2**20), (1e-4, 10**9), (1e-9, 10**9)]:
    b, _, _ = scar_bytes(10 * 3600 * 100 / P_YR_S, mu / 1e-4, nb)
    print(f"  belt mu={mu:.0e}, N={nb:.1e}: {b:5.2f} B/body -> {b:.1f} GB at 1e9"
          f"{'  (real main-belt mu)' if mu == 1e-9 else ''}")

# crossing times for the 8 GB line (8 B/body) and the full 16 B tube, mu=1e-4
for target, label in [(8, "8 GB line (8 B/body)"), (16, "full tube (16 B/body)")]:
    lo, hi = 1e-3, 1e9  # hours
    for _ in range(200):
        mid = (lo * hi) ** 0.5
        b, _, _ = scar_bytes(mid * 3600 * 100 / P_YR_S)
        if b < target:
            lo = mid
        else:
            hi = mid
    print(f"\ncrosses {label} at {mid:.4g} h of 100x play (mu=1e-4)")

# measured growth law cross-check (G2, last three doublings)
b = [14.1673, 14.4610, 14.9245, 15.2220]
per_doubling = (b[3] - b[0]) / 3 * 8
print(f"\nG2 measured slope (last 3 doublings): {per_doubling:.2f} bits/doubling"
      f" (theory 3.0 = 3x0.5 actions + 1.5 phase)")
g4 = [17.6676, 18.3088, 18.9363, 19.5737]
print(f"G4 cauchy slope: {(g4[3]-g4[0])/3*8:.2f} bits/doubling (theory 4.0 + exception patches)")
