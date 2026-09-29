#!/usr/bin/env python3
"""Rung r3 v2: two bodies as one doll, handoffs, gravity assist.

Shared library: faithful port of the repo's 1PN oracle
(xtask/src/gr_oracle_extended.rs: eih_invariants, damour_deruelle,
bound_constants, bound_period_quad integrands, schwarzschild_from_invariants),
the eob-doll, and Newtonian patched-doll machinery (AU, yr, M_sun, G=4pi^2).
"""
import math
import numpy as np

# ---------------------------------------------------------------- oracle port
def eih_EJ(p, e, nu):
    """eih_invariants: harmonic turning radii p,e -> 1PN reduced E, J. Vectorized."""
    p = np.asarray(p, float); e = np.asarray(e, float); nu = np.asarray(nu, float)
    rp = p / (1.0 + e); ra = p / (1.0 - e); j0 = np.sqrt(p)

    def corr(r):
        return (-(1.0 - 3.0 * nu) * j0**4 / (8.0 * r**4)
                - (3.0 + nu) * j0 * j0 / (2.0 * r**3) + 1.0 / (2.0 * r * r))

    # corr(rp)-corr(ra) = -2e(4+2e^2-nu e^2)/p^2 and j0*(1/rp^2-1/ra^2) = -4e sqrt(p)/p^2
    # exactly (binomial identities), giving the stable closed form below; identical to
    # the ratio in eih_invariants, including its e -> 0 limit (which 0/0s there).
    dj = (4.0 + 2.0 * e * e - nu * e * e) / (2.0 * j0)
    vt = (j0 + dj) / rp * (1.0 - 0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) - (3.0 + nu) / rp)
    v2 = vt * vt
    energy = (0.5 * v2 - 1.0 / rp + 0.375 * (1.0 - 3.0 * nu) * v2 * v2
              + 0.5 / rp * ((3.0 + nu) * v2 + 1.0 / rp))
    angular = rp * vt * (1.0 + 0.5 * (1.0 - 3.0 * nu) * v2 + (3.0 + nu) / rp)
    return energy, angular


def damour_deruelle(energy, angular, nu):
    """1PN quasi-Keplerian: (periastron advance, radial period)."""
    q = -2.0 * energy
    n = q**1.5 * (1.0 + q * (-15.0 + nu) / 8.0)
    return 6.0 * np.pi / (angular * angular), 2.0 * np.pi / n


