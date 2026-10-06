#!/usr/bin/env python3
"""
schwarztide.py -- Schwarzschild tidal tensor in the parallel-transported tetrad
along equatorial timelike geodesics, in closed form in (E, L, r, M).
Reference for the Fermi-frame phase 2 (gate E9).

Units G=c=1.  Conventions (asserted symbolically in work/derive*.py):
  ds^2 = -f dt^2 + dr^2/f + r^2(dth^2 + sin^2th dph^2),  f = 1-2M/r
  R^r_{s m n} = d_m Gam^r_{n s} - d_n Gam^r_{m s} + Gam^r_{m l}Gam^l_{n s}
                - Gam^r_{n l}Gam^l_{m s}
  geodesic deviation  D^2 xi^mu/dtau^2 = -R^mu_{a n b} u^a xi^n u^b
  tidal tensor C_ab = R_{m a n b} lam0^m lam_a^a lam0^n lam_b^b  (a,b spatial)
so in the parallel frame nearby free bodies obey x'' = -C x  (radial stretch C_rr<0).

Frame (Marck 1983 equatorial construction):
  lam1 = e_theta (parallel along any equatorial geodesic)
  lam2', lam3' = static orthonormal frame boosted along the velocity:
        v-hat = (beta_r, 0, beta_ph),  beta_r = rdot/E, beta_ph = L sqrt(f)/(rE)
        lam2' = v_ph e_r - v_r e_ph,  lam3' = gamma(beta e_t + v-hat), gamma = E/sqrt(f)
  parallel frame = (lam2', lam3') rotated by Phi,  dPhi/dtau = -omega.

Closed forms (m = M/r^3, lam = L^2/r^2, G^2 = E^2 - f, rdot^2 = E^2 - f(1+lam)):
  boosted frame (indices: 0 <-> lam1 = e_theta, 1 <-> lam2', 2 <-> lam3'):
    C11 = m (1 + 3 lam)                          rational in (E^2, L^2, 1/r, M)
    C22 = m - 3 M E^2 L^2/(r^5 G^2)              rational
    C33 = -2 m + 3 M f L^2/(r^5 G^2)             rational
    C23 = -3 M E L rdot/(r^4 G^2)                rational in rdot (odd)
    C12 = C13 = 0
  eigenvalues {m(1+3lam), m, -(2+3lam)m}: independent of E (Xin & Mummery agree)
  rotation (fully rational, work/derive6.py):
    omega = E L M/(r^2 (r E^2 + 2M - r)),   dPhi/dphi = -E M/(r E^2 + 2M - r)
    (at E=1: dPhi/dphi = -1/2 exactly)
  parallel frame: C^P = R(Phi) C^B R(Phi)^T (in-plane 2x2 rotation).

verify.py checks all of this three independent ways and emits vectors.json.
"""
import numpy as np

SQ = np.sqrt

# ---------------------------------------------------------------- closed forms
def closed_scalars(M, E, L, r):
    f = 1.0 - 2.0*M/r
    return f, M/r**3, L*L/(r*r), E*E - f

def rdot2(E, L, r, M):
    return E*E - (1.0 - 2.0*M/r)*(1.0 + L*L/(r*r))

def rdot(E, L, r, M, s=+1):
    return s*SQ(max(rdot2(E, L, r, M), 0.0))

def tide_boosted(M, E, L, r, s=+1):
    """C_ab in the star-tied boosted frame; s = sign(rdot)."""
    f, m, lam, G2 = closed_scalars(M, E, L, r)
    rd = rdot(E, L, r, M, s)
    C11 = m*(1.0 + 3.0*lam)
    C22 = m - 3.0*M*E*E*L*L/(r**5*G2)
    C33 = -2.0*m + 3.0*M*f*L*L/(r**5*G2)
    C23 = -3.0*M*E*L*rd/(r**4*G2)
    return np.array([[C11, 0.0, 0.0], [0.0, C22, C23], [0.0, C23, C33]])

def omega(M, E, L, r):
    """Rotation rate of the boosted frame vs parallel transport (dPhi/dtau = -omega).
       Rational in (E^2, L^2, 1/r, M): omega = E L M / (r^2 (r E^2 + 2M - r)).
       Verified against direct g(grad_u l2', l3') at 3e-13 (work/derive6.py path)."""
    return E*L*M/(r*r*(E*E*r + 2.0*M - r))

def dPhi_dphi(M, E, L, r):
    """dPhi/dphi = -E M/(r E^2 + 2M - r); at E=1 exactly -1/2."""
    return -E*M/(E*E*r + 2.0*M - r)

