#!/usr/bin/env python3
"""Cross-check of the shipped schwarztide.py closed forms against the red-team's
CORRECTED kernel (run 20261002-0539-redteam-fermi2-21db, its checker):

  radial tide (parallel frame, circular) = -w (3 gamma^2 - 1),  tangential = +w,
    w = M/r^3,  gamma^2 = f/(1-3M/r),  f = 1-2M/r
  static orthonormal R_{rhat phat rhat phat} = -M/r^3   (the root-cause fix)
  out-of-plane R_{thhat phat thhat phhat} = +2M/r^3     (their 3D note)
  axis: Marck rotation; circular anchor omega = sqrt(M/r^3), i.e. the geodetic
    precession dPhi/dphi = -sqrt(1-3M/r).

Three levels:
  (1) formula: my closed C22/C33/eigenvalues vs theirs, circular, 10 radii;
  (2) static Riemann: my riemann_down -> orthonormal, vs their stated components;
  (3) measurement: THEIR geodesic-pair machinery (eeff.py window_E, no Riemann
      code, no closed form) at r = 6 and 3.1, hspan and eps -> 0, vs my numbers.
"""
import math, sys
import numpy as np
import importlib.util

sys.path.insert(0, "..")
import schwarztide as st

M = 1.0
print("=" * 78)
print("(1) formula level: circular orbits")
print("=" * 78)
print("%8s %12s %12s %12s %12s %10s" % ("r", "C22+wg2m1", "C33-w", "eig-w pair",
                                        "radfac_meas", "radfac_cl"))
worst = {"C22": 0.0, "C33": 0.0, "eig": 0.0}
for rr in (3.1, 3.5, 4.0, 5.0, 6.0, 6.01, 6.02, 10.0, 50.0, 1000.0):
    Lc = math.sqrt(M*rr*rr/(rr-3*M)); Ec = (rr-2*M)/math.sqrt(rr*(rr-3*M))
    E, L = float(Ec), float(Lc)
    w = M/rr**3
    f = 1 - 2*M/rr
    g2 = f/(1 - 3*M/rr)                      # red-team gamma^2
    lam = L*L/(rr*rr)
    Cb = st.tide_boosted(M, E, L, rr, +1)
    e1 = abs(Cb[1, 1] + w*(3*g2 - 1))/abs(w*(3*g2 - 1))
    e2 = abs(Cb[2, 2] - w)/w
    ev = sorted(st.eigenvals(M, L, rr))
    ev_rt = sorted([w*(1+3*lam), w, -w*(3*g2-1)])
    e3 = max(abs(a-b) for a, b in zip(ev, ev_rt))/max(abs(ev[0]), abs(ev[2]))
    worst["C22"] = max(worst["C22"], e1); worst["C33"] = max(worst["C33"], e2)
    worst["eig"] = max(worst["eig"], e3)
    print("%8.2f %12.2e %12.2e %12.2e %12.4f %12.4f"
          % (rr, e1, e2, e3, -(3*g2-1)/2.0, -Cb[1, 1]/(2*w)))
print("worst rel diffs: C22 %.2e  C33 %.2e  eigen %.2e" %
      (worst["C22"], worst["C33"], worst["eig"]))

print()
print("=" * 78)
print("(2) static orthonormal Riemann (my riemann_down, projected on coframe)")
print("=" * 78)
for rr in (3.1, 6.0, 100.0):
    Rf = st.riemann_down(rr, M)
    f = 1 - 2*M/rr
    m = M/rr**3
    e0 = np.array([1/math.sqrt(f), 0, 0, 0]); e1v = np.array([0, math.sqrt(f), 0, 0])
    e2v = np.array([0, 0, 1/rr, 0]); e3v = np.array([0, 0, 0, 1/rr])
    def Rhat(a, b, c, d):
        return np.einsum('pqrs,p,q,r,s->', Rf, a, b, c, d)
    vals = {
        "R_t t": Rhat(e0, e1v, e0, e1v) + 2*m,     # want -2m
        "R_t ph": Rhat(e0, e3v, e0, e3v) - m,      # want +m
        "R_r ph": Rhat(e1v, e3v, e1v, e3v) + m,    # want -m  (red-team fix)
        "R_th ph": Rhat(e2v, e3v, e2v, e3v) - 2*m, # want +2m (their 3D note)
    }
    print("r=%7.2f  " % rr + "  ".join("%s:%+.2e" % kv for kv in vals.items()))
# circular anchors of the rotation
print("omega(circ) - sqrt(M/r^3):", " ".join(
    "%.1e" % abs(st.omega(M, float((rr-2*M)/math.sqrt(rr*(rr-3*M))),
                           float(math.sqrt(M*rr*rr/(rr-3*M))), rr) - math.sqrt(M/rr**3))
    for rr in (6.0, 6.01, 6.02, 10.0, 1000.0)))
print("dPhi/dphi(circ) + sqrt(1-3M/r):", " ".join(
    "%.1e" % abs(st.dPhi_dphi(M, float((rr-2*M)/math.sqrt(rr*(rr-3*M))),
                              float(math.sqrt(M*rr*rr/(rr-3*M))), rr)
                 + math.sqrt(1 - 3*M/rr))
    for rr in (6.0, 6.01, 6.02, 10.0, 1000.0)))

