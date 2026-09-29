"""Rung r3: two bodies as one doll, handoffs, and a gravity assist.

Configs (frozen by the rung):
  eob-doll    relative motion = test body in Schwarzschild M=m1+m2, exact geodesic by
              quadrature; real energy E_real = M*sqrt(1+2*nu*(E_eff-1)) per unit reduced
              mass; handoffs through the sphere of influence with invariants re-expressed.
  test-mass   nu ignored: the lighter body is a test body around a fixed m1.
  newton-doll Kepler motion, no GR.

Units: binaries use G=c=M_total=1 (the oracle's units). The transfer and the flybys use
AU, yr, Msun with the primaries exact (star fixed at the origin, planet on the analytic
circular 1 AU orbit); the reference is a float64 RK4 with step-halving to 1e-9 agreement.
"""
import json
import math
import random
from math import pi, sqrt, hypot, cos, sin, atan2, exp, log

from oracle_port import (bound_constants, bound_period_quad, eih_invariants,
                         damour_deruelle, oracle_1pn, periapsis_elliptic,
                         PERIOD_SERIES_REL_COEFF)

RUN = "lab/results/20260929-1857-rung-r3-two-body-doll-07f6"

# ---------------------------------------------------------------- universe constants
MU_S = 4.0 * pi * pi              # AU^3/yr^2, star = 1 Msun
MU_P = 3.0e-6 * MU_S              # planet = 1 Earth mass
C_AU_YR = 63241.07708807          # speed of light
R_SOI = (3.0e-6) ** 0.4           # sphere of influence, AU
R_PLANET = 6371.0 / 1.495978707e8
OMEGA = sqrt(MU_S)                # planet mean motion (exact circular), = 2pi
# resonant 2:1 transfer speed at 1 AU, tangential: v_inf of the figure-eight encounters
V_INF = sqrt(MU_S * (2.0 - 2.0 ** (-2.0 / 3.0))) - OMEGA

TWO_PI = 2.0 * pi


# ---------------------------------------------------------------- doll propagator
def doll_from_state(mu, gr, x, y, vx, vy):
    """Exact Schwarzschild (or Newtonian if gr=False) invariants and Binet state in a doll
    whose central mass mu is at rest at the origin of this frame."""
    r = hypot(x, y)
    vr = (x * vx + y * vy) / r
    vt = (x * vy - y * vx) / r
    if gr:
        c2 = C_AU_YR * C_AU_YR
        A = 1.0 - 2.0 * mu / (c2 * r)
        u0 = 1.0 / sqrt(A - vr * vr / (c2 * A) - vt * vt / c2)
        E = A * u0
    else:
        A = 1.0
        E = 1.0
        u0 = 1.0
    l = r * vt * u0
    u = 1.0 / r
    phi = atan2(y, x)
    w = -vr * E / (l * A)
    return phi, u, w, E, l


def doll_state_xyv(mu, gr, phi, u, w, E, l):
    """Position and velocity of a propagated doll state."""
    r = 1.0 / u
    if gr:
        c2 = C_AU_YR * C_AU_YR
        A = 1.0 - 2.0 * mu * u / c2
        dphidt = l * u * u * A / E
        vr = -w * l * A / E
    else:
        A = 1.0
        dphidt = l * u * u
        vr = -w * l
    vt = r * dphidt
    cp, sp = cos(phi), sin(phi)
    return r * cp, r * sp, vr * cp - vt * sp, vr * sp + vt * cp


def _deriv(mu, gr, E, l):
    c2 = C_AU_YR * C_AU_YR
    k = 3.0 * mu / c2 if gr else 0.0
    g2 = 2.0 * mu / c2 if gr else 0.0
    mu_l2 = mu / (l * l)

    def f(s):
        u = s[1]
        w = s[2]
        return (1.0, w, mu_l2 - u + k * u * u,
                E / (l * u * u * (1.0 - g2 * u)) if gr else 1.0 / (l * u * u))

    return f


def rk4_step(f, s, h):
    k1 = f(s)
    s2 = [s[i] + 0.5 * h * k1[i] for i in range(4)]
    k2 = f(s2)
    s3 = [s[i] + 0.5 * h * k2[i] for i in range(4)]
    k3 = f(s3)
    s4 = [s[i] + h * k3[i] for i in range(4)]
    k4 = f(s4)
    return [s[i] + h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0 for i in range(4)]


