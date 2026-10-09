#!/usr/bin/env python3
"""Mechanism check: in the gold's own control fleet (seed 27, sigma_lam=0.01),
the mean-longitude gap of an encountering pair equals the difference of their
equations of center (theta - lambda), which is O(e) and unrelated to rho."""
import numpy as np
from invert_train import TAU, RHO, fleet, states, mean_longs, kepler_E

a, e, pom, lam = fleet(200, 1e-5, 0.01, 27)
dt, T = 2e-3, 2 * TAU
best = {}
for s in range(int(T / dt)):
    t = s * dt
    x, y, _, _, th, _ = states(a, e, pom, lam, t)
    o = np.argsort(th)
    ths = th[o]
    gaps = np.append(np.diff(ths), ths[0] + TAU - ths[-1])
    for p in np.where(gaps < 3 * RHO * 1.05)[0]:
        u, v = int(o[p]), int(o[(p + 1) % 200])
        dd = float(np.hypot(x[u] - x[v], y[u] - y[v]))
        if dd < RHO:
            key = (min(u, v), max(u, v))
            if key not in best or dd < best[key][0]:
                best[key] = (dd, t)

rows = []
for (i, j), (d, t) in best.items():
    x, y, _, _, th, _ = states(a, e, pom, lam, t)
    lamt = mean_longs(a, lam, t)
    dlam = abs((lamt[i] - lamt[j] + np.pi) % TAU - np.pi)
    eqc_i = (th[i] - lamt[i] + np.pi) % TAU - np.pi
    eqc_j = (th[j] - lamt[j] + np.pi) % TAU - np.pi
    rows.append((dlam / RHO, abs(eqc_i - eqc_j - 0.0) / RHO if False else abs((eqc_i - eqc_j + np.pi) % TAU - np.pi) / RHO,
                 d, e[i], e[j]))
rows.sort(reverse=True)
print(f"encounters: {len(rows)}")
print("dlam/rho   |eqc_i-eqc_j|/rho   e_i      e_j      d_min/rho")
for r in rows[:8]:
    print(f"{r[0]:8.1f}   {r[1]:8.1f}          {r[3]:.4f}   {r[4]:.4f}   {r[2]/RHO:6.2f}")
med = np.median([r[0] for r in rows])
print(f"median dlam/rho = {med:.1f}; rho = {RHO}; Rayleigh e sigma = 1e-3 (max 1e-2)")
