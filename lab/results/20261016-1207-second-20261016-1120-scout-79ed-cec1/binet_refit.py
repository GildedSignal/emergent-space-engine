#!/usr/bin/env python3
"""The per-band u_k refit for Binet cells, priced on the frozen r1 instrument (float64).

Arms:
  FROZEN  u_k = the band's geometric centre (the r1 rung's letter).
  CONT    frozen everywhere except an orbit contained in one band, whose band constant
          is the geometric mean of the orbit's own turning u's (fe85's open direction 2).
  GEO     one law: every visited band's constant is the geometric mean of the u-extremes
          the orbit attains inside that band (self-consistent fixed point).  For a band
          the orbit merely crosses this is *exactly* the frozen centre; it differs only
          where the orbit turns or is contained.

Oracle: ports of xtask/src/gr_oracle.rs periapsis_elliptic and gr_oracle_extended.rs
bound_period_quad / bound_constants, verbatim in form.
"""
import math, random, json, sys
import numpy as np
from scipy.special import ellipk as scipy_ellipk

PI = math.pi
TAU = 2.0 * PI

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
    chi = np.array
    t = refine(lambda x: (np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(x)))
                          * (p / (1.0 + e * np.cos(x))) ** 2 / angular
                          * energy / (1.0 - 2.0 * (1.0 + e * np.cos(x)) / p)))
    tau = refine(lambda x: np.sqrt(p / (p - 6.0 - 2.0 * e * np.cos(x)))
                 * (p / (1.0 + e * np.cos(x))) ** 2 / angular)
    return t, tau

# ---------------------------------------------------------------- band geometry
def band_of(u, m):
    x = -m * math.log2(u)
    k = math.ceil(x) - 1
    if u > 2.0 ** (-k / m):
        k += 1
    if u <= 2.0 ** (-(k + 1) / m):
        k -= 1
    return k

def band_edges(k, m):
    return 2.0 ** (-(k + 1) / m), 2.0 ** (-k / m)  # (u_lo, u_hi)

def band_centre(k, m):
    return 2.0 ** (-(k + 0.5) / m)

_GL16, _GL16w = np.polynomial.legendre.leggauss(16)

class Plunge(Exception):
    pass

