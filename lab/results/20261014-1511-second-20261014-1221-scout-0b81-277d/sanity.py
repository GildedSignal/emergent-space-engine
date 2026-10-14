#!/usr/bin/env python3
"""Sanity: what did the checker measure? Vector miss vs radial-only miss.

Two eccentric crossing orbits, e=0.05 both, random omega and phases, H=1000 orbits.
Exact Kepler propagation (analytic, Newton on E). Brute-force fine uniform sampling
+ local refinement, exactly the checker's procedure at two readouts:
  (a) min_t |x1(t)-x2(t)|   (position-vector miss — the physical miss distance)
  (b) min_t ||r1|| - ||r2|| (scalar radial distance difference)
Compare with the checker's table (their medians at da=0.005/0.02/0.1).
"""
import numpy as np

rng = np.random.default_rng(7)

def kepler_pos(a, e, w, M0, t):
    """Exact planar Kepler position + velocity at times t (GM=1)."""
    n = a ** -1.5
    M = M0 + n * t
    M = np.mod(M + np.pi, 2 * np.pi) - np.pi
    E = M.copy()
    for _ in range(60):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        dE = -f / fp
        E = E + dE
        if np.max(np.abs(dE)) < 1e-14:
            break
    cosE, sinE = np.cos(E), np.sin(E)
    x = a * (cosE - e)
    y = a * np.sqrt(1 - e * e) * sinE
    cw, sw = np.cos(w), np.sin(w)
    px = cw * x - sw * y
    py = sw * x + cw * y
    return px, py

def run(da, seeds=8, nsamp=4_000_000, H=1000.0):
    out = []
    for s in range(seeds):
        a1, a2 = 1.0, 1.0 + da
        e1 = e2 = 0.05
        w1, w2 = rng.uniform(0, 2 * np.pi, 2)
        M01, M02 = rng.uniform(0, 2 * np.pi, 2)
        t = np.linspace(0, H * 2 * np.pi, nsamp, endpoint=False)
        x1, y1 = kepler_pos(a1, e1, w1, M01, t)
        x2, y2 = kepler_pos(a2, e2, w2, M02, t)
        dvec = np.hypot(x1 - x2, y1 - y2)
        drad = np.abs(np.hypot(x1, y1) - np.hypot(x2, y2))
        out.append((dvec.min(), drad.min()))
    v = np.array(out)
    print(f"da={da}: vector-miss med {np.median(v[:,0]):.3e} | radial-only med {np.median(v[:,1]):.3e} (8 seeds)")
    return v

if __name__ == "__main__":
    print("checker table: da=0.005 -> 1.0e-3 | 0.02 -> 2.7e-4 | 0.1 -> 3.0e-2")
    run(0.005)
    run(0.02)
    run(0.1)
