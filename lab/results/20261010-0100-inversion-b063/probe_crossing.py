#!/usr/bin/env python3
"""Probe: why does the pi/4 crossing yield ~0 encounters in scene_S1? Dense brute force."""
import numpy as np
import sys
sys.path.insert(0, ".")
from harness import P, wrap_pm, kepler_E, body_state, vel_at_M, nu_to_M

rng = np.random.default_rng(11)
n_per, e, rho = 1000, 0.2, 1e-4
wpA, wpB = 0.0, np.pi / 2
M0A = rng.uniform(0, 2 * np.pi, n_per)
M0B = rng.uniform(0, 2 * np.pi, n_per)

for lam in (np.pi / 4, 5 * np.pi / 4):
    MstA = nu_to_M(wrap_pm(lam - wpA), e)
    MstB = nu_to_M(wrap_pm(lam - wpB), e)
    tA = (MstA - M0A) % P
    tB = (MstB - M0B) % P
    dt = wrap_pm(tA[:, None] - tB[None, :])
    cand = np.abs(dt) < 5e-3
    print(f"lam={lam:.4f} MstA={MstA:+.4f} MstB={MstB:+.4f} dMstar={np.pi-0 if False else (MstA-MstB):+.4f} "
          f"cands(|dt|<5e-3)={cand.sum()} cands(|dt|<1e-4)={(np.abs(dt)<1e-4).sum()}")
    # dense brute force over all candidate pairs with |dt| < 5e-3
    ii, jj = np.where(cand)
    d = dt[ii, jj]
    # refine each by dense Kepler sampling around midpoint
    hits = 0
    dmins = []
    for k in range(len(ii)):
        tA_i, tB_j = tA[ii[k]], tB[jj[k]]
        tc = 0.5 * (tA_i + tB_j)
        if tc > P - 0.01 or tc < 0.01:  # avoid wrap edge in this probe
            continue
        ts = np.linspace(tc - 3e-3, tc + 3e-3, 4001)
        xA, yA = body_state(M0A[ii[k]] + ts, e, wpA)[:2]
        xB, yB = body_state(M0B[jj[k]] + ts, e, wpB)[:2]
        dd = np.hypot(xA - xB, yA - yB)
        dmins.append(dd.min())
        if dd.min() < rho:
            hits += 1
    dmins = np.array(dmins)
    print(f"  refined {len(dmins)} pairs: hits(d<rho)={hits}, dmin range "
          f"[{dmins.min():.2e},{dmins.max():.2e}] (paper slope 1.165*|dt|, max|dt|=5e-3 -> 5.8e-3)")
    # empirical slope
    if len(dmins):
        dtt = np.abs(d)[:len(dmins)]
        keep = dtt < 2e-3
        print(f"  slope check: median d/|dt| = {np.median(dmins[keep]/dtt[keep]):.3f} (paper 1.165)")
