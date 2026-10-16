#!/usr/bin/env python3
"""r1v2: the full frozen r1 case set, on the rebuilt walker, band-constant rule named.

Built from 20261016-1120-scout-79ed's binet_refit.py (oracle ports kept verbatim in
form; walker rebuilt). Fixes over that instrument, each named:
  F1  band_of: exact dyadic band edges were assigned two bands off; bands are
      half-open in u, (lo, hi], an edge body belongs to the band it is the upper
      edge of (this was the e=0 "circle defect").
  F2  hyperbolic bands (1-6u_k < 0): the bisection exit search is replaced by the
      exact quadratic in y = e^{lambda*phi} for edge/horizon hits and the closed-form
      turn ln(B/A)/(2*lambda); coordinate time is now integrated over hyperbolic
      segments too (was t=0).
  F3  escape detection: u below the start radius moving outward = escaped (was
      max_events exhaustion -> misread as plunge).
Added channels the scout run never measured: light deflection (64 seeds, exact GR
tail beyond r=1e4), matter capture (6 rows), photon capture (4 rows), ISCO (2 rows),
long runs (32 seeds x 1e4 cycles: shape + the letter's 1e-12 repeat bar), prograde,
crossings, the picture.

Arms: 'centre' (the r1 letter's frozen geometric-centre constant) and 'refit' (the
one-law form: each visited band's u_k = geometric mean of the u-extremes the orbit
attains there, self-consistent fixed point; a band the attained range covers keeps
the frozen centre exactly). The sampler draw is pinned to the letter (one random()
for p, one for e, redraw both on reject; light b's continue the stream).
"""
import math, random, json, sys, time
import numpy as np
from scipy.special import ellipk as scipy_ellipk

PI = math.pi
TAU = 2.0 * PI
LOG2 = math.log(2.0)

# ---------------------------------------------------------------- oracle ports
def ellip_k_minus_half_pi(m):
    if m >= 0.25:
        return scipy_ellipk(m) - PI / 2.0
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
    d = p - 6.0 + 2.0 * e
    s = math.sqrt(p / d)
    s_minus_1 = (6.0 - 2.0 * e) / d / (s + 1.0)
    return 4.0 * (s * ellip_k_minus_half_pi(4.0 * e / d) + PI / 2.0 * s_minus_1)

_GL32, _GL32w = np.polynomial.legendre.leggauss(32)
def _integrate_gl(a, b, pieces, f):
    edges = np.linspace(a, b, pieces + 1)
    tot = 0.0
    for i in range(pieces):
        x = 0.5 * (edges[i] + edges[i + 1]) + 0.5 * (edges[i + 1] - edges[i]) * _GL32
        tot += np.dot(_GL32w, f(x))
    return tot * 0.5 * (edges[1] - edges[0])

def bound_constants(p, e):
    energy = math.sqrt(((p - 2.0) ** 2 - 4.0 * e * e) / (p * (p - 3.0 - e * e)))
    angular = p / math.sqrt(p - 3.0 - e * e)
    return energy, angular

def bound_period_quad(p, e):
    energy, angular = bound_constants(p, e)
    def refine(f):
        pieces, v = 16, _integrate_gl(0.0, TAU, 16, f)
        while pieces < (1 << 14):
            pieces *= 2
            w = _integrate_gl(0.0, TAU, pieces, f)
            done = abs(w - v) <= 1e-14 * abs(w)
            v = w
            if done:
                break
        return v
    t = refine(lambda x: (np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(x)))
                          * (p / (1.0 + e * np.cos(x))) ** 2 / angular
                          * energy / (1.0 - 2.0 * (1.0 + e * np.cos(x)) / p)))
    tau = refine(lambda x: np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(x)))
                 * (p / (1.0 + e * np.cos(x))) ** 2 / angular)
    return t, tau

def deflection_quadrature(b):
    """Port of xtask/src/gr_oracle.rs deflection_quadrature (total, infinity to infinity)."""
    u0 = 1.0 / b
    for _ in range(100):
        h = 2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b)
        dh = 6.0 * u0 * u0 - 2.0 * u0
        step = h / dh
        u0 -= step
        if abs(step) <= 1e-17 * u0:
            break
    total = 0.0
    for j in range(64):
        a, c = j / 64.0, (j + 1) / 64.0
        for i in range(32):
            s = (a + c) / 2.0 + (c - a) / 2.0 * _GL32[i]
            u = u0 * (1.0 - s * s)
            qf, r = u0 + u, 2.0 * (u * u + u * u0 + u0 * u0)
            q = qf - r
            total += _GL32w[i] * (c - a) / 2.0 * 4.0 * math.sqrt(u0) * r / (
                math.sqrt(q * qf) * (math.sqrt(qf) + math.sqrt(q)))
    return total

def gr_tail(b, u_cut):
    """Exact GR phi span from u=0 to u_cut (one leg): integral of the exact integrand."""
    f = lambda u: 1.0 / np.sqrt(1.0 / (b * b) - u * u + 2.0 * u ** 3)
    return float(_integrate_gl(0.0, u_cut, 64, f))

