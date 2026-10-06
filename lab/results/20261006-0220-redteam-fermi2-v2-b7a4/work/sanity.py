#!/usr/bin/env python3
"""Convention sanity check (pre-predictions). Fixes: (a) which sign of R_rphrph the
geodesic side demands, (b) the rotation-rate convention (omega vs -omega), (c) the
unwrap fix for axis tracking. Not the decisive experiment."""
import math
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("p", "probe-orig.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)

# --- sign-fixed Riemann template: R_{r phi r phi} = -M/r^3 (checker's fix)
RT2 = np.zeros((3, 3, 3, 3))
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                for perm, chi in p._GRP:
                    q = (a, b, c, d)
                    key = (q[perm[0]], q[perm[1]], q[perm[2]], q[perm[3]])
                    if (0, 1, 0, 1) in {key} or (0, 2, 0, 2) in {key}:
                        pass
                pass

_BASE2 = {(0, 1, 0, 1): -2.0, (0, 2, 0, 2): 1.0, (1, 2, 1, 2): -1.0}
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                for perm, chi in p._GRP:
                    q = (a, b, c, d)
                    key = (q[perm[0]], q[perm[1]], q[perm[2]], q[perm[3]])
                    if key in _BASE2:
                        RT2[a, b, c, d] = chi * _BASE2[key]
                        break

def einsum_E(origin, RT):
    n = origin.tau.size
    U = np.empty((n, 3))
    E1 = np.empty((n, 3)); E2 = np.empty((n, 3))
    for i in range(n):
        r = origin.r[i]
        U[i] = p.to_orth(origin.Y[3:6, i], r)
        E1[i] = p.to_orth(origin.Y[6:9, i], r)
        E2[i] = p.to_orth(origin.Y[9:12, i], r)
    w = p.M / origin.r**3
    Ehat = np.einsum("acbd,nc,nd->nab", RT, U, U)
    E = np.empty((n, 2, 2))
    E[:, 0, 0] = w * np.einsum("na,nab,nb->n", E1, Ehat, E1)
    E[:, 0, 1] = w * np.einsum("na,nab,nb->n", E1, Ehat, E2)
    E[:, 1, 0] = E[:, 0, 1]
    E[:, 1, 1] = w * np.einsum("na,nab,nb->n", E2, Ehat, E2)
    return E

def axis(E):
    th = np.arctan2(2*E[:, 0, 1], E[:, 0, 0] - E[:, 1, 1])
    return np.unwrap(2*th)/2   # unwrap the doubled angle (period-safe)

for r0 in (6.0, 3.1):
    L = r0*math.sqrt(1.0/(r0-3.0)); En = (1-2/r0)/math.sqrt(1-3/r0)
    o = p.Origin(p.tetradize(p.circular_y0(r0)), 2*math.pi*r0**1.5, n_dense=2000)
    Tp = 2*math.pi*r0**2/L                      # true proper period
    print(f"\n== circ r={r0}: tau_end={o.tau_end:.3f}  Tp={Tp:.3f}  (tau_end/Tp={o.tau_end/Tp:.4f})")
    for tag, RT in (("wrong(+1)", p.RT), ("fixed(-1)", RT2)):
        E = einsum_E(o, RT)
        ax = axis(E)
        dax = np.gradient(ax, o.tau)
        sweep = np.trapz(np.abs(dax), o.tau) * (Tp/o.tau_end)   # per true orbit
        w = 1/r0**3
        print(f"  {tag:10s} E(0)=[{E[0,0,0]:+.6f} {E[0,0,1]:+.2e}; {E[0,1,1]:+.6f}]"
              f"  (closed: {-(2+3*(1/(r0-3))*r0)*w:+.6f}, {w:+.6f})"
              f"  axis sweep/orbit={sweep:.4f} rad  (omega*Tp={math.sqrt(1/r0**3)*Tp:.4f}, 2pi*sqrt(g)={2*math.pi*math.sqrt(1-3/r0):.4f})")
    # geodetic anchor: transported e1 vs static radial direction
    f_ = 1-2/r0
    cph, sph = np.cos(o.ph), np.sin(o.ph)
    # static rhat components on transported frame: g(rhat, e_i)
    a1 = np.empty_like(o.tau); a2 = np.empty_like(o.tau)
    for i in range(len(o.tau)):
        r = o.r[i]; f = 1-2/r
        rh = np.array([0.0, math.sqrt(f), 0.0])
        a1[i] = p.gdot(rh, o.Y[6:9, i], r); a2[i] = p.gdot(rh, o.Y[9:12, i], r)
    th_r = np.arctan2(a2, a1)
    dphi = L/r0**2
    # static rhat sweeps (orbital 2pi + geodetic) in Fermi frame per orbit
    sweep_r = np.trapz(np.abs(np.gradient(np.unwrap(2*th_r)/2, o.tau)), o.tau)*(Tp/o.tau_end)
    geod = 2*math.pi*(1-math.sqrt(1-3/r0))
    print(f"  static rhat sweep/orbit={sweep_r:.4f}  (2pi+geod={2*math.pi+geod:.4f}, 2pi-geod={2*math.pi-geod:.4f})")
