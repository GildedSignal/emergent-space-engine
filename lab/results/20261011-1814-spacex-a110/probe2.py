#!/usr/bin/env python3
"""Brute-force truth: encounters and partner rank-at-epoch by direct
integration (validated against the failed event engine; see dossier).
Units as probe.py (a=1, GM=1, orbit=2pi)."""
import numpy as np, probe, sys
TWO_PI = 2.0 * np.pi

def brute_ranks(sw, b, T_orb, dt, tag):
    a, e, w, M = sw; n = len(a); nn = a ** -1.5; T = TWO_PI * T_orb
    steps = int(T / dt)
    pos0 = probe.order_positions(a, e, w, M, nn, 0.0)
    inside = None; d0s = []; births = 0
    for s in range(steps):
        t = s * dt
        r, th = probe.kepler(a, e, w, np.mod(M + nn * t, TWO_PI))
        th = np.mod(th, TWO_PI)
        X = r * np.cos(th); Y = r * np.sin(th)
        d2 = (X[:, None] - X[None, :]) ** 2 + (Y[:, None] - Y[None, :]) ** 2
        now = d2 < b * b
        if inside is None:
            inside = np.zeros_like(now)
        ent = now & ~inside
        ii, jj = np.nonzero(np.triu(ent, 1))
        if s == 0:
            births = len(ii)
        else:
            for I, J in zip(ii, jj):
                d0s.append(int(probe.circ_d(pos0, np.array([I]),
                                            np.array([J]), n)[0]))
        inside |= now; inside &= now
    d0s = np.array(d0s)
    q = lambda f: (f(d0s) if len(d0s) else -1)
    print(f"{tag}: enc={len(d0s):5d} (births excluded: {births}) "
          f"enc/body/orbit={len(d0s)/(n*T_orb):.4f} "
          f"d0 med={q(np.median):.0f} p99={q(lambda x: np.percentile(x,99)):.0f} "
          f"max={q(max):d} frac<=4={q(lambda x: np.mean(x<=4)):.2f} "
          f"frac<=8={q(lambda x: np.mean(x<=8)):.2f}", flush=True)
    return d0s

if __name__ == "__main__":
    # e-noise sweep on a packed convoy (the gold taleb-09b5's formation)
    for se in (0.0, 0.003, 0.01, 0.03):
        rng = np.random.default_rng(5)
        brute_ranks(probe.swarm(rng, 256, 1e-4, se, "slots"),
                    3e-3, 8.0, 0.05, f"convoy se={se:g}  T=8")
    # ring: the channel trade (circular vs e-noise, same seed)
    for se in (0.0, 0.03):
        rng = np.random.default_rng(99)
        brute_ranks(probe.swarm(rng, 256, 1e-3, se, "ring"),
                    3e-3, 2.0, 0.05, f"ring   se={se:g}  T=2")
