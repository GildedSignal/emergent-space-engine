"""Min-norm Newton corrector + tangent continuation for the symmetric 2:1
periodic family of the circular restricted three-body problem.

Unknowns u = (x0, vy0): ship at (x0, 0), velocity (0, vy0) at t = 0, planet at
(1, 0) with velocity (0, 1). Residuals R(u) = (y(2pi), vx(2pi)): perpendicular
recrossing of the line after one planet period = periodic by reflection
symmetry. The solution set is a curve (the family), so the Newton step is the
minimum-norm (Tikhonov) step, and continuation walks along the null-space
tangent of J.
"""
import math

from common import MU_PLANET
from nbary import rk4_step

TWO_PI = 2.0 * math.pi


def integrate(u, h_bg=4e-4, c_enc=150.0):
    x0, vy0 = u
    y = (0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, x0, 0.0, 0.0, vy0)
    t = 0.0
    min_d = 1e9
    while t < TWO_PI - 1e-15:
        d = math.hypot(y[8] - y[4], y[9] - y[5])
        h = min(h_bg, math.sqrt(d ** 3 / MU_PLANET) / c_enc, TWO_PI - t)
        y = rk4_step(y, h)
        t += h
        min_d = min(min_d, math.hypot(y[8] - y[4], y[9] - y[5]))
    return y, min_d


def residual(u):
    y, min_d = integrate(u)
    return (y[9], y[10]), min_d


def solve_pinv(guess, tol=1e-11, iters=40, eps=1e-6):
    u = list(guess)
    for it in range(iters):
        r, _ = residual(u)
        nrm = math.hypot(*r)
        if nrm < tol:
            return u, nrm, it
        J = [[0.0] * 2 for _ in range(2)]
        for j in range(2):
            up = list(u)
            up[j] += eps
            rp, _ = residual(up)
            J[0][j] = (rp[0] - r[0]) / eps
            J[1][j] = (rp[1] - r[1]) / eps
        # minimum-norm step: du = J^T (J J^T + lam I)^-1 (-r)
        a = J[0][0] ** 2 + J[0][1] ** 2
        b = J[0][0] * J[1][0] + J[0][1] * J[1][1]
        c2 = J[1][0] ** 2 + J[1][1] ** 2
        lam = 1e-10 * (a + c2) + 1e-300
        det = (a + lam) * (c2 + lam) - b * b
        w0 = (-r[0] * (c2 + lam) + r[1] * b) / det
        w1 = (-r[1] * (a + lam) - r[0] * b) / det
        du = (J[0][0] * w0 + J[1][0] * w1, J[0][1] * w0 + J[1][1] * w1)
        nrm_du = math.hypot(*du)
        if nrm_du > 0.05:  # trust region
            du = (du[0] * 0.05 / nrm_du, du[1] * 0.05 / nrm_du)
        u = [u[0] + du[0], u[1] + du[1]]
    r, _ = residual(u)
    return u, math.hypot(*r), -3


def tangent(u):
    r, _ = residual(u)
    J = [[0.0] * 2 for _ in range(2)]
    eps = 1e-6
    for j in range(2):
        up = list(u)
        up[j] += eps
        rp, _ = residual(up)
        J[0][j] = (rp[0] - r[0]) / eps
        J[1][j] = (rp[1] - r[1]) / eps
    t = (-J[1][0], J[0][0])  # null vector of the rank-1 J
    n = math.hypot(*t)
    return (t[0] / n, t[1] / n)


def continue_family(u0, s=2e-3, s_min=1e-5, max_pts=4000):
    u, nrm, it = solve_pinv(u0)
    if nrm > 1e-9:
        return None, u, nrm
    # orient the tangent toward increasing apoapsis (smaller min_d)
    t = tangent(u)
    ua, na, _ = solve_pinv([u[0] + s * t[0], u[1] + s * t[1]])
    ub, nb, _ = solve_pinv([u[0] - s * t[0], u[1] - s * t[1]])
    if ua is not None and na < 1e-9:
        _, mda = integrate(ua)
        _, mdb = integrate(ub) if nb < 1e-9 else (None, 1e9)
        if mda < mdb:
            pass
        else:
            t = (-t[0], -t[1])
    prev = u
    pts = [tuple(u)]
    for _ in range(max_pts):
        t = tangent(u)
        guess = [u[0] + s * t[0], u[1] + s * t[1]]
        un, nrm, _ = solve_pinv(guess)
        if nrm > 1e-9:
            s *= 0.5
            if s < s_min:
                break
            continue
        u = un
        pts.append(tuple(u))
    return pts, u, 0.0


if __name__ == "__main__":
    import sys
    from common import R_SOI
    u0 = (0.874564123, 0.836345952)
    pts, uend, _ = continue_family(u0)
    print(f"points: {len(pts) if pts else 0}")
    if pts:
        best = None
        for i in range(0, len(pts), max(1, len(pts) // 30)):
            y, md = integrate(pts[i])
            if best is None or md < best[1]:
                best = (pts[i], md)
        y, mdb = integrate(best[0])
        print(f"closest conjunction on family: x0={best[0][0]:.6f} vy0={best[0][1]:.6f} "
              f"min_d={best[1]:.6f} = {best[1]/R_SOI:.3f} R_SOI")
        print(f"end: x0={pts[-1][0]:.6f} vy0={pts[-1][1]:.6f}")