def propagate_doll(mu, gr, E, l, s0, h_phi, event, max_steps, arm=True):
    """Advance the Binet state (phi, u, w, t) in phi until event(state) changes sign from
    its armed value. Returns (steps, state_at_crossing). The first step is taken
    unconditionally so a start exactly on the boundary leaves it before arming."""
    f = _deriv(mu, gr, E, l)
    s = list(s0)
    if l < 0.0:                  # retrograde in this doll: march phi the way time flows
        h_phi = -h_phi
    if arm:
        s = rk4_step(f, s, h_phi)
    g = event(s)
    for i in range(max_steps):
        if s[1] <= 1e-9:      # u collapsed: the trajectory escaped or plunged
            return None
        if gr and s[1] < 0.02:      # r > 50 AU: escape guard
            return None
        s1 = rk4_step(f, s, h_phi)
        g1 = event(s1)
        if g * g1 <= 0.0 and (g != 0.0 or g1 != 0.0):
            lo, hi = 0.0, h_phi
            base = s
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                sm = rk4_step(f, base, mid)
                gm = event(sm)
                if g * gm <= 0.0:
                    hi = mid
                else:
                    lo = mid
            sm = rk4_step(f, base, 0.5 * (lo + hi))
            return i, sm
        s, g = s1, g1
    return None


def planet_pos(t, theta0=0.0):
    a = OMEGA * t + theta0
    return cos(a), sin(a)


def planet_vel(t, theta0=0.0):
    a = OMEGA * t + theta0
    return -OMEGA * sin(a), OMEGA * cos(a)


# ---------------------------------------------------------------- patched-conic chain


