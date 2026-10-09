#!/usr/bin/env python3
"""Hypothesis after probe 1: static keys fail; events localize under the
time-to-fire key tau = wrap(dM)/|dn| (matching-engine time priority).
Same toy truth as probe_index.py. Deterministic."""
import numpy as np
from math import pi

rng = np.random.default_rng(20261009)

def make_belt(N, region=(1.0, 1.5), sig_e=0.02):
    a = rng.uniform(*region, N)
    e = rng.rayleigh(sig_e, N).clip(0, 3 * sig_e)
    M = rng.uniform(0, 2 * pi, N)
    return a, e, M

def make_formation(N, sig_a=1e-3, sig_e=1e-3):
    a = 1.0 + sig_a * rng.standard_normal(N)
    e = np.abs(rng.rayleigh(sig_e, N))
    M = rng.uniform(0, 2 * pi, N)
    return a, e, M

wrap = lambda d: np.abs((d + pi) % (2 * pi) - pi)

def belt_timekey(N, K=4):
    a, e, M = make_belt(N)
    n = a ** -1.5
    q, Q = a * (1 - e), a * (1 + e)
    order = np.argsort(q); qs = q[order]
    hi = np.searchsorted(qs, Q[order], 'right') - 1
    ns, Ms, a_s = n[order], M[order], a[order]
    # window: median load 4 events per body
    Lam = np.zeros(N)
    cn = np.concatenate([[0.0], np.cumsum(ns)])
    cnt = np.maximum(hi + 1 - np.arange(N) - 1, 0)
    s = cn[hi + 1] - cn[np.arange(N) + 1]
    Lam = np.abs(s - cnt * ns) / (2 * pi)
    dt = 4 / max(np.median(Lam), 1e-30)
    ranks, fires = [], 0
    for p in range(N):
        l, h = p + 1, hi[p] + 1
        if h <= l: continue
        phi = (Ms[l:h] - Ms[p]) % (2 * pi)          # directed relative phase
        dns = ns[l:h] - ns[p]                        # d(phi)/dt
        dn = np.abs(dns)
        gap = np.where(dns > 0, (2 * pi) - phi, phi) # distance to next crossing
        tau = np.where(dn > 1e-14, gap / np.maximum(dn, 1e-30), np.inf)
        fired = tau <= dt
        fires += fired.sum()
        if fired.any():
            rk = (tau < tau[fired][:, None]).sum(1) + 1  # rank among partners by tau
            ranks.extend(rk.tolist())
    r = np.array(ranks) if ranks else np.array([])
    print(f"[belt N={N}] dt={dt:.2e} fired={fires} tau-rank med={np.median(r):.0f} "
          f"p99={np.quantile(r,.99):.0f} max={r.max()} frac<=4={(r<=4).mean():.3f} "
          f"frac<=8={(r<=8).mean():.3f}")

def formation_timekey(N, K=4):
    a, e, M = make_formation(N)
    n = a ** -1.5
    dn_row = np.abs(n[:, None] - n[None, :])
    Lam = (dn_row.sum(1) - 0) / (2 * pi)          # self term zero anyway
    dt = 4 / np.median(Lam)
    ranks = []
    fires = 0
    for c in range(0, N, 128):
        i = np.arange(c, min(c + 128, N))
        phi = (M[None, :] - M[i, None]) % (2 * pi)
        dns = n[None, :] - n[i, None]
        dn = np.abs(dns)
        gap = np.where(dns > 0, (2 * pi) - phi, phi)
        tau = np.where(dn > 1e-14, gap / np.maximum(dn, 1e-30), np.inf)
        tau[np.arange(len(i)), i] = np.inf
        fired = tau <= dt
        fires += fired.sum()
        # rank of each fired partner among all partners by tau
        rkm = np.argsort(np.argsort(tau, axis=1), axis=1)   # rank by tau, per body
        ranks.extend(rkm[fired].tolist())
    r = np.array(ranks)
    print(f"[formation N={N}] dt={dt:.2e} fired={fires} tau-rank med={np.median(r):.0f} "
          f"p99={np.quantile(r,.99):.0f} max={r.max()} frac<=4={(r<=4).mean():.3f} "
          f"frac<=8={(r<=8).mean():.3f}")

if __name__ == '__main__':
    import time; t0 = time.time()
    for N in (2000, 8000):
        belt_timekey(N)
    for N in (1024, 4096):
        formation_timekey(N)
    print(f"total {time.time()-t0:.1f}s")
