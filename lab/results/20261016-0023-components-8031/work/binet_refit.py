#!/usr/bin/env python3
"""The per-orbit u_k refit row for binet cells (lab wiki binet-cells, open direction 2).

Arms:
  frozen-m{8,16,32}  shipped r1 law: in-band u'' + (1-6u_k)u = 1/L^2 - 3u_k^2,
                     u_k = the band's geometric centre (control).
  mid-m16            one rotation per orbit: omega^2 = 1 - 6*(u_peri+u_apo)/2 (the page's literal refit)
  invL-m16           omega^2 = 1 - 6/L^2                                     (invariant-only centre)
  agm-m{2,8,16}      omega = 2*pi/dphi_exact, dphi_exact = 4*sqrt(p/d)K(4e/d)-2pi
                     compiled from the cycle's own two turning points (AGM, ~30 flops).

Oracle: Python ports of the shipped xtask/src/gr_oracle.rs (periapsis_elliptic) and
gr_oracle_extended.rs (bound_constants, bound_period_quad), validated in-run against an
independent RK4 of the exact Schwarzschild Binet ODE u'' = 1/L^2 + 3u^2 - u.

Units G = c = M = 1. Output: work/metrics.json + a printed table.
"""
import json, math, random
from pathlib import Path

PI = math.pi
OUT = Path(__file__).resolve().parent / "metrics.json"

# ---------------------------------------------------------------- oracle ports
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
    """Advance per radial cycle minus 2*pi (exact, Darwin; port of gr_oracle.rs)."""
    d = p - 6.0 + 2.0 * e
    s = math.sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1)

def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

_GL_CACHE = {}
def gauss_legendre(n):
    if n in _GL_CACHE:
        return _GL_CACHE[n]
    xw = []
    for i in range(1, n + 1):
        x = math.cos(PI * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        p0, p1 = 1.0, x
        for j in range(2, n + 1):
            p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        xw.append((x, 2.0 / ((1 - x * x) * dp * dp)))
    _GL_CACHE[n] = xw
    return xw

def integrate_gl(lo, hi, pieces, nodes, f):
    s = 0.0
    for j in range(pieces):
        a = lo + (hi - lo) * j / pieces
        b = lo + (hi - lo) * (j + 1) / pieces
        for x, w in nodes:
            s += (b - a) * 0.5 * w * f((a + b) * 0.5 + (b - a) * 0.5 * x)
    return s

def refine_gl(lo, hi, nodes, f, tol=1e-13):
    pieces, v = 2, integrate_gl(lo, hi, 2, nodes, f)
    while pieces < 4096:
        pieces *= 2
        w = integrate_gl(lo, hi, pieces, nodes, f)
        done = abs(w - v) <= tol * abs(w)
        v = w
        if done:
            break
    return v

def bound_period_quad(p, e):
    E, L = bound_constants(p, e)
    nodes = gauss_legendre(32)
    def refine(f):
        pieces, v = 16, integrate_gl(0.0, 2 * PI, 16, nodes, f)
        while pieces < 1 << 14:
            pieces *= 2
            w = integrate_gl(0.0, 2 * PI, pieces, nodes, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v
    t = refine(lambda chi: math.sqrt(p / (p - 6.0 - 2.0 * e * math.cos(chi)))
               * (p / (1.0 + e * math.cos(chi))) ** 2 / L * E
               / (1.0 - 2.0 * (1.0 + e * math.cos(chi)) / p))
    tau = refine(lambda chi: math.sqrt(p / (p - 6.0 - 2.0 * e * math.cos(chi)))
                 * (p / (1.0 + e * math.cos(chi))) ** 2 / L)
    return t, tau

_DPHI_CACHE = {}
def dphi_GR(p, e):
    key = (p, e)
    if key not in _DPHI_CACHE:
        _DPHI_CACHE[key] = periapsis_elliptic(p, e) + 2 * PI
    return _DPHI_CACHE[key]

_PER_CACHE = {}
def period_GR(p, e):
    key = (p, e)
    if key not in _PER_CACHE:
        _PER_CACHE[key] = bound_period_quad(p, e)[0]
    return _PER_CACHE[key]


# ------------------------------------------------------- RK4 port validation
def rk4_cycle(p, e, steps_per_rad=2000.0):
    inv_l2 = (p - 3.0 - e * e) / (p * p)
    E, L = bound_constants(p, e)
    f = lambda u: inv_l2 + 3.0 * u * u - u
    h = 1.0 / steps_per_rad
    u, v, phi, t = (1.0 + e) / p, 0.0, 0.0, 0.0
    dtdphi = lambda uu: E / (L * uu * uu * (1.0 - 2.0 * uu))
    def step(u, v, t, h):
        k1u, k1v, k1t = v, f(u), dtdphi(u)
        k2u, k2v, k2t = v + h / 2 * k1v, f(u + h / 2 * k1u), dtdphi(u + h / 2 * k1u)
        k3u, k3v, k3t = v + h / 2 * k2v, f(u + h / 2 * k2u), dtdphi(u + h / 2 * k2u)
        k4u, k4v, k4t = v + h * k3v, f(u + h * k3u), dtdphi(u + h * k3u)
        return (u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u),
                v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v),
                t + h / 6 * (k1t + 2 * k2t + 2 * k3t + k4t))
    seen = False
    for _ in range(int(20 * PI * steps_per_rad)):
        u1, v1, t1 = step(u, v, t, h)
        if v1 > 0:
            seen = True
        if seen and v > 0 and v1 <= 0:
            lo, hi = 0.0, h
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                um, vm, tm = step(u, v, t, mid)
                if vm > 0:
                    lo = mid
                else:
                    hi = mid
            um, vm, tm = step(u, v, t, 0.5 * (lo + hi))
            return phi + 0.5 * (lo + hi), tm
        u, v, t, phi = u1, v1, t1, phi + h
    return None, None

