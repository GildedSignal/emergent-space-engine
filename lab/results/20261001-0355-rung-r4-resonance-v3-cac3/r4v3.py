#!/usr/bin/env python3
"""Rung r4 v3: the resonant normal form vs a dense truth. See dossier.md.

Model (r4 v1/v2 spec, the red-team's): planar, G = 1, m0 = 1-mu,
perturber m2 = mu on a circular orbit with a2 = 1 (n2 = 1, P2 = 2pi),
inner body 1 a test particle (m1 = 1e-8 in the truth's N-body).
Initial phases (red-team's, w2 read in degrees per v3):
  lambda20 = 4 deg, varpi20 = 4 deg (inert, e2 = 0), lambda10 = varpi10 = 0,
  e10 = 0.01 (particle at pericentre).

Canonical resonant variables (Delaunay):
  L1 = sqrt(m0*a1), Gm = L1*(1-sqrt(1-e1^2));  gamma = varpi1-(j+1)l2+j*l1 = -phi
  K(gamma,Gm;Lp) = -m0^2/(2 L1^2) - (j+1)n2 Gm - Rbar,  L1 = Lp + j*Gm,
  Lp = L1 + j*Gm conserved (the resonant Delaunay).
Rbar, averaged over the fast angle lambda1 (first order in mu):
  nf1: C1(a1) e cos gamma
  nf2: nf1 + C2(a1) e^2 cos 2gamma + Csec(a1) e^2
C1, C2, Csec are signed coefficients of the exact heliocentric disturbing
function R = m2[1/|r2-r1| - r1.r2/r2^3], projected on the resonant harmonics
by 2D quadrature over (lambda1, lambda2) at e in {0, 1e-3, 2e-3} and fitted
in e (linear / quadratic; e^3 contamination < 1e-5 relative).

The compiled cycle: the 1-DOF level curve K = E is followed by arc length
(RK4 + projection back onto K = E, so energy is conserved to ~1e-12), the
time of flight is accumulated as a third ODE component, and the motion is
replayed from the closed table for the whole run (the law's cycle memo).
Generator evaluations are counted for every K-gradient call of the trace.

Truth: fixed-step RK4, barycentric 3-body, N steps per initial inner period
(ladder 600/1200/2400, r4 v2's). 16 samples per inner period.
"""
import json
import math
import os
import numpy as np

D2R = math.pi / 180.0
HERE = os.path.dirname(os.path.abspath(__file__))
M1_TINY = 1e-8
E0 = 0.01
LAM20 = 4.0 * D2R
NSYN = 200.0

# ------------------------------------------------------------------ Kepler
def kepler_E(M, e):
    M = np.asarray(M, dtype=float)
    E = M.copy() if np.ndim(M) else float(M)
    E = np.array(E, dtype=float, copy=True)
    for _ in range(80):
        f = E - e * np.sin(E) - M
        d = f / (1.0 - e * np.cos(E))
        E = E - d
        if np.max(np.abs(d)) < 1e-15:
            break
    return E

def helio_vec(a, e, varpi, M, GM):
    """Kepler states for arrays of mean anomaly M (planar)."""
    a = np.asarray(a, float); e = np.asarray(e, float)
    E = kepler_E(M, e)
    cE, sE = np.cos(E), np.sin(E)
    b2 = np.sqrt(np.maximum(1.0 - e * e, 0.0))
    r = a * (1.0 - e * cE)
    n = np.sqrt(GM / a**3)
    xd = a * (cE - e); yd = a * b2 * sE
    vxd = -a * a * n * sE / r; vyd = a * a * n * b2 * cE / r
    cv, sv = np.cos(varpi), np.sin(varpi)
    return (cv*xd - sv*yd, sv*xd + cv*yd, cv*vxd - sv*vyd, sv*vxd + cv*vyd)