def walk_cycle(u0, v0, invL2, E, L, m, consts=None, capture_u=0.0, max_events=20000):
    """One radial cycle from a turning start (or an inward start for capture).

    Returns dict with dphi, t, crossings, umin, umax, visited (band -> (mn, mx)),
    plunge flag.  consts: optional dict band -> u_k override (the refit)."""
    u, v, phi = u0, v0, 0.0
    visited = {}
    crossings = 0
    t_tot = 0.0
    umin = umax = u0
    start_turn = (v0 == 0.0)
    events = 0
    half = False  # passed apoapsis
    start_min = None
    k = None
    while events < max_events:
        events += 1
        if k is None:
            k = band_of(u, m)
        k_prev = k
        u_lo, u_hi = band_edges(k, m)
        c = consts.get(k, band_centre(k, m)) if consts is not None else band_centre(k, m)
        w2 = 1.0 - 6.0 * c
        up = (invL2 - 3.0 * c * c) / w2
        if start_turn and start_min is None:
            start_min = (u - up) < 0.0
        if w2 > 0.0:
            w = math.sqrt(w2)
            a, b = u - up, v / w
            R = math.hypot(a, b)
            if R < 1e-18:
                # degenerate circle: u == u_p exactly (the refit's fixed point)
                uu = np.full_like(_GL16, up)
                dphi = TAU / w
                t_tot += float(np.dot(_GL16w, E / (L * uu * uu * (1.0 - 2.0 * uu)))) * dphi / 2.0
                visited[k_prev] = (up, up)
                return dict(dphi=dphi, t=t_tot, crossings=0, umin=up, umax=up,
                            visited=visited, plunge=False, events=events + 1)
            alpha = math.atan2(-b, a) % TAU
            cands = []
            for edge in (u_lo, u_hi):
                q = (edge - up) / R
                if -1.0 <= q <= 1.0:
                    ac = math.acos(q)
                    for cand in (ac, TAU - ac):
                        while cand <= alpha + 1e-13:
                            cand += TAU
                        cands.append((cand, 'edge', edge))
            for cand in (PI, TAU):
                cc = cand
                while cc <= alpha + 1e-13:
                    cc += TAU
                cands.append((cc, 'turn', cand % TAU))
            _, kind, payload = min(cands, key=lambda x: x[0])
            tgt = min(cands, key=lambda x: x[0])[0]
            dphi = (tgt - alpha) / w
            # coordinate time over the segment
            ph = phi + dphi * 0.5 * (_GL16 + 1.0)
            uu = up + R * np.cos(w * (ph - phi) + alpha)
            t_tot += float(np.dot(_GL16w, E / (L * uu * uu * (1.0 - 2.0 * uu)))) * dphi / 2.0
            if kind == 'edge':
                u_new = payload          # exact edge: no acos round-trip
                v_new = -w * R * math.sin(tgt)
                k = k + 1 if payload == u_lo else k - 1
                crossings += 1
            else:
                u_new = up + R * math.cos(tgt)
                v_new = 0.0
                k = None
                if payload == PI:
                    if start_min:
                        return dict(dphi=phi + dphi, t=t_tot, crossings=crossings,
                                    umin=umin, umax=umax, visited=visited, plunge=False,
                                    events=events)
                    half = True
                elif not start_min and (start_turn or half):
                    return dict(dphi=phi + dphi, t=t_tot, crossings=crossings,
                                umin=umin, umax=umax, visited=visited, plunge=False,
                                events=events)
            phi += dphi
            mn, mx = min(u, u_new), max(u, u_new)
            if k_prev in visited:
                pm, pM = visited[k_prev]
                visited[k_prev] = (min(pm, mn), max(pM, mx))
            else:
                visited[k_prev] = (mn, mx)
            u, v = u_new, v_new
            umin, umax = min(umin, u), max(umax, u)
            if u <= capture_u:
                return dict(dphi=phi, t=t_tot, crossings=crossings, umin=umin, umax=umax,
                            visited=visited, plunge=False, absorbed=True, events=events)
        else:
            # hyperbolic band: turning possible only if B/A > 0
            lam = math.sqrt(-w2)
            A = (u - up + v / lam) / 2.0
            B = (u - up - v / lam) / 2.0
            ft = math.log(B / A) / (2.0 * lam) if A != 0.0 and (B / A) > 0.0 else float('inf')
            fseg = lambda x: up + A * math.exp(lam * x) + B * math.exp(-lam * x)
            # find exit: u reaching an edge or u >= 0.5 (horizon) before the turning
            target = None
            for edge in (u_lo, u_hi):
                lo, hi = 0.0, (ft if math.isfinite(ft) else 50.0 / lam)
                if fseg(hi) > edge > fseg(0.0) or fseg(hi) < edge < fseg(0.0):
                    for _ in range(80):
                        mid = 0.5 * (lo + hi)
                        if (fseg(mid) - edge) * (fseg(0.0) - edge) < 0.0:
                            hi = mid
                        else:
                            lo = mid
                    d = (lo + hi) / 2.0
                    if target is None or d < target[0]:
                        target = (d, edge)
            # horizon check: u reaching 0.5
            lo, hi = 0.0, (ft if math.isfinite(ft) else 50.0 / lam)
            if fseg(hi) > 0.5 > u:
                for _ in range(80):
                    mid = 0.5 * (lo + hi)
                    if fseg(mid) > 0.5:
                        hi = mid
                    else:
                        lo = mid
                d = (lo + hi) / 2.0
                if target is None or d < target[0]:
                    return dict(dphi=phi, t=0.0, crossings=crossings, umin=umin, umax=0.5,
                                visited=visited, plunge=True, absorbed=True, events=events)
            if math.isfinite(ft) and ft > 0.0 and (target is None or ft < target[0]):
                # turns inside the hyperbolic band
                u_new, v_new = fseg(ft), 0.0
                dphi = ft
                mn, mx = min(u, u_new), max(u, u_new)
                if k in visited:
                    pm, pM = visited[k]
                    visited[k] = (min(pm, mn), max(pM, mx))
                else:
                    visited[k] = (mn, mx)
                phi += dphi
                u, v = u_new, v_new
                umin = min(umin, u)
                half = True
                continue
            if target is None:
                raise Plunge("hyperbolic, unbounded")
            d, edge = target
            u_new, v_new = edge, (lam * A * math.exp(lam * d) - lam * B * math.exp(-lam * d))
            mn, mx = min(u, u_new), max(u, u_new)
            if k in visited:
                pm, pM = visited[k]
                visited[k] = (min(pm, mn), max(pM, mx))
            else:
                visited[k] = (mn, mx)
            phi += d
            u, v = u_new, v_new
            crossings += 1
            if u <= capture_u:
                return dict(dphi=phi, t=0.0, crossings=crossings, umin=umin, umax=umax,
                            visited=visited, plunge=False, absorbed=True, events=events)
            continue
    return dict(dphi=float('nan'), t=float('nan'), crossings=crossings, umin=umin, umax=umax,
                visited=visited, plunge=True, events=events)