# ------------------------------------------------------------- the band grid
def band_of(u, m):
    return math.floor(-m * math.log2(u))

def band_for(u, v, m):
    j = math.floor(-m * math.log2(u))
    if v > 0 and u >= (2.0 ** (-j / m)) * (1 - 1e-15):
        j -= 1
    elif v < 0 and u <= (2.0 ** (-(j + 1) / m)) * (1 + 1e-15):
        j += 1
    return j

def band_centre(j, m):
    return 2.0 ** (-(j + 0.5) / m)

def band_lo_hi(j, m):
    return 2.0 ** (-(j + 1) / m), 2.0 ** (-j / m)

def _seg_candidates(w, uc, A, B, lo, hi):
    """Events of u(d) = uc + R cos(w d - psi): turning points and edge crossings.
    Returns list of (d, kind, payload) with d > 0."""
    R, psi = math.hypot(A, B), math.atan2(B, A)
    period = 2 * PI / w
    cands = []
    d = psi / w                      # v(d) = -R w sin(w d - psi): first v=0
    while d <= 1e-15:
        d += PI / w
    if d <= period + 1e-15:
        cands.append((d, "turn", None))
    for edge in (lo, hi):
        cc = (edge - uc) / R
        if abs(cc) < 1.0:
            a = math.acos(cc)
            for base in (psi + a, psi - a):
                d = base / w
                while d <= 1e-15:
                    d += period
                if d <= period + 1e-15:
                    cands.append((d, "edge", edge))
    cands.sort(key=lambda c: c[0])
    return cands

