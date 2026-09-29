import numpy as np
"""Ported GR oracle for rung r1. Faithful ports of xtask/src/gr_oracle.rs (ellip_k,
ellip_k_minus_half_pi, periapsis_elliptic, gauss_legendre, deflection_quadrature) and
xtask/src/gr_oracle_extended.rs (null_turning_radius, bound_constants, bound_period_quad,
integrate_gl). Units G = c = M = 1. Self-checks against the frozen series and RK4.
"""
import math

PI = math.pi


def ellip_k(m):
    a, g = 1.0, math.sqrt(1.0 - m)
    for _ in range(40):
        a1, g1 = (a + g) / 2.0, math.sqrt(a * g)
        if abs(a1 - g1) <= 1e-17 * a1:
            a = a1
            break
        a, g = a1, g1
    return PI / (2.0 * a)


def ellip_k_minus_half_pi(m):
    if m >= 0.25:
        return ellip_k(m) - PI / 2.0
    c, mn, s = 1.0, 1.0, 0.0
    for n in range(1, 200):
        c *= (2 * n - 1) / (2 * n)
        mn *= m
        term = c * c * mn
        s += term
        if term < 1e-19 * s:
            break
    return PI / 2.0 * s


def periapsis_elliptic(p, e):
    """Periapsis-to-periapsis angle minus 2π for bound orbit (p, e)."""
    d = p - 6.0 + 2.0 * e
    s = math.sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1)


def gauss_legendre(n):
    out = []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        dp = 0.0
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p2 = ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
                p0, p1 = p1, p2
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out


_GL_CACHE = {}


def gl(n):
    if n not in _GL_CACHE:
        _GL_CACHE[n] = gauss_legendre(n)
    xs = [t[0] for t in _GL_CACHE[n]]
    ws = [t[1] for t in _GL_CACHE[n]]
    return xs, ws


def integrate_gl_scalar(lo, hi, pieces, n, f):
    xs, ws = gl(n)
    sum_ = 0.0
    for j in range(pieces):
        a = lo + (hi - lo) * j / pieces
        b = lo + (hi - lo) * (j + 1) / pieces
        for x, w in zip(xs, ws):
            sum_ += (b - a) * 0.5 * w * f((a + b) * 0.5 + (b - a) * 0.5 * x)
    return sum_


def deflection_quadrature(b):
    """Total light deflection from infinity: 2*int_0^{u0} du/sqrt(1/b^2 - u^2 + 2u^3) - pi."""
    u0 = 1.0 / b
    for _ in range(100):
        h = 2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b)
        dh = 6.0 * u0 * u0 - 2.0 * u0
        step = h / dh
        u0 -= step
        if abs(step) <= 1e-17 * u0:
            break
    xs, ws = gl(32)
    pieces = 64
    total = 0.0
    for j in range(pieces):
        a, c = j / pieces, (j + 1) / pieces
        for x, w in zip(xs, ws):
            s = (a + c) / 2.0 + (c - a) / 2.0 * x
            u = u0 * (1.0 - s * s)
            qf, r = u0 + u, 2.0 * (u * u + u * u0 + u0 * u0)
            q = qf - r
            total += w * (c - a) / 2.0 * 4.0 * math.sqrt(u0) * r / (
                math.sqrt(q * qf) * (math.sqrt(qf) + math.sqrt(q)))
    return total


def null_turning_radius(b):
    r = b - 1.0
    for _ in range(40):
        f = r * r / (1.0 - 2.0 / r) - b * b
        df = 2.0 * r * r * (r - 3.0) / (r - 2.0) ** 2
        step = f / df
        r -= step
        if abs(step) < 2e-15 * r:
            break
    return r


def bound_constants(p, e):
    energy = np.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / np.sqrt(p - 3.0 - e * e)
    return energy, angular