def planet_doll_arc(gr, x, y, vx, vy, t0, theta0):
    """Planet doll: the planet's freely falling frame with the exact solar tide
    (star pull on ship minus star pull on planet). Cartesian RK4, small fixed steps,
    exit by event bisection at |r_rel| = R_SOI. Returns (t, x, y, vx, vy) heliocentric.
    gr=False drops the relativistic 3mu u^2 term (newton-doll)."""
    def deriv(t, s):
        rx, ry = s[0], s[1]
        r = hypot(rx, ry)
        k = -MU_P / (r * r * r)
        ax = k * rx
        ay = k * ry
        if gr:
            c2 = C_AU_YR * C_AU_YR
            rr = max(r, 1e-12)
            kgr = -1.5 * MU_P / (c2 * rr * rr * rr * rr)
            ax += kgr * rx * (s[2] * rx + s[3] * ry)
            ay += kgr * ry * (s[2] * rx + s[3] * ry)
        px, py = planet_pos(t, theta0)
        pr = hypot(px, py)
        sx, sy = px + rx, py + ry
        sr = hypot(sx, sy)
        ax += -MU_S * (sx / (sr * sr * sr) - px / (pr * pr * pr))
        ay += -MU_S * (sy / (sr * sr * sr) - py / (pr * pr * pr))
        return (s[2], s[3], ax, ay)

    def rk4s(t, s, h):
        k1 = deriv(t, s)
        s2 = [s[i] + 0.5 * h * k1[i] for i in range(4)]
        k2 = deriv(t + 0.5 * h, s2)
        s3 = [s[i] + 0.5 * h * k2[i] for i in range(4)]
        k3 = deriv(t + 0.5 * h, s3)
        s4 = [s[i] + h * k3[i] for i in range(4)]
        k4 = deriv(t + h, s4)
        return [s[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0 for i in range(4)]

    t = t0
    s = [x, y, vx, vy]
    h = 2.0e-4
    s = rk4s(t, s, h)                       # leave the boundary
    g = hypot(s[0], s[1]) - R_SOI
    for i in range(400000):
        if i % 64 == 0:
            h = min(4.0e-4, 0.05 * max(hypot(s[0], s[1]) / max(hypot(s[2], s[3]), 1e-9), 1e-4))
        s1 = rk4s(t, s, h)
        g1 = hypot(s1[0], s1[1]) - R_SOI
        if g * g1 <= 0.0 and g1 != 0.0:
            lo, hi = 0.0, h
            base = s
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                sm = rk4s(t, base, mid)
                if g * (hypot(sm[0], sm[1]) - R_SOI) <= 0.0:
                    hi = mid
                else:
                    lo = mid
            sm = rk4s(t, base, 0.5 * (lo + hi))
            te = t + 0.5 * (lo + hi)
            px, py = planet_pos(te, theta0)
            pvx, pvy = planet_vel(te, theta0)
            return te, sm[0] + px, sm[1] + py, sm[2] + pvx, sm[3] + pvy
        s, g, t = s1, g1, t + h
    return None


def run_patch(gr, ship0, theta0, max_cross, t_limit=400.0, record=None):
    """Ship0 is an inertial state ON the planet's SOI boundary at t=0, entering the planet
    doll. Runs alternating planet/star dolls until max_cross boundary crossings. Returns
    list of crossings (t, x, y, vx, vy) and appends path points to record if given."""
    t = 0.0
    x, y, vx, vy = ship0
    crossings = []
    in_planet = True
    guard = 0
    while len(crossings) < max_cross and t < t_limit:
        guard += 1
        if guard > 2 * max_cross + 20:
            break
        if in_planet:
            px, py = planet_pos(t, theta0)
            pvx, pvy = planet_vel(t, theta0)
            out = planet_doll_arc(gr, x - px, y - py, vx - pvx, vy - pvy, t, theta0)
            if out is None:
                break
            t, x, y, vx, vy = out
            crossings.append((t, x, y, vx, vy))
            if record is not None:
                record.append((t, x, y))
            in_planet = False
        else:
            phi, u, w, E, l = doll_from_state(MU_S, gr, x, y, vx, vy)

            def ev(s, th0=theta0, E=E, l=l):
                if s[1] <= 1e-12:
                    return 1e9
                sx, sy, _, _ = doll_state_xyv(MU_S, gr, s[0], s[1], s[2], E, l)
                px, py = planet_pos(s[3], th0)
                return hypot(sx - px, sy - py) - R_SOI

            res = propagate_doll(MU_S, gr, E, l, (phi, u, w, t), 0.004, ev, 30000)
            if res is None:
                break
            _, s = res
            t = s[3]
            x, y, vx, vy = doll_state_xyv(MU_S, gr, s[0], s[1], s[2], E, l)
            crossings.append((t, x, y, vx, vy))
            if record is not None:
                record.append((t, x, y))
            in_planet = True
    return crossings

def map_cycle(gr, alpha, vr, vt):
    """One cycle on the smooth perihelion section: an entry state (alpha, vr, vt) on the
    SOI (planet at angle 0) runs the planet doll to its exit, then the star doll to the
    ship's next perihelion. Returns the rotating-frame relative state there. A fixed point
    is a periodic figure-eight: the perihelion state IS the next entry state."""
    ca, sa = cos(alpha), sin(alpha)
    x0 = 1.0 + R_SOI * ca
    y0 = R_SOI * sa
    vrx, vry = vr * ca - vt * sa, vr * sa + vt * ca
    x, y, vx, vy = x0, y0, vrx, vry + OMEGA
    # planet doll: entry to exit
    phi, u, w, E, l = doll_from_state(MU_P, gr, x - 1.0, y, vx - 0.0, vy - OMEGA)
    res = propagate_doll(MU_P, gr, E, l, (phi, u, w, 0.0), 0.0015,
                         lambda s: (1.0 / s[1] if s[1] > 1e-12 else 1e12) - R_SOI,
                         20000)
    if res is None:
        return None
    _, s = res
    t = s[3]
    px, py = planet_pos(t)
    pvx, pvy = planet_vel(t)
    x, y, vx, vy = doll_state_xyv(MU_P, gr, s[0], s[1], s[2], E, l)
    x, y, vx, vy = x + px, y + py, vx + pvx, vy + pvy
    # star doll: exit to the next perihelion (w = du/dphi crosses 0 from below)
    phi, u, w, E, l = doll_from_state(MU_S, gr, x, y, vx, vy)
    res = propagate_doll(MU_S, gr, E, l, (phi, u, w, t), 0.004,
                         lambda s: s[2], 60000)
    if res is None:
        return None
    _, s = res
    t = s[3]
    x, y, vx, vy = doll_state_xyv(MU_S, gr, s[0], s[1], s[2], E, l)
    th = OMEGA * t
    c, s_ = cos(th), sin(th)
    rx, ry = x - planet_pos(t)[0], y - planet_pos(t)[1]
    rx, ry = c * rx + s_ * ry, -s_ * rx + c * ry
    pvx, pvy = planet_vel(t)
    wx, wy = vx - pvx, vy - pvy
    wrx, wry = c * wx + s_ * wy, -s_ * wx + c * wy
    alpha2 = atan2(ry, rx)
    n = hypot(rx, ry)
    vr2 = (wrx * rx + wry * ry) / n
    vt2 = (wrx * (-ry) + wry * rx) / n
    return alpha2, vr2, vt2

def entry_map(gr, alpha, vr, vt):
    """Full cycle: an SOI entry state -> the next SOI entry state, in rotating polar."""
    ca, sa = cos(alpha), sin(alpha)
    ship0 = (1.0 + R_SOI * ca, R_SOI * sa, vr * ca - vt * sa, vr * sa + vt * ca + OMEGA)
    cross = run_patch(gr, ship0, 0.0, 2, t_limit=10.0)
    if len(cross) < 2:
        return None
    t, x, y, vx, vy = cross[1]
    th = OMEGA * t
    c, s = cos(th), sin(th)
    rx, ry = x - planet_pos(t)[0], y - planet_pos(t)[1]
    rx, ry = c * rx + s * ry, -s * rx + c * ry
    pvx, pvy = planet_vel(t)
    wx, wy = vx - pvx, vy - pvy
    wrx, wry = c * wx + s * wy, -s * wx + c * wy
    n = hypot(rx, ry)
    return atan2(ry, rx), (wrx * rx + wry * ry) / n, (wrx * (-ry) + wry * rx) / n

def _kep_ell_state(x, y, vx, vy):
    """Ellipse elements (a, e, varpi, f0, t-epoch-independent mean anomaly M0, n)."""
    r = hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / MU_S)
    rv = x * vx + y * vy
    ex_ = ((v2 - MU_S / r) * x - rv * vx) / MU_S
    ey_ = ((v2 - MU_S / r) * y - rv * vy) / MU_S
    e = hypot(ex_, ey_)
    h = x * vy - y * vx
    varpi = atan2(ey_, ex_)
    f0 = atan2((ex_ * y - ey_ * x) * (1.0 if h > 0 else -1.0) / e,
               (ex_ * x + ey_ * y) / e)
    E0 = 2.0 * atan2(sqrt(1.0 - e) * sin(f0 / 2.0), sqrt(1.0 + e) * cos(f0 / 2.0))
    M0 = E0 - e * sin(E0)
    return a, e, varpi, f0, M0, sqrt(MU_S / a ** 3)


