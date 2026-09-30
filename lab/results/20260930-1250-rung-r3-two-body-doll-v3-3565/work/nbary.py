"""N-body reference (adaptive RK4) and the patched-doll law for handoffs/assists.

Units: GM_star = 1, planet GM = 3e-6, planet on a 1 AU orbit (a = 1, e = 0).
The planet's GR content at these scales is ~1e-9 of the dynamics (GM/(r c^2)
with c ~ 1e4 velocity units), so the dolls' Schwarzschild geodesics are the
Kepler conics to far below every tolerance here; the handoff mechanics is what
runs.

Reference: star + planet mutually attracting (float64), ship a test body.
Law: star doll (Kepler, star fixed at the doll centre) and planet doll (Kepler
in the planet's free-falling frame), handoff exactly at the sphere-of-influence
boundary |r_ship - r_planet| = R_SOI = a (m/M)^(2/5), the state re-expressed in
the new doll's frame at each crossing. The planet's own position is derived
from its star-doll tube (exact circle), never stepped.
"""
import math

from common import MU_PLANET, R_SOI


# ----------------------------------------------------------------- reference
def deriv(y):
    xs, ys, vxs, vys, xp, yp, vxp, vyp, xh, yh, vxh, vyh = y
    dxps, dyps = xp - xs, yp - ys
    dps = math.sqrt(dxps * dxps + dyps * dyps)
    acc_s = -MU_PLANET / (dps * dps * dps)
    ax_s, ay_s = acc_s * dxps, acc_s * dyps
    ax_p, ay_p = -dxps / (dps * dps * dps), -dyps / (dps * dps * dps)
    dxhs, dyhs = xh - xs, yh - ys
    dhs = math.sqrt(dxhs * dxhs + dyhs * dyhs)
    dxhp, dyhp = xh - xp, yh - yp
    dhp = math.sqrt(dxhp * dxhp + dyhp * dyhp)
    ax_h = -dxhs / (dhs * dhs * dhs) - MU_PLANET * dxhp / (dhp * dhp * dhp)
    ay_h = -dyhs / (dhs * dhs * dhs) - MU_PLANET * dyhp / (dhp * dhp * dhp)
    return (vxs, vys, ax_s, ay_s, vxp, vyp, ax_p, ay_p, vxh, vyh, ax_h, ay_h)


def rk4_step(y, h):
    k1 = deriv(y)
    k2 = deriv(tuple(y[i] + 0.5 * h * k1[i] for i in range(12)))
    k3 = deriv(tuple(y[i] + 0.5 * h * k2[i] for i in range(12)))
    k4 = deriv(tuple(y[i] + h * k3[i] for i in range(12)))
    return tuple(y[i] + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0
                 for i in range(12))


def run_reference(y0, t_end, targets=(), h_bg=0.001, c_enc=250.0):
    """Adaptive RK4; lands exactly on each target time. Returns (y, samples)."""
    y = tuple(y0)
    t = 0.0
    tg = sorted(targets)
    samples = []
    hit = 0
    while t < t_end - 1e-15:
        dhp = math.hypot(y[8] - y[4], y[9] - y[5])
        h = min(h_bg, math.sqrt(dhp * dhp * dhp / MU_PLANET) / c_enc, t_end - t)
        if hit < len(tg) and t + h > tg[hit]:
            h = tg[hit] - t
            y = rk4_step(y, h)
            t = tg[hit]
            samples.append((t, y))
            hit += 1
            continue
        y = rk4_step(y, h)
        t += h
    return y, samples


def helio_state(y):
    return ((y[8] - y[0], y[9] - y[1]), (y[10] - y[2], y[11] - y[3]))


def helio_energy(y):
    (rx, ry), (vx, vy) = helio_state(y)
    return 0.5 * (vx * vx + vy * vy) - 1.0 / math.hypot(rx, ry)


# -------------------------------------------------- Kepler (universal vars)
def _stumpff(z):
    if z > 1e-8:
        sz = math.sqrt(z)
        return (1.0 - math.cos(sz)) / z, (sz - math.sin(sz)) / (sz * sz * sz)
    if z < -1e-8:
        sz = min(math.sqrt(-z), 700.0)  # e^700 ~ 1e304: no overflow, asymptotic
        return (1.0 - math.cosh(sz)) / z, (math.sinh(sz) - sz) / (sz ** 3)
    return 0.5 - z / 24.0 + z * z / 720.0, 1.0 / 6.0 - z / 120.0 + z * z / 5040.0