def osc_el(rx, ry, vx, vy, GM):
    """Osculating (a, e, varpi, mean longitude) from a heliocentric state."""
    r = np.hypot(rx, ry); v2 = vx*vx + vy*vy; rv = rx*vx + ry*vy
    energy = v2/2 - GM/r
    a = -GM/(2*energy)
    ex = ((v2 - GM/r)*rx - rv*vx)/GM
    ey = ((v2 - GM/r)*ry - rv*vy)/GM
    e = np.hypot(ex, ey)
    cosE = np.clip((1.0 - r/a)/np.maximum(e, 1e-300), -1, 1)
    E = np.arccos(cosE)*np.where(rv >= 0, 1.0, -1.0)
    M = E - e*np.sin(E)
    varpi = np.arctan2(ey, ex)
    return a, e, varpi, np.mod(M + varpi, 2*np.pi)

# -------------------------------------------------- disturbing-function coefs
def R_on_grid(a1, e, GM, m2, N):
    lam1 = np.linspace(0, 2*np.pi, N, endpoint=False)
    lam2 = np.linspace(0, 2*np.pi, N, endpoint=False)
    rx, ry, _, _ = helio_vec(a1, e, 0.0, lam1, GM)     # varpi1 = 0 -> M1 = lam1
    L2 = lam2[None, :]
    r2x = np.cos(L2); r2y = np.sin(L2)                 # a2 = 1
    dx = r2x - rx[:, None]; dy = r2y - ry[:, None]
    d = np.sqrt(dx*dx + dy*dy)
    indirect = (rx[:, None]*r2x + ry[:, None]*r2y)
    return m2*(1.0/d - indirect), lam1, lam2

def coefs_at(j, a1, GM, m2, N=96):
    L2, L1 = np.meshgrid(*[np.linspace(0, 2*np.pi, N, endpoint=False)]*2, indexing="xy")
    th1 = j*L1 - (j+1)*L2
    th2 = 2*th1
    es = (0.0, 1e-3, 2e-3)
    proj1, proj2, mean = [], [], []
    for e in es:
        R, _, _ = R_on_grid(a1, e, GM, m2, N)
        mean.append(R.mean())
        proj1.append((R*np.cos(th1)).mean())
        proj2.append((R*np.cos(th2)).mean())
    C1 = proj1[1]/1e-3                       # e->0: (P(e)-P(0))/e; P(0) = 0 by symmetry
    C1b = (proj1[2]-proj1[1])/1e-3           # Richardson check
    A = np.vstack([np.ones(3), es, np.square(es)]).T
    csec = np.linalg.solve(A, np.array(mean))[2]
    C2 = np.linalg.solve(A, np.array(proj2))[2]
    return C1, C2, csec, C1b - C1

class CoefFit:
    def __init__(self, j, mu, pad=0.15, npts=25):
        GM, m2 = 1.0 - mu, mu
        a1r = (1.0 - mu)**(1/3.0)*(j/(j+1.0))**(2/3)
        grid = a1r*np.exp(np.linspace(-pad, pad, npts))
        cs = np.array([coefs_at(j, a, GM, m2, 96)[:3] for a in grid])
        self.p = [np.polyfit(grid, cs[:, k], 7) for k in range(3)]
        self.grid, self.cs, self.a1r = grid, cs, a1r
        self.j, self.mu, self._cache = j, mu, {}
    def c(self, a1):
        a = np.asarray(a1, float)
        inside = (a >= self.grid[0]) & (a <= self.grid[-1])
        if inside.all():
            return np.array([np.polyval(p, a) for p in self.p])
        if (~inside).all():
            if a.ndim == 0:
                key = float(a)
                if key not in self._cache:
                    self._cache[key] = np.array(coefs_at(self.j, key,
                        1.0 - self.mu, self.mu, 128)[:3])
                return self._cache[key]
            out = []
            for x in a:
                out.append(self.c(float(x)))
            return np.stack(out, axis=-1)
        return np.array([self.c(float(x)) for x in np.atleast_1d(a)])