def _kep_time_at_f(a, e, M0, n, f):
    E = 2.0 * atan2(sqrt(1.0 - e) * sin(f / 2.0), sqrt(1.0 + e) * cos(f / 2.0))
    return (E - e * sin(E) - M0) / n


def _kep_state_at_t(a, e, varpi, M0, n, dt):
    M = M0 + n * dt
    E = M
    for _ in range(50):
        d = (E - e * sin(E) - M) / (1.0 - e * cos(E))
        E -= d
        if abs(d) < 1e-14:
            break
    f = 2.0 * atan2(sqrt(1.0 + e) * sin(E / 2.0), sqrt(1.0 - e) * cos(E / 2.0))
    p_ = a * (1.0 - e * e)
    r = p_ / (1.0 + e * cos(f))
    lam = varpi + f
    h = sqrt(MU_S * p_)
    rdot = MU_S / h * e * sin(f)
    vfx = rdot * cos(lam) - (h / r) * sin(lam)
    vfy = rdot * sin(lam) + (h / r) * cos(lam)
    return r * cos(lam), r * sin(lam), vfx, vfy


def hybrid_residuals(gr, psi_in, vinf, d_off, side=1.0):
    """Smooth r=1-crossing residuals with the REAL planet-doll encounter and an analytic
    Kepler star arm. The entry state is the inbound hyperbola state at r = R_SOI with
    asymptotic speed vinf, impact parameter d_off (in R_SOI) and direction psi_in:
    A = the planet meets the ship's next r=1 crossing, B = the arrival direction
    (planet-local) equals the incoming one."""
    mu = MU_P
    b = R_SOI * d_off
    e_h = sqrt(1.0 + (b * vinf * vinf / mu) ** 2)
    h_orb = b * vinf
    p_orb = h_orb * h_orb / mu
    c = (p_orb / R_SOI - 1.0) / e_h
    if abs(c) >= 1.0:
        return None
    f_r = atan2(sqrt(max(0.0, 1.0 - c * c)), c)      # anomaly where r = R_SOI
    f_inf = atan2(sqrt(max(0.0, e_h * e_h - 1.0)), -1.0)  # arccos(-1/e_h)
    th_in = pi / 2.0 - psi_in                        # cartesian angle of the asymptote
    e_p_ang = th_in + pi + side * f_inf              # periapsis direction (cartesian)
    pos_ang = e_p_ang - side * f_r                   # inbound branch of the hyperbola
    rhat = (cos(pos_ang), sin(pos_ang))
    that = (-side * rhat[1], side * rhat[0])
    f = -side * f_r
    vr_ = mu / h_orb * e_h * sin(f)
    vt_ = mu / h_orb * (1.0 + e_h * cos(f))
    relx = R_SOI * rhat[0]
    rely = R_SOI * rhat[1]
    relvx = vr_ * rhat[0] + vt_ * that[0]
    relvy = vr_ * rhat[1] + vt_ * that[1]
    x0, y0 = 1.0 + relx, rely
    vx0, vy0 = relvx, relvy + OMEGA
    out = planet_doll_arc(gr, relx, rely, relvx, relvy, 0.0, 0.0)
    if out is None:
        return None
    t_e, x, y, vx, vy = out
    a, e, varpi, f0, M0, n = _kep_ell_state(x, y, vx, vy)
    if a <= 0 or e < 1e-6:
        return None
    p_ = a * (1.0 - e * e)
    c = (p_ - 1.0) / e
    if abs(c) >= 1.0:
        return None
    fx = atan2(sqrt(max(0.0, 1.0 - c * c)), c)
    cands = sorted([fx % TWO_PI, (-fx) % TWO_PI])
    fnext = None
    for fc in cands + [f + TWO_PI for f in cands] + [f + 2 * TWO_PI for f in cands]:
        if _kep_time_at_f(a, e, M0, n, fc) > 0.25:
            fnext = fc
            break
    if fnext is None:
        return None
    t_x = _kep_time_at_f(a, e, M0, n, fnext)
    lam_x = varpi + fnext
    sx, sy, svx, svy = _kep_state_at_t(a, e, varpi, M0, n, t_x)
    th = OMEGA * t_x
    wax = svx + OMEGA * sin(th)
    way = svy - OMEGA * cos(th)
    tx_, ty_ = -sin(th), cos(th)
    psi_arr = atan2(wax * cos(th) + way * sin(th), wax * tx_ + way * ty_)
    A = (th - lam_x + pi) % TWO_PI - pi
    B = (psi_arr - psi_in + pi) % TWO_PI - pi
    return A, B, (x0, y0, vx0, vy0), t_x


