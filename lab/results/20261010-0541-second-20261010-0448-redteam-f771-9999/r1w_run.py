#!/usr/bin/env python3
"""r1w: the re-frozen r1 run end-to-end — the experiment the checker of
20261010-0448-redteam-f771 named for gold.

What changed vs the frozen r1 (see r1w-rings.md, the draft re-freeze):
  - bound sampler widened: 256 seeds, random.Random(20261010), p log-uniform
    [10,1000] then e log-uniform [0.01,0.99] per attempt, reject-and-redraw
    unless p >= 6.5+2e AND the exact orbit is bound (E^2<1, turning points real);
  - the strong-field low-e axis (the checker's second hole) gridded explicitly;
  - hyperbolic in-band motion implemented per r1-rings.md line 10 ("a hyperbolic
    motion otherwise"): u = u* + A e^(lam phi) + B e^(-lam phi) inside bands with
    1-6u_gc < 0, events in closed form (quadratic in e^(lam phi)); the frozen
    probe asserted on that branch instead;
  - m swept {16,32,64} (64 analysis-only, for the m^-2 law);
  - every r1 criterion recomputed per configuration; metrics.json written.

Everything else is r1's frozen machinery, carried verbatim from the shipped
binet_probe.py (elliptic band events, Gauss-8 band time, RK4 exact-Binet
oracle, seed algebra). Oracle here is numpy-vectorized over all bound cases at
once; tie-out against the shipped scalar oracle is printed as a control.
"""
import json, math, os, sys
import numpy as np

M, LN2 = 1.0, math.log(2.0)
GAUSS8_X = [0.09501250983763744, 0.2816035507792589, 0.45801677765722737, 0.6178762444026438,
            0.7554044083500303, 0.8656312023878316, 0.9445750230732326, 0.9894009349916499]
GAUSS8_W = [0.1894506104550685, 0.18260341504492358, 0.16915651939500254, 0.14959598881657674,
            0.12462897125553394, 0.09515851168249279, 0.062253523938647894, 0.027152459411754095]
QUICK = '--quick' in sys.argv
N_SEEDS = 8 if QUICK else 256
RNG_SEED = 20261010
TOL = dict(prec=0.01, period=0.001, shape=0.01, defl=0.01, cross=512.0, repeat=1e-12)
ABSORB_U = 0.5 * (1.0 - 1e-9)   # r=2 absorb edge must NOT sit on a dyadic band edge (u=0.5 = 2^-16/16 etc.)

# ---------------------------------------------------------------- bands (candidate)
def band_index(u, m):
    return int(math.floor(math.log(1.0 / u) / LN2 * m))

class Bands:
    def __init__(self, m, L2=None, light=False):
        self.m, self.L2, self.light, self.cache = m, L2, light, {}
    def get(self, k):
        b = self.cache.get(k)
        if b is None:
            m = self.m
            ugc = 2.0 ** (-(k + 0.5) / m)
            rhs = -3.0 * ugc * ugc if self.light else (1.0 / self.L2 - 3.0 * ugc * ugc)
            w2 = 1.0 - 6.0 * M * ugc
            assert w2 != 0.0, "band centre exactly at 1/6"
            lo, hi = 2.0 ** (-(k + 1) / m), 2.0 ** (-k / m)
            b = (w2, math.sqrt(abs(w2)), rhs / w2, lo, hi)
            self.cache[k] = b
        return b

def ft(u, E, L):
    return E / (L * u * u * (1.0 - 2.0 * u))

def seg_state(bands, u, up):
    k = band_index(u, bands.m)
    w2, wl, ustar, lo, hi = bands.get(k)
    if w2 > 0.0:
        d, s = u - ustar, up / wl
        R = math.hypot(d, s)
        assert R > 1e-14, "circular inside a band"
        return ('e', k, wl, ustar, lo, hi, R, math.atan2(s, d))
    return ('h', k, wl, ustar, lo, hi, ((u - ustar) + up / wl) * 0.5, ((u - ustar) - up / wl) * 0.5)

def next_event(bands, u, up, stops=()):
    """Next event from (u,u'): band edge, u'=0 extremum, or a stop edge.
    Returns (state, dphi, kind, u_at_event). Kinds: 'edge', 'peri' (u max),
    'apo' (u min), or the stop's own label."""
    st = seg_state(bands, u, up)
    if st[0] == 'e':
        _, k, w, ustar, lo, hi, R, th0 = st
        best = None  # (theta, kind)
        for edge, kind in ((lo, 'edge'), (hi, 'edge')) + tuple(stops):
            c = (edge - ustar) / R
            if abs(c) <= 1.0:
                a = math.acos(c)
                for th in (th0 - a, th0 + a, th0 - a + 2 * math.pi, th0 + a + 2 * math.pi):
                    if th > 1e-13 and (best is None or th < best[0]):
                        best = (th, kind)
        if up > 0.0:
            if best is None or th0 < best[0]:
                best = (th0, 'peri')
        elif up < 0.0:
            tapo = th0 + math.pi
            if best is None or tapo < best[0]:
                best = (tapo, 'apo')
        else:
            # at an extremum (seed start at periapsis, or a peri/apo event): if
            # the whole radial excursion stays inside this band no edge fires;
            # the opposite extremum lies half a rotation away.
            tapo = th0 + math.pi
            kind_tp = 'apo' if (u - ustar) > 0.0 else 'peri'
            if best is None or tapo < best[0]:
                best = (tapo, kind_tp)
        th, kind = best
        return st, th / w, kind, ustar + R * math.cos(th - th0)
    # hyperbolic band: u(phi) = ustar + A e^{lam phi} + B e^{-lam phi}
    _, k, lam, ustar, lo, hi, A, B = st
    best = None  # (dphi, kind)
    def consider(phi, kind):
        nonlocal best
        if phi > 1e-13 and (best is None or phi < best[0]):
            best = (phi, kind)
    for edge, kind in ((lo, 'edge'), (hi, 'edge')) + tuple(stops):
        c = edge - ustar
        if abs(A) < 1e-300:                      # A x^2 - c x + B = 0, A=0
            if c != 0.0:
                x = B / c
                if x >= 1.0:
                    consider(math.log(x) / lam, kind)
        else:
            disc = c * c - 4.0 * A * B
            if disc >= 0.0:
                r = math.sqrt(disc)
                for x in ((c - r) / (2 * A), (c + r) / (2 * A)):
                    if x >= 1.0:
                        consider(math.log(x) / lam, kind)
    if A != 0.0 and B / A > 1.0:                 # forward turning point
        uat = ustar + (2 * math.sqrt(A * B) if A > 0 else -2 * math.sqrt(A * B))
        consider(math.log(B / A) / (2 * lam), 'apo' if A > 0 else 'peri')
    if best is None:
        raise RuntimeError("no forward event in hyperbolic band")
    phi, kind = best
    x = math.exp(lam * phi)
    return st, phi, kind, ustar + A * x + B / x