# ------------------------------------------------------------- normal form
class NF:
    def __init__(self, j, mu, order, fit=None):
        self.j, self.mu, self.order = j, mu, order
        self.m0 = 1.0 - mu
        self.n2 = 1.0
        self.fit = fit if fit is not None else CoefFit(j, mu)
        self.n_evals = 0
        self._dp = [np.polyder(p) for p in self.fit.p]

    def parts(self, g, G, Lp):
        """K, dK/dG (at fixed Lp), dK/dgamma.  The resonant Hamiltonian:
        K = -m0^2/(2 L1^2) + (j+1) n2 G + Rbar(g, L1, G),
        L1 = Lp - j G  (Lp = L1 + j G is conserved), n2 = 1,
        Rbar = C1(a1) e cos g (+ nf2: C2 e^2 cos 2g + Csec e^2).
        Validated: island at g=0 for C1<0, prograde secular precession
        (truth ctl5), resonance track d(e^2) = -d(a)/(j a) (truth)."""
        j, m0 = self.j, self.m0
        g = np.asarray(g, float); G = np.asarray(G, float)
        L1 = Lp - j*G
        a1 = L1*L1/m0
        C = self.fit.c(a1)
        q = 1.0 - G/L1
        e = np.sqrt(np.maximum(1.0 - q*q, 1e-300))
        K = -m0*m0/(2*L1*L1) + (j+1.0)*G
        dK = -j*m0*m0/L1**3 + (j+1.0)
        dalpha = 2*L1/m0
        dC = np.array([np.polyval(self._dp[k], a1) for k in range(3)])
        de_dG = q*Lp/(L1*L1*e)
        coupling = C[0]*e*np.cos(g)
        dK_coupling = (-dC[0]*dalpha*j*e + C[0]*de_dG)*np.cos(g)
        dKg = -C[0]*e*np.sin(g)
        if self.order >= 2:
            e2 = e*e
            coupling += C[1]*e2*np.cos(2*g) + C[2]*e2
            dK_coupling += (-dC[1]*dalpha*j*e2 + C[1]*2*e*de_dG)*np.cos(2*g)
            dK_coupling += -dC[2]*dalpha*j*e2 + C[2]*2*e*de_dG
            dKg -= 2*C[1]*e2*np.sin(2*g)
        K = K + coupling
        dK = dK + dK_coupling
        self.n_evals += 1
        return K, dK, dKg

    def compile_cycle(self, g0, G0, Lp, dphi=0.25, nmax=200000):
        """Compile the cycle: integrate the 1-DOF averaged flow
        (dtheta/dt = dK/dG, dG/dt = -dK/dgamma) by RK4 until the state
        returns to the initial point on the (theta mod 2pi, G) cylinder;
        the recorded table over one period is then replayed exactly for
        the whole run (the law's cycle memo).  The step is adaptive in
        phase; generator evaluations are counted in parts()."""
        E0v, dK0, dKg0 = self.parts(g0, G0, Lp)
        Gscale = max(G0, 1e-6*Lp)
        def rhs(th, G):
            _, dK, dKg = self.parts(th, G, Lp)
            return dK, -dKg
        th, G = g0, G0
        t = 0.0
        arc = 0.0
        ths = [th]; Gs = [G]; ts = [0.0]
        cross_prev = None
        for _ in range(nmax):
            r1t, r1G = rhs(th, G)
            speed = max(abs(r1t), abs(r1G)/max(Gscale, 1e-300)*0.5)
            if speed <= 1e-300:
                break
            dt = dphi/speed
            # RK4
            k1t, k1G = r1t, r1G
            k2t, k2G = rhs(th + 0.5*dt*k1t, G + 0.5*dt*k1G)
            k3t, k3G = rhs(th + 0.5*dt*k2t, G + 0.5*dt*k2G)
            k4t, k4G = rhs(th + dt*k3t, G + dt*k3G)
            dth = dt*(k1t + 2*k2t + 2*k3t + k4t)/6.0
            dG = dt*(k1G + 2*k2G + 2*k3G + k4G)/6.0
            th_new, G_new = th + dth, G + dG
            t_new = t + dt
            arc += abs(dth)
            # crossing of theta = g0 (mod 2pi) between th and th_new?
            def wrap(x):
                return (x - g0 + math.pi) % (2*math.pi) - math.pi
            if arc > math.pi and len(ts) > 30:
                s0, s1 = wrap(th), wrap(th_new)
                if s0*s1 < 0 and abs(s1 - s0) < math.pi:
                    frac = -s0/(s1 - s0)
                    Gc = G + frac*(G_new - G)
                    tc = t + frac*dt
                    if abs(Gc - G0) < 3e-3*max(Gscale, abs(G0), abs(Gc)):
                        # close the table at the crossing point
                        tab_t = np.array(ts + [tc])
                        thc = ths[-1] + (tc - ts[-1])/(t_new - ts[-1])*(th_new - ths[-1])
                        tab_th = np.array(ths + [thc])
                        tab_G = np.array(Gs + [Gc])
                        unwrapped = np.unwrap(tab_th)
                        winding = (unwrapped[-1] - unwrapped[0])/(2*math.pi)
                        closed = abs(winding) < 0.5
                        return dict(g=unwrapped, G=tab_G, t=tab_t - tab_t[0],
                                    period=float(tab_t[-1] - tab_t[0]),
                                    closed=bool(closed), E=float(E0v), Lp=Lp)
            th, G, t = th_new, G_new, t_new
            ths.append(th); Gs.append(G); ts.append(t)
            if G <= 0.0 or Lp - self.j*G <= 1e-9*Lp:
                return None
        return None

    def replay(self, cyc, times):
        """(gamma(t), G(t)) from the compiled table (exact periodic replay)."""
        T = cyc["period"]
        u = np.mod(times, T)
        i = np.searchsorted(cyc["t"], u) - 1
        i = np.clip(i, 0, len(cyc["t"]) - 2)
        t0, t1 = cyc["t"][i], cyc["t"][i+1]
        frac = (u - t0)/np.maximum(t1 - t0, 1e-300)
        if "gu" not in cyc:
            cyc["gu"] = np.unwrap(cyc["g"])
        g0i, g1i = cyc["gu"][i], cyc["gu"][i+1]
        return g0i + frac*(g1i - g0i), cyc["G"][i] + frac*(cyc["G"][i+1] - cyc["G"][i])

    def state_from_cycle(self, cyc, times):
        g, G = self.replay(cyc, times)
        L1 = cyc["Lp"] - self.j*G
        q = 1.0 - G/L1
        e = np.sqrt(np.maximum(1.0 - q*q, 0.0))
        return np.mod(-g, 2*np.pi), e, L1   # phi = -gamma

