"""Shared exact-GR instrument (Schwarzschild, G=M=c=1).

Independent of run 20261012-1117's ODE path: the radial cycle phase dphi comes
from the cubic roots of  R(u) = E^2 - (1-2u)(1+L^2 u^2)  and a Gauss-Legendre
quadrature on the root-factored, substitution-smoothed integral (no ODE):
    dphi_cycle = 4/sqrt(2(u3-u_a)) * K(m),  m = (u_p-u_a)/(u3-u_a) < 1,
    K(m) = int_0^{pi/2} dtheta/sqrt(1-m sin^2 theta).
The prior run's ODE solver is copied verbatim below as the cross-check.

Root structure (E<1): three positive roots u_a < u_p < u3 (sum = 1/2, each
< 0.5).  The allowed radial regions are (u_a, u_p) [bound] and (u3, inf)
[plunge: horizon side].  WHICH region a body is in is decided by its position
(region_pair); the sorted pair alone is not enough (at fixed u_p below the
unstable-circular angular momentum L_c = 1/sqrt(u_p(1-3 u_p)) the sorted pair
is an unrelated inner orbit).  Parabolic E=1: roots {0, u_p, u3}.

Conventions (Darwin, from turning points): r_p = p/(1+e), r_a = p/(1-e),
p = 2/(u_p+u_a), e = (u_p-u_a)/(u_p+u_a), separatrix p_crit(e) = 6+2e.
"""
import numpy as np
from scipy.integrate import solve_ivp

_GLN = 200
_xg, _wg = np.polynomial.legendre.leggauss(_GLN)
_th = 0.5 * np.pi * (_xg + 1.0)
_WTH = 0.25 * np.pi * _wg
_SINTH2 = np.sin(_th) ** 2

def roots3(E, L):
    """Roots of 2L^2 u^3 - L^2 u^2 + 2u + (E^2-1) = 0, sorted; nreal = 3 iff
    three distinct real roots (trig method; the discriminant decides)."""
    E = np.atleast_1d(np.asarray(E, float)); L = np.atleast_1d(np.asarray(L, float))
    L2 = L * L
    p = 1.0 / L2 - 1.0 / 12.0
    q = -1.0 / 108.0 + 1.0 / (6.0 * L2) + (E * E - 1.0) / (2.0 * L2)
    disc = -(4.0 * p ** 3 + 27.0 * q * q)
    three = disc > 0.0
    sq = 2.0 * np.sqrt(np.maximum(-p, 0.0) / 3.0)
    with np.errstate(invalid='ignore'):
        arg = np.clip(3.0 * q / (2.0 * p) * np.sqrt(-3.0 / p), -1.0, 1.0)
    th = np.arccos(arg) / 3.0
    roots = np.empty((len(E), 3))
    for j, off in enumerate([0.0, 2.0, 4.0]):
        roots[:, j] = np.where(three, sq * np.cos(th - np.pi * off / 3.0), np.nan)
    roots += 1.0 / 6.0
    roots = np.where(three[:, None], np.sort(roots, axis=1), np.nan)
    return roots, np.where(three, 3, 1)

def bound_pair(E, L):
    """(u_a, u_p, u3): the sorted three-root structure, NaN where it does not
    exist.  Valid as the body's orbit only when the body is in (u_a, u_p)."""
    rr, nreal = roots3(E, L)
    ok = (nreal == 3) & (rr[:, 0] >= -1e-12)
    ua = np.where(ok, np.maximum(rr[:, 0], 0.0), np.nan)
    up = np.where(ok, rr[:, 1], np.nan)
    u3 = np.where(ok, rr[:, 2], np.nan)
    return ua, up, u3

def region_pair(E, L, u_body):
    """Turning points of the allowed region CONTAINING u_body: (u_a, u_p) if
    bound (u_body below the middle root), NaN if in the plunge region."""
    rr, nreal = roots3(E, L)
    ok = (nreal == 3) & (rr[:, 0] >= -1e-12)
    ua = np.maximum(rr[:, 0], 0.0)
    bound = ok & (u_body <= rr[:, 1] + 1e-9)
    return np.where(bound, ua, np.nan), np.where(bound, rr[:, 1], np.nan)

def margin(ua, up):
    p = 2.0 / (up + ua)
    e = (up - ua) / (up + ua)
    return p - 6.0 - 2.0 * e, p, e

def dphi_quad(E, L):
    """Exact radial-cycle phase for a bound (E, L)."""
    ua, up, u3 = bound_pair(E, L)
    m = (up - ua) / (u3 - ua)
    K = np.sum(_WTH / np.sqrt(1.0 - m[:, None] * _SINTH2), axis=1)
    return 4.0 / np.sqrt(2.0 * (u3 - ua)) * K

def seed_from_pe(p, e):
    """Orbit (p, e) -> (u_p, L) (falsifier2's formula); E = E_of(u_p, L)."""
    rp, ra = p / (1 + e), p / (1 - e)
    up_, ua_ = 1.0 / rp, 1.0 / ra
    L2 = ((1 - 2 * ua_) - (1 - 2 * up_)) / ((1 - 2 * up_) * up_ ** 2 - (1 - 2 * ua_) * ua_ ** 2)
    return up_, np.sqrt(L2)

def E_of(up, L):
    return np.sqrt((1 - 2 * up) * (1 + (L * up) ** 2))