# ------------------------------------------------------- frozen r1 band law
def frozen_cycle(p, e, m, max_events=4000):
    """One radial cycle from the exact periapsis. Returns (dphi, T, crossings) or
    ('PLUNGE', phi, crossings) if u >= 0.5 is reached."""
    E, L = bound_constants(p, e)
    dtdphi = lambda uu: E / (L * uu * uu * (1.0 - 2.0 * uu))
    nodes = gauss_legendre(24)
    u, v, phi, T, cross = (1.0 + e) / p, 0.0, 0.0, 0.0, 0
    u_start = u
    turnings = 0
    for _ in range(max_events):
        if u >= 0.5:
            return ("PLUNGE", phi, cross)
        j = band_for(u, v, m)
        uk = band_centre(j, m)
        w2 = 1.0 - 6.0 * uk
        lo, hi = band_lo_hi(j, m)
        if w2 > 0:
            w = math.sqrt(w2)
            uc = (1.0 / L ** 2 - 3.0 * uk * uk) / w2
            A, B = u - uc, v / w
            cands = _seg_candidates(w, uc, A, B, lo, hi)
            d, kind, payload = cands[0]
            T += refine_gl(0.0, d, nodes,
                           lambda s: dtdphi(uc + A * math.cos(w * s) + B * math.sin(w * s)))
            u = payload if kind == "edge" else (
                uc + A * math.cos(w * d) + B * math.sin(w * d))
            v = w * (-A * math.sin(w * d) + B * math.cos(w * d))
            phi += d
            if kind == "edge":
                cross += 1
            else:
                turnings += 1
                # the start is a turning point of the map; the cycle closes at the
                # next turning that returns to the start level (either extremum)
                if turnings >= 2 and abs(u - u_start) <= 1e-6 * u_start:
                    return (phi, T, cross)
        else:
            nu = math.sqrt(-w2)
            uc = (1.0 / L ** 2 - 3.0 * uk * uk) / w2
            A, B = u - uc, v / nu
            def uat(d):
                s = min(nu * d, 700.0)
                return uc + A * math.cosh(s) + B * math.sinh(s)
            # a turning point inside the hyperbolic band: du/dd = 0 at tanh(nu d) = -B/A
            events = []
            if A != 0.0 and abs(B / A) < 1.0 and -B / A > 0.0:
                d_t = math.atanh(-B / A) / nu
                if d_t > 1e-15:
                    events.append((d_t, "turn", None))
            for edge in (lo, hi):
                g0 = uat(0.0) - edge
                if g0 == 0.0:
                    continue
                prev_d, prev_g, hid = 0.0, g0, 1.0
                found = None
                while hid <= 64.0:
                    gd = uat(hid) - edge
                    if gd == 0.0 or (gd > 0) != (prev_g > 0):
                        lo_d, hi_d = prev_d, hid
                        for _ in range(200):
                            mid = 0.5 * (lo_d + hi_d)
                            gm = uat(mid) - edge
                            if (gm > 0) == (prev_g > 0):
                                lo_d = mid
                            else:
                                hi_d = mid
                        found = 0.5 * (lo_d + hi_d)
                        break
                    prev_d, prev_g, hid = hid, gd, hid * 2
                if found is not None:
                    events.append((found, "edge", edge))
            events.sort(key=lambda ev: ev[0])
            if not events:
                return ("PLUNGE", phi, cross)   # u runs away
            d, hkind, edge = events[0]
            d = min(d, 700.0 / nu)
            T += refine_gl(0.0, d, nodes, lambda s: dtdphi(uat(s)))
            if hkind == "turn":
                u = uat(d)
                v = 0.0
            else:
                u = edge
                v = nu * (A * math.sinh(min(nu * d, 700.0)) + B * math.cosh(min(nu * d, 700.0)))
            phi += d
            if hkind == "edge":
                cross += 1
            if u >= 0.5 - 1e-15:
                return ("PLUNGE", phi, cross)
    return ("NOCYCLE", phi, cross)

# --------------------------------------------------------------- rotation arms
def rotation_cycle(p, e, omega):
    """One radial cycle of u = 1/p + (e/p)cos(omega*phi) from periapsis."""
    E, L = bound_constants(p, e)
    dphi = 2 * PI / omega
    nodes = gauss_legendre(32)
    dtdphi = lambda uu: E / (L * uu * uu * (1.0 - 2.0 * uu))
    if e == 0.0:
        T = dphi * dtdphi(1.0 / p)
    else:
        T = refine_gl(0.0, dphi, nodes,
                      lambda s: dtdphi((1.0 + e * math.cos(omega * s)) / p))
    return dphi, T

