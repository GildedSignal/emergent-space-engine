#!/usr/bin/env python3
"""Cross-check of the B19 oracle (kerr.rs) at 40 digits, written independently of it.

    uv run --with mpmath python xtask/src/behave/kerr_mpmath.py > xtask/src/behave/kerr_mp.json

Everything is derived from the Kerr metric itself, equatorial Boyer-Lindquist (G = c = M = 1), never from the closed
forms that kerr.rs uses (BPT's ISCO, photon orbit and circular-orbit formulas, Glampedakis-Kennefick's (E, L), the
radial polynomial):
  - R(r) = r⁴ṙ² = r²Δ(−μ² − g^{AB}p_A p_B) from the inverse of the (t, φ) block, p_t = −E, p_φ = L;
  - circular orbits from Ω = ±1/(r^{3/2} ± a), u^t from the normalisation, E, L by lowering; the ISCO is the minimum of
    E_circ(r), the photon orbit the zero of u^t⁻², the marginally bound orbit E_circ = 1, b = L/E from the photon orbit's
    direction; (E, L) of a bound orbit by Newton's method on R(r_p) = R(r_a) = 0 (seeded by a float closed form,
    which only decides the starting point), the separatrix by a double root R = R' = 0 at r_p;
  - cycles by Gauss-Legendre quadrature in Darwin's ψ of dφ, dt and dτ = (dr/dψ)·r²/√R, light's deflection from
    the turning point by Gauss-Legendre in t with r = r0/(1 − t²);
  - the ZAMO from the ADM split, the tubes' rates from the inverse metric, the Penrose split by projecting p onto
    the two null directions of the ZAMO frame and lowering the fragments with the metric.
The script also asserts that the textbook formulas agree with these (the polynomial R, BPT's ISCO).
Each case carries its arguments as doubles (kerr.rs reads exactly the same doubles) and the value to 35 digits.
"""
import json
import math
import sys

from mpmath import mp, mpf, sqrt, cos, sin, acos, findroot, quad, diff, pi

mp.dps = 40
CHI = ["0.5", "0.9", "0.998"]


# ---- the metric ----------------------------------------------------------------------------------------------------
def metric(a, r):
    return -(1 - 2 / r), -2 * a / r, r * r + a * a + 2 * a * a / r  # g_tt, g_tφ, g_φφ


def inverse_block(a, r):
    gtt, gtp, gpp = metric(a, r)
    d = gtt * gpp - gtp * gtp
    return gpp / d, -gtp / d, gtt / d  # g^tt, g^tφ, g^φφ


def delta(a, r):
    return r * r - 2 * r + a * a


def radial(a, e, l, r, mu2=1):
    """R(r) = r⁴ṙ² from the metric."""
    itt, itp, ipp = inverse_block(a, r)
    q = itt * e * e - 2 * itp * e * l + ipp * l * l
    return r * r * delta(a, r) * (-mu2 - q)


def radial_poly(a, e, l, r):
    """Chandrasekhar's polynomial form, only for the Newton derivative of the separatrix (asserted equal to `radial`)."""
    return (e * e - 1) * r**4 + 2 * r**3 + (a * a * (e * e - 1) - l * l) * r**2 + 2 * (l - a * e) ** 2 * r


def radial_poly_d(a, e, l, r):
    return 4 * (e * e - 1) * r**3 + 6 * r**2 + 2 * (a * a * (e * e - 1) - l * l) * r + 2 * (l - a * e) ** 2


def rates(a, e, l, r):
    """(dt/dτ, dφ/dτ) from the inverse metric."""
    itt, itp, ipp = inverse_block(a, r)
    return -itt * e + itp * l, -itp * e + ipp * l


# ---- circular orbits, from the metric --------------------------------------------------------------------------------
def omega(a, r, s):
    return s / (r * sqrt(r) + s * a)


def circular(a, r, s):
    gtt, gtp, gpp = metric(a, r)
    w = omega(a, r, s)
    ut = 1 / sqrt(-(gtt + 2 * gtp * w + gpp * w * w))
    return -(gtt + gtp * w) * ut, (gtp + gpp * w) * ut