def dphi_cycle_ode(u_p, L):
    """falsifier2's ODE path, verbatim (cross-check instrument)."""
    L2 = L * L
    E = np.sqrt((1 - 2 * u_p) * (1 + L2 * u_p * u_p))
    u_pp = 1.0 / L2 + 3 * u_p * u_p - u_p
    eps0 = 1e-6
    y0 = [u_p + 0.5 * u_pp * eps0 * eps0, u_pp * eps0, 0.0]
    def rhs(phi, y):
        u, up, t = y
        return [up, 1.0 / L2 + 3 * u * u - u, E / (L * u * u * (1 - 2 * u))]
    def peri(phi, y): return y[1]
    peri.direction = -1.0; peri.terminal = True
    s = solve_ivp(rhs, [eps0, 200 * np.pi], y0, events=peri, method='DOP853',
                  rtol=1e-11, max_step=0.02, atol=[1e-13, 1e-13, 1e-8])
    assert len(s.t_events[0]), "no periapsis found (plunge?)"
    return s.t_events[0][0] - eps0, s.y[2, -1], E

# ---- local-velocity kick map (static-observer orthonormal frame at radius r)
def kick_E_L(u, vt, vr):
    """Local static-frame velocity components -> Schwarzschild (E, L)."""
    gam = 1.0 / np.sqrt(np.maximum(1.0 - vt * vt - vr * vr, 1e-12))
    E = gam * np.sqrt(1.0 - 2.0 * u)
    L = gam * vt / u
    return E, L

def parabolic_periapsis_state(rp):
    """Parabolic orbit at periapsis: (u, v_t, E, L); v_t = sqrt(2/rp) exactly."""
    u = 1.0 / rp
    vt = np.sqrt(2.0 * u)
    E, L = kick_E_L(u, vt, 0.0)
    return u, vt, E, L

def classify(E, L, u_body, band_hi=0.3):
    """Fates by the allowed region containing u_body:
    0 plunge, 1 band (0 < mu <= band_hi), 2 bound wider, 3 unbound."""
    E = np.atleast_1d(np.asarray(E, float)); L = np.atleast_1d(np.asarray(L, float))
    u_body = np.broadcast_to(np.asarray(u_body, float), E.shape)
    ua, up = region_pair(E, L, u_body)
    mu, p, e = margin(ua, up)
    fate = np.zeros(len(E), dtype=int)                 # default plunge
    fate[E >= 1.0] = 3
    bnd = (E < 1.0) & np.isfinite(ua)
    fate[bnd & (mu > band_hi)] = 2
    fate[bnd & (mu > 0.0) & (mu <= band_hi)] = 1
    return fate, mu, p, e

# ---- fixed-u_p family (tangential kicks at periapsis preserve u_p) ----
def _mu_of_L(up, L):
    E = E_of(up, L)
    ua, upp, u3 = bound_pair(np.array([E]), np.array([L]))
    m, p, e = margin(ua, upp)
    v = float(m[0])
    return v if np.isfinite(v) else -1.0

def _bisect_mu(up, mu_target, L_c, L_par):
    """L in (L_c, L_par) with margin = mu_target.  On this branch margin rises
    from 0+ at the unstable-circular separatrix L_c to mu_max at L_par."""
    Ll = L_c * (1 + 1e-12); Lh = L_par * (1 - 1e-12)
    while _mu_of_L(up, Ll) > mu_target and Ll < L_par * 0.999999:
        Ll = np.sqrt(Ll * L_par)
    for _ in range(400):
        Lm = 0.5 * (Ll + Lh)
        if _mu_of_L(up, Lm) < mu_target: Ll = Lm
        else: Lh = Lm
    return 0.5 * (Ll + Lh)

def build_family(up, n_grid=20001, mu_hi=3.0, mu_lo=5e-3):
    """Grid over L along the periapsis-preserving family (bound branch):
    L in (L(mu_lo), L(mu_hi or mu_max)), with dphi(L) and its derivative.
    L_c = 1/sqrt(u_p(1-3u_p)) is the unstable circular at r_p = 1/u_p: the
    family's separatrix (mu -> 0).  L_par = sqrt(2/(u_p(1-2u_p))) is the
    parabolic member (E=1): mu_max = 2/u_p - 8."""
    L_par = np.sqrt(2.0 / (up * (1 - 2 * up)))
    L_c = 1.0 / np.sqrt(up * (1 - 3 * up))
    L_lo = _bisect_mu(up, mu_lo, L_c, L_par)
    mu_par = _mu_of_L(up, L_par * (1 - 1e-9))
    if np.isfinite(mu_par) and mu_par > mu_hi:
        L_hi = _bisect_mu(up, mu_hi, L_c, L_par)
    else:
        L_hi = L_par * (1 - 1e-9)
    Ls = np.linspace(L_lo, L_hi, n_grid)
    E = E_of(up, Ls)
    ua, upp, u3 = bound_pair(E, Ls)
    mu, p, e = margin(ua, upp)
    dphi = dphi_quad(E, Ls)
    dd = np.gradient(dphi, Ls, edge_order=2)
    assert np.all(np.isfinite(dphi)), "NaN in family grid"
    assert np.all(np.diff(mu) > 0), "mu not monotone on family"
    return dict(L=Ls, mu=mu, dphi=dphi, ddphi=dd, L_sep=L_lo, L_c=L_c,
                L_par=L_par, mu_max=float(mu[-1]), e0=e[0], p0=p[0])