def ref_cycle_min(ship0, tmax=3.6):
    """Reference RK4 from t=0; rotating-frame polar state at the closest approach to the
    planet after t > 0.3 yr. Always defined and smooth in the initial state."""
    grid = [0.002 * (i + 1) for i in range(int(tmax / 0.002))]
    out = reference_run(list(ship0), tmax, grid)
    best = None
    for t, s in out:
        if t < 0.3:
            continue
        px, py = planet_pos(t)
        d = hypot(s[0] - px, s[1] - py)
        if best is None or d < best[0]:
            best = (d, t, s)
    if best is None:
        return None
    d0, t0, s0 = best

    def dat(tt):
        res = reference_run(list(s0), tt, [tt], tol=1e-12, t_start=t0)
        s_ = res[-1][1]
        px, py = planet_pos(tt)
        return hypot(s_[0] - px, s_[1] - py), s_

    lo, hi = t0, t0 + 0.004
    for _ in range(40):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        d1, _ = dat(m1)
        d2, _ = dat(m2)
        if d1 < d2:
            hi = m2
        else:
            lo = m1
    t = 0.5 * (lo + hi)
    d, s_ = dat(t)
    px, py = planet_pos(t)
    th = OMEGA * t
    c, sn = cos(th), sin(th)
    rx, ry = s_[0] - px, s_[1] - py
    rx, ry = c * rx + sn * ry, -sn * rx + c * ry
    pvx, pvy = planet_vel(t)
    wx, wy = s_[2] - pvx, s_[3] - pvy
    wrx, wry = c * wx + sn * wy, -sn * wx + c * wy
    n = hypot(rx, ry)
    return d, atan2(ry, rx), (wrx * rx + wry * ry) / n, (wrx * (-ry) + wry * rx) / n