def rotation_crossings(p, e, m):
    if e == 0:
        return 0
    u_peri, u_apo = (1 + e) / p, (1 - e) / p
    j_peri = math.floor(-m * math.log2(u_peri))   # smaller index (deeper)
    j_apo = math.floor(-m * math.log2(u_apo))
    return 2 * max(0, j_apo - j_peri)

def compile_cycle_agm(E, L):
    """The engine-side compile: the cycle's two turning points from the conserved
    (E, L) by the exact cubic (closed form), then the exact advance by AGM.
    Returns (omega, p_c, e_c)."""
    b = 1.0 / (L * L)
    c = (E * E - 1.0) / (2.0 * L * L)
    pp = b - 1.0 / 12.0
    qq = -1.0 / 108.0 + b / 6.0 + c
    arg = 3.0 * qq / (2.0 * pp) * math.sqrt(-3.0 / pp)
    th = math.acos(max(-1.0, min(1.0, arg)))
    roots = sorted(2.0 * math.sqrt(-pp / 3.0) * math.cos((th - 2.0 * PI * k) / 3.0)
                   + 1.0 / 6.0 for k in (0, 1, 2))
    u_apo, u_peri = roots[0], roots[1]
    pc = 2.0 / (u_peri + u_apo)
    ec = (u_peri - u_apo) / (u_peri + u_apo)
    return 2.0 * PI / (periapsis_elliptic(pc, ec) + 2.0 * PI), pc, ec


def frozen_e0_errors(p, m):
    """e=0 worst-offset family for the frozen arm: circle at u0=1/p, worst adjacent centre.
    Returns (adv_err, per_err) worst over centres within one half band-width."""
    E, L = bound_constants(p, 0.0)
    u0 = 1.0 / p
    j = band_of(u0, m)
    half = u0 * (2 ** (1.0 / (2 * m)) - 1) * 1.01
    worst = (0.0, 0.0)
    for jc in (j - 1, j, j + 1):
        uk = band_centre(jc, m)
        if abs(uk - u0) > half:
            continue
        w2 = 1.0 - 6.0 * uk
        if w2 <= 0:
            return (1.0, 1.0)
        dphi_map = 2 * PI / math.sqrt(w2)
        uc = (1.0 / L ** 2 - 3.0 * uk * uk) / w2
        T_map = dphi_map * E / (L * uc * uc * (1.0 - 2.0 * uc))
        adv = abs(dphi_map - dphi_GR(p, 0.0)) / dphi_GR(p, 0.0)
        per = abs(T_map - period_GR(p, 0.0)) / period_GR(p, 0.0)
        worst = (max(worst[0], adv), max(worst[1], per))
    return worst

def rotation_e0_errors(p, omega_fn):
    E, L = bound_constants(p, 0.0)
    u0 = 1.0 / p
    omega = omega_fn(p, 0.0, L)
    dphi_map = 2 * PI / omega
    T_map = dphi_map * E / (L * u0 * u0 * (1.0 - 2.0 * u0))
    return (abs(dphi_map - dphi_GR(p, 0.0)) / dphi_GR(p, 0.0),
            abs(T_map - period_GR(p, 0.0)) / period_GR(p, 0.0))

# ------------------------------------------------------------------- sampler
def sampler():
    rng = random.Random(20260930)
    seeds = []
    while len(seeds) < 256:
        p = math.exp(math.log(10.0) + rng.random() * (math.log(1000.0) - math.log(10.0)))
        e = 0.7 * rng.random()
        if p >= 6.5 + 2.0 * e:
            seeds.append((p, e))
    return seeds

