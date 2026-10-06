#!/usr/bin/env python3
"""E_eff: the Fermi-frame tidal tensor measured directly from exact Schwarzschild
geodesics (pair differences of members launched at window-local tetrad offsets,
second derivative from a quadratic fit). No Riemann code involved.
Then compare with (a) the einsum-projected tensor, (b) the naive Newtonian-form
kernel (M/r^3)(I-3rr^T) with r = coordinate radial direction."""
import math, sys
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("p", "probe.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)

def window_E(origin, i0, eps=0.02, npts=9, hspan=None):
    """Launch 4 members from grid index i0 (+-eps e1, +-eps e2, U=u), reconstruct
    their Fermi X over a short tau window ahead of tau[i0], fit quadratics, return
    (E_eff[2x2], taus) with xi_dd = -E xi."""
    n = len(origin.tau)
    tau0 = origin.tau[i0]
    hspan = hspan or min(0.05 * (origin.tau[-1] - origin.tau[0]), 0.3 * math.sqrt(origin.r[i0]**3))
    taus_w = tau0 + np.linspace(0, hspan, npts)
    idx_w = np.clip(np.searchsorted(origin.tau, taus_w), 0, n - 1)
    u, e1, e2 = origin.Y[3:6, i0], origin.Y[6:9, i0], origin.Y[9:12, i0]
    P0 = np.array([origin.t[i0], origin.r[i0], origin.ph[i0]])
    def series(X0):
        P = P0 + X0[0] * e1 + X0[1] * e2
        mem = p.Member(np.concatenate([P, u.copy()]), 5 * origin.tau[-1] + 10)
        mem.X0n = float(np.linalg.norm(X0)); mem.V0n = 0.0
        Xt, prev = [], None
        for i in idx_w:
            out = p.fermi_X(mem, origin, int(i), prev)
            if out is None: return None
            Xv, tm = out
            Xt.append(Xv); prev = (tm, float(np.linalg.norm(Xv)))
        return np.array(Xt)
    cols = []
    for d in (0, 1):
        sP = series(np.array([eps, 0.0]) if d == 0 else np.array([0.0, eps]))
        sM = series(np.array([-eps, 0.0]) if d == 0 else np.array([0.0, -eps]))
        if sP is None or sM is None: return None
        xi = (sP - sM) / 2.0
        tt = origin.tau[idx_w]
        A = np.vstack([tt**0, tt - tt[0], (tt - tt[0])**2]).T
        c = np.linalg.lstsq(A, xi, rcond=None)[0]
        cols.append(2 * c[2])
    E = np.stack([-cols[0], -cols[1]], axis=1)
    E[:, [0, 1]] = E[:, [0, 1]]
    # cols[j] = d2/dt2 xi for unit offset in direction j -> column j of (-E): fix assembly
    Eeff = np.empty((2, 2))
    Eeff[:, 0] = -cols[0] / eps
    Eeff[:, 1] = -cols[1] / eps
    return Eeff, origin.tau[idx_w]

def angle(E):
    return 0.5 * math.atan2(2 * E[0, 1], E[0, 0] - E[1, 1])

for r0 in (1000.0, 6.0, 3.1):
    T = 2 * math.pi * r0**1.5
    o = p.Origin(p.tetradize(p.circular_y0(r0)), T, n_dense=800)
    n = len(o.tau)
    w = 1.0 / r0**3
    print(f"\n== circ r={r0}  (Newtonian kernel eigen: {-2*w:+.6f}, {w:+.6f}) ==")
    print(f"{'tau/T':>7s} {'Eeff':>33s} {'Eein':>33s} {'naiveFrac':>9s}")
    for frac in (0.0, 0.125, 0.25, 0.375, 0.5):
        i0 = int(frac * (n - 1))
        out = window_E(o, i0, eps=min(0.02, 0.01 * r0))
        if out is None: print(frac, "failed"); continue
        Eeff, _ = out
        Eein = o.E[i0]
        th_n = o.thnaive[i0]
        nn = np.array([math.cos(th_n), math.sin(th_n)])
        Ena = (1.0 / o.r[i0]**3) * (np.eye(2) - 3 * np.outer(nn, nn))
        fn = np.linalg.norm(Eeff - Ena) / np.linalg.norm(Ena)
        fe = np.linalg.norm(Eeff - Eein) / max(np.linalg.norm(Eein), 1e-300)
        print(f"{frac:7.3f} [{Eeff[0,0]:+.5f} {Eeff[0,1]:+.5f}; {Eeff[1,1]:+.5f}]"
              f" ein[{Eein[0,0]:+.5f} {Eein[0,1]:+.5f}; {Eein[1,1]:+.5f}]"
              f" |naive|diff={fn:.4f} |ein|diff={fe:.4f}")
