#!/usr/bin/env python3
"""Fermi extrapolation: belt two-body relaxation vs the scar quantum.
t_sat = (Q/sigma_s)^2 orbits, sigma_s/v per orbit = 1/sqrt(t_relax) in orbits.
Chandrasekhar: t_relax = v^3 / (G^2 m^2 n lnL); verified scaling 0.1N/lnN."""
import math

G = 6.674e-11
AU = 1.496e11
V = math.pi * 14 * AU ** 2 * 0.1 * AU        # belt 2-4 AU, thickness 0.1 AU
Torb = 5 * 3.15e7                            # ~3 AU orbit
N = 1e9
v = 5e3
lnL = 10

for label, Mtot in [("real belt (3e21 kg)", 3e21),
                    ("gamey heavy belt (1e-3 Msun)", 2e30),
                    ("young dense belt (1e-2 Msun)", 2e31)]:
    n = N / V
    m = Mtot / N
    tr = v ** 3 / (G ** 2 * m ** 2 * n * lnL) / Torb
    sig = tr ** -0.5                          # per-orbit kick rms, units of v
    for Qrel in (1e-6, 1e-9):
        print("%-30s t_relax=%9.2e orbits  sigma_s/v=%8.2e  Q/v=%g -> t_sat=%9.2e orbits"
              % (label, tr, sig, Qrel, Qrel ** 2 * tr))