# ---------------------------------------------------------------- band geometry
def band_of(u, m):  # F1
    x = -m * math.log2(u)
    k = math.floor(x)
    if x - k < 1e-9:      # exact dyadic edge: u is band round(x)'s upper edge
        k = int(round(x))
    return int(k)

def band_edges(k, m):
    return 2.0 ** (-(k + 1) / m), 2.0 ** (-k / m)  # (u_lo, u_hi]

def band_centre(k, m):
    return 2.0 ** (-(k + 0.5) / m)

_GL16, _GL16w = np.polynomial.legendre.leggauss(16)
_GL16t = tuple((float(_GL16[i]), float(_GL16w[i])) for i in range(16))

EPS_PHI = 1e-13

class Plunge(Exception):
    pass

# ---------------------------------------------------------------- one segment
def segment(u, v, k, m, invL2, consts):
    """Advance from (u, v) inside band k to the next event.

    Returns (dphi, u_new, v_new, kind, k_new, mode) where kind is 'edge' (cross to
    k_new), 'turn' (v_new == 0, k_new None) or 'capture' (u reached 1/2); v_new is
    None for edge/capture (the caller uses seg_exit_v). Returns None for the
    degenerate circle (u == the band ODE's equilibrium to 1e-14).
    """
    c = consts.get(k) if consts is not None else None
    if c is None:
        c = band_centre(k, m)
    u_lo, u_hi = band_edges(k, m)
    w2 = 1.0 - 6.0 * c
    up = (invL2 - 3.0 * c * c) / w2
    if w2 > 0.0:
        w = math.sqrt(w2)
        a, b = u - up, v / w
        R = math.hypot(a, b)
        if R <= 1e-14 * abs(up):
            return None
        psi = math.atan2(b, a)
        def first_hit(theta_target):
            d = (theta_target + psi) % TAU / w
            if d <= EPS_PHI:
                d += TAU / w
            return d
        cands = [(first_hit(0.0), 'turn', 1.0), (first_hit(PI), 'turn', -1.0)]
        for edge, kk in ((u_hi, k - 1), (u_lo, k + 1)):
            q = (edge - up) / R
            if -1.0 <= q <= 1.0:
                ac = math.acos(q)
                kind = 'capture' if edge >= 0.5 else 'edge'
                pay = None if kind == 'capture' else (edge, kk)
                cands.append((first_hit(ac), kind, pay))
                cands.append((first_hit(-ac), kind, pay))
        qcap = (0.5 - up) / R
        if -1.0 <= qcap <= 1.0:
            ac = math.acos(qcap)
            cands.append((first_hit(ac), 'capture', None))
            cands.append((first_hit(-ac), 'capture', None))
        cands.sort(key=lambda x: x[0])
        dphi, kind, payload = cands[0]
        if kind == 'edge':
            u_new, v_new, k_new = payload[0], None, payload[1]
        elif kind == 'turn':
            u_new, v_new, k_new = up + payload * R, 0.0, None
        else:
            u_new, v_new, k_new = 0.5, None, None
        return dphi, u_new, v_new, kind, k_new, ('rot', up, R, psi, w)
    else:
        lam = math.sqrt(-w2)
        A = (u - up + v / lam) * 0.5
        B = (u - up - v / lam) * 0.5
        cands = []
        if A != 0.0 and (A * B) > 0.0 and (B / A) > 1.0:
            d = math.log(B / A) / (2.0 * lam)
            if d > EPS_PHI:
                cands.append((d, 'turn', None))
        for edge, kk in ((u_hi, k - 1), (u_lo, k + 1), (0.5, None)):
            C = edge - up
            disc = C * C - 4.0 * A * B
            if disc < 0.0:
                continue
            sq = math.sqrt(disc)
            if A != 0.0:
                roots = ((C + sq) / (2.0 * A), (C - sq) / (2.0 * A))
            elif B != 0.0:
                roots = (C / (2.0 * B),)
            else:
                roots = ()
            kind = 'capture' if edge >= 0.5 else 'edge'
            for root in roots:
                if root >= 1.0 + 1e-12 and root < 1e308:
                    d = math.log(root) / lam
                    if d > EPS_PHI:
                        cands.append((d, kind, (edge, kk) if kind == 'edge' else None))
        if not cands:
            raise Plunge("hyperbolic segment with no exit")
        cands.sort(key=lambda x: x[0])
        dphi, kind, payload = cands[0]
        if kind == 'edge':
            u_new, v_new, k_new = payload[0], None, payload[1]
        elif kind == 'turn':
            u_new, v_new, k_new = up + 2.0 * math.sqrt(A * B), 0.0, None
        else:
            u_new, v_new, k_new = 0.5, None, None
        return dphi, u_new, v_new, kind, k_new, ('hyp', up, A, B, lam)