def tide_parallel(M, E, L, r, Phi, s=+1):
    """C_ab in the parallel frame at angle Phi vs the boosted frame."""
    C = tide_boosted(M, E, L, r, s)
    h = 0.5*(C[1, 1] - C[2, 2])
    c2, s2 = np.cos(2.0*Phi), np.sin(2.0*Phi)
    C22p = -0.5*C[0, 0] + h*c2 + C[1, 2]*s2
    C23p = C[1, 2]*c2 - h*s2
    C33p = -C[0, 0] - C22p
    return np.array([[C[0, 0], 0.0, 0.0], [0.0, C22p, C23p], [0.0, C23p, C33p]])

def eigenvals(M, L, r):
    m, lam = M/r**3, L*L/(r*r)
    return np.array([m*(1.0 + 3.0*lam), m, -m*(2.0 + 3.0*lam)])

# ------------------------------------------------ coordinate Schwarzschild bits
def metric_diag(r, th, M):
    f = 1.0 - 2.0*M/r
    return np.array([-(f), 1.0/f, r*r, r*r*np.sin(th)**2])

def christoffels(r, th, M):
    """Gamma^mu_{ab}, full 4D."""
    f = 1.0 - 2.0*M/r
    s, c = np.sin(th), np.cos(th)
    G = np.zeros((4, 4, 4))
    G[0][0][1] = G[0][1][0] = M/(r*r*f)
    G[1][0][0] = M*f/(r*r)
    G[1][1][1] = -M/(r*r*f)
    G[1][2][2] = -r*f
    G[1][3][3] = -r*f*s*s
    G[2][1][2] = G[2][2][1] = 1.0/r
    G[2][3][3] = -s*c
    G[3][1][3] = G[3][3][1] = 1.0/r
    G[3][2][3] = G[3][3][2] = (c/s if abs(s) > 1e-300 else 0.0)
    return G

def riemann_down(r, M):
    """Full R_{mu a n b} (equatorial) with all symmetries, generated from the six
       static-orthonormal values (verified symbolically in work/derive.py):
       R_thatrhat_thatrhat = -2M/r^3, R_tth = R_tph = M/r^3,
       R_rth = R_rph = -M/r^3, R_thph = 2M/r^3, coframe projection."""
    m = M/r**3
    f = 1.0 - 2.0*M/r
    w = np.array([[np.sqrt(f), 0, 0, 0], [0, 1.0/np.sqrt(f), 0, 0],
                  [0, 0, r, 0], [0, 0, 0, r]])         # orthonormal coframe
    Rhat = np.zeros((4, 4, 4, 4))
    Rhat[0][1][0][1] = -2*m; Rhat[0][2][0][2] = m; Rhat[0][3][0][3] = m
    Rhat[1][2][1][2] = -m; Rhat[1][3][1][3] = -m; Rhat[2][3][2][3] = 2*m
    Rf = np.einsum('abcd,ai,bj,ck,dl->ijkl', Rhat, w, w, w, w)
    # fill remaining symmetry images of the six seed entries
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    v = Rf[a][b][c][d]
                    if v != 0.0:
                        continue
                    if Rf[b][a][c][d] != 0.0:
                        Rf[a][b][c][d] = -Rf[b][a][c][d]
                    elif Rf[a][b][d][c] != 0.0:
                        Rf[a][b][c][d] = -Rf[a][b][d][c]
                    elif Rf[c][d][a][b] != 0.0:
                        Rf[a][b][c][d] = Rf[c][d][a][b]
    return Rf

def C_from_frame(M, r, u, frame):
    """C_ab = R_{m a n b} u^m lam_a^a u^n lam_b^b, coordinate level."""
    Rf = riemann_down(r, M)
    U = np.einsum('m,manb,n->ab', u, Rf, u)
    return np.array([[np.dot(frame[a], U.dot(frame[b])) for b in range(3)]
                     for a in range(3)])

def u_of(E, L, r, M, s=+1):
    f = 1.0 - 2.0*M/r
    return np.array([E/f, rdot(E, L, r, M, s), 0.0, L/(r*r)])

def boosted_frame(E, L, r, M, s=+1):
    """lam1, lam2', lam3' coordinate components (equatorial)."""
    f = 1.0 - 2.0*M/r
    rd = rdot(E, L, r, M, s)
    G = SQ(E*E - f)
    l1 = np.array([0.0, 0.0, 1.0/r, 0.0])
    l2 = np.array([0.0, L*f/(r*G), 0.0, -rd/(r*G)])
    l3 = np.array([G/f, rd*E/G, 0.0, L*E/(r*r*G)])
    return l1, l2, l3