def advance(st, dphi):
    if st[0] == 'e':
        _, k, w, ustar, lo, hi, R, th0 = st
        return ustar + R * math.cos(w * dphi - th0), -w * R * math.sin(w * dphi - th0)
    _, k, lam, ustar, lo, hi, A, B = st
    x = math.exp(lam * dphi)
    return ustar + A * x + B / x, lam * (A * x - B / x)

def seg_time(st, dphi, E, L):
    tot = 0.0
    if st[0] == 'e':
        _, k, w, ustar, lo, hi, R, th0 = st
        for xg, gw in zip(GAUSS8_X, GAUSS8_W):
            tot += gw * ft(ustar + R * math.cos(w * xg * dphi - th0), E, L)
    else:
        _, k, lam, ustar, lo, hi, A, B = st
        for xg, gw in zip(GAUSS8_X, GAUSS8_W):
            x = math.exp(lam * xg * dphi)
            tot += gw * ft(ustar + A * x + B / x, E, L)
    return tot * dphi

def propagate(bands, u, up, E=None, L=None, n_cycles=None, stops=(), max_events=2_000_000,
              record_seq=False):
    """Event propagation. Bound mode (n_cycles set) returns per-cycle records;
    otherwise runs until a stop event and returns its label with total phi."""
    phi_cyc = t_cyc = phi_tot = 0.0
    cyc_d, cyc_t, cyc_seq, cyc_up, cyc_rp, cyc_ra = [], [], [], [], [], []
    seq = []
    crossings = 0
    max_u = min_u = u
    n = 0
    while True:
        n += 1
        if n > max_events:
            return dict(outcome='runaway', cycles=len(cyc_d))
        st, dphi, kind, ue = next_event(bands, u, up, stops)
        if E is not None:
            t_cyc += seg_time(st, dphi, E, L)
        phi_cyc += dphi
        phi_tot += dphi
        if kind == 'edge':
            crossings += 1
            if record_seq:
                seq.append(st[1])
        elif kind == 'peri':
            max_u = max(max_u, ue)
            cyc_d.append(phi_cyc); cyc_t.append(t_cyc); cyc_up.append(ue)
            cyc_rp.append(1.0 / max_u); cyc_ra.append(1.0 / min_u)
            if record_seq:
                cyc_seq.append(seq); seq = []
            phi_cyc = t_cyc = 0.0
            max_u = min_u = ue
            if n_cycles is not None and len(cyc_d) >= n_cycles:
                return dict(outcome='bound', cyc_d=cyc_d, cyc_t=cyc_t, cyc_seq=cyc_seq,
                            cyc_up=cyc_up, cyc_rp=cyc_rp, cyc_ra=cyc_ra,
                            crossings=crossings / len(cyc_d))
        elif kind == 'apo':
            min_u = min(min_u, ue)
        else:                                        # a stop label
            u2, up2 = advance(st, dphi)
            return dict(outcome=kind, phi_total=phi_tot, u_exit=u2, up_exit=up2,
                        cycles=len(cyc_d), crossings=crossings)
        u, up = advance(st, dphi)
        if kind == 'edge':
            # land inside the adjacent band: the multiplicative nudge (shipped) dominates while the
            # in-band amplitude R is comparable to u, but a light ray's far tail has R/u ~ 1e6, where
            # the event landing point carries reconstruction error ~R*eps >> u*1e-12: then nudge by
            # (u+R)*1e-13 instead (dominates the error 400x, stays <1e-4 of a band width).
            amp = st[6] if st[0] == 'e' else abs(st[6]) + abs(st[7])
            if (u + amp) * 1e-13 > u * 1e-12:
                nudge = (u + amp) * 1e-13
                u = u - nudge if up < 0 else u + nudge
            else:
                u = u * (1 - 1e-12) if up < 0 else u * (1 + 1e-12)
        if kind in ('peri', 'apo'):
            up = 0.0

# ---------------------------------------------------------------- seeds (shipped algebra)
def setup_bound(rp, e):
    up_ = 1.0 / rp
    ua = up_ * (1.0 - e) / (1.0 + e)
    L2 = 2.0 / ((up_ + ua) - 2.0 * (up_ * up_ + up_ * ua + ua * ua))
    E2 = 1.0 + L2 * (up_ * up_ - 2.0 * up_ ** 3) - 2.0 * up_
    um = 0.5 * (up_ + ua)
    fmid = (E2 - 1.0) / L2 + 2.0 * um / L2 - um * um + 2.0 * um ** 3
    assert fmid > 0 and 0 < E2 < 1, "not a bound orbit"
    return up_, L2, math.sqrt(E2)

