#!/usr/bin/env python3
"""Rung r1: orbits in rings around one static Schwarzschild mass (G=c=M=1, equatorial plane).

Oracle ports (float64, independent of the configurations):
  periapsis_elliptic, deflection_quadrature, gauss_legendre  <- xtask/src/gr_oracle.rs
  integrate_gl, bound_constants, bound_period_quad           <- xtask/src/gr_oracle_extended.rs
  deflection_tail: exact outgoing-tail excess deflection beyond r0 (same quadrature).

Models, all float64, all event-based (no per-body steps):
  binet_*   : rings with edges r = 2^(k/m), m bands per octave; inside band k the orbit
              obeys u'' + (1-6u_k) u = 1/L^2 - 3u_k^2  (light: RHS = -3u_k^2), u_k the
              value at the band's geometric centre; u, u' continuous across edges; the
              per-band solution is exact (rotation, hyperbolic, parabolic safety branch).
              dt/dphi = E/(L u^2 (1-2u)) integrated by fixed 16-node Gauss-Legendre over
              each band piece's phi-interval (a rule of the band, E and L only).
  river_*   : same ring edges; inside ring k the flow is the constant radial flow
              beta_k = -sqrt(2/r_k) r_hat with r_k the ring's geometric-centre radius;
              H = sqrt(1+|p|^2) + beta.p (light: |p| + beta.p); straight lines inside a
              ring; H and L conserved exactly at each crossing (one quadratic; no real
              root => reflection); the root keeps the radial-velocity sign, else is the
              one nearest the incoming radial momentum.
  square    : dyadic cells refined while side > |centre|/16 (root level 16, so side is
              within a factor 2 of r/16); constant flow per cell from the cell centre;
              H and the edge-parallel momentum conserved at cell edges (Snell), the
              perpendicular momentum solved (quadratic; no real root => reflection back
              into the old cell).
  tiltonly  : rings m=16; straight lines; at each crossing the velocity is rotated
              toward the mass by delta = arcs/(r_k^2 |v|) (Newtonian impulse, M=1),
              keeping |v|; light runs at |v| = 1.

A radial cycle is apoapsis-to-apoapsis. Binet advances phi exactly; the Cartesian
models read a cycle as 2pi plus the wrapped-to-(-pi,pi] change of the position angle
between apoapsis events (every case's advance here is within pi of 2pi; per-segment
sweeps are < 0.9 rad, so phi_swept accumulates without ambiguity). Cycles are counted
between apoapsis events; the partial cycle from the launch state is discarded.

Sampler: random.Random(20260930); bound seeds first (p log-uniform [10,1000], e
uniform [0,0.7], reject the pair unless p >= 6.5+2e), then light seeds (b log-uniform
[10,1000]).
"""
import math
import random
from math import floor, sqrt, log, log2, exp, atan2, acos, cos, sin, pi, hypot, ldexp

SEQ_CYCLES = (1, 2)      # cycles whose crossing sequences are kept for the repeat check

# ---------------------------------------------------------------- oracle ports
def ellip_k(m):
    a, g = 1.0, sqrt(1.0 - m)
    for _ in range(40):
        a1, g1 = (a + g) / 2.0, sqrt(a * g)
        if abs(a1 - g1) <= 1e-17 * a1:
            a = a1
            break
        a, g = a1, g1
    return pi / (2.0 * a)

def ellip_k_minus_half_pi(m):
    if m >= 0.25:
        return ellip_k(m) - pi / 2.0
    c, mn, s = 1.0, 1.0, 0.0
    for n in range(1, 200):
        c *= (2 * n - 1) / (2 * n)
        mn *= m
        term = c * c * mn
        s += term
        if term < 1e-19 * s:
            break
    return pi / 2.0 * s

def periapsis_elliptic(p, e):
    """Periapsis-to-periapsis angle minus 2pi: the apsidal advance per radial cycle."""
    d = p - 6.0 + 2.0 * e
    s = sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + pi / 2.0 * s_minus_1)

def gauss_legendre(n):
    out = []
    for i in range(1, n + 1):
        x = cos(pi * (i - 0.25) / (n + 0.5))
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

def _defl_turning_u0(b):
    u0 = 1.0 / b
    for _ in range(100):
        h = 2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b)
        dh = 6.0 * u0 * u0 - 2.0 * u0
        step = h / dh
        u0 -= step
        if abs(step) <= 1e-17 * u0:
            break
    return u0

def _defl_integrand(s, u0):
    u = u0 * (1.0 - s * s)
    qf = u0 + u
    r = 2.0 * (u * u + u * u0 + u0 * u0)
    q = qf - r
    return 4.0 * sqrt(u0) * r / (sqrt(q * qf) * (sqrt(qf) + sqrt(q)))

