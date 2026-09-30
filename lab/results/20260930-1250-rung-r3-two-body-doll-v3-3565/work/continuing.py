"""Arc-length continuation of the symmetric 2:1 periodic family, CR3BP
formulation (star fixed, planet exact circle, ship test particle), with an
inlined RK4 stepper for speed. Walks from the distant branch toward
apoapsis-at-conjunction (SOI-crossing members).
"""
import math
import sys

MU = 3.0e-6
TWO_PI = 2.0 * math.pi


def integrate(u, h_bg=1e-3, c_enc=150.0):
    """u = (x0, vy0); returns (y, vx, min_d) after one planet period."""
    x, y = u[0], 0.0
    vx, vy = 0.0, u[1]
    t = 0.0
    min_d = 1e9
    sqrt = math.sqrt
    while t < TWO_PI - 1e-15:
        px, py = math.cos(t), math.sin(t)
        d = sqrt((x - px) ** 2 + (y - py) ** 2)
        h = h_bg
        tau = sqrt(d ** 3 / MU)
        if tau / c_enc < h:
            h = tau / c_enc
        if t + h > TWO_PI:
            h = TWO_PI - t

        def acc(xx, yy, tt):
            r = sqrt(xx * xx + yy * yy)
            ppx, ppy = math.cos(tt), math.sin(tt)
            dd = sqrt((xx - ppx) ** 2 + (yy - ppy) ** 2)
            return (-xx / (r * r * r) - MU * (xx - ppx) / (dd * dd * dd),
                    -yy / (r * r * r) - MU * (yy - ppy) / (dd * dd * dd))

        k1x, k1y = vx, vy
        a1x, a1y = acc(x, y, t)
        k2x, k2y = vx + 0.5 * h * a1x, vy + 0.5 * h * a1y
        a2x, a2y = acc(x + 0.5 * h * k1x, y + 0.5 * h * k1y, t + 0.5 * h)
        k3x, k3y = vx + 0.5 * h * a2x, vy + 0.5 * h * a2y
        a3x, a3y = acc(x + 0.5 * h * k2x, y + 0.5 * h * k2y, t + 0.5 * h)
        k4x, k4y = vx + h * a3x, vy + h * a3y
        a4x, a4y = acc(x + h * k3x, y + h * k3y, t + h)
        x += h * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0
        y += h * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
        vx += h * (a1x + 2 * a2x + 2 * a3x + a4x) / 6.0
        vy += h * (a1y + 2 * a2y + 2 * a3y + a4y) / 6.0
        t += h
        dd = sqrt((x - math.cos(t)) ** 2 + (y - math.sin(t)) ** 2)
        if dd < min_d:
            min_d = dd
    return y, vx, min_d


def residual(u):
    y, vx, min_d = integrate(u)
    return (y, vx), min_d


def solve_pinv(guess, tol=1e-11, iters=80, eps=1e-6, cap=0.01):
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
        a, b, c, d = J[0][0], J[0][1], J[1][0], J[1][1]
        aa = a * a + b * b
        bb = a * c + b * d
        cc = c * c + d * d
        lam = 1e-9 * (aa + cc) + 1e-300
        det = (aa + lam) * (cc + lam) - bb * bb
        w0 = (-r[0] * (cc + lam) + r[1] * bb) / det
        w1 = (-r[1] * (aa + lam) - r[0] * bb) / det
        du = (a * w0 + c * w1, b * w0 + d * w1)
        nd = math.hypot(*du)
        if nd > cap:
            du = (du[0] * cap / nd, du[1] * cap / nd)
        # line search
        lam_ls = 1.0
        for _ in range(10):
            un = [u[0] + lam_ls * du[0], u[1] + lam_ls * du[1]]
            rn, _ = residual(un)
            if math.hypot(*rn) < nrm:
                u = un
                break
            lam_ls *= 0.5
        else:
            return u, nrm, -2
    r, _ = residual(u)
    return u, math.hypot(*r), -3


def main():
    from common import R_SOI
    u = [0.874564123, 0.836345952]
    u, nrm, _ = solve_pinv(u)
    print(f"base: {u} |r|={nrm:.1e}", flush=True)
    pts = [tuple(u)]
    s = 5e-3
    for step in range(5000):
        # tangent from last two family points
        if len(pts) >= 2:
            tx, ty = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
            n = math.hypot(tx, ty) or 1.0
            tx, ty = tx / n, ty / n
        else:
            tx, ty = 1.0, 0.0
        while True:
            guess = [u[0] + s * tx, u[1] + s * ty]
            un, nrm, it = solve_pinv(guess, iters=60)
            if nrm < 1e-10:
                u = un
                break
            s *= 0.5
            if s < 1e-6:
                print("stalled", flush=True)
                return
            if step % 1 == 0:
                pass
        pts.append(tuple(u))
        _, _, md = integrate(u)
        if len(pts) % 10 == 0:
            print(f"pt {len(pts)}: x0={u[0]:.6f} vy0={u[1]:.6f} min_d={md:.5f} "
                  f"({md/R_SOI:.2f} R_SOI) s={s:.1e}", flush=True)
        if md < 0.4 * R_SOI:
            print("deep enough", flush=True)
            break
    import json
    json.dump(pts, open("family.json", "w"))


if __name__ == "__main__":
    main()
