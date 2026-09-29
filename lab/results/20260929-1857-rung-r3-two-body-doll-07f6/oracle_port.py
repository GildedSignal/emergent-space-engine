"""Faithful pure-Python port of the r3 oracle pieces from xtask/src/gr_oracle.rs and
xtask/src/gr_oracle_extended.rs. Units G = c = M_total = 1 (lengths in GM/c^2) unless noted.
The checker verifies each value against the Rust originals."""
import math
from math import pi as PI

# Frozen coefficients (gr_oracle.rs): calibrated sizes of the 2PN remainder when a 1PN
# quantity is compared with an exact one, or two 1PN methods are compared.
PERIOD_SERIES_REL_COEFF = 300.0   # /p^2
TEST_MASS_1PN_REL_COEFF = 20.0    # /p
EIH_ADVANCE_REL_COEFF = 20.0      # /p
EIH_PERIOD_REL_COEFF = 100.0      # /p^2

_GL_CACHE = {}

def gauss_legendre(n):
    if n in _GL_CACHE:
        return _GL_CACHE[n]
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
    _GL_CACHE[n] = out
    return out

def integrate_gl(lo, hi, pieces, n, f):
    nodes = gauss_legendre(n)
    total = 0.0
    span = (hi - lo) / pieces
    for j in range(pieces):
        a = lo + j * span
        b = a + span
        h = (b - a) * 0.5
        mid = (a + b) * 0.5
        for x, w in nodes:
            total += h * w * f(mid + h * x)
    return total

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
    """Exact Schwarzschild periastron advance (minus 2pi) for Darwin elements (p, e)."""
    d = p - 6.0 + 2.0 * e
    s = math.sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1)

def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

def bound_period_quad(p, e):
    """Exact coordinate-time and proper-time radial periods of the Schwarzschild geodesic
    with Darwin elements (p, e), by Gauss-Legendre quadrature in chi (H0193 refinement)."""
    energy, angular = bound_constants(p, e)

    def refine(f):
        pieces = 16
        v = integrate_gl(0.0, 2.0 * PI, pieces, 32, f)
        while pieces < 1 << 14:
            pieces *= 2
            w = integrate_gl(0.0, 2.0 * PI, pieces, 32, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v

    def f_t(chi):
        c = math.cos(chi)
        r = p / (1.0 + e * c)
        dphi = math.sqrt(p / (p - 6.0 - 2.0 * e * c))
        return dphi * r * r / angular * energy / (1.0 - 2.0 / r)

    def f_tau(chi):
        c = math.cos(chi)
        r = p / (1.0 + e * c)
        return math.sqrt(p / (p - 6.0 - 2.0 * e * c)) * r * r / angular

    return refine(f_t), refine(f_tau)

def eih_invariants(p, e, nu):
    """1PN harmonic-CM reduced energy and angular momentum for an orbit whose harmonic
    radial turning radii are p/(1+e), p/(1-e). Battista & De Falco (2023) eq. (2)."""
    rp = p / (1.0 + e)
    ra = p / (1.0 - e)
    j0 = math.sqrt(p)

    def correction(r):
        return (-(1.0 - 3.0 * nu) * j0 ** 4 / (8.0 * r ** 4)
                - (3.0 + nu) * j0 * j0 / (2.0 * r ** 3)
                + 1.0 / (2.0 * r * r))

    dj = -(correction(rp) - correction(ra)) / (j0 * (1.0 / (rp * rp) - 1.0 / (ra * ra)))
    vt = (j0 + dj) / rp * (1.0 - 0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) - (3.0 + nu) / rp)
    v2 = vt * vt
    energy = (0.5 * v2 - 1.0 / rp
              + 0.375 * (1.0 - 3.0 * nu) * v2 * v2
              + 0.5 / rp * ((3.0 + nu) * v2 + 1.0 / rp))
    angular = rp * vt * (1.0 + 0.5 * (1.0 - 3.0 * nu) * v2 + (3.0 + nu) / rp)
    return rp, vt, energy, angular

def damour_deruelle(energy, angular, nu):
    """1PN Damour-Deruelle periastron advance and radial period from specific reduced
    invariants: 6pi/J^2 and 2pi/n with n = (-2E)^{3/2}(1 + (-2E)(nu-15)/8)."""
    q = -2.0 * energy
    n = q ** 1.5 * (1.0 + q * (-15.0 + nu) / 8.0)
    return 6.0 * PI / (angular * angular), 2.0 * PI / n