def deflection_quadrature(b):
    """Total asymptotic (infinity to infinity) light deflection."""
    u0 = _defl_turning_u0(b)
    nodes = gauss_legendre(32)
    pieces = 64
    total = 0.0
    for j in range(pieces):
        a, c = j / pieces, (j + 1) / pieces
        for x, w in nodes:
            total += w * (c - a) / 2.0 * _defl_integrand((a + c) / 2.0 + (c - a) / 2.0 * x, u0)
    return total

def deflection_tail(b, r0):
    """Exact excess deflection accumulated beyond r0, one side, same quadrature.

    u in [0, 1/r0] maps to s in [sqrt(1-u_s/u0), 1] on one half-path; one side's tail
    is half of that integral."""
    u0 = _defl_turning_u0(b)
    s_s = sqrt(max(0.0, 1.0 - (1.0 / r0) / u0))
    nodes = gauss_legendre(32)
    pieces = 8
    total = 0.0
    for j in range(pieces):
        a = s_s + (1.0 - s_s) * j / pieces
        c = s_s + (1.0 - s_s) * (j + 1) / pieces
        for x, w in nodes:
            total += w * (c - a) / 2.0 * _defl_integrand((a + c) / 2.0 + (c - a) / 2.0 * x, u0)
    return 0.5 * total

def integrate_gl(lo, hi, pieces, n, f):
    nodes = gauss_legendre(n)
    s = 0.0
    for j in range(pieces):
        a = lo + (hi - lo) * j / pieces
        b = lo + (hi - lo) * (j + 1) / pieces
        for x, w in nodes:
            s += (b - a) * 0.5 * w * f((a + b) * 0.5 + (b - a) * 0.5 * x)
    return s

def bound_constants(p, e):
    energy = sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / sqrt(p - 3.0 - e * e)
    return energy, angular