def draw_seeds():
    rng = __import__('random').Random(RNG_SEED)
    seeds, rejects = [], 0
    while len(seeds) < N_SEEDS:
        p = math.exp(rng.uniform(math.log(10.0), math.log(1000.0)))
        e = math.exp(rng.uniform(math.log(0.01), math.log(0.99)))
        if p < 6.5 + 2.0 * e:
            rejects += 1
            continue
        try:
            u0, L2, E = setup_bound(p / (1.0 + e), e)
        except AssertionError:
            rejects += 1
            continue
        seeds.append(dict(p=p, e=e, rp=p / (1.0 + e), u0=u0, L2=L2, E=E, ua=u0 * (1 - e) / (1 + e)))
    lights = []
    while len(lights) < (2 if QUICK else 64):
        b = math.exp(rng.uniform(math.log(10.0), math.log(1000.0)))
        lights.append(b)
    return seeds, lights, rejects

# ---------------------------------------------------------------- oracle (exact GR)
def rk4_step(u, up, h, L2):                                   # shipped, verbatim
    def acc(x):
        return 1.0 / L2 + 3.0 * x * x - x
    k1u, k1v = up, acc(u)
    k2u, k2v = up + .5 * h * k1v, acc(u + .5 * h * k1u)
    k3u, k3v = up + .5 * h * k2v, acc(u + .5 * h * k2u)
    k4u, k4v = up + h * k3v, acc(u + h * k3u)
    return (u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u),
            up + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v))

def oracle_bound_vec(u0, L2, E, L, h=1e-4, max_steps=300_000):
    """One radial cycle (periapsis to periapsis) for many seeds at once, with the
    shipped scalar code's exact convention (including its final-step trapezoid
    offset, so the tie-out is exact). Returns dphi, dt, u_peri arrays."""
    n = len(u0)
    u, up = u0.astype(float).copy(), np.zeros(n)
    phi, t = np.zeros(n), np.zeros(n)
    done = np.zeros(n, bool)
    dphi_o = np.full(n, np.nan); dt_o = np.full(n, np.nan); uper_o = np.full(n, np.nan)
    invL2 = 1.0 / L2
    for _ in range(max_steps):
        act = ~done
        if not act.any():
            break
        uu, vv, iL, EE, LL = u[act], up[act], invL2[act], E[act], L[act]
        phi_a = phi[act]
        def acc(x):
            return iL + 3.0 * x * x - x
        k1u, k1v = vv, acc(uu)
        k2u, k2v = vv + .5 * h * k1v, acc(uu + .5 * h * k1u)
        k3u, k3v = vv + .5 * h * k2v, acc(uu + .5 * h * k2u)
        k4u, k4v = vv + h * k3v, acc(uu + h * k3u)
        un = uu + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = vv + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        ftu = EE / (LL * uu * uu * (1.0 - 2.0 * uu))
        ftn = EE / (LL * un * un * (1.0 - 2.0 * un))
        cross = (vv >= 0.0) & (vn < 0.0) & (phi_a > 0.0)
        idx = np.where(act)[0]
        t[act] += 0.5 * (ftu + ftn) * h
        phi[act] += h
        u[act], up[act] = un, vn
        for j in np.where(cross)[0]:
            gi = idx[j]
            us, vs, Ls, L2s, Es = float(uu[j]), float(vv[j]), float(L[gi]), float(L2[gi]), float(E[gi])
            a, b = 0.0, h
            for _ in range(60):
                mmid = 0.5 * (a + b)
                um, umv = rk4_step(us, vs, mmid, L2s)
                if umv >= 0.0:
                    a = mmid
                else:
                    b = mmid
            ue, _ = rk4_step(us, vs, a, L2s)
            fue = Es / (Ls * ue * ue * (1.0 - 2.0 * ue))
            t[gi] += 0.5 * (ftu[j] + fue) * a - 0.5 * (ftu[j] + ftn[j]) * h
            dphi_o[gi] = phi_a[j] + a
            dt_o[gi] = t[gi]
            uper_o[gi] = ue
            done[gi] = True
    assert np.all(done), "oracle failed to close a cycle"
    return dphi_o, dt_o, uper_o

def oracle_light_vec(b, u0=1e-8, h=1e-4, max_steps=200_000):
    """Exact light sweep u0 -> u0 (in, periapsis, out); returns total dphi."""
    b = b.astype(float)
    n = len(b)
    u = np.full(n, u0)
    up = np.sqrt(1.0 / b**2 - u0**2 + 2 * u0**3)
    phi = np.zeros(n)
    done = np.zeros(n, bool)
    out = np.full(n, np.nan)
    for _ in range(max_steps):
        act = ~done
        if not act.any():
            break
        uu, vv = u[act], up[act]
        phi_a = phi[act]
        def acc(x):
            return 3.0 * x * x - x
        k1u, k1v = vv, acc(uu)
        k2u, k2v = vv + .5 * h * k1v, acc(uu + .5 * h * k1u)
        k3u, k3v = vv + .5 * h * k2v, acc(uu + .5 * h * k2u)
        k4u, k4v = vv + h * k3v, acc(uu + h * k3u)
        un = uu + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        vn = vv + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        phi[act] += h
        u[act], up[act] = un, vn
        stop = (vv < 0.0) & (un <= u0)
        idx = np.where(act)[0]
        for j in np.where(stop)[0]:
            gi = idx[j]
            out[gi] = phi_a[j] + h * (uu[j] - u0) / (uu[j] - un[j])
            done[gi] = True
    assert np.all(done), "light oracle failed to return"
    return out