def float_bpt(a, s):
    """Float seeds only (the roots below are found independently)."""
    a = float(a)
    z1 = 1 + (1 - a * a) ** (1 / 3) * ((1 + a) ** (1 / 3) + (1 - a) ** (1 / 3))
    z2 = math.sqrt(3 * a * a + z1 * z1)
    isco = 3 + z2 - s * math.sqrt((3 - z1) * (3 + z1 + 2 * z2))
    ph = 2 * (1 + math.cos(2 / 3 * math.acos(-s * a)))
    mb = 2 - s * a + 2 * math.sqrt(1 - s * a)
    return isco, ph, mb


def isco(a, s):
    guess = float_bpt(a, s)[0]
    return findroot(lambda r: diff(lambda rr: circular(a, rr, s)[0], r), mpf(guess), tol=mpf(10) ** -33)


def photon_orbit(a, s):
    def f(r):
        gtt, gtp, gpp = metric(a, r)
        w = omega(a, r, s)
        return gtt + 2 * gtp * w + gpp * w * w

    return findroot(f, mpf(float_bpt(a, s)[1]), tol=mpf(10) ** -33)


def photon_b(a, s):
    r = photon_orbit(a, s)
    gtt, gtp, gpp = metric(a, r)
    w = omega(a, r, s)
    return (gtp + gpp * w) / (-(gtt + gtp * w))


def marginally_bound(a, s):
    r = findroot(lambda rr: circular(a, rr, s)[0] - 1, mpf(float_bpt(a, s)[2]), tol=mpf(10) ** -33)
    return r, circular(a, r, s)[1]


# ---- bound orbits -------------------------------------------------------------------------------------------------------
def float_bound(a, p, e, s):
    """Float closed form (a quadratic in x² = (L − aE)²): the seed for Newton's method, nothing more."""
    a, p, e = float(a), float(p), float(e)
    ua, up = (1 - e) / p, (1 + e) / p
    al0, al1 = p - a * a, ((3 + e * e) - p) / p
    c0 = 1 - 2 * ua + a * a * ua * ua + al0 * ua * ua
    c1 = ua * ua + al1 * ua * ua - 2 * ua**3
    f, n, c = al1 * al1 - 4 * a * a * c1, 2 * al0 * al1 - 4 * a * a * c0, al0 * al0
    disc = n * n - 4 * f * c
    if disc < 0 or f == 0:
        return None
    q = -0.5 * (n + math.copysign(math.sqrt(disc), n))
    best = None
    for y in (q / f, c / q if q != 0 else float("nan")):
        big_a = al0 + al1 * y
        if not y > 0 or big_a == 0:
            continue
        x = math.copysign(math.sqrt(y), big_a)
        en = big_a / (2 * a * x)
        if not (0 < en < 1 and (x + a * en) * s > 0):
            continue
        if best is None or (y < best[0] if s > 0 else y > best[0]):
            best = (y, x, en)
    if best is None:
        return None
    _, x, en = best
    l = x + a * en
    uc = (a * a + x * x + 2 * a * x * en) / (2 * x * x) - 2 / p
    stable = 0 < en < 1 and l * s > 0 and uc > up and p / (1 + e) > 1 + math.sqrt(1 - a * a)
    return (en, l, stable)


def float_separatrix(a, e, s):
    p = 400.0
    while True:
        lo = p / 1.02
        r = float_bound(a, lo, e, s)
        if r is None or not r[2]:
            break
        p = lo
    hi = p
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        r = float_bound(a, mid, e, s)
        if r is not None and r[2]:
            hi = mid
        else:
            lo = mid
    return hi


def bound_constants(a, p, e, s):
    p, e = mpf(p), mpf(e)
    rp, ra = p / (1 + e), p / (1 - e)
    seed = float_bound(a, p, e, s)
    assert seed is not None and seed[2], f"no stable orbit at p = {p} e = {e} s = {s}"
    sol = findroot(lambda en, l: (radial(a, en, l, rp), radial(a, en, l, ra)), (mpf(seed[0]), mpf(seed[1])), tol=mpf(10) ** -60, maxsteps=60)
    return sol[0], sol[1]