def geo_consts(u0, v0, invL2, E, L, m, rounds=12):
    """Fixed point: constants from visited extremes, re-walk until settled."""
    consts = {}
    for rnd in range(rounds):
        res = walk_cycle(u0, v0, invL2, E, L, m, consts=consts)
        new = {}
        for k, (mn, mx) in res['visited'].items():
            u_lo, u_hi = band_edges(k, m)
            frozen = band_centre(k, m)
            if mn <= u_lo + 0.0 and mx >= u_hi - 0.0:
                new[k] = frozen          # crossing band: frozen exactly
            else:
                new[k] = math.sqrt(max(mn, 1e-300) * max(mx, 1e-300))
        delta = max((abs(new.get(k, 0.0) - consts.get(k, new[k])) / new[k] for k in new), default=0.0)
        consts = new
        if rnd >= 2 and delta < 1e-15:
            break
    return consts, res

def cont_consts(u0, v0, invL2, E, L, m):
    """Contained refit: one frozen pass; if the orbit's turnings share a band, refit it."""
    res = walk_cycle(u0, v0, invL2, E, L, m)
    kmin, kmax = band_of(res['umin'], m), band_of(res['umax'], m)
    if kmin == kmax and res['umin'] < res['umax']:
        k = kmax
        u_lo, u_hi = band_edges(k, m)
        if u_lo < res['umin'] and res['umax'] <= u_hi:
            return {k: math.sqrt(res['umin'] * res['umax'])}, res
    return {}, res

def advance_period(u0, v0, invL2, E, L, m, arm):
    if arm == 'FROZEN':
        res = walk_cycle(u0, v0, invL2, E, L, m)
    elif arm == 'CONT':
        consts, _ = cont_consts(u0, v0, invL2, E, L, m)
        res = walk_cycle(u0, v0, invL2, E, L, m, consts=consts)
    else:
        consts, res = geo_consts(u0, v0, invL2, E, L, m)
        res = walk_cycle(u0, v0, invL2, E, L, m, consts=consts)
    return res['dphi'] - TAU, res['t'], res

# ---------------------------------------------------------------- cases
def sampler_seeds():
    rng = random.Random(20260930)
    seeds = []
    while len(seeds) < 256:
        p = 10.0 ** (10.0 + rng.random() * 2.0) / 1000.0  # log-uniform in [10, 1000]
        p = math.exp(math.log(10.0) + rng.random() * (math.log(1000.0) - math.log(10.0)))
        e = rng.random() * 0.7
        if p >= 6.5 + 2.0 * e:
            seeds.append((p, e))
    return seeds

def circle_cases():
    out = []
    for p_t in np.geomspace(8.0, 1000.0, 40):
        j = round(m_glob * math.log2(p_t))
        for name, r in (('edge', 2.0 ** (j / m_glob)),
                        ('centre', 2.0 ** ((j + 0.5) / m_glob))):
            if 15.0 < r < 1100.0:
                out.append((r, name))
    return out

m_glob = 16

