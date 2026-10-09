#!/usr/bin/env python3
"""Audit pinwheel encounters: exact distance at tm (fine sampled), wrapped
dtheta, true in-between count (circular), vs the linearized d_min."""
import numpy as np
from invert_train import TAU, RHO, kepler_E, inv_kepler_M, states, mean_longs

nc, seed, ecc, a_hw, orbits = 400, 11, 0.05, 1e-5, 20.0
r = np.random.default_rng(seed)
a = 1.0 + (2 * r.random(nc) - 1) * a_hw
e = np.full(nc, ecc) + r.rayleigh(1e-3, nc)
pom = TAU * r.random(nc)
lam0 = TAU * r.random(nc)
n = a ** -1.5
T = orbits * TAU
ks = np.arange(0, int(orbits) + 4)

def cross_enc(i, j):
    dp = (pom[i] - pom[j] + np.pi) % TAU - np.pi
    if abs(dp) < 1e-6:
        return []
    out = []
    for half in (0.0, np.pi):
        thc = (pom[i] + pom[j]) / 2.0 + half
        fi = (thc - pom[i] + np.pi) % TAU - np.pi
        fj = (thc - pom[j] + np.pi) % TAU - np.pi
        Mi, Mj = inv_kepler_M(fi, e[i]), inv_kepler_M(fj, e[j])
        ti = (pom[i] + Mi - lam0[i]) / n[i] + ks * (TAU / n[i])
        tj = (pom[j] + Mj - lam0[j]) / n[j] + ks * (TAU / n[j])
        ti = ti[(ti > TAU) & (ti < T - TAU)]
        tj = tj[(tj > 0) & (tj < T)]
        if len(ti) == 0 or len(tj) == 0:
            continue
        dtm = np.abs(ti[:, None] - tj[None, :])
        p, q = np.unravel_index(np.argmin(dtm), dtm.shape)
        D = ti[p] - tj[q]
        if abs(D) > 0.3:
            continue
        out.append((ti[p], tj[q]))
    return out

encs = []
for i in range(nc):
    for j in range(i + 1, nc):
        for ti, tj in cross_enc(i, j):
            encs.append((i, j, ti, tj))
# keep only linear d_min < rho, same as the scene run
def lin_dmin(i, j, ti, tj):
    # reproduce impact geometry
    dp = (pom[i] - pom[j] + np.pi) % TAU - np.pi
    for half in (0.0, np.pi):
        thc = (pom[i] + pom[j]) / 2.0 + half
        fi = (thc - pom[i] + np.pi) % TAU - np.pi
        fj = (thc - pom[j] + np.pi) % TAU - np.pi
        Mi, Mj = inv_kepler_M(fi, e[i]), inv_kepler_M(fj, e[j])
        ci = (pom[i] + Mi - lam0[i]) / n[i]
        cj = (pom[j] + Mj - lam0[j]) / n[j]
        if abs((ci % (TAU / n[i])) - 0) < 1e18:  # pass
            pass
    return None

# simpler: recompute exact by sampling around tm for every candidate pair
sel = []
for (i, j, ti, tj) in encs:
    tm = 0.5 * (ti + tj)
    ts = tm + np.linspace(-0.25, 0.25, 4001)
    xi = np.array([states(a[i:i+1], e[i:i+1], pom[i:i+1], lam0[i:i+1], tt)[0][0] for tt in ts])
    yi = np.array([states(a[i:i+1], e[i:i+1], pom[i:i+1], lam0[i:i+1], tt)[1][0] for tt in ts])
    xj = np.array([states(a[j:j+1], e[j:j+1], pom[j:j+1], lam0[j:j+1], tt)[0][0] for tt in ts])
    yj = np.array([states(a[j:j+1], e[j:j+1], pom[j:j+1], lam0[j:j+1], tt)[1][0] for tt in ts])
    dd = np.hypot(xi - xj, yi - yj)
    k = int(np.argmin(dd))
    if dd[k] < 2 * RHO:
        sel.append((i, j, float(dd[k]), float(ts[k])))

print(f"candidates with exact d_min < 2rho: {len(sel)} (of {len(encs)} pass coincidences)")
for (i, j, d, t) in sel:
    x, y, _, _, th, _ = states(a, e, pom, lam0, t)
    dth = abs((th[i] - th[j] + np.pi) % TAU - np.pi)
    ths = np.sort(th)
    # circular in-between count: ships strictly between i and j going the short way
    lo, hi = min(th[i], th[j]), max(th[i], th[j])
    between = int(np.sum((ths > lo) & (ths < hi)))
    lam = mean_longs(a, lam0, t)
    dlam = abs((lam[i] - lam[j] + np.pi) % TAU - np.pi)
    print(f"pair ({i:3d},{j:3d}) d={d/RHO:6.2f}rho dth={dth:.2e} between={between:3d} "
          f"dlam={dlam/RHO:7.1f}rho dpom={(abs((pom[i]-pom[j]+np.pi)%TAU-np.pi)):.3f}")
