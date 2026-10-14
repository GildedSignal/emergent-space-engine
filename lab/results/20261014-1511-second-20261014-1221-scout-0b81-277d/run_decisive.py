#!/usr/bin/env python3
"""Decisive: the quantum gate's yield on the author's three Dohnanyi spectra,
with Kepler-true conjunction misses (exact event search), plus the free
post-processing variants (Q52, real-belt mass x52, the two mass controls)."""
import numpy as np
import gate2 as G

NPAIRS = 12_000
out = []
P = out.append

n = 200_000
a = G.rng.uniform(0.95, 1.05, n)
e = G.rng.rayleigh(0.05, n).clip(max=0.35)
w = G.rng_phase.uniform(0, 2 * np.pi, n)
M0 = G.rng_phase.uniform(0, 2 * np.pi, n)
P(f"belt: n={n} bodies, a~U[0.95,1.05], e~Rayleigh(0.05) clip 0.35, phases random")

scenarios = [
    (70.0, 4.7e5, "real-belt-like (Ceres top)"),
    (70.0, 3.0e5, "300-km top"),
    (50.0, 3.0e5, "50-m floor, 300-km top"),
]
results = {}
for (dmin_, dmax_, tag) in scenarios:
    D = G.dohnyani(n, dmin_, dmax_)
    m = G.mass_of_D(D)
    belt_mass = m.mean() * 1e9
    i, j = G.candidate_pairs(a, e, NPAIRS)
    wmin, dmin, vmin, K = G.exact_gate(a, e, w, M0, i, j, nproc=6)
    results[(dmin_, dmax_)] = (i, j, wmin, dmin, vmin, K, m, D)
    del_, dEi, dEj = G.deleted_from(wmin, m, i, j, a)
    surv = 1 - del_.mean()
    dkeep = np.median(D[i[~del_]]) if (~del_).any() else float('nan')
    P(f"\n== D in [{dmin_:.0f}m,{dmax_:.0f}m] {tag}: belt mass {belt_mass:.1e} M_sun ==")
    P(f"   pairs {len(i)} | K(conj per 10^3 orbits) med {np.median(K):.0f} p90 {np.percentile(K,90):.0f}")
    P(f"   dmin med {np.median(dmin):.3e} p10 {np.percentile(dmin,10):.3e} | vrel@event med {np.median(vmin):.4f} p10 {np.percentile(vmin,10):.4f}")
    P(f"   DELETABLE {del_.mean():.6f} | surviving {surv:.3e} | surviving member D med {dkeep:.0f} m")

# variants on scenario 1 (free: same wmin/vmin arrays, different mass/quantum)
(i, j, wmin, dmin, vmin, K, m, D) = results[(70.0, 4.7e5)]
P("\n== variants on D in [70m,470km] ==")
del52, _, _ = G.deleted_from(wmin, m, i, j, a, quant=2.0**-52)
P(f"   Q52 quantum: deletable {del52.mean():.6f}")
m52 = m * (1.2e-9 / (m.mean() * 1e9))
delM, _, _ = G.deleted_from(wmin, m52, i, j, a)
P(f"   real-belt mass x52 (total 1.2e-9 M_sun): deletable {delM.mean():.6f}")
m50 = np.full(n, G.mass_of_D(50.0))
delC, _, _ = G.deleted_from(wmin, m50, i, j, a)
P(f"   all-50m control: deletable {delC.mean():.6f} (c7eb anchor: 0/1000 -> ~1.0)")
m10k = np.full(n, G.mass_of_D(1e4))
delN, _, _ = G.deleted_from(wmin, m10k, i, j, a)
P(f"   all-10km control: deletable {delN.mean():.6f} (author model said 0.118)")

# true-conjunction count (for the amortized gate cost): events with d < 0.05
# and the K distribution feed events-per-refresh
print("\n".join(out))
with open(__file__.replace(".py", "-out.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