# ------------------------------------------------- capture / ISCO (band channel)
def band_propagate(m, L, E, u, v, max_events=200000, plunge_u=0.5):
    """Generic event stepper for the frozen band law. Returns
    ('plunge'|'escape'|'timeout', phi, crossings, cycles_completed)."""
    phi, cross, cycles = 0.0, 0, 0
    for _ in range(max_events):
        if not (u == u) or u <= 0.0 or u < 1e-12:
            return ("escape", phi, cross, cycles)
        if u >= plunge_u:
            return ("plunge", phi, cross, cycles)
        j = band_for(u, v, m)
        uk = band_centre(j, m)
        lo, hi = band_lo_hi(j, m)
        w2 = 1.0 - 6.0 * uk
        if w2 <= 0:
            nu = math.sqrt(-w2)
            uc = (1.0 / L ** 2 - 3.0 * uk * uk) / w2
            A, B = u - uc, v / nu
            def uat(d):
                s = min(nu * d, 700.0)
                return uc + A * math.cosh(s) + B * math.sinh(s)
            events = []
            if A != 0.0 and abs(B / A) < 1.0 and -B / A > 0.0:
                d_t = math.atanh(-B / A) / nu
                if d_t > 1e-15:
                    events.append((d_t, "turn", None))
            for edge in (lo, hi):
                g0 = uat(0.0) - edge
                if g0 == 0.0:
                    continue
                prev_d, prev_g, hid = 0.0, g0, 1.0
                found = None
                while hid <= 64.0:
                    gd = uat(hid) - edge
                    if gd == 0.0 or (gd > 0) != (prev_g > 0):
                        lo_d, hi_d = prev_d, hid
                        for _ in range(200):
                            mid = 0.5 * (lo_d + hi_d)
                            gm = uat(mid) - edge
                            if (gm > 0) == (prev_g > 0):
                                lo_d = mid
                            else:
                                hi_d = mid
                        found = 0.5 * (lo_d + hi_d)
                        break
                    prev_d, prev_g, hid = hid, gd, hid * 2
                if found is not None:
                    events.append((found, "edge", edge))
            events.sort(key=lambda ev: ev[0])
            if not events:
                return ("plunge", phi, cross, cycles)
            d, hkind, edge = events[0]
            d = min(d, 700.0 / nu)
            if hkind == "turn":
                u = uat(d)
                v = 0.0
            else:
                u = edge
                v = nu * (A * math.sinh(min(nu * d, 700.0)) + B * math.cosh(min(nu * d, 700.0)))
            phi += d
            if hkind == "edge":
                cross += 1
            continue
        w = math.sqrt(w2)
        uc = (1.0 / L ** 2 - 3.0 * uk * uk) / w2
        A, B = u - uc, v / w
        cands = _seg_candidates(w, uc, A, B, lo, hi)
        d, kind, payload = cands[0]
        u2 = payload if kind == "edge" else (
            uc + A * math.cos(w * d) + B * math.sin(w * d))
        v2 = w * (-A * math.sin(w * d) + B * math.cos(w * d))
        phi += d
        if kind == "edge":
            cross += 1
        else:
            if v > 0:          # v: + -> 0 -> -  => periapsis, a completed cycle
                cycles += 1
        u, v = u2, (0.0 if kind == "turn" else v2)
    return ("timeout", phi, cross, cycles)

def frozen_capture(m, L, E=1.0):
    u = 0.01
    v2 = 2 * u ** 3 - u * u + 2 * u / L ** 2 + (E * E - 1) / L ** 2
    if v2 < 0:
        return False, 0.0, 0
    res, phi, cross, _ = band_propagate(m, L, E, u, math.sqrt(v2))
    return (res == "plunge"), phi, cross