def seg_time(dphi, mode, E, L):
    """Integral of dt/dphi = E/(L u^2 (1-2u)) over one segment via GL16."""
    tot = 0.0
    half = 0.5 * dphi
    if mode[0] == 'rot':
        _, up, R, psi, w = mode
        for x, wx in _GL16t:
            ph = half * (x + 1.0)
            uu = up + R * math.cos(w * ph - psi)
            tot += wx * E / (L * uu * uu * (1.0 - 2.0 * uu))
    else:
        _, up, A, B, lam = mode
        if lam * dphi > 700.0:
            raise Plunge("hyperbolic time integral overflow")
        for x, wx in _GL16t:
            s = half * (x + 1.0)
            e1 = math.exp(lam * s)
            uu = up + A * e1 + B / e1
            tot += wx * E / (L * uu * uu * (1.0 - 2.0 * uu))
    return tot * half

def seg_exit_v(dphi, mode):
    """v = du/dphi at the segment end (before snapping)."""
    if mode[0] == 'rot':
        _, up, R, psi, w = mode
        return -R * w * math.sin(w * dphi - psi)
    _, up, A, B, lam = mode
    e1 = math.exp(lam * dphi)
    return lam * (A * e1 - B / e1)
# ---------------------------------------------------------------- walkers
def walk_cycle(u0, m, invL2, E, L, consts=None, max_events=20000, trace=None):
    """One radial cycle from a turning start (u0, v0=0). Returns dict.

    The walk is exactly reversible per band, so the cycle closes to rounding; the
    returned apoapsis u_end is audited by the caller.
    """
    u, v, phi, t = u0, 0.0, 0.0, 0.0
    k = band_of(u, m)
    visited = {}
    crossings = 0
    turns = 0
    umin = umax = u0
    events = 0
    n_tr = 0
    while events < max_events:
        events += 1
        k_seg = k
        seg = segment(u, v, k, m, invL2, consts)
        if seg is None:  # degenerate circle
            c = consts.get(k) if consts else None
            c = c if c is not None else band_centre(k, m)
            uu = (invL2 - 3.0 * c * c) / (1.0 - 6.0 * c)
            dphi = TAU / math.sqrt(1.0 - 6.0 * c)
            t += dphi * E / (L * uu * uu * (1.0 - 2.0 * uu))
            if k in visited:
                pm, pM = visited[k]
                visited[k] = (min(pm, uu), max(pM, uu))
            else:
                visited[k] = (uu, uu)
            return dict(dphi=phi + dphi, t=t, crossings=crossings, umin=umin, umax=umax,
                        visited=visited, absorbed=False, u_end=uu, events=events,
                        n_turn=0, degenerate=True)
        dphi, u_new, v_new, kind, k_new, mode = seg
        t += seg_time(dphi, mode, E, L)
        if trace is not None:
            trace.append((phi + dphi, u_new))
        phi += dphi
        mn, mx = min(u, u_new), max(u, u_new)
        if k_seg in visited:
            pm, pM = visited[k_seg]
            visited[k_seg] = (min(pm, mn), max(pM, mx))
        else:
            visited[k_seg] = (mn, mx)
        if kind == 'edge':
            v_new = seg_exit_v(dphi, mode)
            k = k_new
            crossings += 1
        elif kind == 'capture':
            return dict(dphi=phi, t=t, crossings=crossings, umin=umin, umax=0.5,
                        visited=visited, absorbed=True, u_end=0.5, events=events, n_turn=turns)
        else:  # turn
            k = band_of(u_new, m)
            turns += 1
            if turns >= 2:
                umin, umax = min(umin, u_new), max(umax, u_new)
                return dict(dphi=phi, t=t, crossings=crossings, umin=umin, umax=umax,
                            visited=visited, absorbed=False, u_end=u_new, events=events,
                            n_turn=turns)
        u, v = u_new, v_new
        umin, umax = min(umin, u_new), max(umax, u_new)
    raise Plunge("cycle max_events exhausted")