def separatrix(a, e, s):
    e = mpf(e)
    ps = float_separatrix(a, float(e), s)
    seed = float_bound(a, ps * 1.0000001, float(e), s)

    def f(en, l, p):
        rp, ra = p / (1 + e), p / (1 - e)
        return radial(a, en, l, rp), radial_poly_d(a, en, l, rp), radial(a, en, l, ra)

    sol = findroot(f, (mpf(seed[0]), mpf(seed[1]), mpf(ps)), tol=mpf(10) ** -50, maxsteps=100)
    return sol[2]


def cycle(a, p, e, s):
    p, e = mpf(p), mpf(e)
    en, l = bound_constants(a, p, e, s)

    def parts(psi):
        r = p / (1 + e * cos(psi))
        drdpsi = p * e * sin(psi) / (1 + e * cos(psi)) ** 2
        dtau = drdpsi * r * r / sqrt(radial(a, en, l, r))
        tdot, pdot = rates(a, en, l, r)
        return pdot * dtau, tdot * dtau, dtau

    kw = dict(method="gauss-legendre", maxdegree=9)
    dphi = 2 * quad(lambda x: parts(x)[0], [0, pi], **kw)
    t = 2 * quad(lambda x: parts(x)[1], [0, pi], **kw)
    tau = 2 * quad(lambda x: parts(x)[2], [0, pi], **kw)
    return abs(dphi) - 2 * pi, t, tau


# ---- light --------------------------------------------------------------------------------------------------------------
def deflection(a, b):
    b = mpf(b)
    # Turning point: the largest real root of the null R(r) = 0. The cubic r³ − (b² − a²)r + 2(b − a)² only seeds it;
    # the root is refined on the metric's R.
    seed = max(r.real for r in mp.polyroots([1, 0, -(b * b - a * a), 2 * (b - a) ** 2], maxsteps=200, extraprec=100) if abs(r.imag) < mpf(10) ** -20)
    r0 = findroot(lambda x: radial(a, 1, b, x, mu2=0), seed, tol=mpf(10) ** -35)

    def f(t):
        r = r0 / (1 - t * t)
        drdt = 2 * r0 * t / (1 - t * t) ** 2
        tdot, pdot = rates(a, 1, b, r)
        return pdot * r * r / sqrt(radial(a, 1, b, r, mu2=0)) * drdt

    total = 2 * quad(f, [0, 1], method="gauss-legendre", maxdegree=9)
    return abs(total) - pi


# ---- the ZAMO, tubes and the Penrose split -----------------------------------------------------------------------------
def zamo(a, r):
    gtt, gtp, gpp = metric(a, r)
    return sqrt(-gtt + gtp * gtp / gpp), -gtp / gpp, gpp


def state_constants(a, r, vr, vphi):
    alpha, om, gpp = zamo(a, r)
    gamma = 1 / sqrt(1 - vr * vr - vphi * vphi)
    l = sqrt(gpp) * gamma * vphi
    return alpha * gamma + om * l, l


def split(a, e0, l0, r):
    alpha, om, gpp = zamo(a, r)
    gtt, gtp, gpp_ = metric(a, r)
    tdot, pdot = rates(a, e0, l0, r)
    csum = alpha * tdot  # c_f + c_b
    cdif = sqrt(gpp) * (pdot - om * tdot)  # c_f − c_b
    cf, cb = (csum + cdif) / 2, (csum - cdif) / 2

    def lower(c, sign):
        kt, kp = c / alpha, c * om / alpha + sign * c / sqrt(gpp)
        return -(gtt * kt + gtp * kp), gtp * kt + gpp_ * kp  # (E, L)

    return lower(cf, 1), lower(cb, -1)