def oracle_1pn(p, e, nu):
    """The rung r3 oracle: (periastron advance, radial period) at 1PN for drawn (p, e, nu)."""
    _, _, energy, angular = eih_invariants(p, e, nu)
    return damour_deruelle(energy, angular, nu)

def eih_weak_series(p, e, nu):
    rp = p / (1.0 + e)
    ra = p / (1.0 - e)
    j0 = math.sqrt(p)
    v0 = math.sqrt(p) / rp

    def correction(r):
        return (-(1.0 - 3.0 * nu) * j0 ** 4 / (8.0 * r ** 4)
                - (3.0 + nu) * j0 * j0 / (2.0 * r ** 3)
                + 1.0 / (2.0 * r * r))

    dj = -(correction(rp) - correction(ra)) / (j0 * (1.0 / (rp * rp) - 1.0 / (ra * ra)))
    dv = dj / rp - v0 * (0.5 * (1.0 - 3.0 * nu) * j0 * j0 / (rp * rp) + (3.0 + nu) / rp)
    e0 = 0.5 * v0 * v0 - 1.0 / rp
    e1 = (v0 * dv + 0.375 * (1.0 - 3.0 * nu) * v0 ** 4
          + 0.5 / rp * ((3.0 + nu) * v0 * v0 + 1.0 / rp))
    q0 = -2.0 * e0
    q1 = -2.0 * e1
    newton = 2.0 * PI / q0 ** 1.5
    period = newton * (1.0 - 1.5 * q1 / q0 + q0 * (15.0 - nu) / 8.0)
    return 6.0 * PI / p, newton, period

def _rel(a, b):
    return abs((a - b) / b)

if __name__ == "__main__":
    bad = 0
    for (p, e) in [(20.0, 0.2), (30.0, 0.5), (100.0, 0.2), (1000.0, 0.5), (10000.0, 0.2)]:
        qt, qtau = bound_period_quad(p, e)
        a = p / (1.0 - e * e)
        st = 2.0 * PI * a ** 1.5 * (1.0 + 3.0 / a)
        stau = 2.0 * PI * a ** 1.5 * (1.0 + 1.5 / a)
        pe = periapsis_elliptic(p, e)
        print(f"bound p={p} e={e}: T_quad={qt:.12g} T_series_rel={_rel(st, qt):.2e} "
              f"(band {PERIOD_SERIES_REL_COEFF / p / p:.2e}) adv={pe:.12g}")
        if p >= 100 and not (_rel(st, qt) < PERIOD_SERIES_REL_COEFF / p / p
                             and _rel(stau, qtau) < PERIOD_SERIES_REL_COEFF / p / p):
            bad += 1
    for p in (100.0, 300.0, 1000.0):
        for e in (0.2, 0.5):
            for nu in (0.0, 0.05, 0.1, 0.25):
                _, _, energy, angular = eih_invariants(p, e, nu)
                adv, per = damour_deruelle(energy, angular, nu)
                _, newton, ser = eih_weak_series(p, e, nu)
                td = _rel(ser, per)
                # The weak series keeps only O(1/p) relative to Kepler's law; the repo's
                # EIH band is for the ODE, so this comparison is diagnostic only.
                if nu in (0.0, 0.25):
                    print(f"eih p={p} e={e} nu={nu}: dd_adv={adv:.12g} dd_T={per:.12g} "
                          f"series_T_rel={td:.2e} (diagnostic)")
    # test-mass limit: DD with the exact Schwarzschild invariants vs exact quadrature.
    for (p, e) in [(100.0, 0.2), (1000.0, 0.5), (10000.0, 0.2)]:
        es, l = bound_constants(p, e)
        adv, per = damour_deruelle(es - 1.0, l, 0.0)
        qper, _ = bound_period_quad(p, e)
        print(f"test-mass p={p} e={e}: adv_rel={_rel(adv, periapsis_elliptic(p, e)):.3e} "
              f"(band {TEST_MASS_1PN_REL_COEFF / p:.2e}) per_rel={_rel(per, qper):.3e} "
              f"(band {PERIOD_SERIES_REL_COEFF / p / p:.2e})")
    print("SELFTEST", "OK" if bad == 0 else f"BAD({bad})")