def walk_scatter(u0, v0, m, invL2, E, L, consts=None, u_esc=None, max_events=20000):
    """Scattering/capture walk from (u0, v0): ends at u>=0.5 (absorbed), u<u_esc
    (escaped), or events exhausted (raises). Returns dict with dphi and visited."""
    u, v, phi = u0, v0, 0.0
    k = band_of(u, m)
    visited = {}
    crossings = 0
    turned = False
    events = 0
    while events < max_events:
        events += 1
        k_seg = k
        seg = segment(u, v, k, m, invL2, consts)
        if seg is None:
            c = consts.get(k) if consts else None
            c = c if c is not None else band_centre(k, m)
            uu = (invL2 - 3.0 * c * c) / (1.0 - 6.0 * c)
            dphi = TAU / math.sqrt(1.0 - 6.0 * c)
            pm, pM = visited.get(k, (uu, uu))
            visited[k] = (min(pm, uu), max(pM, uu))
            return dict(dphi=phi + dphi, visited=visited, crossings=crossings,
                        absorbed=True, escaped=False, events=events,
                        u_end=uu, note='degenerate orbit in scatter')
        dphi, u_new, v_new, kind, k_new, mode = seg
        phi += dphi
        mn, mx = min(u, u_new), max(u, u_new)
        if k_seg in visited:
            pm, pM = visited[k_seg]
            visited[k_seg] = (min(pm, mn), max(pM, mx))
        else:
            visited[k_seg] = (mn, mx)
        if u_esc is not None:
            # exact stop at u_esc inside this segment (no band-edge overshoot)
            if mode[0] == 'rot':
                _, up, R, psi, w = mode
                q = (u_esc - up) / R
                if -1.0 <= q <= 1.0:
                    ac = math.acos(q)
                    for tgt in (ac, -ac):
                        d = (tgt + psi) % TAU / w
                        if d <= EPS_PHI:
                            d += TAU / w
                        if d < dphi - 1e-15:
                            return dict(dphi=phi - dphi + d, visited=visited,
                                        crossings=crossings, absorbed=False, escaped=True,
                                        events=events, u_end=u_esc,
                                        v_end=seg_exit_v(d, mode), turned=turned)
            else:
                _, up, A, B, lam = mode
                C = u_esc - up
                disc = C * C - 4.0 * A * B
                if disc >= 0.0 and A != 0.0:
                    sq = math.sqrt(disc)
                    for root in ((C + sq) / (2.0 * A), (C - sq) / (2.0 * A)):
                        if 1.0 < root < 1e308:
                            d = math.log(root) / lam
                            if EPS_PHI < d < dphi - 1e-15:
                                return dict(dphi=phi - dphi + d, visited=visited,
                                            crossings=crossings, absorbed=False,
                                            escaped=True, events=events, u_end=u_esc,
                                            v_end=seg_exit_v(d, mode), turned=turned)
        if kind == 'edge':
            v_new = seg_exit_v(dphi, mode)
            k = k_new
            crossings += 1
        elif kind == 'turn':
            k = band_of(u_new, m)
            turned = True
        else:  # capture
            return dict(dphi=phi, visited=visited, crossings=crossings, absorbed=True,
                        escaped=False, events=events, u_end=0.5, turned=turned)
        u, v = u_new, v_new
        if u_esc is not None and u < u_esc:
            return dict(dphi=phi, visited=visited, crossings=crossings, absorbed=False,
                        escaped=True, events=events, u_end=u, turned=turned)

# ---------------------------------------------------------------- refit laws
def refit_from_visited(visited, m):
    new = {}
    for k, (mn, mx) in visited.items():
        u_lo, u_hi = band_edges(k, m)
        if mn <= u_lo + 1e-15 * u_lo and mx >= u_hi - 1e-15 * u_hi:
            new[k] = band_centre(k, m)          # crossed: frozen exactly
        else:
            new[k] = math.sqrt(max(mn, 1e-300) * max(mx, 1e-300))
    return new

def consts_bound(u0, m, invL2, E, L, arm, rounds=12):
    """Constants for a bound orbit; returns (consts, last_walk)."""
    if arm == 'centre':
        return {}, None
    consts = {}
    res = None
    for rnd in range(rounds):
        res = walk_cycle(u0, m, invL2, E, L, consts=consts)
        new = refit_from_visited(res['visited'], m)
        delta = max((abs(new.get(k, 0.0) - consts.get(k, new[k])) / new[k]
                     for k in new), default=0.0)
        consts = new
        if rnd >= 1 and delta < 1e-15:
            break
    return consts, res

def consts_scatter(u0, v0, m, invL2, E, L, arm, u_esc, rounds=12):
    if arm == 'centre':
        return {}
    consts = {}
    for rnd in range(rounds):
        res = walk_scatter(u0, v0, m, invL2, E, L, consts=consts, u_esc=u_esc)
        if res['absorbed'] and not res.get('turned'):
            return {}          # pure plunge: no turning band, refit is the frozen law
        new = refit_from_visited(res['visited'], m)
        delta = max((abs(new.get(k, 0.0) - consts.get(k, new[k])) / new[k]
                     for k in new), default=0.0)
        consts = new
        if rnd >= 1 and delta < 1e-15:
            break
    return consts

def advance_period(u0, m, invL2, E, L, arm):
    """Advance per radial cycle and cycle time under the named arm."""
    consts, res = consts_bound(u0, m, invL2, E, L, arm)
    if res is not None and not res['absorbed'] and abs(res['u_end'] - u0) <= 1e-9 * u0:
        r = res
    else:
        r = walk_cycle(u0, m, invL2, E, L, consts=consts)
    return r['dphi'] - TAU, r['t'], r

# ---------------------------------------------------------------- cases
def sampler_seeds():
    rng = random.Random(20260930)
    seeds = []
    while len(seeds) < 256:
        p = math.exp(math.log(10.0) + rng.random() * (math.log(1000.0) - math.log(10.0)))
        e = rng.random() * 0.7
        if p >= 6.5 + 2.0 * e:
            seeds.append((p, e))
    light = [math.exp(math.log(10.0) + rng.random() * (math.log(1000.0) - math.log(10.0)))
             for _ in range(64)]
    return seeds, light