def run():
    report = {}
    seeds = sampler_seeds()
    oracle = {}
    for (p, e) in seeds:
        oracle[(p, e)] = (periapsis_elliptic(p, e), bound_period_quad(p, e)[0])
    print("oracle precomputed", flush=True)
    for m in (8, 16, 32):
        for arm in ('FROZEN', 'CONT', 'GEO'):
            prec = per = 0
            errs = []
            cr = []
            adv_shift = 0
            for (p, e) in seeds:
                E, L = bound_constants(p, e)
                invL2 = 1.0 / (L * L)
                u0 = (1.0 + e) / p
                try:
                    adv, t, res = advance_period(u0, 0.0, invL2, E, L, m, arm)
                    advf, tf, _ = advance_period(u0, 0.0, invL2, E, L, m, 'FROZEN')
                except (Plunge, ValueError, ZeroDivisionError):
                    errs.append(float('inf'))
                    continue
                adv_or, t_or = oracle[(p, e)]
                if abs(adv - adv_or) <= 0.01 * abs(adv_or):
                    prec += 1
                if abs(t - t_or) <= 0.001 * t_or:
                    per += 1
                errs.append(abs(adv - adv_or) / max(abs(adv_or), 1e-300))
                cr.append(res['crossings'])
                if abs(adv - advf) > 1e-6 * max(abs(advf), 1e-300):
                    adv_shift += 1
            report[f'sampler_m{m}_{arm}'] = dict(
                precession_pass=prec / 256, period_pass=per / 256,
                median_crossings=float(np.median(cr)),
                **{'advance_changed_beyond_1e-6': adv_shift},
                median_adv_err=float(np.median(errs)),
                worst_adv_err_95pct=float(np.percentile([x for x in errs if math.isfinite(x)], 95)))
            print(f"m={m} {arm}: prec {prec}/256 per {per}/256 cr_med {np.median(cr):.0f} "
                  f"adv_changed {adv_shift} med_err {np.median(errs):.2e}", flush=True)
    # ---- deterministic circles
    for m in (8, 16, 32):
        globals()['m_glob'] = m
        for arm in ('FROZEN', 'CONT', 'GEO'):
            worst_p = worst_a = 0.0
            n = 0
            for (r, place) in circle_cases():
                E, L = bound_constants(r, 0.0)
                invL2 = 1.0 / (L * L)
                adv, t, res = advance_period(1.0 / r, 0.0, invL2, E, L, m, arm)
                adv_or = periapsis_elliptic(r, 0.0)
                _, t_or = bound_period_quad(r, 0.0)
                worst_a = max(worst_a, abs(adv - adv_or) / max(abs(adv_or), 1e-300))
                worst_p = max(worst_p, abs(t - t_or) / t_or)
                n += 1
            report[f'circles_m{m}_{arm}'] = dict(n=n, worst_advance_rel=worst_a,
                                                 worst_period_rel=worst_p)
            print(f"circles m={m} {arm}: n={n} worst adv {worst_a:.2e} worst per {worst_p:.2e}",
                  flush=True)
    # ---- strong-field held-out rows
    rows = [(8.5, 0.9), (7.7, 0.7), (6.9, 0.3)]
    sf = {}
    for (p, e) in rows:
        E, L = bound_constants(p, e)
        invL2 = 1.0 / (L * L)
        adv_or = periapsis_elliptic(p, e)
        row = {}
        for arm in ('FROZEN', 'CONT', 'GEO'):
            try:
                adv, t, res = advance_period((1.0 + e) / p, 0.0, invL2, E, L, 16, arm)
                row[arm] = dict(adv_err=abs(adv - adv_or) / abs(adv_or),
                                period_err=abs(t - bound_period_quad(p, e)[0]) / bound_period_quad(p, e)[0])
            except (Plunge, ValueError, ZeroDivisionError):
                row[arm] = dict(adv_err=float('nan'), period_err=float('nan'))
        sf[f"p{p}_e{e}"] = row
        print(f"strong p={p} e={e}: " + " ".join(f"{a}:{row[a]['adv_err']:.2e}" for a in row), flush=True)
    report['strong_field_m16'] = sf
    # ---- ISCO rows (m=16)
    isco = {}
    for r, above in ((7.0, True), (5.5, False)):
        Lc = r / math.sqrt(r - 3.0)
        L = Lc * (1.01 if above else 0.99)
        u0 = 1.0 / r
        Ec = (r - 2.0) / math.sqrt(r * (r - 3.0))
        invL2 = 1.0 / (L * L)
        # a slightly-off-circular orbit: start at u0 with the circular speed mismatch
        # v0 from the exact first integral
        v2 = invL2 - u0 * u0 + 2.0 * u0 ** 3
        v0 = math.sqrt(max(v2, 0.0))
        res = {}
        for arm in ('FROZEN', 'CONT', 'GEO'):
            try:
                r_ = walk_cycle(0.1, -math.sqrt(max(invL2 - 0.01 + 2e-3, 0.0)) if invL2 > 0.008 else -1e-9,
                                invL2, Ec, L, 16, capture_u=0.5 - 1e-12, max_events=20000)
                res[arm] = 'plunge' if r_.get('absorbed') else 'bound'
            except (Plunge, ValueError):
                res[arm] = 'plunge'
        isco[f"r{r}"] = res
    report['isco_m16'] = isco
    print('isco', isco, flush=True)
    # ---- capture rows (matter E=1, and photon)
    cap = {}
    for x in (0.5, 0.9, 0.97, 1.03, 1.1, 1.5):
        L = 4.0 * x
        invL2 = 1.0 / (L * L)
        u0, E = 0.01, 1.0
        v0 = -math.sqrt(max(invL2 - u0 * u0 + 2 * u0 ** 3, 0.0))
        truth = 'absorbed' if x < 1.0 else 'escaped'
        row = {}
        for arm in ('FROZEN', 'CONT', 'GEO'):
            try:
                r = walk_cycle(u0, v0, invL2, E, L, 16, capture_u=0.5 - 1e-12)
                got = 'absorbed' if r.get('absorbed') else 'escaped'
            except (Plunge, ValueError):
                got = 'absorbed'
            row[arm] = got
        cap[f"L/4={x}"] = dict(truth=truth, **row)
    for x in (0.9, 0.97, 1.03, 1.1):
        b = 3.0 * math.sqrt(3.0) * x
        invL2 = 0.0
        u0 = 1e-6
        v0 = math.sqrt(1.0 / (b * b) - u0 * u0 + 2 * u0 ** 3)
        truth = 'absorbed' if x < 1.0 else 'escaped'
        row = {}
        for arm in ('FROZEN', 'CONT', 'GEO'):
            try:
                r = walk_cycle(u0, v0, 0.0, 1.0, b, 16, capture_u=0.5 - 1e-12)
                got = 'absorbed' if r.get('absorbed') else 'escaped'
            except (Plunge, ValueError):
                got = 'absorbed'
            row[arm] = got
        cap[f"b/bc={x}"] = dict(truth=truth, **row)
    report['capture_m16'] = cap
    mis = {arm: sum(1 for v in cap.values() if v[arm] != v['truth']) for arm in ('FROZEN', 'CONT', 'GEO')}
    report['capture_misclassified'] = mis
    print('capture misclassified', mis, flush=True)
    # ---- repeat exactness: two cycles identical (structure)
    rep = {}
    for arm in ('FROZEN', 'CONT', 'GEO'):
        ok = 0
        for (p, e) in seeds[:16]:
            E, L = bound_constants(p, e)
            invL2 = 1.0 / (L * L)
            adv, t, res = advance_period((1.0 + e) / p, 0.0, invL2, E, L, 16, arm)
            adv2, t2, _ = advance_period(res['umax'], 0.0, invL2, E, L, 16, arm)
            ok += int(abs(adv2 - adv) < 1e-12 * max(1.0, abs(adv)) and abs(t2 - t) < 1e-12 * t)
        rep[arm] = ok
    report['repeat_ok_of_16'] = rep
    print('repeat', rep, flush=True)
    with open(sys.argv[1] if len(sys.argv) > 1 else 'report.json', 'w') as f:
        json.dump(report, f, indent=1)

if __name__ == '__main__':
    run()