def isco_case(m):
    r = 7.0
    Lc = r / math.sqrt(r - 3.0)
    Ec = math.sqrt((1 - 2 / r) ** 2 / (1 - 3 / r))
    res, phi, cross, cycles = band_propagate(m, Lc * 1.01, Ec, 1.0 / r, 0.0, max_events=400000)
    ok1 = res == "timeout" and cycles >= 100
    r = 5.5
    Lc = r / math.sqrt(r - 3.0)
    Ec = math.sqrt((1 - 2 / r) ** 2 / (1 - 3 / r))
    res, phi, cross, cycles = band_propagate(m, Lc * 0.99, Ec, 1.0 / r, 0.0, max_events=400000)
    ok2 = res == "plunge" and cycles <= 50
    return ok1, ok2

# ----------------------------------------------------------------------- main
def main():
    out = {"port_validation": {}, "sampler": {}, "e0_family": {}, "heldout": {},
           "capture": {}, "isco": {}, "crossings": {}, "repeat": {}}

    for (p, e) in [(20.0, 0.2), (30.0, 0.5), (100.0, 0.2), (12.0, 0.6)]:
        phi_rk, t_rk = rk4_cycle(p, e)
        out["port_validation"][f"p{p}_e{e}"] = {
            "advance_rel_diff": abs(phi_rk - dphi_GR(p, e)) / dphi_GR(p, e),
            "period_rel_diff": abs(t_rk - period_GR(p, e)) / period_GR(p, e),
        }

    seeds = sampler()

    w_mid = lambda p, e, L: math.sqrt(1.0 - 6.0 / p)
    w_invL = lambda p, e, L: math.sqrt(1.0 - 6.0 / L ** 2)
    w_agm = lambda p, e, L: compile_cycle_agm(bound_constants(p, e)[0], L)[0]

    def frozen_metrics(m):
        adv, per, crosses = [], [], []
        for (p, e) in seeds:
            res = frozen_cycle(p, e, m)
            if isinstance(res[0], str):
                adv.append(float("nan")); per.append(float("nan"))
            else:
                dphi, T, cr = res
                adv.append(abs(dphi - dphi_GR(p, e)) / dphi_GR(p, e))
                per.append(abs(T - period_GR(p, e)) / period_GR(p, e))
                crosses.append(cr)
        return adv, per, crosses

    def rotation_metrics(omega_fn):
        adv, per = [], []
        for (p, e) in seeds:
            E, L = bound_constants(p, e)
            dphi, T = rotation_cycle(p, e, omega_fn(p, e, L))
            adv.append(abs(dphi - dphi_GR(p, e)) / dphi_GR(p, e))
            per.append(abs(T - period_GR(p, e)) / period_GR(p, e))
        return adv, per

    arms = {}
    for m in (8, 16, 32):
        a, pe, c = frozen_metrics(m)
        arms[f"frozen-m{m}"] = (a, pe, c)
    arms["mid-m16"] = (*rotation_metrics(w_mid), None)
    a_agm, p_agm = rotation_metrics(w_agm)
    for m in (2, 8, 16):
        arms[f"agm-m{m}"] = (a_agm, p_agm, None)

    for name, (a, pe, c) in arms.items():
        ok = [x for x in a if not math.isnan(x)]
        okp = [x for x in pe if not math.isnan(x)]
        row = {
            "precession_pass_fraction": sum(1 for x in a if x <= 0.01) / len(a),
            "period_pass_fraction": sum(1 for x in pe if x <= 0.001) / len(pe),
            "advance_err_median": sorted(ok)[len(ok) // 2],
            "advance_err_worst": max(ok),
            "period_err_median": sorted(okp)[len(okp) // 2],
            "period_err_worst": max(okp),
            "n_plunge": sum(1 for x in a if math.isnan(x)),
        }
        if c:
            row["crossings_median"] = sorted(c)[len(c) // 2]
        out["sampler"][name] = row

    ps = [6.5, 8.0, 10.0, 15.0, 20.0, 30.0, 35.0, 60.0, 100.0, 300.0, 1000.0]
    for m in (8, 16, 32):
        out["e0_family"][f"frozen-m{m}"] = {str(p): frozen_e0_errors(p, m) for p in ps}
    out["e0_family"]["mid"] = {str(p): rotation_e0_errors(p, w_mid) for p in ps}
    out["e0_family"]["invL"] = {str(p): rotation_e0_errors(p, w_invL) for p in ps}
    out["e0_family"]["agm"] = {str(p): rotation_e0_errors(p, w_agm) for p in ps}

    for (p, e) in [(8.5, 0.9), (1000.0, 0.69), (10.0, 0.05), (100.0, 0.7)]:
        row = {}
        for m in (8, 16, 32):
            res = frozen_cycle(p, e, m)
            row[f"frozen-m{m}"] = (abs(res[0] - dphi_GR(p, e)) / dphi_GR(p, e)
                                   if not isinstance(res[0], str) else res[0])
        for nm, fn in (("mid", w_mid), ("invL", w_invL), ("agm", w_agm)):
            E, L = bound_constants(p, e)
            dphi, T = rotation_cycle(p, e, fn(p, e, L))
            row[nm] = {"advance": abs(dphi - dphi_GR(p, e)) / dphi_GR(p, e),
                       "period": abs(T - period_GR(p, e)) / period_GR(p, e)}
        out["heldout"][f"p{p}_e{e}"] = row

    cap, mis = {}, 0
    for q in (0.5, 0.9, 0.97, 1.03, 1.1, 1.5):
        L = 4.0 * q
        absorbed, phi, cr = frozen_capture(16, L)
        truth = L <= 4.0
        mis += int(absorbed != truth)
        cap[f"L{L:.2f}"] = {"map_absorbed": absorbed, "truth": truth}
    out["capture"] = {"cases": cap, "misclassified": mis}

    ok1, ok2 = isco_case(16)
    out["isco"] = {"bound_case_pass": ok1, "plunge_case_pass": ok2}

    for m in (2, 8, 16):
        cs = sorted(rotation_crossings(p, e, m) for (p, e) in seeds)
        out["crossings"][f"agm-m{m}"] = cs[len(cs) // 2]

    rep = []
    for (p, e) in seeds[:8]:
        d1 = []
        good = True
        for _ in range(3):
            res = frozen_cycle(p, e, 16)
            if res[0] == "PLUNGE":
                good = False
                break
            d1.append(res[0])
        if good and len(d1) == 3:
            rep.append((max(d1) - min(d1)) / max(d1))
    out["repeat"]["frozen-m16_max_cycle_spread_8seeds"] = max(rep) if rep else None

    OUT.write_text(json.dumps(out, indent=1, default=str))

    hdr = (f"{'arm':<12} {'prec_pass':>9} {'per_pass':>9} {'adv_med':>10} {'adv_worst':>10} "
           f"{'per_med':>10} {'per_worst':>10} {'cross_med':>9}")
    print(hdr)
    print("-" * len(hdr))
    for name, row in out["sampler"].items():
        print(f"{name:<12} {row['precession_pass_fraction']:>9.4f} {row['period_pass_fraction']:>9.4f} "
              f"{row['advance_err_median']:>10.2e} {row['advance_err_worst']:>10.2e} "
              f"{row['period_err_median']:>10.2e} {row['period_err_worst']:>10.2e} "
              f"{row.get('crossings_median', float('nan')):>9.0f}")
    print("\nport validation:", json.dumps(out["port_validation"], indent=1))
    print("\ne=0 family worst-offset (advance err):")
    for name, fam in out["e0_family"].items():
        print(f"  {name:<12} " + " ".join(f"{p}:{v[0]:.1e}" for p, v in fam.items()))
    print("e=0 family worst-offset (period err):")
    for name, fam in out["e0_family"].items():
        print(f"  {name:<12} " + " ".join(f"{p}:{v[1]:.1e}" for p, v in fam.items()))
    print("\nheld-out:", json.dumps(out["heldout"], indent=1, default=str))
    print("\ncapture misclassified:", out["capture"]["misclassified"], "isco:", out["isco"])
    print("crossings medians (agm):", out["crossings"])
    print("repeat spread:", out["repeat"])

if __name__ == "__main__":
    main()