def kepler_propagate(rvec, vvec, mu, dt):
    """Universal-variable Kepler propagation; Newton to machine precision."""
    if dt == 0.0:
        return rvec, vvec
    rx, ry = rvec
    vx, vy = vvec
    r0 = math.hypot(rx, ry)
    vr0 = (rx * vx + ry * vy) / r0
    alpha = 2.0 / r0 - (vx * vx + vy * vy) / mu
    sqmu = math.sqrt(mu)
    if alpha > 0.0:
        X = sqmu * dt * alpha
    else:
        X = math.asinh(math.sqrt(-alpha) * sqmu * dt) / math.sqrt(-alpha)
    for _ in range(100):
        z = alpha * X * X
        C, S = _stumpff(z)
        F = ((r0 * vr0 / sqmu) * X * X * C + (1.0 - r0 * alpha) * X ** 3 * S
             + r0 * X - sqmu * dt)
        dF = ((r0 * vr0 / sqmu) * X * (1.0 - z * S)
              + (1.0 - r0 * alpha) * X * X * C + r0)
        step = F / dF
        step = max(-1e4, min(1e4, step))
        X -= step
        if abs(step) < 1e-13 * max(1.0, abs(X)):
            break
    z = alpha * X * X
    C, S = _stumpff(z)
    f = 1.0 - X * X / r0 * C
    g = dt - X ** 3 / sqmu * S
    rxn = f * rx + g * vx
    ryn = f * ry + g * vy
    rn = math.hypot(rxn, ryn)
    fd = math.sqrt(mu) / (rn * r0) * X * (z * S - 1.0)
    gd = 1.0 - X * X / rn * C
    return (rxn, ryn), (fd * rx + gd * vx, fd * ry + gd * vy)


def planet_state(t):
    """Planet's star-doll tube: exact 1 AU circle, planet at angle t."""
    return (math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))


def law_ship(t0, rvec, vvec, in_planet, t):
    """Heliocentric ship state at time t, from the doll state at t0."""
    dt = t - t0
    if in_planet:
        rr, vv = kepler_propagate(rvec, vvec, MU_PLANET, dt)
        p, pv = planet_state(t)
        return (p[0] + rr[0], p[1] + rr[1]), (pv[0] + vv[0], pv[1] + vv[1])
    return kepler_propagate(rvec, vvec, 1.0, dt)


def run_law_transfer(r0, v0, n_cross=100, win=0.02, sample_dt=0.05, nudge=1e-4,
                     t_max=400.0):
    """Patched-doll propagation. Returns (crossings, path, t_final).

    crossings: (t, E_helio, entering) at each SOI boundary event. law_ship
    always returns the heliocentric state; the re-expression into the new
    doll subtracts the planet's own star-doll state, then the nudge step runs
    in the new doll's frame.
    """
    t = 0.0
    rvec, vvec = r0, v0  # heliocentric while in the star doll
    p0, pv0 = planet_state(0.0)
    in_planet = math.hypot(r0[0] - p0[0], r0[1] - p0[1]) < R_SOI
    if in_planet:
        rvec = (r0[0] - p0[0], r0[1] - p0[1])
        vvec = (v0[0] - pv0[0], v0[1] - pv0[1])
    crossings = []
    path = [(0.0, r0[0], r0[1], 0.0)]
    t_sample = 0.0

    def rel_sep(tt):
        rs, _ = law_ship(t, rvec, vvec, in_planet, tt)
        p, _ = planet_state(tt)
        return math.hypot(rs[0] - p[0], rs[1] - p[1])

    while len(crossings) < n_cross and t < t_max:
        t_next = t + win
        g0 = rel_sep(t) - R_SOI
        g1 = rel_sep(t_next) - R_SOI
        if (g0 > 0) != (g1 > 0):
            lo, hi = t, t_next
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                if ((rel_sep(mid) - R_SOI) > 0) != (g0 > 0):
                    hi = mid
                else:
                    lo = mid
            tc = 0.5 * (lo + hi)
            rs, vs = law_ship(t, rvec, vvec, in_planet, tc)
            E = 0.5 * (vs[0] ** 2 + vs[1] ** 2) - 1.0 / math.hypot(rs[0], rs[1])
            entering = not in_planet
            crossings.append((tc, E, entering))
            if entering:
                p, pv = planet_state(tc)
                r_rel = (rs[0] - p[0], rs[1] - p[1])
                v_rel = (vs[0] - pv[0], vs[1] - pv[1])
                in_planet = True
                rvec, vvec = kepler_propagate(r_rel, v_rel, MU_PLANET, nudge)
            else:
                in_planet = False
                rvec, vvec = kepler_propagate(rs, vs, 1.0, nudge)
            t = tc + nudge
            path.append((t, rs[0], rs[1], t))
            t_sample = t
        else:
            if in_planet:
                rvec, vvec = kepler_propagate(rvec, vvec, MU_PLANET, t_next - t)
            else:
                rvec, vvec = kepler_propagate(rvec, vvec, 1.0, t_next - t)
            t = t_next
            if t >= t_sample + sample_dt:
                rs, _ = law_ship(t, rvec, vvec, in_planet, t)
                path.append((t, rs[0], rs[1], t))
                t_sample = t
    return crossings, path, t