def island_halfwidth(j, mu, order=2, e_probe=E0):
    """Half-width in n1 of the libration region of the nf{order} model, by
    bisection on the initial n1 with (phi0, e0) fixed: the largest
    n1 - n1c whose level curve closes (librates)."""
    n1c = (j + 1.0)/j
    nf = NF(j, mu, order)
    def librates(n1):
        m0 = 1.0 - mu
        a1 = (m0/n1/n1)**(1/3.0)
        L1 = math.sqrt(m0*a1)
        G = L1*(1.0 - math.sqrt(1.0 - e_probe*e_probe))
        Lp = L1 + j*G
        g0 = -(j+1)*LAM20
        cyc = nf.compile_cycle(g0, G, Lp)
        return cyc is not None and cyc["closed"]
    w0 = 0.05*math.sqrt(mu)*n1c
    cap = 0.3*n1c
    while librates(n1c + w0) and w0 < cap:
        w0 *= 2
    lo, hi_w = w0/2, min(w0, cap)
    for _ in range(40):
        mid = 0.5*(lo + hi_w)
        if librates(n1c + mid):
            lo = mid
        else:
            hi_w = mid
    return lo

def make_cases(mu_ctl=3e-3):
    cases = []
    for j in (1, 2):
        for mu in (3e-5, 3e-4, 3e-3):
            n1c = (j + 1.0)/j
            hw = island_halfwidth(j, mu)
            m0 = 1.0 - mu
            for tag, sgn in (("m", -1.0), ("0", 0.0), ("p", +1.0)):
                n1 = n1c + sgn*hw/3.0
                a1 = (m0/n1/n1)**(1/3.0)
                cases.append(dict(name=f"{j+1}:{j}-mu{mu:g}-{tag}", j=j, mu=mu,
                                  n1=n1, a1=a1, control=False))
    for ratio in (5.0, 2.55, 2.15):
        n1 = ratio**1.5
        mu = mu_ctl
        m0 = 1.0 - mu
        a1 = (m0/n1/n1)**(1/3.0)
        cases.append(dict(name=f"ctl{ratio:g}", j=1, mu=mu, n1=n1, a1=a1, control=True))
    return cases