print()
print("=" * 78)
print("(3) measurement level: red-team geodesic pairs (window_E), r = 6 and 3.1")
print("=" * 78)
spec = importlib.util.spec_from_file_location("p", "work/redteam/probe.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)

def window_E(o, i0, eps, hspan):
    """verbatim port of the red-team eeff.window_E (their measurement, U=u)."""
    n = len(o.tau)
    tau0 = o.tau[i0]
    taus_w = tau0 + np.linspace(0, hspan, 9)
    idx_w = np.clip(np.searchsorted(o.tau, taus_w), 0, n - 1)
    u, e1, e2 = o.Y[3:6, i0], o.Y[6:9, i0], o.Y[9:12, i0]
    P0 = np.array([o.t[i0], o.r[i0], o.ph[i0]])
    def series(X0):
        P = P0 + X0[0]*e1 + X0[1]*e2
        mem = p.Member(np.concatenate([P, u.copy()]), 5*o.tau[-1] + 10)
        mem.X0n = float(np.linalg.norm(X0)); mem.V0n = 0.0
        Xt, prev = [], None
        for i in idx_w:
            out = p.fermi_X(mem, o, int(i), prev)
            if out is None: return None
            Xv, tm = out
            Xt.append(Xv); prev = (tm, float(np.linalg.norm(Xv)))
        return np.array(Xt)
    cols = []
    for d in (0, 1):
        sP = series(np.array([eps, 0.0]) if d == 0 else np.array([0.0, eps]))
        sM = series(np.array([-eps, 0.0]) if d == 0 else np.array([0.0, -eps]))
        if sP is None or sM is None: return None
        xi = (sP - sM)/2.0
        tt = o.tau[idx_w]
        A = np.vstack([tt**0, tt - tt[0], (tt - tt[0])**2]).T
        c = np.linalg.lstsq(A, xi, rcond=None)[0]
        cols.append(2*c[2])
    Eeff = np.empty((2, 2))
    Eeff[:, 0] = -cols[0]/eps
    Eeff[:, 1] = -cols[1]/eps
    return Eeff

def gdot3(a, b, r):   # (t,r,ph) components
    f = 1 - 2*M/r
    return -f*a[0]*b[0] + a[1]*b[1]/f + r*r*a[2]*b[2]

for r0 in (6.0, 3.1):
    T = 2*math.pi*r0**1.5
    o = p.Origin(p.tetradize(p.circular_y0(r0)), T, n_dense=1600)
    n = len(o.tau)
    i0 = int(0.125*(n - 1))
    w = M/r0**3
    f = 1 - 2*M/r0
    g2 = f/(1 - 3*M/r0)
    L = r0*math.sqrt(M/(r0 - 3*M)); E = (1 - 2*M/r0)/math.sqrt(1 - 3*M/r0)
    ev_cl = sorted([w, -w*(3*g2 - 1)])          # my closed in-plane eigenvalues
    print("\n== circ r=%.1f: closed in-plane eigenvalues {%.6f, %.6f}  "
          "(rad factor %.4f x -2w) ==" % (r0, ev_cl[0], ev_cl[1], (3*g2 - 1)/2))
    h0 = min(0.05*(o.tau[-1] - o.tau[0]), 0.3*math.sqrt(r0**3))
    for (hs, ep) in ((h0/2, 0.01), (h0/4, 0.005), (h0/8, 0.0025),
                     (h0/16, 0.00125), (h0/32, 0.000625), (h0/64, 0.0003125)):
        Eeff = window_E(o, i0, ep, hs)
        if Eeff is None:
            print("  hs=%.4f eps=%.4f  FAILED" % (hs, ep)); continue
        ev = sorted(np.linalg.eigvalsh(Eeff))
        de = max(abs(a - b) for a, b in zip(ev, ev_cl))/max(abs(ev_cl[0]), abs(ev_cl[1]))
        # full-matrix check at the window midpoint phase (e1 vs my boosted pair)
        imid = int(np.clip(np.searchsorted(o.tau, o.tau[i0] + hs/2), 0, n - 1))
        rm = o.r[imid]
        _, l2p, l3p = st.boosted_frame(E, L, rm, M, +1)
        l2p = np.array([l2p[0], l2p[1], l2p[3]]); l3p = np.array([l3p[0], l3p[1], l3p[3]])
        psi = math.atan2(gdot3(o.Y[6:9, imid], l3p, rm), gdot3(o.Y[6:9, imid], l2p, rm))
        Cp = st.tide_parallel(M, E, L, rm, psi, +1)[1:3, 1:3]
        dm = np.max(np.abs(Eeff - Cp))/max(np.max(np.abs(Cp)), 1e-300)
        print("  hs=%.4f eps=%.4f  eigdiff=%.2e  matrixdiff(mid-phase)=%.2e  "
              "radfac=%.4f" % (hs, ep, de, dm, -ev[0]/(2*w)))