def gdot(a, b, r, M):
    f = 1.0 - 2.0*M/r
    return -f*a[0]*b[0] + (a[1]*b[1])/f + r*r*a[2]*b[2] + r*r*a[3]*b[3]

def gram_schmidt(frame, u, r, M):
    """Re-orthonormalize a transported frame against u (metric-aware)."""
    out = []
    for v in frame:
        w = v.copy()
        w = w + gdot(w, u, r, M)*u   # g(u,u)=-1: this removes the u-part
        for o in out:
            w = w - gdot(w, o, r, M)*o
        w = w/SQ(abs(gdot(w, w, r, M)))
        out.append(w)
    return out

# ------------------------------------------------------------ RK4 machinery
def rk4_step(y, t, h, rhs):
    k1 = rhs(y, t)
    k2 = rhs(y + 0.5*h*k1, t + 0.5*h)
    k3 = rhs(y + 0.5*h*k2, t + 0.5*h)
    k4 = rhs(y + h*k3, t + h)
    return y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def geodesic_rhs(M):
    def rhs(y, t):
        x, v = y[:4], y[4:]
        G = christoffels(x[1], x[2], M)
        return np.concatenate([v, -np.einsum('mab,a,b->m', G, v, v)])
    return rhs

def advance_geodesic(x, v, h, M, n):
    rhs = geodesic_rhs(M)
    y = np.concatenate([x, v])
    hh = h/n
    for i in range(n):
        y = rk4_step(y, i*hh, hh, rhs)
    return y[:4], y[4:]

class Orbit:
    """Equatorial base orbit from (E, L): r(tau), phi(tau) by first-integral RK4.
       s flips automatically at radial turning points."""
    def __init__(self, M, E, L, r0, s=+1):
        self.M, self.E, self.L, self.s = M, E, L, s
        self.state = np.array([r0, 0.0])
    def rhs(self, y, t):
        r = y[0]
        return np.array([rdot(self.E, self.L, r, self.M, self.s), self.L/(r*r)])
    def step(self, h, n=100):
        hh = h/n
        for i in range(n):
            ynew = rk4_step(self.state, i*hh, hh, self.rhs)
            if rdot2(self.E, self.L, ynew[0], self.M) < -1e-9:  # truly crossed a turning point
                self.s *= -1
            self.state = ynew
    @property
    def r(self): return self.state[0]
    @property
    def phi(self): return self.state[1]

def transport(M, E, L, s, r0, phi0, h, n=400, frame0=None):
    """Parallel-transport the frame along the orbit for proper time h.
       Returns (r, phi, s, frame). Re-Gram-Schmidts at every substep."""
    if frame0 is None:
        frame0 = boosted_frame(E, L, r0, M, s)
    y = np.concatenate([[r0, phi0]] + [v for v in frame0])
    st = {'s': s}
    def rhs(yy, t):
        r = yy[0]
        u = u_of(E, L, r, M, st['s'])
        G = christoffels(r, np.pi/2, M)
        out = [u[1], u[3]]
        for k in range(3):
            v = yy[2 + 4*k:6 + 4*k]
            out.extend(-np.einsum('mab,a,b->m', G, u, v))  # dlam/dtau = -Gamma(u,lam)
        return np.array(out)
    hh = h/n
    for i in range(n):
        ytry = rk4_step(y, i*hh, hh, rhs)
        if rdot2(E, L, ytry[0], M) < -1e-9:
            st['s'] *= -1
            y = rk4_step(y, i*hh, hh, rhs)
        else:
            y = ytry
        r = y[0]
        u = u_of(E, L, r, M, st['s'])
        fr = gram_schmidt([y[2 + 4*k:6 + 4*k] for k in range(3)], u, r, M)
        for k in range(3):
            y[2 + 4*k:6 + 4*k] = fr[k]
    fr = [y[2 + 4*k:6 + 4*k] for k in range(3)]
    return y[0], y[1], st['s'], fr

def frame_angle(M, E, L, r, s, frame):
    """Phi = angle of transported frame vs local boosted frame:
       cos Phi = g(lam2, lam2'), sin Phi = g(lam2, lam3')."""
    _, l2p, l3p = boosted_frame(E, L, r, M, s)
    c = gdot(frame[1], l2p, r, M)
    sn = gdot(frame[1], l3p, r, M)
    return np.arctan2(sn, c)