def circle_cases(m):
    """12 bands covering r in [6.5, 1000] geometrically; 5 offsets each."""
    out = []
    for kk in np.linspace(round(m * math.log2(6.5)), round(m * math.log2(1000.0)), 12):
        k = int(round(kk))
        uc = band_centre(k, m)
        if not (1.0 / 1000.0 <= uc <= 1.0 / 6.5):
            continue
        for f in (-0.99, -0.5, 0.0, 0.5, 0.99):
            u0 = uc * 2.0 ** (f / (2.0 * m))
            out.append((1.0 / u0, u0, f))
    return out

STRONG_ROWS = [(8.5, 0.9), (7.7, 0.7), (6.9, 0.3), (6.5, 0.1), (9.5, 0.5), (12, 0.7)]

def run_config(m, arm, seeds, light_bs, oracle, long_oracle):
    cfg = f"binet-m{m}-{arm}"
    t0 = time.time()
    met = {}
    # ---- sampler: prec, prog, period, crossings
    prec = per = prog = 0
    errs, cr = [], []
    throws = 0
    for (p, e) in seeds:
        E, L = bound_constants(p, e)
        invL2 = 1.0 / (L * L)
        u0 = (1.0 + e) / p
        try:
            adv, t, res = advance_period(u0, m, invL2, E, L, arm)
        except (Plunge, ValueError, ZeroDivisionError, OverflowError):
            throws += 1
            errs.append(float('inf'))
            continue
        adv_or, t_or = oracle[(p, e)]
        if abs(adv - adv_or) <= 0.01 * abs(adv_or):
            prec += 1
        if t_or > 0 and abs(t - t_or) <= 0.001 * t_or:
            per += 1
        if adv > 0:
            prog += 1
        errs.append(abs(adv - adv_or) / max(abs(adv_or), 1e-300))
        cr.append(res['crossings'])
    met['precession_pass_fraction'] = prec / 256.0
    met['period_pass_fraction'] = per / 256.0
    met['prograde_fraction'] = prog / 256.0
    met['crossings_per_cycle'] = float(np.median(cr)) if cr else float('nan')
    met['median_adv_err'] = float(np.median(errs))
    met['sampler_throws'] = throws
    # ---- deterministic near-circular rows
    nc_pass = 0
    nc_rows = []
    for (r, u0, f) in circle_cases(m):
        E, L = bound_constants(r, 0.0)
        invL2 = 1.0 / (L * L)
        try:
            adv, t, res = advance_period(u0, m, invL2, E, L, arm)
            adv_or = periapsis_elliptic(r, 0.0)
            t_or = bound_period_quad(r, 0.0)[0]
            ok = (abs(adv - adv_or) <= 0.01 * abs(adv_or)) and (abs(t - t_or) <= 0.001 * t_or)
            nc_rows.append(dict(r=r, f=f, adv_rel=abs(adv - adv_or) / abs(adv_or),
                                per_rel=abs(t - t_or) / t_or, ok=bool(ok)))
        except (Plunge, ValueError, ZeroDivisionError, OverflowError) as ex:
            nc_rows.append(dict(r=r, f=f, adv_rel=float('inf'), per_rel=float('inf'),
                                ok=False, exc=type(ex).__name__))
        nc_pass += nc_rows[-1]['ok']
    met['nearcircular_pass_fraction'] = nc_pass / len(nc_rows)
    met['_nearcircular_worst'] = max((r['adv_rel'] for r in nc_rows), default=float('nan'))
    met['_nearcircular_worst_per'] = max((r['per_rel'] for r in nc_rows), default=float('nan'))
    # ---- strong-field rows
    sf_rows = []
    for (p, e) in STRONG_ROWS:
        E, L = bound_constants(p, e)
        invL2 = 1.0 / (L * L)
        adv_or = periapsis_elliptic(p, e)
        t_or = bound_period_quad(p, e)[0]
        try:
            adv, t, res = advance_period((1.0 + e) / p, m, invL2, E, L, arm)
            ok = (abs(adv - adv_or) <= 0.01 * abs(adv_or)) and (abs(t - t_or) <= 0.001 * t_or)
            sf_rows.append(dict(p=p, e=e, adv_rel=abs(adv - adv_or) / abs(adv_or),
                                per_rel=abs(t - t_or) / t_or, ok=bool(ok),
                                crossings=res['crossings']))
        except (Plunge, ValueError, ZeroDivisionError, OverflowError) as ex:
            sf_rows.append(dict(p=p, e=e, adv_rel=float('inf'), per_rel=float('inf'),
                                ok=False, exc=type(ex).__name__))
    met['strongfield_pass_fraction'] = sum(r['ok'] for r in sf_rows) / len(sf_rows)
    met['_strongrows'] = sf_rows
    # ---- light deflection (64 seeds, exact GR tail beyond r=1e4)
    defl = 0
    dmax = 0.0
    u_cut = 1e-4
    for b in light_bs:
        consts = consts_scatter(u_cut, math.sqrt(1.0 / (b * b) - u_cut * u_cut + 2e-12),
                                m, 0.0, 1.0, b, arm, u_esc=u_cut * (1.0 - 1e-9))
        res = walk_scatter(u_cut, math.sqrt(1.0 / (b * b) - u_cut * u_cut + 2e-12),
                           m, 0.0, 1.0, b, consts=consts, u_esc=u_cut * (1.0 - 1e-9))
        measured = res['dphi'] + 2.0 * gr_tail(b, u_cut) - PI
        dor = deflection_quadrature(b)
        rel = abs(measured - dor) / dor
        dmax = max(dmax, rel)
        if rel <= 0.01:
            defl += 1
    met['deflection_pass_fraction'] = defl / 64.0
    met['_defl_worst_rel'] = dmax
    # ---- matter capture
    mis = 0
    cap_rows = []
    for x in (0.5, 0.9, 0.97, 1.03, 1.1, 1.5):
        L = 4.0 * x
        invL2 = 1.0 / (L * L)
        u0 = 0.01
        v0 = math.sqrt(max(2.0 * u0 / (L * L) - u0 * u0 + 2 * u0 ** 3, 0.0))
        truth = 'absorbed' if x < 1.0 else 'escaped'
        consts = consts_scatter(u0, v0, m, invL2, 1.0, L, arm, u_esc=1e-6)
        try:
            res = walk_scatter(u0, v0, m, invL2, 1.0, L, consts=consts, u_esc=1e-6)
            got = 'absorbed' if res['absorbed'] else 'escaped'
        except Plunge:
            got = 'void'
        cap_rows.append(dict(row=f"L/4={x}", truth=truth, got=got))
        mis += got != truth
    for x in (0.9, 0.97, 1.03, 1.1):
        b = 3.0 * math.sqrt(3.0) * x
        u0 = 1e-4
        v0 = math.sqrt(1.0 / (b * b) - u0 * u0 + 2 * u0 ** 3)
        truth = 'absorbed' if x < 1.0 else 'escaped'
        consts = consts_scatter(u0, v0, m, 0.0, 1.0, b, arm, u_esc=u0 * (1.0 - 1e-9))
        try:
            res = walk_scatter(u0, v0, m, 0.0, 1.0, b, consts=consts,
                               u_esc=u0 * (1.0 - 1e-9))
            got = 'absorbed' if res['absorbed'] else 'escaped'
        except Plunge:
            got = 'void'
        cap_rows.append(dict(row=f"b/bc={x}", truth=truth, got=got))
        mis += got != truth
    met['capture_misclassified'] = mis
    met['_caprows'] = cap_rows
    # ---- ISCO
    isco_ok = True
    isco_rows = []
    for r, above in ((7.0, True), (5.5, False)):
        Lc = r / math.sqrt(r - 3.0)
        L = Lc * (1.01 if above else 0.99)
        u0 = 1.0 / r
        E = math.sqrt((1.0 - 2.0 * u0) * (1.0 + L * L * u0 * u0))
        invL2 = 1.0 / (L * L)
        want = 'bound' if above else 'plunge'
        try:
            if above:
                consts, _ = consts_bound(u0, m, invL2, E, L, arm)
                ok = True
                u_start = u0
                for cyc in range(100):
                    res = walk_cycle(u_start, m, invL2, E, L, consts=consts)
                    if res['absorbed']:
                        ok = False
                        break
                    u_start = res['u_end']
                got = 'bound' if ok else 'plunge'
            else:
                consts = consts_scatter(u0, 0.0, m, invL2, E, L, arm, u_esc=1e-6)
                got = 'plunge'
                u_start = u0
                for cyc in range(50):
                    res = walk_scatter(u_start, 0.0, m, invL2, E, L, consts=consts,
                                       u_esc=1e-6)
                    if res['absorbed']:
                        break
                    u_start = res['u_end']  # turned: walk the next cycle
                else:
                    got = 'bound'
        except Plunge:
            got = 'plunge' if not above else 'plunge'
        isco_rows.append(dict(r=r, want=want, got=got))
        isco_ok = isco_ok and (got == want)
    met['isco_correct'] = 1 if isco_ok else 0
    met['_iscorows'] = isco_rows
    # ---- long runs: first 32 seeds, 1e4 cycles (shape + repeat)
    nlong = {8: 32, 16: 32, 32: 16}[m]   # pre-registered cut: m32 halved (predictions.md)
    NCYC = 10000
    shape_ok = 0
    repeat_ok = 0
    lr_detail = []
    for si in range(nlong):
        (p, e) = seeds[si]
        E, L = bound_constants(p, e)
        invL2 = 1.0 / (L * L)
        u0 = (1.0 + e) / p
        try:
            consts, _ = consts_bound(u0, m, invL2, E, L, arm)
            cyc1 = walk_cycle(u0, m, invL2, E, L, consts=consts)
            dphi1, t1 = cyc1['dphi'], cyc1['t']
            uper1, uap1 = cyc1['umin'], cyc1['umax']
            u_start = cyc1['u_end']
            seq2 = None
            ok_shape = True
            ok_rep = True
            dmax = tmax = 0.0
            cyc2 = walk_cycle(u_start, m, invL2, E, L, consts=consts)
            dmax = max(dmax, abs(cyc2['dphi'] - dphi1) / max(abs(dphi1), 1e-300))
            tmax = max(tmax, abs(cyc2['t'] - t1) / max(t1, 1e-300))
            if (abs(cyc2['umin'] - uper1) > 1e-9 * uper1
                    or abs(cyc2['umax'] - uap1) > 1e-9 * uap1):
                ok_rep = False  # crossing structure changed
            u_cur = cyc2['u_end']
            for cyc in range(3, NCYC + 1):
                rc = walk_cycle(u_cur, m, invL2, E, L, consts=consts)
                if rc['absorbed']:
                    ok_shape = ok_rep = False
                    break
                dmax = max(dmax, abs(rc['dphi'] - dphi1) / max(abs(dphi1), 1e-300))
                tmax = max(tmax, abs(rc['t'] - t1) / max(t1, 1e-300))
                if (abs(rc['umin'] - uper1) > 0.01 * uper1
                        or abs(rc['umax'] - uap1) > 0.01 * uap1):
                    ok_shape = False
                u_cur = rc['u_end']
            if dmax > 1e-12 or tmax > 1e-12:
                ok_rep = False
            shape_ok += ok_shape
            repeat_ok += ok_rep
            lr_detail.append(dict(p=p, e=e, dphi_drift=dmax, t_drift=tmax,
                                  ok_shape=bool(ok_shape), ok_rep=bool(ok_rep)))
        except (Plunge, ValueError, ZeroDivisionError, OverflowError) as ex:
            lr_detail.append(dict(p=seeds[si][0], e=seeds[si][1],
                                  exc=type(ex).__name__, ok_shape=False, ok_rep=False))
    met['shape_kept_fraction'] = shape_ok / nlong
    met['cycle_repeat_fraction'] = repeat_ok / nlong
    met['_longruns'] = dict(n=nlong, cycles=NCYC,
                            worst_dphi_drift=max((d.get('dphi_drift', 0) or 0)
                                                 for d in lr_detail),
                            worst_t_drift=max((d.get('t_drift', 0) or 0)
                                              for d in lr_detail),
                            n_exc=sum('exc' in d for d in lr_detail))
    met['_elapsed_s'] = time.time() - t0
    return cfg, met