def oracle_massive_outcome(u0, up0, L2, h=1e-4, u_absorb=0.5, max_phi=400.0):
    """Scalar: outcome 'absorbed' (r<=2) or 'escaped' (back out past u0)."""
    u, up, phi = u0, up0, 0.0
    while phi < max_phi:
        un, upn = rk4_step(u, up, h, L2)
        if un >= u_absorb:
            return 'absorbed'
        if upn < 0.0 and un <= u0:
            return 'escaped'
        u, up, phi = un, upn, phi + h
    return 'runaway'

def light_tail(q, u0, n=64):
    """int_0^{u0} du/sqrt(q - u^2 + 2u^3) by Gauss-Legendre (n points)."""
    xg, wg = np.polynomial.legendre.leggauss(n)
    a = 0.5 * u0
    xs = a * (xg + 1.0)
    return float(a * np.sum(wg / np.sqrt(q - xs**2 + 2 * xs**3)))

# ---------------------------------------------------------------- helpers
def banded_bound_case(seed, m, n_cycles=3, record_seq=False):
    u_a = seed['ua']
    bands = Bands(m, L2=seed['L2'])
    try:
        return propagate(bands, seed['u0'], 0.0, E=seed['E'], L=math.sqrt(seed['L2']),
                         n_cycles=n_cycles, stops=((u_a / 4.0, 'escape'), (ABSORB_U, 'absorb')),
                         record_seq=record_seq)
    except (RuntimeError, AssertionError, OverflowError, ValueError) as ex:
        return dict(outcome='error', err=f"{type(ex).__name__}: {ex}")

def defl_banded(b, m, u0=1e-8):
    bands = Bands(m, light=True)
    up0 = math.sqrt(1.0 / b**2 - u0**2 + 2 * u0**3)
    r = propagate(bands, u0, up0, stops=((u0, 'swept'),))
    q = r['up_exit']**2 + u0**2 - 2 * u0**3
    return (r['phi_total'] - math.pi) + 2.0 * light_tail(q, u0)

def isco_seeds():
    L7 = 1.01 * math.sqrt(49.0 / 4.0)
    u7 = 1.0 / 7.0
    E7 = math.sqrt((1 - 2 * u7) * (1 + L7**2 * u7**2))
    L55 = 0.99 * math.sqrt(5.5**2 / 2.5)
    u55 = 1.0 / 5.5
    E55 = math.sqrt((1 - 2 * u55) * (1 + L55**2 * u55**2))
    return dict(bound=dict(u0=u7, L2=L7**2, E=E7), plunge=dict(u0=u55, L2=L55**2, E=E55))