def bound_period_quad(p, e):
    """(coordinate-time, proper-time) per radial cycle, Darwin chi quadrature."""
    energy, angular = bound_constants(p, e)
    def refine(f):
        pieces = 16
        v = integrate_gl(0.0, 2.0 * pi, pieces, 32, f)
        while pieces < 1 << 14:
            pieces *= 2
            w = integrate_gl(0.0, 2.0 * pi, pieces, 32, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v
    t = refine(lambda chi: sqrt(p / (p - 6.0 - 2.0 * e * cos(chi)))
               * (p / (1.0 + e * cos(chi))) ** 2 / angular * energy
               / (1.0 - 2.0 * (1.0 + e * cos(chi)) / p))
    tau = refine(lambda chi: sqrt(p / (p - 6.0 - 2.0 * e * cos(chi)))
                 * (p / (1.0 + e * cos(chi))) ** 2 / angular)
    return t, tau

GLN, GLW = zip(*gauss_legendre(16))

# ---------------------------------------------------------------- seeds
def draw_seeds():
    rng = random.Random(20260930)
    def logu():
        return exp(math.log(10.0) + rng.random() * math.log(100.0))
    bound = []
    while len(bound) < 256:
        p = logu()
        e = 0.7 * rng.random()
        if p >= 6.5 + 2.0 * e:
            bound.append((p, e))
    light = [logu() for _ in range(64)]
    return bound, light

def seed_state(p, e):
    E, L = bound_constants(p, e)
    return E, L, (1.0 - e) / p

# ---------------------------------------------------------------- Binet ring model
_W2_EPS = 1e-12

def binet_run(m, E, L, u0, w0=0.0, light=False, ncycles=2, max_pieces=None,
              escape_u=0.0, phi_cap=None, collect_points=None):
    """Start at (u0, w0); w0 = 0 means a turning point (direction from u''). Returns
    dict with cycles = [(dphi, dt, ncross, r_peri, r_apo)] between apoapsis events,
    seqs, absorbed, escaped, timeout, phi, u, w, points."""
    ln2m = math.log(2.0) / m
    invL2 = 0.0 if light else 1.0 / (L * L)
    u, w, phi, t = u0, w0, 0.0, 0.0
    k = int(floor(-m * log2(u)))
    if w0 != 0.0:
        direction = 1 if w0 > 0.0 else -1
    else:
        uk0 = exp(-(k + 0.5) * ln2m)
        w20 = 1.0 - 6.0 * uk0
        B0 = invL2 - 3.0 * uk0 * uk0
        direction = 1 if (B0 - w20 * u) > 0 else -1
    if max_pieces is None:
        max_pieces = ncycles * 4000 + 8000
    cycles, seqs = [], {}
    seq = []
    cyc_dphi = cyc_dt = 0.0
    r_peri = float('inf')
    pending = False
    absorbed = escaped = timeout = False
    points = [] if collect_points is not None else None
    for _ in range(max_pieces):
        Uout = exp(-k * ln2m)
        Uin = exp(-(k + 1) * ln2m)
        uk = sqrt(Uout * Uin)
        w2 = 1.0 - 6.0 * uk
        B = invL2 - 3.0 * uk * uk
        ev = None
        if w2 > _W2_EPS:
            om = sqrt(w2)
            C = B / w2
            A = u - C
            D = w / om
            R = hypot(A, D)
            psi = atan2(D, A)
            if direction > 0:
                bval = Uin if Uin <= 0.5 else 0.5
                if C + R >= bval:
                    q = (bval - C) / R
                    q = 1.0 if q > 1.0 else (-1.0 if q < -1.0 else q)
                    thx = -acos(q)
                    dphi = (thx + psi) / om
                    ev = 'absorb' if (bval == 0.5 and Uin > 0.5) else 'cross_in'
                    nu, nw = bval, -R * om * sin(thx)
                else:
                    dphi = psi / om
                    ev = 'peri'
                    nu, nw = C + R, 0.0
            else:
                if C - R <= Uout:
                    q = (Uout - C) / R
                    q = 1.0 if q > 1.0 else (-1.0 if q < -1.0 else q)
                    thx = acos(q)
                    dphi = (thx + psi) / om
                    ev = 'cross_out'
                    nu, nw = Uout, -R * om * sin(thx)
                else:
                    dphi = (pi + psi) / om
                    ev = 'apo'
                    nu, nw = C - R, 0.0
            def u_at(d, C=C, R=R, om=om, psi=psi):
                return C + R * cos(om * d - psi)
        elif w2 < -_W2_EPS:
            kap = sqrt(-w2)
            C = B / w2
            A = u - C
            D = w / kap
            S = A * A - D * D
            def vsolve(y):
                if abs(A + D) < 1e-300:
                    return log((A - D) / (2.0 * y)) / kap
                disc = y * y - S
                if disc < 0.0:
                    return None
                rt = sqrt(disc)
                z = (y + rt) / (A + D) if direction > 0 else (y - rt) / (A + D)
                if z < 1.0:
                    z2 = (y - rt) / (A + D) if direction > 0 else (y + rt) / (A + D)
                    if z2 >= 1.0:
                        z = z2
                if z < 1.0:
                    return None
                return log(z) / kap
            if direction > 0:
                bval = Uin if Uin <= 0.5 else 0.5
                d_turn = log(sqrt((A - D) / (A + D))) / kap if (S > 0.0 and A < 0.0) else None
                if d_turn is not None and d_turn >= 0.0 and C - sqrt(S) < bval:
                    dphi, ev = d_turn, 'peri'
                    nu, nw = C - sqrt(S), 0.0
                else:
                    dphi = vsolve(bval)
                    if dphi is None:
                        dphi = max(d_turn, 0.0) if d_turn is not None else 0.0
                        ev = 'peri'
                        nu = C - sqrt(S) if S > 0.0 else u
                        nw = 0.0
                    else:
                        ev = 'absorb' if (bval == 0.5 and Uin > 0.5) else 'cross_in'
                        nu = bval
                        kd = kap * dphi
                        nw = kap * 0.5 * ((A + D) * exp(kd) - (A - D) * exp(-kd))
            else:
                d_turn = log(sqrt((A - D) / (A + D))) / kap if (S > 0.0 and A > 0.0) else None
                if d_turn is not None and d_turn >= 0.0 and C + sqrt(S) > Uout:
                    dphi, ev = d_turn, 'apo'
                    nu, nw = C + sqrt(S), 0.0
                else:
                    dphi = vsolve(Uout)
                    if dphi is None:
                        dphi = max(d_turn, 0.0) if d_turn is not None else 0.0
                        ev = 'apo'
                        nu = C + sqrt(S) if S > 0.0 else u
                        nw = 0.0
                    else:
                        ev = 'cross_out'
                        nu = Uout
                        kd = kap * dphi
                        nw = kap * 0.5 * ((A + D) * exp(kd) - (A - D) * exp(-kd))
            def u_at(d, C=C, A=A, D=D, kap=kap):
                kd = kap * d
                return C + 0.5 * (A + D) * exp(kd) + 0.5 * (A - D) * exp(-kd)
        else:
            half = 0.5 * B
            if direction > 0:
                bval = Uin if Uin <= 0.5 else 0.5
                dphi = None
                if abs(half) > 1e-300:
                    disc = w * w - 2.0 * half * (u - bval)
                    if disc >= 0.0:
                        rt = sqrt(disc)
                        cand = [d for d in ((-w + rt) / (2.0 * half), (-w - rt) / (2.0 * half)) if d > 0.0]
                        if cand:
                            dphi = min(cand)
                elif w > 0.0:
                    dphi = (bval - u) / w
                if dphi is not None:
                    ev = 'absorb' if (bval == 0.5 and Uin > 0.5) else 'cross_in'
                    nu, nw = bval, w + B * dphi
                else:
                    dphi = -w / B
                    ev = 'peri'
                    nu = u + w * dphi + half * dphi * dphi
                    nw = 0.0
            else:
                dphi = None
                if abs(half) > 1e-300:
                    disc = w * w - 2.0 * half * (u - Uout)
                    if disc >= 0.0:
                        rt = sqrt(disc)
                        cand = [d for d in ((-w + rt) / (2.0 * half), (-w - rt) / (2.0 * half)) if d > 0.0]
                        if cand:
                            dphi = min(cand)
                elif w < 0.0:
                    dphi = (Uout - u) / w
                if dphi is not None:
                    ev = 'cross_out'
                    nu, nw = Uout, w + B * dphi
                else:
                    dphi = -w / B
                    ev = 'apo'
                    nu = u + w * dphi + half * dphi * dphi
                    nw = 0.0
            def u_at(d, u=u, w=w, half=half):
                return u + w * d + half * d * d
        if not light and dphi > 0.0:
            halfd = 0.5 * dphi
            dt = 0.0
            for xn, wn in zip(GLN, GLW):
                un = u_at(halfd * (1.0 + xn))
                if un < 1e-300:
                    un = 1e-300
                dt += wn * halfd * E / (L * un * un * (1.0 - 2.0 * un))
            t += dt
            cyc_dt += dt
        if collect_points is not None and dphi > 0.0:
            for i in range(7):
                d = dphi * i / 6.0
                uu = u_at(d)
                ph = phi + d
                collect_points.append((cos(ph) / uu, sin(ph) / uu))
        phi += dphi
        cyc_dphi += dphi
        u, w = nu, nw
        if ev in ('cross_in', 'cross_out'):
            seq.append(k)
            k = k + 1 if ev == 'cross_in' else k - 1
            if escape_u > 0.0 and u < escape_u:
                escaped = True
                break
        elif ev == 'peri':
            r_peri = min(r_peri, 1.0 / u)
            direction = -1
        elif ev == 'apo':
            if pending:
                cycles.append((cyc_dphi, cyc_dt, len(seq),
                               r_peri if r_peri < float('inf') else 1.0 / u, 1.0 / u))
                if len(cycles) in SEQ_CYCLES:
                    seqs[len(cycles)] = seq[:]
                if len(cycles) >= ncycles:
                    break
            pending = True
            cyc_dphi = 0.0
            cyc_dt = 0.0
            seq = []
            r_peri = float('inf')
            direction = 1
        else:                                   # absorb
            absorbed = True
            break
        if phi_cap is not None and phi > phi_cap:
            break
    else:
        timeout = True
    return {'cycles': cycles, 'seqs': seqs, 'absorbed': absorbed, 'escaped': escaped,
            'timeout': timeout, 'phi': phi, 't': t, 'u': u, 'w': w, 'points': points}

# ---------------------------------------------------------------- shared Cartesian bits
def _wrap_pi(a):
    while a > pi:
        a -= 2.0 * pi
    while a <= -pi:
        a += 2.0 * pi
    return a

def _pr_roots_ring(H, L, R, beta, light):
    """Roots for p_r at radius R with radial flow beta, conserving H and p_t = L/R."""
    p_t = L / R
    aa = 1.0 - beta * beta
    bb = -2.0 * beta * H
    cc = p_t * p_t - H * H if light else 1.0 + p_t * p_t - H * H
    disc = bb * bb - 4.0 * aa * cc
    if disc < 0.0:
        return None
    rt = sqrt(disc)
    return (p_t, (bb + rt) / (2.0 * aa)), (p_t, (bb - rt) / (2.0 * aa))

def _vr_of(pr, pt, beta, light):
    if light:
        return pr / sqrt(pr * pr + pt * pt) + beta
    return pr / sqrt(1.0 + pr * pr + pt * pt) + beta

def ring_band(r, m):
    return int(floor(m * log2(r)))

# ---------------------------------------------------------------- river ring model
def river_run(m, x0, y0, px0, py0, H, light=False, ncycles=2, max_events=None,
              escape_r=0.0, phi_cap=None, collect_points=None):
    ln2m = math.log(2.0) / m
    x, y, t = x0, y0, 0.0
    px, py = px0, py0
    k = ring_band(sqrt(x0 * x0 + y0 * y0), m)
    if max_events is None:
        max_events = ncycles * 4000 + 8000
    cycles, seqs = [], {}
    seq = []
    cyc_dt = 0.0
    prev_phi = None
    phi_swept = atan2(y0, x0)
    r_peri = float('inf')
    absorbed = escaped = timeout = False
    points = [] if collect_points is not None else None
    n_ev = 0
    while n_ev < max_events:
        n_ev += 1
        r = sqrt(x * x + y * y)
        Rc = exp((k + 0.5) * ln2m)
        beta = -sqrt(2.0 / Rc)
        if light:
            pn = sqrt(px * px + py * py)
            vx = px / pn + beta * x / r
            vy = py / pn + beta * y / r
        else:
            g = sqrt(1.0 + px * px + py * py)
            vx = px / g + beta * x / r
            vy = py / g + beta * y / r
        v2 = vx * vx + vy * vy
        rv = x * vx + y * vy
        outward = rv > 0
        R_t = exp((k + 1) * ln2m) if outward else exp(k * ln2m)
        disc = rv * rv - v2 * (r * r - R_t * R_t)
        tau = (-rv + sqrt(disc)) / v2 if disc >= 0.0 else None
        tau_star = -rv / v2
        if tau is None or (tau_star > 0.0 and tau_star < tau):
            # turning point inside the ring (a periapsis on a straight segment)
            xn = x + vx * tau_star
            yn = y + vy * tau_star
            rr = sqrt(xn * xn + yn * yn)
            if rr <= 2.0:
                return {'cycles': cycles, 'seqs': seqs, 'absorbed': True,
                        'escaped': False, 'timeout': False, 'points': points,
                        't': t, 'phi': phi_swept, 'x': xn, 'y': yn, 'px': px, 'py': py}
            if collect_points is not None:
                points.append((xn, yn))
            phi_swept += abs(_wrap_pi(atan2(yn, xn) - atan2(y, x)))
            x, y = xn, yn
            t += tau_star
            cyc_dt += tau_star
            r_peri = min(r_peri, rr)
            continue
        if tau <= 0.0:
            tau = 0.0
        xn = x + vx * tau
        yn = y + vy * tau
        phi_swept += abs(_wrap_pi(atan2(yn, xn) - atan2(y, x)))
        x, y = xn, yn
        t += tau
        cyc_dt += tau
        rr = sqrt(x * x + y * y)
        if collect_points is not None:
            points.append((x, y))
        vr_before = (x * vx + y * vy) / rr
        if rr <= 2.0:
            absorbed = True
            break
        k_new = k + 1 if outward else k - 1
        Rc_new = exp((k_new + 0.5) * ln2m)
        beta_new = -sqrt(2.0 / Rc_new)
        L_now = x * py - y * px
        roots = _pr_roots_ring(H, L_now, rr, beta_new, light)
        rx, ry = x / rr, y / rr
        p_r_in = px * rx + py * ry
        sgn_in = 1.0 if vr_before > 0.0 else -1.0
        refl = True
        if roots is not None:
            cands = [(pr, pt, _vr_of(pr, pt, beta_new, light)) for pr, pt in roots]
            same = [c for c in cands if (1.0 if c[2] > 0.0 else -1.0) == sgn_in]
            if same:
                pr, pt, vr_after = min(same, key=lambda c: abs(c[0] - p_r_in))
            else:
                pr, pt, vr_after = min(cands, key=lambda c: abs(c[2]))
            refl = False
        if refl:
            px = px - 2.0 * p_r_in * rx
            py = py - 2.0 * p_r_in * ry
            vr_after = -vr_before + 2.0 * beta
        else:
            tx, ty = -ry, rx
            px = pt * tx + pr * rx
            py = pt * ty + pr * ry
            k = k_new
        seq.append(k)
        if vr_before > 0.0 and vr_after <= 0.0:          # apoapsis at this crossing
            phi_ev = atan2(y, x)
            if prev_phi is not None:
                dphi = 2.0 * pi + _wrap_pi(phi_ev - prev_phi)
                cycles.append((dphi, cyc_dt, len(seq),
                               r_peri if r_peri < float('inf') else rr, rr))
                if len(cycles) in SEQ_CYCLES:
                    seqs[len(cycles)] = seq[:]
                if len(cycles) >= ncycles:
                    break
            prev_phi = phi_ev
            cyc_dt = 0.0
            seq = []
            r_peri = float('inf')
        elif vr_before < 0.0 and vr_after >= 0.0:
            r_peri = min(r_peri, rr)
        if escape_r > 0.0 and rr > escape_r:
            escaped = True
            break
        if phi_cap is not None and phi_swept > phi_cap:
            break
    else:
        timeout = True
    return {'cycles': cycles, 'seqs': seqs, 'absorbed': absorbed, 'escaped': escaped,
            'timeout': timeout, 'points': points, 't': t, 'phi': phi_swept,
            'x': x, 'y': y, 'px': px, 'py': py}

# ---------------------------------------------------------------- tilt-only model
def tilt_run(m, x0, y0, vx0, vy0, light=False, ncycles=2, max_events=None, escape_r=0.0,
             phi_cap=None, collect_points=None):
    ln2m = math.log(2.0) / m
    x, y, t = x0, y0, 0.0
    vx, vy = vx0, vy0
    k = ring_band(sqrt(x0 * x0 + y0 * y0), m)
    if max_events is None:
        max_events = ncycles * 4000 + 8000
    cycles, seqs = [], {}
    seq = []
    cyc_dt = 0.0
    prev_phi = None
    phi_swept = atan2(y0, x0)
    r_peri = float('inf')
    absorbed = escaped = timeout = False
    points = [] if collect_points is not None else None
    n_ev = 0
    while n_ev < max_events:
        n_ev += 1
        r = sqrt(x * x + y * y)
        v2 = vx * vx + vy * vy
        rv = x * vx + y * vy
        outward = rv > 0
        R_t = exp((k + 1) * ln2m) if outward else exp(k * ln2m)
        disc = rv * rv - v2 * (r * r - R_t * R_t)
        tau = (-rv + sqrt(disc)) / v2 if disc >= 0.0 else None
        tau_star = -rv / v2
        if tau is None or (tau_star > 0.0 and tau_star < tau):
            xn = x + vx * tau_star
            yn = y + vy * tau_star
            rr = sqrt(xn * xn + yn * yn)
            if rr <= 2.0:
                return {'cycles': cycles, 'seqs': seqs, 'absorbed': True,
                        'escaped': False, 'timeout': False, 'points': points,
                        't': t, 'phi': phi_swept, 'x': xn, 'y': yn, 'vx': vx, 'vy': vy}
            if collect_points is not None:
                points.append((xn, yn))
            phi_swept += abs(_wrap_pi(atan2(yn, xn) - atan2(y, x)))
            x, y = xn, yn
            t += tau_star
            cyc_dt += tau_star
            r_peri = min(r_peri, rr)
            continue
        if tau <= 0.0:
            tau = 0.0
        arcs = sqrt(v2) * tau
        phi0 = atan2(y, x)
        x = x + vx * tau
        y = y + vy * tau
        phi_swept += abs(_wrap_pi(atan2(y, x) - phi0))
        t += tau
        cyc_dt += tau
        rr = sqrt(x * x + y * y)
        if collect_points is not None:
            points.append((x, y))
        vr_before = (x * vx + y * vy) / rr
        if rr <= 2.0:
            absorbed = True
            break
        vv = sqrt(v2)
        Rc = exp((k + 0.5) * ln2m)
        delta = arcs / (Rc * Rc * vv)
        hx, hy = -x / rr, -y / rr
        vxh, vyh = vx / vv, vy / vv
        dotp = hx * vxh + hy * vyh
        wx, wy = hx - dotp * vxh, hy - dotp * vyh
        wn = sqrt(wx * wx + wy * wy)
        if wn > 1e-15 and delta > 0.0:
            wx, wy = wx / wn, wy / wn
            cd, sd = cos(delta), sin(delta)
            vx = vv * (vxh * cd + wx * sd)
            vy = vv * (vyh * cd + wy * sd)
        vr_after = (x * vx + y * vy) / rr
        k = k + 1 if outward else k - 1
        seq.append(k)
        if vr_before > 0.0 and vr_after <= 0.0:
            phi_ev = atan2(y, x)
            if prev_phi is not None:
                dphi = 2.0 * pi + _wrap_pi(phi_ev - prev_phi)
                cycles.append((dphi, cyc_dt, len(seq),
                               r_peri if r_peri < float('inf') else rr, rr))
                if len(cycles) in SEQ_CYCLES:
                    seqs[len(cycles)] = seq[:]
                if len(cycles) >= ncycles:
                    break
            prev_phi = phi_ev
            cyc_dt = 0.0
            seq = []
            r_peri = float('inf')
        elif vr_before < 0.0 and vr_after >= 0.0:
            r_peri = min(r_peri, rr)
        if escape_r > 0.0 and rr > escape_r:
            escaped = True
            break
        if phi_cap is not None and phi_swept > phi_cap:
            break
    else:
        timeout = True
    return {'cycles': cycles, 'seqs': seqs, 'absorbed': absorbed, 'escaped': escaped,
            'timeout': timeout, 'points': points, 't': t, 'phi': phi_swept,
            'x': x, 'y': y, 'vx': vx, 'vy': vy}

# ---------------------------------------------------------------- square model
_ROOT_LEVEL = 16

def _cell_of(x, y):
    """(level, i, j, side, cx, cy, |centre|) of the mesh cell containing (x, y)."""
    r_est = sqrt(x * x + y * y)
    if r_est <= 0.0:
        r_est = 1e-300
    lvl = int(floor(log2(r_est))) - 4
    if lvl > _ROOT_LEVEL:
        lvl = _ROOT_LEVEL
    if lvl < -40:
        lvl = -40
    for _ in range(12):
        s = ldexp(1.0, lvl)
        i = int(floor(x / s))
        j = int(floor(y / s))
        cx, cy = (i + 0.5) * s, (j + 0.5) * s
        rc = sqrt(cx * cx + cy * cy)
        if s > rc / 16.0:
            lvl -= 1
            continue
        if lvl < _ROOT_LEVEL:
            s2 = 2.0 * s
            ip = int(floor(x / s2))
            jp = int(floor(y / s2))
            cpx, cpy = (ip + 0.5) * s2, (jp + 0.5) * s2
            rcp = sqrt(cpx * cpx + cpy * cpy)
            if s2 <= rcp / 16.0:
                lvl += 1
                continue
        return lvl, i, j, s, cx, cy, rc
    s = ldexp(1.0, lvl)
    i, j = int(floor(x / s)), int(floor(y / s))
    cx, cy = (i + 0.5) * s, (j + 0.5) * s
    return lvl, i, j, s, cx, cy, sqrt(cx * cx + cy * cy)

def _pr_roots_edge(H, p_par, bn, be, light):
    """Roots for p_perp conserving H with edge-parallel momentum p_par; bn = beta.n,
    be = beta.e for the new cell's flow."""
    aa = 1.0 - bn * bn
    bb = -2.0 * H * bn + 2.0 * bn * be * p_par
    cc = (0.0 if light else 1.0) + p_par * p_par - H * H + 2.0 * H * be * p_par \
        - be * be * p_par * p_par
    disc = bb * bb - 4.0 * aa * cc
    if disc < 0.0:
        return None
    rt = sqrt(disc)
    return (bb + rt) / (2.0 * aa), (bb - rt) / (2.0 * aa)

def square_run(x0, y0, px0, py0, H, light=False, ncycles=2, max_events=None,
               escape_r=0.0, phi_cap=None, collect_points=None):
    x, y, t = x0, y0, 0.0
    px, py = px0, py0
    lvl, i, j, s, cx, cy, rc = _cell_of(x, y)
    beta = -sqrt(2.0 / rc)
    bx, by = beta * cx / rc, beta * cy / rc
    if max_events is None:
        max_events = ncycles * 4000 + 8000
    cycles, seqs = [], {}
    seq = []
    cyc_dt = 0.0
    prev_phi = None
    phi_swept = atan2(y0, x0)
    r_peri = float('inf')
    absorbed = escaped = timeout = False
    points = [] if collect_points is not None else None
    n_ev = 0
    while n_ev < max_events:
        n_ev += 1
        r = sqrt(x * x + y * y)
        if light:
            pn = sqrt(px * px + py * py)
            vx = px / pn + bx
            vy = py / pn + by
        else:
            g = sqrt(1.0 + px * px + py * py)
            vx = px / g + bx
            vy = py / g + by
        v2 = vx * vx + vy * vy
        if v2 <= 0.0:
            absorbed = True
            break
        rv = x * vx + y * vy
        x_lo, x_hi = i * s, (i + 1) * s
        y_lo, y_hi = j * s, (j + 1) * s
        tau = float('inf')
        axis, sgn = 0, 1
        if vx > 0.0:
            tt = (x_hi - x) / vx
            if tt < tau:
                tau, axis, sgn = tt, 0, 1
        elif vx < 0.0:
            tt = (x_lo - x) / vx
            if tt < tau:
                tau, axis, sgn = tt, 0, -1
        if vy > 0.0:
            tt = (y_hi - y) / vy
            if tt < tau:
                tau, axis, sgn = tt, 1, 1
        elif vy < 0.0:
            tt = (y_lo - y) / vy
            if tt < tau:
                tau, axis, sgn = tt, 1, -1
        if tau == float('inf'):
            timeout = True
            break
        tau_star = -rv / v2
        if 0.0 < tau_star < tau:
            xn = x + vx * tau_star
            yn = y + vy * tau_star
            rr = sqrt(xn * xn + yn * yn)
            if rr <= 2.0:
                return {'cycles': cycles, 'seqs': seqs, 'absorbed': True,
                        'escaped': False, 'timeout': False, 'points': points,
                        't': t, 'phi': phi_swept, 'x': xn, 'y': yn, 'px': px, 'py': py}
            if collect_points is not None:
                points.append((xn, yn))
            phi_swept += abs(_wrap_pi(atan2(yn, xn) - atan2(y, x)))
            x, y = xn, yn
            t += tau_star
            cyc_dt += tau_star
            r_peri = min(r_peri, rr)
            continue
        if tau <= 0.0:
            tau = 0.0
        phi0 = atan2(y, x)
        x = x + vx * tau
        y = y + vy * tau
        phi_swept += abs(_wrap_pi(atan2(y, x) - phi0))
        t += tau
        cyc_dt += tau
        rr = sqrt(x * x + y * y)
        if collect_points is not None:
            points.append((x, y))
        vr_before = rv / rr
        if rr <= 2.0:
            absorbed = True
            break
        nudge = s * 1e-9
        if axis == 0:
            edge_x = x_hi if sgn > 0 else x_lo
            nx, ny, ex, ey = float(sgn), 0.0, 0.0, 1.0
        else:
            edge_y = y_hi if sgn > 0 else y_lo
            nx, ny, ex, ey = 0.0, float(sgn), 1.0, 0.0
        # step across, look up the new cell, and decide refraction vs reflection
        if axis == 0:
            x_guessed = edge_x + sgn * nudge
            lvl2, i2, j2, s2, cx2, cy2, rc2 = _cell_of(x_guessed, y)
        else:
            y_guessed = edge_y + sgn * nudge
            lvl2, i2, j2, s2, cx2, cy2, rc2 = _cell_of(x, y_guessed)
        beta2 = -sqrt(2.0 / rc2)
        b2x, b2y = beta2 * cx2 / rc2, beta2 * cy2 / rc2
        bn = b2x * nx + b2y * ny
        be = b2x * ex + b2y * ey
        p_par = px * ex + py * ey
        roots = _pr_roots_edge(H, p_par, bn, be, light)
        p_perp_in = px * nx + py * ny
        p_perp = None
        if roots is not None:
            cands = [c for c in roots if math.isfinite(c)]
            if cands:
                p_perp = min(cands, key=lambda c: abs(c - p_perp_in))
        if p_perp is None:
            # reflection: stay in the old cell, flip the perpendicular momentum
            px = px - 2.0 * p_perp_in * nx
            py = py - 2.0 * p_perp_in * ny
            if axis == 0:
                x = edge_x - sgn * nudge
            else:
                y = edge_y - sgn * nudge
            g2 = sqrt(1.0 + px * px + py * py) if not light else sqrt(px * px + py * py)
            if light:
                vr_after = (x * (px / g2 + bx) + y * (py / g2 + by)) / rr
            else:
                vr_after = (x * (px / g2 + bx) + y * (py / g2 + by)) / rr
        else:
            px = p_par * ex + p_perp * nx
            py = p_par * ey + p_perp * ny
            lvl, i, j, s, cx, cy, rc = lvl2, i2, j2, s2, cx2, cy2, rc2
            bx, by = b2x, b2y
            if axis == 0:
                x = edge_x + sgn * nudge
            else:
                y = edge_y + sgn * nudge
            if light:
                vr_after = (x * (px / sqrt(px * px + py * py) + bx)
                            + y * (py / sqrt(px * px + py * py) + by)) / rr
            else:
                g2 = sqrt(1.0 + px * px + py * py)
                vr_after = (x * (px / g2 + bx) + y * (py / g2 + by)) / rr
        seq.append((lvl, i, j))
        if vr_before > 0.0 and vr_after <= 0.0:
            phi_ev = atan2(y, x)
            if prev_phi is not None:
                dphi = 2.0 * pi + _wrap_pi(phi_ev - prev_phi)
                cycles.append((dphi, cyc_dt, len(seq),
                               r_peri if r_peri < float('inf') else rr, rr))
                if len(cycles) in SEQ_CYCLES:
                    seqs[len(cycles)] = seq[:]
                if len(cycles) >= ncycles:
                    break
            prev_phi = phi_ev
            cyc_dt = 0.0
            seq = []
            r_peri = float('inf')
        elif vr_before < 0.0 and vr_after >= 0.0:
            r_peri = min(r_peri, rr)
        if escape_r > 0.0 and rr > escape_r:
            escaped = True
            break
        if phi_cap is not None and phi_swept > phi_cap:
            break
    else:
        timeout = True
    return {'cycles': cycles, 'seqs': seqs, 'absorbed': absorbed, 'escaped': escaped,
            'timeout': timeout, 'points': points, 't': t, 'phi': phi_swept,
            'x': x, 'y': y, 'px': px, 'py': py}