CRITERIA = [
    ('prec', 'behaviour', 'precession_pass_fraction', '>=', 0.99),
    ('prog', 'type', 'prograde_fraction', '>=', 1.0),
    ('period', 'behaviour', 'period_pass_fraction', '>=', 0.99),
    ('defl', 'behaviour', 'deflection_pass_fraction', '>=', 0.99),
    ('capture', 'behaviour', 'capture_misclassified', '<=', 0),
    ('isco', 'behaviour', 'isco_correct', '>=', 1),
    ('shape', 'type', 'shape_kept_fraction', '>=', 0.99),
    ('repeat', 'type', 'cycle_repeat_fraction', '>=', 0.99),
    ('cost', 'cost', 'crossings_per_cycle', '<=', 512),
    ('nearcirc', 'behaviour', 'nearcircular_pass_fraction', '>=', 0.99),
    ('strongf', 'behaviour', 'strongfield_pass_fraction', '>=', 1.0),
]

def judge(met):
    rows = []
    all_pass = True
    for cid, kind, key, op, thr in CRITERIA:
        v = met.get(key)
        ok = (v >= thr) if op == '>=' else (v <= thr)
        all_pass = all_pass and ok
        rows.append(f"  {cid:9s} {kind:9s} {key:28s} {v!r:24s} {op} {thr}  {'PASS' if ok else 'FAIL'}")
    return all_pass, rows

