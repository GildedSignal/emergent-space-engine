#!/usr/bin/env python3
"""Independent check of one E1 missed encounter (own Kepler solver; no crate code).
Pair dumped by `inversion audit`: rank 8, equal exact periods, encounters repeating
every orbit. Elements are truncated to 4-6 digits in the dump, so expect ~% agreement."""
import numpy as np
TAU = 2 * np.pi
a_i, e_i, pom_i, lam_i0 = 1.0, 1.078e-2, 3.262995, 0.917410
a_j, e_j, pom_j, lam_j0 = 1.0, 1.836e-2, 5.298488, 0.866732
n = 1.0  # a = 1


def state(a, e, pom, lam0, t):
    M = (lam0 - pom + n * t) % TAU
    E = M.copy()
    for _ in range(80):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    x, y = a * (np.cos(E) - e), a * np.sqrt(1 - e * e) * np.sin(E)
    cp, sp = np.cos(pom), np.sin(pom)
    return x * cp - y * sp, x * sp + y * cp


t = np.linspace(0, 20 * TAU, 4_000_001)
xi, yi = state(a_i, e_i, pom_i, lam_i0, t)
xj, yj = state(a_j, e_j, pom_j, lam_j0, t)
d = np.hypot(xi - xj, yi - yj)
k = int(np.argmin(d))
print(f"min distance over 20 orbits: {d[k]:.4e} at t={t[k]:.6f}")
print(f"Rust truth claimed:          1.779e-4 at t=0.087888 + k*TAU")
print(f"periodicity: min repeats at t+k*TAU with equal depth:",
      f"{d[int(np.argmin(np.abs(t - (t[k] % TAU))))]:.4e} (first period)")
print(f"mean-longitude gap at t0: {(lam_i0 - lam_j0) % TAU:.6f} rad "
      f"= {((lam_i0 - lam_j0) % TAU) / (TAU / 300):.2f} spacings of the 300-ring")
print(f"below rho=1e-3 for {np.mean(d < 1e-3) * 100:.2f}% of the horizon "
      f"({int(np.sum(d < 1e-3))} samples): a permanent far-rank partner, order frozen")
