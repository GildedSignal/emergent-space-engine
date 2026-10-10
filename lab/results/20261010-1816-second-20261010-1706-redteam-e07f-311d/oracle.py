#!/usr/bin/env python3
"""Oracle for the second-author falsifier: exact Binet (u" + u = 1/l^2 + 3u^2)
integrated in float64 from the SAME decoded integer states the shipped law saw
(sweep.out columns), plunge iff u >= 1/2 (the horizon), vectorized RK4 in phi.
A float algebra oracle (cubic discriminant of the decoded (E, L), ~1e-12)
adjudicates razor states whose whirl outlasts phimax. Mirrors binet_isco.py of
run 20261010-1706-redteam-e07f; shares no code with the crate.
"""
import numpy as np

R = 'lab/results/20261010-1816-second-20261010-1706-redteam-e07f-311d'

def load():
    rows = []
    for line in open(f'{R}/sweep.out'):
        t = line.split()
        if len(t) < 7:
            continue
        rows.append((float(t[0]), float(t[1]), float(t[2]), float(t[3]),
                     t[6], t[7] if len(t) > 7 else '', t[8] if len(t) > 8 else ''))
    return rows

def invariants(rs, vt):
    u = 1.0 / rs
    den = 1.0 - 2.0 * u - vt * vt
    L = rs * vt / np.sqrt(den)
    E2 = (1.0 - 2.0 * u) * (1.0 + (L / rs) ** 2)
    return u, L, E2

def rk4(u0, ih2, phimax=1600.0, dphi=2e-3):
    """Vectorized RK4 of u" = ih2 - u + 3u^2, u'(0)=0. Returns plunge mask, umin, umax."""
    u = u0.copy()
    up = np.zeros_like(u)
    alive = np.ones_like(u, dtype=bool)
    umin, umax = u.copy(), u.copy()
    n = int(phimax / dphi)
    for _ in range(n):
        m = alive
        if not m.any():
            break
        um, upm, ih = u[m], up[m], ih2[m]
        k1u, k1p = upm, ih - um + 3 * um * um
        u1, p1 = um + 0.5 * dphi * k1u, upm + 0.5 * dphi * k1p
        k2u, k2p = p1, ih - u1 + 3 * u1 * u1
        u2, p2 = um + 0.5 * dphi * k2u, upm + 0.5 * dphi * k2p
        k3u, k3p = p2, ih - u2 + 3 * u2 * u2
        u3, p3 = um + dphi * k3u, upm + dphi * k3p
        k4u, k4p = p3, ih - u3 + 3 * u3 * u3
        un = um + dphi / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        pn = upm + dphi / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
        u[m], up[m] = un, pn
        np.minimum(umin[m], un, out=umin[m])
        np.maximum(umax[m], un, out=umax[m])
        dead = un >= 0.5
        if dead.any():
            idx = np.flatnonzero(m)
            alive[idx[dead]] = False
    return ~alive, umin, umax

def main():
    rows = load()
    print(f"loaded {len(rows)} states")
    for eps in (1e-3, -1e-3, 0.0):
        cls = [r for r in rows if r[1] == eps]
        rs = np.array([r[2] for r in cls])
        vt = np.array([r[3] for r in cls])
        law = np.array([1 if r[4] == 'bound' else -1 for r in cls])
        # sanity: L^2 vs r0^2/(r0-3)
        u, L, E2 = invariants(rs, vt)
        l2h = np.array([r[0] ** 2 / (r[0] - 3.0) for r in cls])
        sane = np.max(np.abs(L ** 2 / l2h - 1))
        plunge, umin, umax = rk4(1.0 / rs, 1.0 / L ** 2)
        oracle = np.where(plunge, -1, 1)
        dis = law != oracle
        disa = dis  # algebra adjudication lives in exact.py (exact rational)
        n = len(cls)
        print(f"\n=== eps={eps:+.0e}: {n} states, max|L^2/r0^2/(r0-3)-1| = {sane:.2e}")
        b = np.flatnonzero(law[:-1] != law[1:])
        for i in b:
            print(f"  law boundary: refuse[{cls[i][0]:.6f}] -> bound[{cls[i+1][0]:.6f}] (step {cls[i+1][0]-cls[i][0]:.2e})")
        ob = np.flatnonzero(oracle[:-1] != oracle[1:])
        for i in ob[:6]:
            print(f"  rk4 oracle boundary: plunge[{cls[i][0]:.6f}] -> bound[{cls[i+1][0]:.6f}]")
        print(f"  law-vs-rk4 disagreements: {dis.sum()}/{n}")
        print(f"  (algebra adjudication of every state: exact.py)")
        if dis.sum():
            idx = np.flatnonzero(dis)
            print(f"  disagreement r0 range: [{cls[idx[0]][0]:.6f}, {cls[idx[-1]][0]:.6f}] width {cls[idx[-1]][0]-cls[idx[0]][0]:.2e}")
            # widths of contiguous disagreement runs
            runs, start = [], idx[0]
            for a, b2 in zip(idx[:-1], idx[1:]):
                if b2 != a + 1:
                    runs.append((start, a)); start = b2
            runs.append((start, idx[-1]))
            for a, b2 in runs[:8]:
                side = 'law=bound,oracle=plunge' if law[a] == 1 else 'law=refuse,oracle=bound'
                print(f"    run [{cls[a][0]:.6f},{cls[b2][0]:.6f}] w={cls[b2][0]-cls[a][0]:.2e} ({side})")
        print("  (bound/plunge adjudication of every state: exact.py, exact rational)")

if __name__ == '__main__':
    main()