def close_figure_eight(gr, verbose=True):
    """Shoot the periodic figure-eight on the always-smooth reference map: unknowns are
    the rotating-frame SOI entry state (alpha, vr, vt); residuals compare the closest
    approach of the following cycle with it. The candidate then runs the same state."""
    def fres(x):
        ca, sa = cos(x[0]), sin(x[0])
        ship0 = (1.0 + R_SOI * ca, R_SOI * sa,
                 x[1] * ca - x[2] * sa, x[1] * sa + x[2] * ca + OMEGA)
        out = ref_cycle_min(ship0)
        if out is None:
            return None
        d, a_m, vr_m, vt_m = out
        da = (a_m - x[0] + pi) % TWO_PI - pi
        return [d - R_SOI, da, vt_m - x[2]]

    def nm(F):
        return abs(F[0]) + abs(F[1]) + abs(F[2]) if F else float("inf")

    best = None
    for a0 in (-0.8, -0.4, -0.1, 0.2, 0.6):
        for r0 in (-0.5, -0.2):
            for t0 in (0.8, 1.2, 1.6):
                F = fres([a0, r0, t0])
                if F is not None and (best is None or nm(F) < nm(best[0])):
                    best = (F, [a0, r0, t0])
    if best is None:
        return None
    F, x = best
    for it in range(60):
        fn = nm(F)
        if verbose:
            print(f"  shoot {it}: x=({x[0]:+.6f},{x[1]:+.6f},{x[2]:+.6f}) |F|={fn:.2e}")
        if fn < 1e-11:
            return x
        J = [[0.0] * 3 for _ in range(3)]
        ok = True
        for j in range(3):
            xp = list(x)
            xp[j] += 1e-6
            Fp = fres(xp)
            if Fp is None:
                ok = False
                break
            for i in range(3):
                J[i][j] = (Fp[i] - F[i]) / 1e-6
        if not ok:
            return None
        M_ = [J[i][:] + [-F[i]] for i in range(3)]
        for col in range(3):
            piv = max(range(col, 3), key=lambda rr: abs(M_[rr][col]))
            M_[col], M_[piv] = M_[piv], M_[col]
            pv = M_[col][col]
            if abs(pv) < 1e-14:
                return None
            for rr in range(3):
                if rr != col and M_[rr][col] != 0.0:
                    fac = M_[rr][col] / pv
                    M_[rr] = [M_[rr][k] - fac * M_[col][k] for k in range(4)]
        dx = [M_[i][3] / M_[i][i] for i in range(3)]
        cap = max(abs(dd) for dd in dx)
        if cap > 0.4:
            dx = [0.4 * dd / cap for dd in dx]
        moved = False
        for k in range(16):
            damp = 0.5 ** k
            xn = [x[i] + damp * dx[i] for i in range(3)]
            Fn = fres(xn)
            if Fn is not None and nm(Fn) < fn:
                x, F, moved = xn, Fn, True
                break
        if not moved:
            return None
    return None


# ---------------------------------------------------------------- N-body reference
def _accel(t, s):
    x, y, vx, vy = s
    r = hypot(x, y)
    ax = -MU_S * x / (r * r * r)
    px, py = planet_pos(t)
    dx, dy = x - px, y - py
    d = hypot(dx, dy)
    k = -MU_P / (d * d * d)
    return (vx, vy, ax + k * dx, k * dy)