def picture(all_metrics, seeds, light_bs, path):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    p, e = 20.0, 0.5
    E, L = bound_constants(p, e)
    invL2 = 1.0 / (L * L)
    u0 = (1.0 + e) / p
    ax = axes[0]
    for m, arm, style in ((16, 'centre', '--'), (16, 'refit', '-'),
                          (32, 'centre', '--'), (32, 'refit', '-')):
        consts, _ = consts_bound(u0, m, invL2, E, L, arm)
        uu, v, phi, k = u0, 0.0, 0.0, band_of(u0, m)
        tr = [(0.0, uu)]
        for _ in range(5):
            turns = 0
            while turns < 2:
                seg = segment(uu, v, k, m, invL2, consts)
                if seg is None:
                    break
                dphi, un, vn, kind, kn, mode = seg
                phi += dphi
                tr.append((phi, un))
                if kind == 'edge':
                    vn = seg_exit_v(dphi, mode)
                    k = kn
                elif kind == 'turn':
                    vn = 0.0
                    k = band_of(un, m)
                    turns += 1
                uu, v = un, vn
        xs = [math.cos(ph) / ub for ph, ub in tr]
        ys = [math.sin(ph) / ub for ph, ub in tr]
        ax.plot(xs, ys, style, lw=1.6 if arm == 'refit' else 0.9, alpha=0.8,
                label=f"m{m}-{arm}")
    ax.plot(0, 0, 'k*', ms=10)
    ax.set_title("p=20, e=0.5, 5 cycles (dashed=centre, solid=refit)")
    ax.set_aspect('equal')
    ax.legend(fontsize=7)
    ax2 = axes[1]
    for b in (10.0, 20.0, 50.0, 200.0, 1000.0):
        u_cut = 1e-4
        v0 = math.sqrt(1.0 / (b * b) - u_cut * u_cut + 2e-12)
        consts = consts_scatter(u_cut, v0, 16, 0.0, 1.0, b, 'refit', u_esc=u_cut * (1 - 1e-9))
        res = walk_scatter(u_cut, v0, 16, 0.0, 1.0, b, consts=consts,
                           u_esc=u_cut * (1 - 1e-9))
        uu, v, phi, k = u_cut, v0, 0.0, band_of(u_cut, 16)
        tr = [(phi, uu)]
        while True:
            seg = segment(uu, v, k, 16, 0.0, consts)
            if seg is None:
                break
            dphi, un, vn, kind, kn, mode = seg
            phi += dphi
            tr.append((phi, un))
            if kind == 'edge':
                vn = seg_exit_v(dphi, mode)
                k = kn
            elif kind == 'turn':
                vn = 0.0
                k = band_of(un, 16)
            else:
                break
            uu, v = un, vn
            if uu < u_cut:
                break
        xs = [math.cos(ph) / ub for ph, ub in tr]
        ys = [math.sin(ph) / ub for ph, ub in tr]
        ax2.plot(xs, ys, lw=1.0, label=f"b={b:g}")
    ax2.plot(0, 0, 'k*', ms=10)
    ax2.set_title("light paths, m16-refit")
    ax2.set_aspect('equal')
    ax2.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    return path

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else 'report.json'
    seeds, light_bs = sampler_seeds()
    print("seeds drawn (letter-pinned)", len(seeds), len(light_bs), flush=True)
    oracle = {}
    for (p, e) in seeds:
        oracle[(p, e)] = (periapsis_elliptic(p, e), bound_period_quad(p, e)[0])
    print("oracle precomputed", flush=True)
    all_m = {}
    for m in (8, 16, 32):
        for arm in ('centre', 'refit'):
            cfg, met = run_config(m, arm, seeds, light_bs, oracle, None)
            all_m[cfg] = met
            print(f"[{cfg}] prec {met['precession_pass_fraction']:.4f} "
                  f"per {met['period_pass_fraction']:.4f} "
                  f"prog {met['prograde_fraction']:.4f} "
                  f"defl {met['deflection_pass_fraction']:.4f} "
                  f"cap {met['capture_misclassified']} isco {met['isco_correct']} "
                  f"shape {met['shape_kept_fraction']:.4f} "
                  f"rep {met['cycle_repeat_fraction']:.4f} "
                  f"cr {met['crossings_per_cycle']:.0f} "
                  f"nc {met['nearcircular_pass_fraction']:.4f} "
                  f"sf {met['strongfield_pass_fraction']:.4f} "
                  f"({met['_elapsed_s']:.1f}s)", flush=True)
    # verdict table
    verdict = {}
    print("\n== r1v2 verdict (freeze: r1v2-rings-band-constant.md) ==")
    for cfg, met in all_m.items():
        ok, rows = judge(met)
        verdict[cfg] = dict(passes=ok,
                            fails=[r.split()[0] for r in rows if 'FAIL' in r])
        print(f"{cfg}: {'PASS' if ok else 'FAIL'} (failed: {verdict[cfg]['fails']})")
        for r in rows:
            print(r)
    metrics = {cfg: {k: v for k, v in met.items()} for cfg, met in all_m.items()}
    pic = picture(all_m, seeds, light_bs, 'r1v2-picture.png')
    with open(out_path, 'w') as f:
        json.dump(dict(metrics=metrics, verdict=verdict, picture=pic), f, indent=1)
    print("\npicture:", pic, flush=True)
    # detail dumps for the dossier
    with open('detail.json', 'w') as f:
        json.dump({cfg: dict(nearcircular=met.get('_nearcircular_worst'),
                             nearcircular_per=met.get('_nearcircular_worst_per'),
                             strongrows=met.get('_strongrows'),
                             caprows=met.get('_caprows'),
                             iscorows=met.get('_iscorows'),
                             longruns=met.get('_longruns'),
                             defl_worst=met.get('_defl_worst_rel'),
                             sampler_throws=met.get('sampler_throws'),
                             median_adv_err=met.get('median_adv_err'))
                   for cfg, met in all_m.items()}, f, indent=1, default=float)
    print("done", flush=True)

if __name__ == '__main__':
    main()