def bound_period_quad(p, e, pieces=1024):
    """(T_t, T_tau) radial period. Darwin chi quadrature, converged piece count."""
    energy, angular = bound_constants(p, e)
    xs, ws = gl(32)
    def refine(f):
        pc = 16
        v = integrate_gl_scalar(0.0, 2.0 * PI, pc, 32, f)
        while pc < 1 << 14:
            pc *= 2
            w = integrate_gl_scalar(0.0, 2.0 * PI, pc, 32, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v
    t = refine(lambda chi: math.sqrt(p / (p - 6.0 - 2.0 * e * math.cos(chi)))
               * (p / (1.0 + e * math.cos(chi))) ** 2 / angular
               * energy / (1.0 - 2.0 * (1.0 + e * math.cos(chi)) / p))
    tau = refine(lambda chi: math.sqrt(p / (p - 6.0 - 2.0 * e * math.cos(chi)))
                 * (p / (1.0 + e * math.cos(chi))) ** 2 / angular)
    return t, tau


def light_tail(b, u_s, pieces=8, n=32):
    """int_0^{u_s} du/sqrt(1/b^2 - u^2 + 2u^3): the exact bending beyond r=1/u_s, per side."""
    return integrate_gl_scalar(0.0, u_s, pieces, n,
                               lambda u: 1.0 / math.sqrt(1.0 / (b * b) - u * u + 2.0 * u * u * u))


# ---------------- independent cross-checks (series + RK4), not used by configs ----------
def _check():
    rows = []
    for (p, e) in [(20.0, 0.5), (100.0, 0.2), (1000.0, 0.7), (10.0, 0.0), (7.9, 0.7)]:
        adv = periapsis_elliptic(p, e)
        series = 6 * PI / p * (1 + (18 + e * e) / (4 * p))
        # RK4 on u'' + u = 1/L^2 + 3u^2
        inv_l2 = (p - 3.0 - e * e) / (p * p)
        f = lambda u: inv_l2 + 3.0 * u * u - u
        h = 1e-4
        u, v, phi = (1.0 + e) / p, 0.0, 0.0
        seen = False
        rk = float('nan')
        for _ in range(int(20 * PI / h)):
            k1u, k1v = v, f(u)
            k2u, k2v = v + h / 2 * k1v, f(u + h / 2 * k1u)
            k3u, k3v = v + h / 2 * k2v, f(u + h / 2 * k2u)
            k4u, k4v = v + h * k3v, f(u + h * k3u)
            u1 = u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
            v1 = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            if v1 > 0:
                seen = True
            if seen and v > 0 and v1 <= 0:
                lo, hi = 0.0, h
                for _ in range(80):
                    mid = 0.5 * (lo + hi)
                    # re-step from (u,v) by mid
                    a1, a2 = v, f(u)
                    b1, b2 = v + mid / 2 * a2, f(u + mid / 2 * a1)
                    c1, c2 = v + mid / 2 * b2, f(u + mid / 2 * b1)
                    d1, d2 = v + mid * c2, f(u + mid * c1)
                    vv = v + mid / 6 * (a2 + 2 * b2 + 2 * c2 + d2)
                    if vv > 0:
                        lo = mid
                    else:
                        hi = mid
                rk = phi + 0.5 * (lo + hi) - 2 * PI
                break
            u, v, phi = u1, v1, phi + h
        rows.append((p, e, adv, series, rk))
    for (p, e, adv, series, rk) in rows:
        rel_s = abs(adv - series) / abs(adv)
        rel_r = abs(adv - rk) / abs(rk)
        print(f"periapsis p={p:7.1f} e={e:.2f} elliptic={adv:.12g} series={series:.12g} "
              f"rk4={rk:.12g} rel(series)={rel_s:.2e} rel(rk4)={rel_r:.2e}")
    for b in (10.0, 100.0, 1000.0):
        dq = deflection_quadrature(b)
        series = 4.0 / b + 15 * PI / (4 * b * b)
        print(f"deflection b={b:7.1f} quad={dq:.12g} series={series:.12g} rel={abs(dq-series)/dq:.2e}")
    for (p, e) in [(20.0, 0.5), (100.0, 0.2), (1000.0, 0.5)]:
        t, tau = bound_period_quad(p, e)
        a = p / (1 - e * e)
        newton = 2 * PI * a ** 1.5
        print(f"period p={p:7.1f} e={e:.2f} T_t={t:.12g} series(1+3/a)={newton*(1+3/a):.12g} "
              f"rel={abs(t-newton*(1+3/a))/t:.2e}")
    print("tail b=100 u_s=1e-4:", light_tail(100.0, 1e-4), "flat:", 100.0 * 1e-4)


if __name__ == "__main__":
    _check()