def run_length(case):
    n1 = case["n1"]
    return NSYN*2*np.pi/abs(n1 - 1.0)      # n2 = 1

# ------------------------------------------------------------- the truth
def truth_batch(cases, N, out_path):
    """Fixed-step RK4 on the barycentric 3-body problem, all cases at once."""
    nc = len(cases)
    m = np.array([1.0 - c["mu"] for c in cases])
    m2 = np.array([c["mu"] for c in cases])
    mp = np.full(nc, M1_TINY)
    th2 = LAM20
    # star/perturber on a circular mutual orbit, separation 1 (n2 = 1)
    z = np.zeros((nc, 3), dtype=complex)
    v = np.zeros((nc, 3), dtype=complex)
    e2c = complex(math.cos(th2), math.sin(th2))
    t2c = complex(-math.sin(th2), math.cos(th2))
    mtot = m + m2
    z[:, 0] = -(m2/mtot)*e2c
    z[:, 2] = (m/mtot)*e2c
    v[:, 0] = -(m2/mtot)*t2c
    v[:, 2] = (m/mtot)*t2c
    for i, c in enumerate(cases):
        hx, hy, hvx, hvy = helio_vec(c["a1"], E0, 0.0, 0.0, m[i])
        z[i, 1] = complex(hx, hy) + z[i, 0]
        v[i, 1] = complex(hvx, hvy) + v[i, 0]
    masses = np.stack([m, mp, m2], axis=1)          # (nc, 3)
    def accel(z, ms):
        a = np.zeros_like(z)
        for (p, q) in ((0, 1), (0, 2), (1, 2)):
            d = z[:, q] - z[:, p]
            r = np.abs(d)
            fac = d/(r*r*r)
            a[:, p] += ms[:, q]*fac
            a[:, q] -= ms[:, p]*fac
        return a
    def deriv(z, v, ms):
        return v, accel(z, ms)
    h_step = np.array([(2*np.pi/c["n1"])/N for c in cases])
    T_end = np.array([run_length(c) for c in cases])
    n_steps_max = int(np.ceil(np.max(T_end/h_step)))
    sample_every = max(1, int(round(N/16)))
    n_samp = n_steps_max//sample_every + 2
    samp_t = np.zeros((nc, n_samp))
    samp_e = np.zeros((nc, n_samp))
    samp_phi = np.zeros((nc, n_samp))
    samp_a = np.zeros((nc, n_samp))
    t = np.zeros(nc)
    si = np.zeros(nc, dtype=int)
    def sample():
        rx = (z[:, 1] - z[:, 0]).real; ry = (z[:, 1] - z[:, 0]).imag
        vx = (v[:, 1] - v[:, 0]).real; vy = (v[:, 1] - v[:, 0]).imag
        a1, e1, varpi, lam = osc_el(rx, ry, vx, vy, m)
        lam2 = np.mod(th2 + t, 2*np.pi)
        phi = np.mod((cases_jp1)*(lam2) - cases_j*(lam) - varpi, 2*np.pi)
        for i in range(nc):
            if t[i] <= T_end[i] and si[i] < n_samp:
                k = si[i]
                samp_t[i, k] = t[i]; samp_e[i, k] = e1[i]
                samp_phi[i, k] = phi[i]; samp_a[i, k] = a1[i]
                si[i] += 1
    cases_j = np.array([c["j"] for c in cases])
    cases_jp1 = cases_j + 1
    sample()
    for step in range(n_steps_max):
        alive = t + h_step <= T_end + 1e-12
        if not alive.any():
            break
        idx = np.where(alive)[0]
        zs = z[idx]; vs = v[idx]; hs = h_step[idx]
        k1v, k1a = deriv(zs, vs, masses[idx])
        k2v, k2a = deriv(zs + 0.5*hs[:, None]*k1v, vs + 0.5*hs[:, None]*k1a, masses[idx])
        k3v, k3a = deriv(zs + 0.5*hs[:, None]*k2v, vs + 0.5*hs[:, None]*k2a, masses[idx])
        k4v, k4a = deriv(zs + hs[:, None]*k3v, vs + hs[:, None]*k3a, masses[idx])
        z[idx] = zs + hs[:, None]*(k1v + 2*k2v + 2*k3v + k4v)/6.0
        v[idx] = vs + hs[:, None]*(k1a + 2*k2a + 2*k3a + k4a)/6.0
        t[idx] += hs
        if (step + 1) % sample_every == 0:
            sample()
    np.savez_compressed(out_path, names=np.array([c["name"] for c in cases]),
                        t=samp_t, e=samp_e, phi=samp_phi, a=samp_a,
                        counts=si, N=N)
    return None