def _rk4_ref(t, s, h):
    k1 = _accel(t, s)
    s2 = [s[i] + 0.5 * h * k1[i] for i in range(4)]
    k2 = _accel(t + 0.5 * h, s2)
    s3 = [s[i] + 0.5 * h * k2[i] for i in range(4)]
    k3 = _accel(t + 0.5 * h, s3)
    s4 = [s[i] + h * k3[i] for i in range(4)]
    k4 = _accel(t + h, s4)
    return [s[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0
            for i in range(4)]


def reference_run(s0, t_end, sample_times, tol=1e-9, t_start=0.0):
    """Adaptive RK4 (step vs two half steps agreeing to tol). Returns states at
    sample_times (sorted, absolute), using clipped steps to land exactly on each."""
    samples = sorted(sample_times)
    out = []
    t = t_start
    s = list(s0)
    h = 0.01
    si = 0
    guard = 0
    while t < t_end - 1e-12 and guard < 4_000_000:
        guard += 1
        if si < len(samples) and t + h > samples[si]:
            h = samples[si] - t
            if h <= 0:
                si += 1
                continue
            s = _rk4_ref(t, s, h)
            t += h
            out.append((t, s))
            si += 1
            h = 0.005
            continue
        y1 = _rk4_ref(t, s, h)
        y2 = _rk4_ref(t, _rk4_ref(t, s, 0.5 * h), 0.5 * h)
        err = max(abs(y1[i] - y2[i]) / (1.0 + abs(s[i])) for i in range(4))
        if err > tol:
            h *= 0.5
            continue
        s = y2
        t += h
        h = min(2.0 * h, 0.02) if err > 0.0 else h
    return out


def helio_energy(s):
    x, y, vx, vy = s
    r = hypot(x, y)
    return 0.5 * (vx * vx + vy * vy) - MU_S / r


# ---------------------------------------------------------------- sampler
def sample():
    rng = random.Random(20261002)
    binaries = []
    for _ in range(256):
        p = exp(rng.uniform(log(20.0), log(1000.0)))
        e = rng.uniform(0.0, 0.6)
        nu = rng.uniform(0.01, 0.25)
        binaries.append((p, e, nu))
    flybys = []
    for _ in range(64):
        b = exp(rng.uniform(log(1.5), log(50.0)))     # planet radii
        side = 1.0 if rng.random() < 0.5 else -1.0
        theta0 = TWO_PI * rng.random()
        alpha0 = TWO_PI * rng.random()
        flybys.append((b, side, theta0, alpha0))
    return binaries, flybys


# ---------------------------------------------------------------- binaries
def binary_metrics(cfg, binaries, diag):
    prec_pass = prec_n = per_pass = per_incl = per_excl = nu_pass = nu_n = 0
    for (p, e, nu) in binaries:
        adv_o, T_o = oracle_1pn(p, e, nu)
        _, T_o0 = oracle_1pn(p, e, 0.0)
        if cfg == "eob-doll":
            adv_c = periapsis_elliptic(p, e)
            E_eff, _ = bound_constants(p, e)
            T_eff, _ = bound_period_quad(p, e)
            f = sqrt(1.0 + 2.0 * nu * (E_eff - 1.0))
            T_c = f * T_eff
            T_c0 = T_eff
        elif cfg == "test-mass":
            m1 = 0.5 * (1.0 + sqrt(1.0 - 4.0 * nu))
            p1 = p / m1
            adv_c = periapsis_elliptic(p1, e)
            T_c, _ = bound_period_quad(p1, e)
            T_c0 = T_eff = bound_period_quad(p, e)[0]
        else:  # newton-doll
            adv_c = 0.0
            a = p / (1.0 - e * e)
            T_c = TWO_PI * a ** 1.5
            T_c0 = T_c
        if abs((adv_c - adv_o) / adv_o) <= 0.01:
            prec_pass += 1
        prec_n += 1
        est = PERIOD_SERIES_REL_COEFF / (p * p)      # oracle truncation, frozen calibration
        if est > 5e-4:
            per_excl += 1
        else:
            per_incl += 1
            if abs((T_c - T_o) / T_o) <= 1e-3:
                per_pass += 1
        if nu >= 0.05:
            c_c = (T_c / T_c0 - 1.0) / nu
            c_o = (T_o / T_o0 - 1.0) / nu
            if c_c * c_o > 0.0 and abs(c_c - c_o) <= 0.1 * abs(c_o):
                nu_pass += 1
            nu_n += 1
    d = diag.setdefault(cfg, {})
    d["prec_pass"] = prec_pass
    d["period_included"] = per_incl
    d["period_excluded"] = per_excl
    d["period_pass_of_included"] = per_pass
    d["nu_cases"] = nu_n
    d["nu_pass"] = nu_pass
    return {
        "precession_pass_fraction": prec_pass / prec_n,
        "period_pass_fraction": (per_pass / per_incl) if per_incl else 0.0,
        "nu_effect_pass_fraction": (nu_pass / nu_n) if nu_n else 0.0,
    }


# ---------------------------------------------------------------- assists
def flyby_states(b_Rp, side, theta0, alpha0):
    v_hyp = sqrt(V_INF * V_INF + 2.0 * MU_P / R_SOI)
    beta = math.asin(min(1.0, b_Rp * R_PLANET * V_INF / (R_SOI * v_hyp)))
    ca, sa = cos(alpha0), sin(alpha0)
    px, py = planet_pos(0.0, theta0)
    x0 = px + R_SOI * ca
    y0 = py + R_SOI * sa
    vrx = v_hyp * (-cos(beta) * ca - side * sin(beta) * sa)
    vry = v_hyp * (-cos(beta) * sa + side * sin(beta) * ca)
    pvx, pvy = planet_vel(0.0, theta0)
    return (x0, y0, vrx + pvx, vry + pvy)


def assist_metrics(gr, flybys, diag, results):
    t_end = 0.02
    npass = 0
    for (b, side, theta0, alpha0) in flybys:
        s0 = flyby_states(b, side, theta0, alpha0)
        # candidate: planet doll to SOI exit, then star doll to exactly t_end
        x, y, vx, vy = s0
        out = planet_doll_arc(gr, x - planet_pos(0.0, theta0)[0],
                              y - planet_pos(0.0, theta0)[1],
                              vx - planet_vel(0.0, theta0)[0],
                              vy - planet_vel(0.0, theta0)[1], 0.0, theta0)
        if out is None:
            continue
        t, x, y, vx, vy = out
        phi, u, w, E, l = doll_from_state(MU_S, gr, x, y, vx, vy)
        res = propagate_doll(MU_S, gr, E, l, (phi, u, w, t), 0.004,
                             lambda s: s[3] - t_end, 20000)
        _, s = res
        xv, yv, vxc, vyc = doll_state_xyv(MU_S, gr, s[0], s[1], s[2], E, l)
        dvx, dvy = vxc - s0[2], vyc - s0[3]
        # reference
        ref = reference_run(list(s0), t_end, [t_end])
        _, sref = ref[0]
        dvxr, dvyr = sref[2] - s0[2], sref[3] - s0[3]
        mag_c, mag_r = hypot(dvx, dvy), hypot(dvxr, dvyr)
        cosang = (dvx * dvxr + dvy * dvyr) / (mag_c * mag_r)
        ang = math.acos(max(-1.0, min(1.0, cosang)))
        ok = abs(mag_c - mag_r) / mag_r <= 0.01 and ang <= 0.01
        npass += 1 if ok else 0
        results.append((b, mag_c, mag_r, ang, ok))
    return npass / len(flybys)


# ---------------------------------------------------------------- transfer
def transfer_metrics(gr, diag, store):
    x = close_figure_eight(gr)
    if x is None:
        return None
    alpha, vr, vt = x
    ca, sa = cos(alpha), sin(alpha)
    ship0 = (1.0 + R_SOI * ca, R_SOI * sa,
             vr * ca - vt * sa, vr * sa + vt * ca + OMEGA)
    path = []
    cross = run_patch(gr, ship0, 0.0, 100, t_limit=400.0, record=path)
    diag["transfer_crossings_candidate"] = len(cross)
    t_end = (cross[-1][0] + 0.5) if len(cross) >= 100 else 8.0
    grid = [t_end * (i + 1) / 300.0 for i in range(300)]
    ref = reference_run(list(ship0), t_end, sorted(set([c[0] for c in cross] + grid)))
    refmap = {t: s for t, s in ref}
    errs = []
    for i, (t, x_, y_, vx_, vy_) in enumerate(cross):
        sref = None
        for tt, ss in ref:
            if abs(tt - t) < 1e-9:
                sref = ss
                break
        if sref is None:
            continue
        errs.append((i + 1, abs(helio_energy((x_, y_, vx_, vy_)) - helio_energy(sref))))
    n = len(errs)
    if n >= 10:
        lx = [log(i) for i, _ in errs]
        ly = [log(d) for _, d in errs]
        mx, my = sum(lx) / n, sum(ly) / n
        sxx = sum((a - mx) ** 2 for a in lx)
        slope = sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sxx
    else:
        slope = 99.0      # the chained transfer does not exist in this doll: no fit
    store["ship0"] = ship0
    store["path"] = path
    store["cross"] = cross
    store["ref"] = ref
    store["errs"] = errs
    store["fixed_point"] = x
    return slope


# ---------------------------------------------------------------- main
def main():
    binaries, flybys = sample()
    diag = {}
    metrics = {}
    assist_results = []
    for cfg in ("eob-doll", "test-mass", "newton-doll"):
        print(f"== {cfg}")
        m = binary_metrics(cfg, binaries, diag)
        gr = cfg != "newton-doll"
        m["assist_pass_fraction"] = assist_metrics(gr, flybys, diag, assist_results if cfg == "eob-doll" else [])
        store = {}
        slope = transfer_metrics(gr, diag if cfg == "eob-doll" else {}, store)
        m["handoff_energy_growth_exponent"] = slope if slope is not None else 99.0
        m["events_per_orbit"] = 0.0     # binaries: one doll, solved by quadrature
        metrics[cfg] = m
        print(f"   {json.dumps(m)}")
        d = diag.get(cfg, {})
        print(f"   diag: {d}")
        if cfg == "eob-doll":
            json.dump({"ship0": store.get("ship0"),
                       "fixed_point": store.get("fixed_point"),
                       "path": store.get("path"),
                       "cross": store.get("cross"),
                       "ref": store.get("ref"),
                       "errs": store.get("errs"),
                       "assist": assist_results},
                      open(f"{RUN}/transfer_data.json", "w"))
    with open(f"{RUN}/metrics.json", "w") as fh:
        json.dump(metrics, fh, indent=1)
    print("metrics.json written")


if __name__ == "__main__":
    main()