# ---- the table ---------------------------------------------------------------------------------------------------------
def main():
    cases = []

    def add(chi, kind, args, value):
        cases.append({"chi": chi, "kind": kind, "args": [float(x) for x in args], "value": mp.nstr(value, 35)})

    checks = []
    for chi in CHI:
        a = mpf(float(chi))
        rh = 1 + sqrt(1 - a * a)
        add(chi, "horizon", [], rh)
        for s in (1, -1):
            ri = isco(a, s)
            checks.append((chi, s, "isco vs BPT", abs(ri / mpf(float_bpt(a, s)[0]) - 1)))
            add(chi, "isco", [s], ri)
            add(chi, "photon_orbit", [s], photon_orbit(a, s))
            add(chi, "photon_b", [s], photon_b(a, s))
            rm, lm = marginally_bound(a, s)
            add(chi, "mb_radius", [s], rm)
            add(chi, "mb_angular", [s], lm)
            rph = photon_orbit(a, s)
            for r in (10.0, 40.0, float(0.5 * (rph + ri))):
                e, l = circular(a, mpf(r), s)
                add(chi, "circular_energy", [r, s], e)
                add(chi, "circular_angular", [r, s], l)
            for e in (0.3, 0.6):
                add(chi, "separatrix", [e, s], separatrix(a, e, s))
            near = 1.15 * float_separatrix(a, 0.4, s)
            for p, e in ((12.0, 0.3), (40.0, 0.6), (300.0, 0.1), (near, 0.4)):
                en, l = bound_constants(a, p, e, s)
                add(chi, "bound_energy", [p, e, s], en)
                add(chi, "bound_angular", [p, e, s], l)
                adv, t, tau = cycle(a, p, e, s)
                add(chi, "advance", [p, e, s], adv)
                add(chi, "period", [p, e, s], t)
                add(chi, "proper_period", [p, e, s], tau)
        for b in (9.0, 25.0, 200.0):
            for sign in (1, -1):
                add(chi, "deflection", [sign * b], deflection(a, sign * b))
        rmid = float(rh + (2 - rh) / 2)
        for r in (2.5, 6.0, 50.0, rmid):
            al, om, _ = zamo(a, mpf(r))
            add(chi, "zamo_lapse", [r], al)
            add(chi, "zamo_omega", [r], om)
        rdeep = float(rh + (2 - rh) / 10)
        for r, vr, vp in ((rmid, 0.3, -0.7), (rmid, 0.1, 0.5), (3.0, -0.2, 0.4), (rdeep, -0.5, -0.5)):
            e, l = state_constants(a, mpf(r), mpf(vr), mpf(vp))
            e, l = float(e), float(l)  # the doubles the oracle will be given
            tdot, pdot = rates(a, mpf(e), mpf(l), mpf(r))
            add(chi, "tube_phi_rate", [e, l, r], pdot / tdot)
            add(chi, "tube_clock_rate", [e, l, r], 1 / tdot)
        for r, vp in ((rmid, 0.6), (float(rh + (2 - rh) / 4), 0.9), (3.0, 0.6)):
            e0, l0 = state_constants(a, mpf(r), mpf(0), mpf(vp))
            e0, l0 = float(e0), float(l0)
            (ef, _), (eb, _) = split(a, mpf(e0), mpf(l0), mpf(r))
            add(chi, "split_forward_energy", [e0, l0, r], ef)
            add(chi, "split_backward_energy", [e0, l0, r], eb)
        # The textbook polynomial R is the metric's R.
        en, l = bound_constants(a, 40.0, 0.3, 1)
        for r in (mpf(7), mpf(30), mpf(55)):
            checks.append((chi, 0, "R polynomial vs metric", abs(radial(a, en, l, r) / radial_poly(a, en, l, r) - 1)))
    worst = max(c[3] for c in checks)
    print(f"# textbook formulas vs metric-derived roots: worst relative difference {mp.nstr(worst, 3)}", file=sys.stderr)
    assert worst < mpf(10) ** -12, checks
    json.dump({"dps": mp.dps, "script": "kerr_mpmath.py", "cases": cases}, sys.stdout, indent=0)
    print()


if __name__ == "__main__":
    main()