# ------------------------------------------------------------- negatives
GL8_X = None
def gl8():
    global GL8_X
    if GL8_X is None:
        import numpy.polynomial.legendre as L
        x, w = np.polynomial.legendre.leggauss(8)
        GL8_X = (x, w)
    return GL8_X

def perturbing_accel(r1, th2):
    """Heliocentric perturbing acceleration (direct + indirect) at the
    particle position r1 (complex), perturber circular at angle th2, a2=1."""
    r2 = np.exp(1j*th2)
    d = r2 - r1
    return MU_G*(d/np.abs(d)**3 - r2)

MU_G = None

def run_arc_g8(case):
    """r4 v2's killed configuration: exact Kepler arcs between conjunctions,
    one Gauss-8 kick per window (Gauss planetary equations integrated along
    the unperturbed arc, full direct+indirect acceleration; Gauss-Picard,
    first order)."""
    j = case["j"]; mu = case["mu"]
    m0 = 1.0 - mu; n2 = 1.0
    a, e, varpi = case["a1"], E0, 0.0
    lam10, lam20 = 0.0, LAM20
    n1 = math.sqrt(m0/a**3)
    T_end = run_length(case)
    n_samp = int(T_end*n1*16) + 2
    sample_times = np.linspace(0.0, T_end, n_samp)
    ts, es, phis = [], [], []
    si = 0; evals = 0; wins = 0
    xg, wg = gl8()
    t_win, M0_win = 0.0, lam10 - varpi
    def lam1_at(s):
        return M0_win + n1*(s - t_win) + varpi
    def emit(tt):
        nonlocal si
        while si < n_samp and sample_times[si] <= tt:
            s = sample_times[si]
            lam1 = lam1_at(s)
            ts.append(s); es.append(e)
            phis.append(np.mod((j+1)*(lam20 + n2*s) - j*lam1 - varpi, 2*np.pi))
            si += 1
    t = 0.0
    emit(0.0)
    while t < T_end:
        rate = n1 - n2
        D0 = lam1_at(t) - (lam20 + n2*t)
        m = D0/(2*math.pi)
        frac = (m - math.floor(m)) % 1.0
        if rate > 0:
            dist = (1.0 - frac) % 1.0
        else:
            dist = frac
        if dist < 1e-9:
            dist = 1.0
        dt_win = dist*2*math.pi/abs(rate)
        t_c = min(t + dt_win, T_end)
        nodes = 0.5*(t + t_c) + 0.5*(t_c - t)*xg
        wts = wg*0.5*(t_c - t)
        da = de = dvarpi = 0.0
        for xn, wn in zip(nodes, wts):
            Mn = M0_win + n1*(xn - t_win)
            En = float(kepler_E(np.array([Mn]), e)[0])
            rn = a*(1 - e*math.cos(En))
            fn = 2*math.atan2(math.sqrt(1+e)*math.sin(En/2),
                              math.sqrt(1-e)*math.cos(En/2))
            r1 = rn*complex(math.cos(varpi + fn), math.sin(varpi + fn))
            th2n = lam20 + n2*xn
            r2 = complex(math.cos(th2n), math.sin(th2n))
            d = r2 - r1
            acc = mu*(d/abs(d)**3 - r2)
            rot = complex(math.cos(varpi + fn), -math.sin(varpi + fn))
            ar = (acc*rot).real; at = (acc*rot).imag
            p_ = a*(1 - e*e); h_ = math.sqrt(m0*p_)
            cosE = math.cos(En)
            dadt = 2*a*a/h_*(e*math.sin(fn)*ar + (p_/rn)*at)
            dedt = (math.sin(fn)*ar + (cosE + math.cos(fn))*at)/h_
            dvarpidt = (-math.cos(fn)*ar + (1 + rn/p_)*math.sin(fn)*at)/(h_*max(e, 1e-12))
            da += wn*dadt; de += wn*dedt; dvarpi += wn*dvarpidt
            evals += 1
        emit(t_c)
        lam_c = lam1_at(t_c)
        a += da; e += de; varpi += dvarpi
        n1 = math.sqrt(m0/a**3)
        M0_win, t_win, t = lam_c - varpi, t_c, t_c
        wins += 1
        if e < 0.0 or a <= 0.0:
            break
    return dict(t=np.array(ts), e=np.array(es),
                phi=np.mod(np.array(phis), 2*np.pi),
                wins=wins, evals=evals, orbits=T_end*math.sqrt(m0/case["a1"]**3)/(2*math.pi))

def run_averaged(case, fit):
    """The negative: the full orbit average (resonant angle averaged away),
    as in H0190 K2: one orbit-averaged kick per conjunction window; for the
    circular restricted problem the averaged de = da = 0 and dvarpi/dt is the
    secular precession g_sec = -2 Csec/Lambda1."""
    j = case["j"]; mu = case["mu"]
    m0 = 1.0 - mu; n2 = 1.0
    a1 = case["a1"]; e = E0
    n1 = math.sqrt(m0/a1**3)
    L1 = math.sqrt(m0*a1)
    Csec = float(fit.c(a1)[2])
    g_sec = 2.0*Csec/L1
    T_end = run_length(case)
    n_samp = int(T_end*n1*16) + 2
    ts = np.linspace(0.0, T_end, n_samp)
    gam0 = -(j+1)*LAM20
    gam = gam0 + (j*n1 - (j+1)*n2 + g_sec)*ts
    phis = np.mod(-gam, 2*np.pi)
    wins = int(T_end*abs(n1 - n2)/(2*np.pi)) + 1
    return dict(t=ts, e=np.full_like(ts, e), phi=phis,
                wins=wins, evals=wins, orbits=T_end*n1/(2*math.pi))
