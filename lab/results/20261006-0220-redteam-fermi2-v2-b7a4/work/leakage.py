#!/usr/bin/env python3
"""Window-leakage probe (dossier K2): orbit-scale windows do not measure the kernel.
At 3.1M members launched at rest +/-0.02M plunge inside one orbit (window impossible);
at 6M orbit-scale windows give 0.4x..1.8x the true eigenvalue. h->0 sequences are in
decisive.log (kernel.py)."""
import math, numpy as np, importlib.util
spec = importlib.util.spec_from_file_location("p", "probe-orig.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
M = p.M

def eig2(E):
    a = 0.5*(E[0,0]+E[1,1]); d = 0.5*(E[0,0]-E[1,1]); r = math.hypot(d, E[0,1])
    return a-r, a+r

def probe(r0, eps=0.02):
    L = r0*math.sqrt(M/(r0-3*M)); Tp = 2*math.pi*r0**2/L
    dtau = (2*math.pi*r0**1.5)/3999
    o = p.Origin(p.tetradize(p.circular_y0(r0)), 2*math.pi*r0**1.5, n_dense=4000)
    w = M/r0**3
    def window_E(i0, m_steps):
        n = len(o.tau)
        idx_w = np.clip(i0 + np.round(np.linspace(0, m_steps, 9)).astype(int), 0, n-1)
        u, e1, e2 = o.Y[3:6, i0], o.Y[6:9, i0], o.Y[9:12, i0]
        P0 = np.array([o.t[i0], o.r[i0], o.ph[i0]])
        h = o.tau[idx_w[-1]] - o.tau[idx_w[0]]
        def series(X0):
            P = P0 + X0[0]*e1 + X0[1]*e2
            r = P[1]
            un = u.copy()
            nrm = -p.f_of(r)*un[0]**2 + un[1]**2/p.f_of(r) + r*r*un[2]**2
            un /= math.sqrt(-nrm)     # renormalized launch (valid initial data)
            mem = p.Member(np.concatenate([P, un]), h + 5.0)
            mem.X0n = float(np.linalg.norm(X0))
            if mem.plunged or not np.all(np.isfinite(mem.rs)): return None
            Xt, prev = [], None
            for i in idx_w:
                out = p.fermi_X(mem, o, int(i), prev)
                if out is None: return None
                Xt.append(out[0]); prev = (out[1], float(np.linalg.norm(out[0]))+1e-12)
            return np.array(Xt)
        cols = []
        for d in (0, 1):
            sP = series(np.array([eps, 0.0]) if d == 0 else np.array([0.0, eps]))
            sM = series(np.array([-eps, 0.0]) if d == 0 else np.array([0.0, -eps]))
            if sP is None or sM is None: return None, h
            xi = (sP - sM)/2.0
            tt = o.tau[idx_w]
            A = np.vstack([tt**0, tt-tt[0], (tt-tt[0])**2]).T
            c = np.linalg.lstsq(A, xi, rcond=None)[0]
            cols.append(2*c[2])
        E = np.empty((2,2)); E[:,0] = -cols[0]/eps; E[:,1] = -cols[1]/eps
        return 0.5*(E+E.T), h
    print(f"circ r={r0}: Tp={Tp:.4f}; h->0 Richardson radial/2w from kernel.py")
    for m, lbl in ((int(round(Tp/4/dtau)), "Tp/4"), (int(round(Tp/2/dtau)), "Tp/2"),
                   (int(round(Tp/dtau)), "Tp"),
                   (int(round(2*math.pi*r0**1.5/dtau)), "prior-run window (1/sqrt(g) orbits)")):
        out = window_E(0, m)
        if out[0] is None:
            print(f"  h={lbl:30s}: FAILED (member plunge / bracket)"); continue
        E, h = out
        print(f"  h={lbl:30s} h={h:8.3f}: radial/2w = {eig2(E)[0]/(2*w):+8.4f}")

probe(3.1)
probe(6.0)