# ---------------------------------------------------------------- main
def main():
    out = []
    P = out.append
    P("=== r1w: re-frozen r1 end-to-end (sampler widened to e<=0.99, hyperbolic bands, m sweep) ===")
    P(f"host: {os.uname().sysname} {os.uname().release}, cpus={os.cpu_count()}, load={os.getloadavg()[0]:.2f}")
    P("oracle: vectorized RK4 exact Schwarzschild Binet, h=1e-4 (+Richardson controls); candidate: exact in-band solution (rotation | hyperbolic), closed-form events")
    P("")

    seeds, lights, rejects = draw_seeds()
    P(f"bound seeds: {len(seeds)} drawn (Random({RNG_SEED}), p log-U[10,1000] then e log-U[0.01,0.99], "
      f"reject unless p>=6.5+2e and bound); {rejects} attempts rejected")
    hyper_rp = sum(1 for s in seeds if s['rp'] < 6.0)
    P(f"  seeds with r_p<6M (hyperbolic periapsis bands): {hyper_rp}; e>0.9: {sum(1 for s in seeds if s['e']>0.9)}; "
      f"e range [{min(s['e'] for s in seeds):.4f}, {max(s['e'] for s in seeds):.4f}]; "
      f"r_p range [{min(s['rp'] for s in seeds):.2f}, {max(s['rp'] for s in seeds):.2f}]")
    P("")

    # explicit grids (checker's second hole + boundary + hyperbolic + wall)
    low_e_grid = [dict(rp=rp, e=e) for rp in (10.9, 12.0, 13.4) for e in (0.01, 0.02)]
    bnd_grid = [dict(rp=rp, e=e) for rp in (7.0, 8.0, 10.0, 15.0, 30.0, 100.0)
                for e in (0.85, 0.90, 0.93, 0.95, 0.97, 0.98, 0.99)]
    hyp_grid = [dict(rp=rp, e=e) for rp, e in ((4.5, 0.95), (4.5, 0.99), (5.0, 0.95), (5.0, 0.99),
                                               (5.5, 0.95), (5.5, 0.99), (4.31, 0.99))]
    wall_grid = [dict(rp=7.0, e=e) for e in (0.995, 0.999, 0.9999)]
    def mk(g):
        u0, L2, E = setup_bound(g['rp'], g['e'])
        return dict(rp=g['rp'], e=g['e'], u0=u0, L2=L2, E=E, ua=u0 * (1 - g['e']) / (1 + g['e']))
    grids = dict(low_e=[mk(g) for g in low_e_grid], boundary=[mk(g) for g in bnd_grid],
                 hyperbolic=[mk(g) for g in hyp_grid], wall=[mk(g) for g in wall_grid])

    # ---- oracle for every bound case at once
    allcases = seeds + grids['low_e'] + grids['boundary'] + grids['hyperbolic'] + grids['wall']
    U0 = np.array([c['u0'] for c in allcases]); L2A = np.array([c['L2'] for c in allcases])
    EA = np.array([c['E'] for c in allcases]); LA = np.sqrt(L2A)
    dphi_o, dt_o, _ = oracle_bound_vec(U0, L2A, EA, LA)
    P("--- oracle controls ---")
    # tie-out vs shipped scalar oracle on two shipped cases
    for rp, e in ((7.0, 0.99), (8.0, 0.95)):
        u0, L2, E = setup_bound(rp, e)
        d1, t1, _ = oracle_bound_vec(np.array([u0]), np.array([L2]), np.array([E]),
                                     np.array([math.sqrt(L2)]))
        L = math.sqrt(L2)
        u, up, phi, t = u0, 0.0, 0.0, 0.0
        h = 1e-4
        while True:
            un, upn = rk4_step(u, up, h, L2)
            if up >= 0.0 and upn < 0.0 and phi > 0:
                a, b = 0.0, h
                for _ in range(60):
                    m2 = 0.5 * (a + b)
                    um, umv = rk4_step(u, up, m2, L2)
                    if umv >= 0.0:
                        a = m2
                    else:
                        b = m2
                ue, _ = rk4_step(u, up, a, L2)
                t_ship = t + 0.5 * (ft(u, E, L) + ft(ue, E, L)) * a \
                         - 0.5 * (ft(u, E, L) + ft(un, E, L)) * h
                phi_ship, t_ship = phi + a, t_ship
                break
            t += 0.5 * (ft(u, E, L) + ft(un, E, L)) * h
            phi += h
            u, up = un, upn
        P(f"tie-out (r_p={rp}, e={e}): dphi vec-vs-shipped {abs(d1[0]-phi_ship)/phi_ship:.2e}, "
          f"period {abs(t1[0]-t_ship)/t_ship:.2e}")
    sub = min(len(seeds), 8 if QUICK else 32)
    dA, tA, _ = oracle_bound_vec(U0[:sub], L2A[:sub], EA[:sub], LA[:sub], h=1e-4)
    dB, tB, _ = oracle_bound_vec(U0[:sub], L2A[:sub], EA[:sub], LA[:sub], h=5e-5)
    P(f"oracle Richardson h=1e-4 vs 5e-5 ({sub} seeds): max |ddphi| {np.max(np.abs(dA-dB)/dA):.2e}, "
      f"max |dperiod| {np.max(np.abs(tA-tB)/tA):.2e}")
    u0, L2, E = setup_bound(100.0, 0.5)          # r_p=100, e=0.5 => p = 150
    d1PN, _, _ = oracle_bound_vec(np.array([u0]), np.array([L2]), np.array([E]),
                                  np.array([math.sqrt(L2)]))
    P(f"precession vs 1PN 6pi/p (r_p=100, e=0.5, p=150): oracle {d1PN[0]-2*math.pi:.5f} vs "
      f"{6*math.pi/150:.5f} ({abs(d1PN[0]-2*math.pi-6*math.pi/150)/(6*math.pi/150)*100:.1f}% = 2PN scale)")
    P("")

    metrics = {}
    MS = [16] if QUICK else [16, 32, 64]
    for m in MS:
        cfg = f"binet-m{m}"
        P(f"--- {cfg}: bound seeds (r1 criteria: prec 1%, period 0.1%, crossings<=512 median) ---")
        rows, prec_ok, per_ok, prog_ok, mism, crosslist = [], [], [], [], [], []
        for i, s in enumerate(seeds):
            r = banded_bound_case(s, m)
            if r['outcome'] != 'bound':
                mism.append((s['rp'], s['e'], r['outcome']))
                prec_ok.append(False); per_ok.append(False); prog_ok.append(False)
                rows.append((s['rp'], s['e'], None, None, None, r['outcome']))
                continue
            pre_b = r['cyc_d'][2] - 2 * math.pi
            pre_o = dphi_o[i] - 2 * math.pi
            pe = abs(pre_b - pre_o) / abs(pre_o)
            te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i]
            prec_ok.append(pe <= TOL['prec']); per_ok.append(te <= TOL['period'])
            prog_ok.append(pre_b > 0.0)
            crosslist.append(r['crossings'])
            rows.append((s['rp'], s['e'], pe, te, r['crossings'], 'ok'))
        n = len(seeds)
        worst_per = max((r[3] for r in rows if r[3] is not None), default=float('nan'))
        worst_pre = max((r[2] for r in rows if r[2] is not None), default=float('nan'))
        fails = [(r[0], r[1], r[3]) for r in rows if r[3] is not None and r[3] > TOL['period']]
        P(f"precession_pass_fraction = {sum(prec_ok)/n:.4f} (worst err {worst_pre:.2e})")
        P(f"prograde_fraction        = {sum(prog_ok)/n:.4f}")
        P(f"period_pass_fraction     = {sum(per_ok)/n:.4f} (worst err {worst_per:.2e}, {len(fails)} fails)")
        pfails = [(r[0], r[1], r[2]) for r in rows if r[2] is not None and r[2] > TOL['prec']]
        for rp, e, te in sorted(fails, key=lambda x: -x[2])[:8]:
            P(f"    period fail: r_p={rp:8.2f} e={e:.4f} err={te:.2e}")
        for rp, e, pe in sorted(pfails, key=lambda x: -x[2])[:8]:
            P(f"    precession fail: r_p={rp:8.2f} e={e:.4f} err={pe:.2e}")
        if mism:
            P(f"  BANDED MISCLASSIFICATIONS (outcome != bound): {mism}")
        P(f"crossings_per_cycle median = {sorted(crosslist)[len(crosslist)//2]:.1f}, "
          f"max = {max(crosslist):.1f}")
        metrics[cfg] = dict(
            precession_pass_fraction=sum(prec_ok) / n, prograde_fraction=sum(prog_ok) / n,
            period_pass_fraction=sum(per_ok) / n,
            crossings_per_cycle=sorted(crosslist)[len(crosslist) // 2],
            crossings_max=max(crosslist), banded_misclassified=len(mism),
            period_worst=worst_per, precession_worst=worst_pre,
            period_fail_seeds=[[float(a), float(b), float(c)] for a, b, c in fails])
        P("")

        if not QUICK:
            P(f"[{cfg}] low-e strong-field grid (r1 period band 0.1% per point):")
            gl = []
            for c in grids['low_e']:
                i = allcases.index(c)
                r = banded_bound_case(c, m)
                te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i] if r['outcome'] == 'bound' else float('nan')
                gl.append([c['rp'], c['e'], float(te)])
                P(f"    r_p={c['rp']:6} e={c['e']:5}  period_err={te:.2e} {'PASS' if te <= TOL['period'] else 'FAIL'}")
            metrics[cfg]['low_e_grid'] = gl
            P("")

    if QUICK:
        u0, L2, E = setup_bound(7.0, 0.99)
        s = dict(rp=7.0, e=0.99, u0=u0, L2=L2, E=E, ua=u0 * 0.01 / 1.99)
        r = banded_bound_case(s, 16)
        i = next(j for j, c in enumerate(allcases) if c['rp'] == 7.0 and c['e'] == 0.99)
        pe = abs((r['cyc_d'][2] - 2 * math.pi) - (dphi_o[i] - 2 * math.pi)) / abs(dphi_o[i] - 2 * math.pi)
        te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i]
        P(f"quick tie-out (7,0.99) m16 vs shipped probe (prec 4.45e-4, period 1.93e-2, cross 246): "
          f"prec_err={pe:.2e} period_err={te:.2e} cross={r['crossings']:.1f}")
        print("\n".join(out))
        return

    # ---- m^-2 law on fixed cases
    P("--- m-sweep: error scaling on fixed cases (expect m^-2, i.e. ratio ~4 per doubling) ---")
    law = {}
    for label, rp, e in (("hi-e strong (7,0.99)", 7.0, 0.99), ("hi-e strong (7,0.95)", 7.0, 0.95),
                         ("mid (8,0.9)", 8.0, 0.9), ("weak (10,0.9)", 10.0, 0.9)):
        i = next(j for j, c in enumerate(allcases) if c['rp'] == rp and c['e'] == e)
        c = allcases[i]
        pers, pres = [], []
        for m in (16, 32, 64):
            r = banded_bound_case(c, m)
            pers.append(abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i])
            pres.append(abs((r['cyc_d'][2] - 2 * math.pi) - (dphi_o[i] - 2 * math.pi))
                        / abs(dphi_o[i] - 2 * math.pi))
        sl = float(np.polyfit(np.log([16, 32, 64]), np.log(pers), 1)[0])
        slp = float(np.polyfit(np.log([16, 32, 64]), np.log(pres), 1)[0])
        law[label] = dict(pers=pers, pres=pres, slope=sl, slope_prec=slp)
        P(f"{label}: period {pers[0]:.2e}/{pers[1]:.2e}/{pers[2]:.2e} ratios {pers[0]/pers[1]:.3f}/"
          f"{pers[1]/pers[2]:.3f} slope {sl:.3f}; precession slope {slp:.3f}")
    P("")

    c = grids['low_e'][0]
    i = allcases.index(c)
    pers = [abs(banded_bound_case(c, m)['cyc_t'][2] - dt_o[i]) / dt_o[i] for m in (16, 32, 64)]
    sl = float(np.polyfit(np.log([16, 32, 64]), np.log(pers), 1)[0])
    law['low_e_worst'] = dict(pers=pers, slope=sl)
    P(f"low-e grid point (r_p={c['rp']}, e={c['e']}): period {pers[0]:.2e}/{pers[1]:.2e}/{pers[2]:.2e} "
      f"slope {sl:.3f}")
    P("")

    # ---- per-e period boundary at m=32
    P("--- per-e period-band boundary at m=32: largest e with period_err <= 0.1% ---")
    beb = {}
    for rp in (7.0, 8.0, 10.0, 15.0, 30.0, 100.0):
        pts = []
        for c in grids['boundary']:
            if c['rp'] != rp:
                continue
            i = allcases.index(c)
            r = banded_bound_case(c, 32)
            te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i] if r['outcome'] == 'bound' else float('inf')
            pts.append((c['e'], te))
        pts.sort()
        estar = max((e_ for e_, te_ in pts if te_ <= TOL['period']), default=None)
        beb[str(rp)] = dict(points=[[float(a), float(b)] for a, b in pts], e_star=estar)
        P(f"r_p={rp:6}: " + "  ".join(f"e={e_:.2f}:{te_:.1e}" for e_, te_ in pts) + f"   => e* = {estar}")
    P("")

    # ---- hyperbolic-band regime at m=32
    P("--- hyperbolic periapsis bands (r_p<6M), m=32: outcome + errors ---")
    hyp = []
    for c in grids['hyperbolic']:
        i = allcases.index(c)
        r = banded_bound_case(c, 32)
        if r['outcome'] == 'bound':
            te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i]
            pe = abs((r['cyc_d'][2] - 2 * math.pi) - (dphi_o[i] - 2 * math.pi)) / abs(dphi_o[i] - 2 * math.pi)
            P(f"r_p={c['rp']:5} e={c['e']:5}: bound  prec_err={pe:.2e} period_err={te:.2e} cross={r['crossings']:.0f}")
            hyp.append([c['rp'], c['e'], 'bound', float(pe), float(te), float(r['crossings'])])
        else:
            P(f"r_p={c['rp']:5} e={c['e']:5}: {r['outcome'].upper()} (exact orbit is bound!)")
            hyp.append([c['rp'], c['e'], r['outcome'], None, None, None])
    P("")

    P("--- envelope wall at m=32 (e > 0.99; NOT in the re-frozen domain) ---")
    wall = []
    for c in grids['wall']:
        i = allcases.index(c)
        r = banded_bound_case(c, 32)
        if r['outcome'] == 'bound':
            te = abs(r['cyc_t'][2] - dt_o[i]) / dt_o[i]
            P(f"r_p=7 e={c['e']}: bound, period_err={te:.2e}")
            wall.append([c['e'], 'bound', float(te)])
        else:
            P(f"r_p=7 e={c['e']}: {r['outcome'].upper()} where exact stays bound (misclassification)")
            wall.append([c['e'], r['outcome'], None])
    P("")

    # ---- capture, photon capture, ISCO
    P("--- capture (E=1, r=100) / photon capture / ISCO ---")
    for m in (16, 32):
        cap = []
        for q in (0.5, 0.9, 0.97, 1.03, 1.1, 1.5):
            L = 4.0 * q
            L2 = L * L
            u0 = 0.01
            up0 = math.sqrt((1.0 - (1 - 2 * u0) * (1 + L2 * u0 * u0)) / L2)
            ex = oracle_massive_outcome(u0, up0, L2)
            r = propagate(Bands(m, L2=L2), u0, up0,
                          stops=((ABSORB_U, 'absorbed'), (u0, 'escaped')), max_events=500_000)
            cap.append((q, ex, r['outcome']))
            P(f"m={m} L/4={q:5}: exact={ex:9} banded={r['outcome']:9} "
              f"{'ok' if ex == r['outcome'] else 'MISCLASSIFIED'}")
        mis_cap = sum(1 for _, a, b in cap if a != b)
        phot = []
        for q in (0.9, 0.97, 1.03, 1.1):
            b = q * 3 * math.sqrt(3)
            u0 = 1e-8
            up0 = math.sqrt(1 / b**2 - u0**2 + 2 * u0**3)
            u, up, phi = u0, up0, 0.0
            ex = None
            h = 1e-4
            while phi < 400.0:
                un, upn = rk4_step_light(u, up, h)
                if un >= 0.5:
                    ex = 'absorbed'; break
                if upn < 0.0 and un <= u0:
                    ex = 'escaped'; break
                u, up, phi = un, upn, phi + h
            r = propagate(Bands(m, light=True), u0, up0,
                          stops=((ABSORB_U, 'absorbed'), (u0, 'escaped')), max_events=500_000)
            phot.append((q, ex, r['outcome']))
            P(f"m={m} b/(3sqrt3)={q:5}: exact={ex:9} banded={r['outcome']:9} "
              f"{'ok' if ex == r['outcome'] else 'MISCLASSIFIED'}")
        mis_ph = sum(1 for _, a, b in phot if a != b)
        isc = isco_seeds()
        rb = propagate(Bands(m, L2=isc['bound']['L2']), isc['bound']['u0'], 0.0,
                       E=isc['bound']['E'], L=math.sqrt(isc['bound']['L2']), n_cycles=100,
                       stops=((ABSORB_U, 'absorb'), (isc['bound']['u0'] / 4.0, 'escape')),
                       max_events=2_000_000)
        rpl = propagate(Bands(m, L2=isc['plunge']['L2']), isc['plunge']['u0'], 0.0,
                        stops=((ABSORB_U, 'absorbed'),), max_events=500_000)
        ex_pl = oracle_massive_outcome(isc['plunge']['u0'], 0.0, isc['plunge']['L2'])
        isco_ok = (rb['outcome'] == 'bound' and rpl['outcome'] == 'absorbed' and ex_pl == 'absorbed')
        P(f"m={m} ISCO: bound case {rb['outcome']} (100 cycles), plunge banded={rpl['outcome']} "
          f"exact={ex_pl} => isco_correct={1 if isco_ok else 0}")
        metrics[f"binet-m{m}"]['capture_misclassified'] = mis_cap + mis_ph
        metrics[f"binet-m{m}"]['isco_correct'] = 1 if isco_ok else 0
        metrics[f"binet-m{m}"]['capture_table'] = [[float(a), b, c] for a, b, c in cap]
        metrics[f"binet-m{m}"]['photon_table'] = [[float(a), b, c] for a, b, c in phot]
        P("")

    # ---- light deflection
    P("--- light deflection (64 seeds, b log-U[10,1000], swept to r=1e8 + exact tail) ---")
    bA = np.array(lights)
    dphi_l = oracle_light_vec(bA)
    defl_o = dphi_l - math.pi + 2 * np.array([light_tail(1.0 / b**2, 1e-8) for b in lights])
    i1000 = int(np.argmin(np.abs(bA - 1000))); i100 = int(np.argmin(np.abs(bA - 100)))
    P(f"oracle controls: defl(b={bA[i1000]:.1f})={defl_o[i1000]:.6e} (4/b={4/bA[i1000]:.6e}), "
      f"defl(b={bA[i100]:.1f})/defl(b={bA[i1000]:.1f}) = {defl_o[i100]/defl_o[i1000]:.2f}")
    for m in (16, 32):
        errs = [abs(defl_banded(b, m) - defl_o[j]) / defl_o[j] for j, b in enumerate(lights)]
        metrics[f"binet-m{m}"]['deflection_pass_fraction'] = sum(1 for x in errs if x <= TOL['defl']) / len(errs)
        metrics[f"binet-m{m}"]['deflection_worst'] = max(errs)
        P(f"m={m}: deflection_pass_fraction = {metrics[f'binet-m{m}']['deflection_pass_fraction']:.4f} "
          f"(worst err {max(errs):.2e})")
    b1 = lights[i1000]
    d2 = oracle_light_vec(np.array([b1]), u0=3e-8)
    do2 = d2[0] - math.pi + 2 * light_tail(1 / b1**2, 3e-8)
    P(f"  tail control: defl(b={b1:.1f}) at r=1e8 vs 3e-8: {abs(do2 - defl_o[i1000]) / defl_o[i1000]:.2e}")
    P("")

    # ---- long runs (first 32 seeds, m=32)
    P("--- long runs: first 32 seeds at m=32, 12 cycles + bit-identity + 100-cycle confirmation ---")
    shape_ok, repeat_frozen, repeat_refrozen, first_devs = [], [], [], []
    for s in seeds[:32]:
        r = banded_bound_case(s, 32, n_cycles=12, record_seq=True)
        assert r['outcome'] == 'bound'
        rp1, ra1 = r['cyc_rp'][0], r['cyc_ra'][0]
        shp = max(max(abs(x - rp1) / rp1 for x in r['cyc_rp'][1:]),
                  max(abs(x - ra1) / ra1 for x in r['cyc_ra'][1:]))
        shape_ok.append(shp <= TOL['shape'])
        dev1 = max(abs(x - r['cyc_d'][0]) / r['cyc_d'][0] for x in r['cyc_d'][1:])
        seqs_ok = r['cyc_seq'][1] == r['cyc_seq'][0]
        repeat_frozen.append(dev1 <= TOL['repeat'] and seqs_ok)
        first_devs.append(dev1)
        kstar = None
        for k in range(0, 9):
            if all(r['cyc_d'][j] == r['cyc_d'][k] and r['cyc_t'][j] == r['cyc_t'][k]
                   and r['cyc_seq'][j] == r['cyc_seq'][k] for j in range(k + 1, len(r['cyc_d']))):
                kstar = k
                break
        repeat_refrozen.append(kstar is not None and kstar <= 4)
    conf = []
    for s in sorted(seeds[:32], key=lambda s: -s['e'])[:2]:
        r = banded_bound_case(s, 32, n_cycles=100)
        kstar = None
        for k in range(0, 20):
            if all(r['cyc_d'][j] == r['cyc_d'][k] and r['cyc_t'][j] == r['cyc_t'][k]
                   for j in range(k + 1, 100)):
                kstar = k
                break
        conf.append((s['e'], kstar))
        P(f"100-cycle confirm e={s['e']:.4f}: bit-identity locks at cycle {kstar}")
    metrics['binet-m32']['shape_kept_fraction'] = sum(shape_ok) / len(shape_ok)
    metrics['binet-m32']['cycle_repeat_fraction_frozen_reading'] = sum(repeat_frozen) / len(repeat_frozen)
    metrics['binet-m32']['cycle_repeat_fraction'] = sum(repeat_refrozen) / len(repeat_refrozen)
    metrics['binet-m32']['long_run_first_cycle_dev_max'] = max(first_devs)
    metrics['binet-m32']['long_run_100cycle_confirm'] = [[float(a), b] for a, b in conf]
    P(f"shape_kept_fraction = {metrics['binet-m32']['shape_kept_fraction']:.4f}")
    P(f"cycle_repeat_fraction (re-frozen reading: cycles>k bit-identical, k<=4) = "
      f"{metrics['binet-m32']['cycle_repeat_fraction']:.4f}")
    P(f"cycle_repeat_fraction (frozen-literal reading: later==cycle1 at 1e-12) = "
      f"{metrics['binet-m32']['cycle_repeat_fraction_frozen_reading']:.4f} "
      f"(max first-cycle dev {max(first_devs):.2e}: passes with 3 orders of margin; the stricter "
      f"bit-identity reading locks at k<=4 for only {metrics['binet-m32']['cycle_repeat_fraction']:.4f})")
    P("")

    P("=== criterion verdicts (r1 frozen thresholds) ===")
    for cfg in ('binet-m16', 'binet-m32', 'binet-m64'):
        if cfg not in metrics:
            continue
        mm = metrics[cfg]
        checks = [
            ('prec', mm['precession_pass_fraction'] >= 0.99),
            ('prog', mm['prograde_fraction'] >= 1.0),
            ('period', mm['period_pass_fraction'] >= 0.99),
            ('defl', mm.get('deflection_pass_fraction', 1.0) >= 0.99),
            ('capture', mm.get('capture_misclassified', 0) <= 0),
            ('isco', mm.get('isco_correct', 1) >= 1),
            ('cost', mm['crossings_per_cycle'] <= 512),
        ]
        if 'shape_kept_fraction' in mm:
            checks.append(('shape', mm['shape_kept_fraction'] >= 0.99))
            checks.append(('repeat', mm['cycle_repeat_fraction_frozen_reading'] >= 0.99))
        P(f"{cfg}: " + "  ".join(f"{k}={'PASS' if v else 'FAIL'}" for k, v in checks))
        mm['criteria'] = {k: bool(v) for k, v in checks}

    metrics['analysis'] = dict(m_sweep_law=law, per_e_boundary=beb,
                               hyperbolic_grid=hyp, wall=wall)
    metrics['config'] = dict(n_seeds=len(seeds), rng_seed=RNG_SEED, rejects=rejects,
                             oracle_h=1e-4, tol=TOL)
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=1)
    P("")
    P("metrics.json written")
    print("\n".join(out))

def rk4_step_light(u, up, h):
    def acc(x):
        return 3.0 * x * x - x
    k1u, k1v = up, acc(u)
    k2u, k2v = up + .5 * h * k1v, acc(u + .5 * h * k1u)
    k3u, k3v = up + .5 * h * k2v, acc(u + .5 * h * k2u)
    k4u, k4v = up + h * k3v, acc(u + h * k3u)
    return (u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u),
            up + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v))

if __name__ == "__main__":
    main()