def bound_constants(p, e):
    """Exact Schwarzschild first integrals of the orbit with turning radii p,e."""
    energy = np.sqrt(((p - 2.0)**2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / np.sqrt(p - 3.0 - e * e)
    return energy, angular


_GLN = 512
_c, _w = np.polynomial.legendre.leggauss(_GLN)
CHI = np.pi * (_c + 1.0)          # chi in (0, 2pi)
_W = _w * np.pi


def schw_cycle(pt, et):
    pt = np.atleast_1d(np.asarray(pt, float)); et = np.atleast_1d(np.asarray(et, float))
    E, L = bound_constants(pt, et)
    cs = np.cos(CHI)
    r = pt[..., None] / (1.0 + et[..., None] * cs)
    K = np.sqrt(pt / (pt - 6.0 - 2.0 * et))[..., None] * np.ones_like(cs)
    dphi = np.sum(K * _W, axis=-1)
    Tt = np.sum(K * r * r / L[..., None] * E[..., None] / (1.0 - 2.0 / r) * _W, axis=-1)
    if dphi.ndim == 0:
        return float(dphi), float(Tt)
    return dphi, Tt


def orbit_from_invariants(Eeff, J, p_guess):
    """schwarzschild_from_invariants: (E_eff, J) -> (p_t, e_t). Vectorized Newton."""
    l2 = np.asarray(J)**2
    e2 = Eeff**2
    p = np.array(p_guess, float).copy()
    for _ in range(60):
        f = (l2 + 4.0) / p - 8.0 * l2 / (p * p) + 16.0 * l2 / p**3 - e2
        df = -(l2 + 4.0) / (p * p) + 16.0 * l2 / p**3 - 48.0 * l2 / p**4
        step = f / df
        p = p - step
        if np.max(np.abs(step) / p) < 2e-14:
            break
    return p, np.sqrt(p - 3.0 - p * p / l2)


# ------------------------------------------------------------------- dolls
def doll_binaries(p, e, nu, mode):
    """One config's (periastron advance, radial period).
    eob   : EOB energy map on the exact effective Schwarzschild geodesic.
    test  : nu ignored entirely (invariants at nu=0, no map).
    newton: Kepler motion (advance 2pi exactly, no precession)."""
    if mode == 'newton':
        a = p / (1.0 - e * e)
        return 2.0 * np.pi, 2.0 * np.pi * a**1.5
    if mode == 'eob':
        E, J = eih_EJ(p, e, nu)
        E_bind = E + nu * E * E / 2.0       # effective binding energy; exact round trip of
        Etot = np.sqrt(1.0 + 2.0 * nu * E_bind)   # E_real = sqrt(1+2nu(E_eff-1)) = 1+nu E at 1PN
        Eschw = 1.0 + E_bind                # dimensionless Schwarzschild first integral
    elif mode == 'test':
        E, J = eih_EJ(p, e, 0.0)
        Eschw, Etot = 1.0 + E, 1.0
    else:
        raise ValueError(mode)
    pt, et = orbit_from_invariants(Eschw, J, J * J)
    dphi, Tt = schw_cycle(pt, et)
    return dphi, Tt * Etot


# ------------------------------------------------- Newtonian patched dolls
GM_STAR = 4.0 * np.pi * np.pi
M_PLANET = 3.0e-6
GM_PLANET = GM_STAR * M_PLANET
SOI = 1.0 * M_PLANET**0.4                    # a (m_p/M*)^{2/5}
R_EARTH_AU = 6371.0e3 / 1.495978707e11
PLANET_OMEGA = 2.0 * np.pi                   # circular at 1 AU


def planet_state(t):
    c, s = math.cos(PLANET_OMEGA * t), math.sin(PLANET_OMEGA * t)
    return (c, s), (-s * PLANET_OMEGA, c * PLANET_OMEGA)


def kepler_prop(r0, v0, dt, mu):
    """Universal-variable two-body propagation (scalar states, tuples)."""
    rx, ry = r0; vx, vy = v0
    r0n = math.hypot(rx, ry)
    v2 = vx * vx + vy * vy
    rdotv = rx * vx + ry * vy
    alpha = 2.0 / r0n - v2 / mu               # 1/a
    sqmu = math.sqrt(mu)
    if alpha > 1e-12:
        chi0 = sqmu * abs(dt) * alpha
    else:
        chi0 = sqmu * abs(dt) / r0n
    def CS(z):
        if z > 1e-8:
            sz = math.sqrt(z)
            return (1.0 - math.cos(sz)) / z, (sz - math.sin(sz)) / (z * sz)
        if z < -1e-8:
            sz = math.sqrt(-z)
            return (math.cosh(sz) - 1.0) / (-z), (math.sinh(sz) - sz) / (-z * sz)
        return 0.5 - z / 24.0 + z * z / 720.0, 1.0 / 6.0 - z / 120.0 + z * z / 5040.0

    def Fun(chi):
        C, S = CS(alpha * chi * chi)
        return ((rdotv / sqmu) * chi * chi * C + (1.0 - alpha * r0n) * chi**3 * S
                + r0n * chi - sqmu * dt)

    # safeguarded Newton with a bisection bracket: F is increasing in chi for dt > 0,
    # F(0) = -sqmu dt < 0; plain Newton suffers catastrophic cancellation in dF.
    lo, hi = 0.0, chi0
    while Fun(hi) < 0.0:
        lo = hi
        hi *= 2.0
    chi = hi
    for _ in range(100):
        C, S = CS(alpha * chi * chi)
        F = ((rdotv / sqmu) * chi * chi * C + (1.0 - alpha * r0n) * chi**3 * S
             + r0n * chi - sqmu * dt)
        if F > 0.0:
            hi = chi
        else:
            lo = chi
        dF = (rdotv / sqmu) * chi * (1.0 - alpha * chi * chi * S) \
            + (1.0 - alpha * r0n) * chi * chi * C + r0n
        if 0.0 < dF < float('inf'):
            step = F / dF
            nxt = chi - step
            if not (lo < nxt < hi):
                nxt = 0.5 * (lo + hi)
        else:
            nxt = 0.5 * (lo + hi)
        if abs(nxt - chi) < 1e-14 * max(1.0, abs(chi)):
            chi = nxt
            break
        chi = nxt
    z = alpha * chi * chi
    if z > 1e-8:
        sz = math.sqrt(z)
        C = (1.0 - math.cos(sz)) / z
        S = (sz - math.sin(sz)) / (z * sz)
    elif z < -1e-8:
        sz = math.sqrt(-z)
        C = (math.cosh(sz) - 1.0) / (-z)
        S = (math.sinh(sz) - sz) / (-z * sz)
    else:
        C = 0.5 - z / 24.0 + z * z / 720.0
        S = 1.0 / 6.0 - z / 120.0 + z * z / 5040.0
    f = 1.0 - chi * chi / r0n * C
    g = dt - chi**3 / sqmu * S
    x = f * rx + g * vx
    y = f * ry + g * vy
    rn = math.hypot(x, y)
    fd = sqmu / (rn * r0n) * (alpha * chi**3 * S - chi)
    gd = 1.0 - chi * chi / rn * C
    return (x, y), (fd * rx + gd * vx, fd * ry + gd * vy)


# ------------------------- N-body reference integrator (RK4, adaptive by halving)
def nb_accel(s):
    """s = [x*2, y*2, vx*2, vy*2, x, y, vx, vy] for star, planet, ship (massless).
    Masses 1, m_p, 0. Star+planet+ship mutual gravity."""
    m1, m2 = 1.0, M_PLANET
    x1, y1, x2, y2, x3, y3 = s[0], s[1], s[2], s[3], s[4], s[5]
    dx12, dy12 = x2 - x1, y2 - y1
    d12 = math.sqrt(dx12 * dx12 + dy12 * dy12)
    a = 1.0 / (d12 * d12 * d12)
    dx13, dy13 = x3 - x1, y3 - y1
    d13 = math.sqrt(dx13 * dx13 + dy13 * dy13)
    b = 1.0 / (d13 * d13 * d13)
    dx23, dy23 = x3 - x2, y3 - y2
    d23 = math.sqrt(dx23 * dx23 + dy23 * dy23)
    c = 1.0 / (d23 * d23 * d23)
    G = GM_STAR
    # accelerations
    ax1 = G * (m2 * a * dx12) + G * 0.0
    ay1 = G * (m2 * a * dy12)
    ax2 = -G * m1 * a * dx12
    ay2 = -G * m1 * a * dy12
    ax3 = -G * (m1 * b * dx13 - m2 * c * dx23)
    ay3 = -G * (m1 * b * dy13 - m2 * c * dy23)
    ax2 += G * 0.0
    return (ax1, ay1, ax2, ay2, ax3, ay3)


def nb_deriv(s):
    ax1, ay1, ax2, ay2, ax3, ay3 = nb_accel(s)
    return [s[6], s[7], s[8], s[9], s[10], s[11], ax1, ay1, ax2, ay2, ax3, ay3]


def rk4(s, h):
    k1 = nb_deriv(s)
    s2 = [s[i] + 0.5 * h * k1[i] for i in range(12)]
    k2 = nb_deriv(s2)
    s3 = [s[i] + 0.5 * h * k2[i] for i in range(12)]
    k3 = nb_deriv(s3)
    s4 = [s[i] + h * k3[i] for i in range(12)]
    k4 = nb_deriv(s4)
    return [s[i] + h / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(12)]


def integrate_ship(s0, t_end, tol=1e-9, dtmax=2e-3, events=None):
    """Adaptive RK4 with half-step agreement to tol. Returns final state, list of
    (t, state) at event times, and count of steps."""
    s = list(s0); t = 0.0; dt = dtmax
    nsteps = 0
    ev = []
    while t < t_end - 1e-15:
        if t + dt > t_end:
            dt = t_end - t
        a = rk4(s, dt)
        b = rk4(rk4(s, 0.5 * dt), 0.5 * dt)
        err = max(abs(a[i] - b[i]) for i in range(12))
        if err > tol:
            dt *= 0.5
            continue
        ev_before = events(t, s) if events else None
        s = a; t += dt; nsteps += 1
        if events:
            ev_after = events(t, s)
            if ev_before is not None and ev_after is not None and ev_before != ev_after:
                lo, hi = t - dt, t
                sl = list(s)
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    sm = propagate_to(s, t - dt, mid) if False else None
                    break
                # simple bisection using re-integration is expensive; instead record bracket
                ev.append((t, list(s)))
        if err < tol / 100.0 and dt < dtmax:
            dt *= 1.3
    return s, ev, nsteps
