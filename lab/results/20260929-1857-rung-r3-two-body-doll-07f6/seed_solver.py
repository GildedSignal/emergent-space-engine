"""Analytic patched-conic seed for the resonant figure-eight chain.

Model: the encounter turns the planet-relative velocity v_inf by the hyperbolic angle
delta (tan(delta/2) = mu_p / (b v_inf^2)). The outgoing heliocentric arm is a Kepler
orbit from r = 1 AU with velocity v_planet + v_inf / psi_out. The chain closes iff the
next r = 1 crossing of that orbit meets the planet (timing+place) and the arrival
v_inf direction equals the incoming one. Two residuals in (psi_in, delta) or
(psi_out, delta); solved on a grid, polished by Newton, all in closed-form Kepler.
"""
from math import sqrt, cos, sin, acos, atan2, pi, hypot

MU_S = 4.0 * pi * pi
MU_P = 3.0e-6 * MU_S
OMEGA = sqrt(MU_S)
V_INF = sqrt(MU_S * (2.0 - 2.0 ** (-2.0 / 3.0))) - OMEGA
R_SOI = (3.0e-6) ** 0.4


def kepler_E(M, e):
    E = M if e < 0.8 else pi
    for _ in range(60):
        d = (E - e * sin(E) - M) / (1.0 - e * cos(E))
        E -= d
        if abs(d) < 1e-14:
            break
    return E


def outgoing_arm(psi_out):
    """Kepler orbit from r=1 AU at angle 0 with v = v_planet + v_inf at angle psi_out
    (psi measured from prograde tangential). Returns (a, e_vec, f0, next r=1 crossing
    time and inertial longitude, arrival relative speed and direction)."""
    vx = V_INF * sin(psi_out)
    vy = OMEGA + V_INF * cos(psi_out)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 - v2 / MU_S)
    h = 1.0 * vy            # r x v at (1,0)
    # eccentricity vector: ((v2 - mu/r) r_vec - (r.v) v_vec)/mu with r = (1,0), r.v = vx
    ex = (v2 - MU_S) / MU_S
    ey = -vx * vy / MU_S
    e = hypot(ex, ey)
    if e < 1e-12:
        return None
    # true anomaly of the current point: cos f0 = r.e/e, sin f0 = cross(r,e)/e = e_y/e
    f0 = atan2(ey / e, ex / e)
    varpi = atan2(ey, ex)
    # next r=1 crossing: r = a(1-e^2)/(1+e cos f) = 1
    c = (a * (1.0 - e * e) - 1.0) / e
    if abs(c) > 1.0:
        return None
    fx = acos(c)
    # from f0 moving forward (prograde, df>0): pick the first of +fx, -fx(+2pi) ahead of f0
    cands = sorted([fx % (2 * pi), (-fx) % (2 * pi)])
    fnext = None
    for fcand in cands + [f + 2 * pi for f in cands]:
        if fcand > f0 + 1e-9:
            fnext = fcand
            break
    if fnext is None:
        return None
    # time of flight f0 -> fnext via eccentric anomaly
    def time_at(f):
        E = 2.0 * atan2(sqrt(1.0 - e * e) * sin(f / 2.0), sqrt(1.0 + e * e) * cos(f / 2.0) * (1.0 / 1.0))
        E = 2.0 * atan2(sqrt(1.0 - e) * sin(f / 2.0), sqrt(1.0 + e) * cos(f / 2.0))
        M = E - e * sin(E)
        return M / sqrt(MU_S / a ** 3)
    t_x = time_at(fnext) - time_at(f0)
    lam_x = varpi + fnext        # inertial longitude of the crossing
    # arrival velocity at the crossing
    p_ = a * (1.0 - e * e)
    vf = sqrt(MU_S * (2.0 / 1.0 - 1.0 / a))
    rdot = MU_S / h * e * sin(fnext)
    vfx = rdot * cos(lam_x) - (h / 1.0) * sin(lam_x)
    vfy = rdot * sin(lam_x) + (h / 1.0) * cos(lam_x)
    # planet at t_x: angle OMEGA*t_x, velocity tangential
    pavx = -OMEGA * sin(OMEGA * t_x)
    pavy = OMEGA * cos(OMEGA * t_x)
    wax, way = vfx - pavx, vfy - pavy
    va = hypot(wax, way)
    psi_arr = atan2(wax, way)    # direction relative to planet's velocity
    return a, e, t_x, lam_x, va, psi_arr


def residuals(psi_in, delta, side):
    psi_out = psi_in + side * delta
    arm = outgoing_arm(psi_out)
    if arm is None:
        return None
    a, e, t_x, lam_x, va, psi_arr = arm
    A = (OMEGA * t_x - lam_x + pi) % (2 * pi) - pi   # planet at the crossing?
    B = (psi_arr - psi_in + pi) % (2 * pi) - pi      # arrival direction matches?
    return A, B


def solve():
    best = None
    for side in (1.0, -1.0):
        for i in range(61):
            psi_in = -0.30 + 0.01 * i
            for j in range(40):
                delta = 0.005 + 0.005 * j
                r = residuals(psi_in, delta, side)
                if r is None:
                    continue
                d = abs(r[0]) + abs(r[1])
                if best is None or d < best[0]:
                    best = (d, psi_in, delta, side, r)
    print("best grid:", best)
    return best


if __name__ == "__main__":
    solve()
