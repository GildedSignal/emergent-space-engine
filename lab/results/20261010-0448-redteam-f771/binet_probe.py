#!/usr/bin/env python3
"""Held-out probe of representation.md §1 Binet cells, beyond r1's frozen seed set.

Candidate (r1-rings.md, binet-m16): bands are rings r_k = 2^(k/16); inside band k
the orbit obeys u" + (1 - 6 u_gc) u = 1/L^2 - 3 u_gc^2 (u_gc = band's geometric
centre); u and u' continuous across bands. In-band solution is the exact rotation
u = u* + R cos(w (phi - phi_c)); we propagate event-to-event in closed form
(band edges and u'=0 extrema solved analytically), so the candidate carries no
ODE stepping error at all -- it is exactly the banded law.
Oracle: exact Schwarzschild timelike Binet u" + u = 1/L^2 + 3 u^2, RK4 with
Richardson check. dt/dphi = E/(L u^2 (1-2u)) is the same rule on both sides, so
the comparison isolates the band-model error.

Held out from r1 (seeds: e <= 0.7, bound only): bound e in [0.75, 0.99] at
r_p in {7, 8, 10} M, and massive hyperbolic flybys (E in [1.05, 2.0], r_p in
{8, 10, 15} M). r1 tolerance bands applied unchanged: precession 1%, period
0.1%, shape 1%, crossings per cycle <= 512; scattering judged against the
light-gate 1% band.
"""
import math, os

M, MBANDS, LN2 = 1.0, 16, math.log(2.0)
GAUSS8_X = [0.09501250983763744, 0.2816035507792589, 0.45801677765722737, 0.6178762444026438,
            0.7554044083500303, 0.8656312023878316, 0.9445750230732326, 0.9894009349916499]
GAUSS8_W = [0.1894506104550685, 0.18260341504492358, 0.16915651939500254, 0.14959598881657674,
            0.12462897125553394, 0.09515851168249279, 0.062253523938647894, 0.027152459411754095]


def band_index(u):
    return int(math.floor(math.log(1.0 / u) / LN2 * MBANDS))


class Bands:
    def __init__(self, L2):
        self.L2 = L2
        self.cache = {}

    def get(self, k):
        b = self.cache.get(k)
        if b is None:
            ugc = 2.0 ** (-(k + 0.5) / MBANDS)
            w2 = 1.0 - 6.0 * M * ugc
            assert w2 > 0, f"hyperbolic band u_gc={ugc}"
            w = math.sqrt(w2)
            ustar = (1.0 / self.L2 - 3.0 * ugc * ugc) / w2
            lo, hi = 2.0 ** (-(k + 1) / MBANDS), 2.0 ** (-k / MBANDS)
            b = (w, ustar, lo, hi)
            self.cache[k] = b
        return b


def ft(u, E, L):
    """dt/dphi for Schwarzschild timelike geodesics."""
    return E / (L * u * u * (1.0 - 2.0 * u))


def segment_state(bands, u, up):
    """Represent (u, u') as rotation params in the current band:
    u(phi) = ustar + R cos(w*phi - th0), u'(phi) = -w R sin(w*phi - th0)."""
    k = band_index(u)
    w, ustar, lo, hi = bands.get(k)
    d, s = u - ustar, up / w
    R = math.hypot(d, s)
    th0 = math.atan2(s, d)  # u'(0) = -w R sin(-th0) = w R sin(th0)
    return k, w, ustar, lo, hi, R, th0


def seg_time(bands, u, up, dphi, E, L):
    """Gauss-8 quadrature of dt/dphi over one in-band segment."""
    k, w, ustar, lo, hi, R, th0 = segment_state(bands, u, up)
    tot = 0.0
    for x, gw in zip(GAUSS8_X, GAUSS8_W):
        th = th0 - w * x * dphi
        uu = ustar + R * math.cos(th)
        tot += gw * ft(uu, E, L)
    return tot * dphi


def next_event(bands, u, up, extra_edges=()):
    """Next event from state (u, u'): band edge, u'=0 extremum, or a virtual
    edge (sweep stop). Returns (dphi, kind, u_at_event); kinds: 'edge', 'peri'
    (u max), 'apo' (u min), 'stop'."""
    k, w, ustar, lo, hi, R, th0 = segment_state(bands, u, up)
    assert R > 1e-14, "circular inside a band (unsupported case)"
    best = None  # (theta, kind)
    for edge in (lo, hi) + tuple(extra_edges):
        c = (edge - ustar) / R
        if abs(c) <= 1.0:
            a = math.acos(c)
            for th in (th0 - a, th0 + a, th0 - a + 2 * math.pi, th0 + a + 2 * math.pi):
                if th > 1e-13 and (best is None or th < best[0]):
                    kind = 'stop' if edge in extra_edges else 'edge'
                    best = (th, kind)
    if up > 0.0:  # inbound in u: periapsis (u max) at th0
        if best is None or th0 < best[0]:
            best = (th0, 'peri')
    elif up < 0.0:  # outbound in u: apoapsis (u min) at th0 + pi
        tapo = th0 + math.pi
        if best is None or tapo < best[0]:
            best = (tapo, 'apo')
    # up == 0: starting at an extremum; only edge/stop candidates apply
    th, kind = best
    return th / w, kind, ustar + R * math.cos(th - th0)


def propagate(bands, u, up, E, L, n_cycles=None, u_stop=None, max_events=2_000_000):
    """Propagate by events. Bound mode: per-cycle (dphi, dtime) lists,
    crossings/cycle, loop (r_p, r_a). Sweep mode: phi swept to u_stop."""
    phi_cyc, t_cyc = 0.0, 0.0
    cyc_d, cyc_t = [], []
    crossings = 0
    max_u = min_u = u
    extra = (u_stop,) if u_stop is not None else ()
    n = 0
    while True:
        n += 1
        if n > max_events:
            raise RuntimeError("event limit")
        dphi, kind, ue = next_event(bands, u, up, extra)
        t_cyc += seg_time(bands, u, up, dphi, E, L)
        phi_cyc += dphi
        if kind == 'edge' or kind == 'stop':
            crossings += 1
        elif kind == 'peri':
            max_u = max(max_u, ue)
            cyc_d.append(phi_cyc)
            cyc_t.append(t_cyc)
            phi_cyc, t_cyc = 0.0, 0.0
            if n_cycles is not None and len(cyc_d) >= n_cycles:
                return cyc_d, cyc_t, crossings / n_cycles, (1.0 / max_u, 1.0 / min_u)
        else:  # apo
            min_u = min(min_u, ue)
        # advance the state exactly to the event
        k, w, ustar, lo, hi, R, th0 = segment_state(bands, u, up)
        u = ustar + R * math.cos(w * dphi - th0)
        up = -w * R * math.sin(w * dphi - th0)
        if kind == 'edge':
            u = u * (1 - 1e-12) if up < 0 else u * (1 + 1e-12)  # land inside the adjacent band
        if kind in ('peri', 'apo'):
            up = 0.0  # extremum: u' is exactly zero there
        if kind == 'stop':
            return phi_cyc, None, crossings, (1.0 / max_u, 1.0 / min_u)
        if u <= 0 or (1.0 - 2.0 * u) <= 0:
            raise RuntimeError(f"bad u={u}")


def run_banded(u0, L2, E, L, n_cycles):
    bands = Bands(L2)
    return propagate(bands, u0, 0.0, E, L, n_cycles=n_cycles)


def banded_sweep(u0, L2, E, L, u_stop=1e-3):
    bands = Bands(L2)
    phi, _, _, _ = propagate(bands, u0, 0.0, E, L, u_stop=u_stop)
    return phi


def rk4_step(u, up, h, L2):
    def acc(x):
        return 1.0 / L2 + 3.0 * x * x - x
    k1u, k1v = up, acc(u)
    k2u, k2v = up + .5 * h * k1v, acc(u + .5 * h * k1u)
    k3u, k3v = up + .5 * h * k2v, acc(u + .5 * h * k2u)
    k4u, k4v = up + h * k3v, acc(u + h * k3u)
    return (u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u),
            up + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v))


def oracle_cycle(u0, L2, E, L, h=1e-4):
    u, up, phi, t = u0, 0.0, 0.0, 0.0
    max_u = min_u = u0
    while True:
        un, upn = rk4_step(u, up, h, L2)
        if un <= 0:
            raise RuntimeError("oracle escape")
        if up >= 0.0 and upn < 0.0 and phi > 0:
            a, b = 0.0, h
            for _ in range(60):
                m = 0.5 * (a + b)
                um, umv = rk4_step(u, up, m, L2)
                if umv >= 0:
                    a = m
                else:
                    b = m
            ue, _ = rk4_step(u, up, a, L2)
            t += 0.5 * (ft(u, E, L) + ft(ue, E, L)) * a - 0.5 * (ft(u, E, L) + ft(un, E, L)) * h
            max_u = max(max_u, ue)
            return phi + a, t, 1.0 / max_u, 1.0 / min_u
        t += 0.5 * (ft(u, E, L) + ft(un, E, L)) * h
        max_u, min_u = max(max_u, un), min(min_u, un)
        phi += h
        u, up = un, upn


def setup_bound(rp, e):
    up_ = 1.0 / rp
    ua = up_ * (1.0 - e) / (1.0 + e)
    L2 = 2.0 / ((up_ + ua) - 2.0 * (up_ * up_ + up_ * ua + ua * ua))
    E2 = 1.0 + L2 * (up_ * up_ - 2.0 * up_ ** 3) - 2.0 * up_
    um = 0.5 * (up_ + ua)
    fmid = (E2 - 1.0) / L2 + 2.0 * um / L2 - um * um + 2.0 * um ** 3
    assert fmid > 0 and 0 < E2 < 1, "not a bound orbit"
    return up_, L2, math.sqrt(E2)


def setup_scatter(rp, E):
    up_ = 1.0 / rp
    L2 = (E * E - 1.0 + 2.0 * up_) / (up_ * up_ * (1.0 - 2.0 * up_))
    udd = 1.0 / L2 + 3.0 * up_ * up_ - up_
    assert udd < 0, "closest-approach branch invalid"
    return up_, L2


def oracle_sweep(u0, L2, h=1e-4, u_stop=1e-3, max_phi=200.0):
    u, up, phi = u0, 0.0, 0.0
    while u > u_stop:
        un, upn = rk4_step(u, up, h, L2)
        if un <= 0 or (1.0 - 2.0 * un) <= 0:
            return None
        u, up, phi = un, upn, phi + h
        if phi > max_phi:
            return None
    return phi


def main():
    print("=== Held-out Binet probe: r1 bands applied beyond r1's seed set (e<=0.7) ===")
    print(f"host: {os.uname().sysname} {os.uname().release}, cpus={os.cpu_count()}, load={os.getloadavg()[0]:.2f}")
    print(f"M={M}, m={MBANDS} bands/octave; candidate = exact in-band rotation, closed-form events; oracle = RK4 exact Binet ODE")
    print()
    print("--- bound orbits (r1 criteria: prec 1%, period 0.1%, shape 1%, crossings 512) ---")
    for rp in (7.0, 8.0, 10.0):
        for e in (0.75, 0.85, 0.9, 0.95, 0.99):
            try:
                u0, L2, E = setup_bound(rp, e)
            except AssertionError as ex:
                print(f"r_p={rp:5} e={e:5}: skipped ({ex})")
                continue
            L = math.sqrt(L2)
            try:
                dphi_b, dt_b, cross, (rp_b, ra_b) = run_banded(u0, L2, E, L, 3)
                dphi_o, t_o, rp_o, ra_o = oracle_cycle(u0, L2, E, L)
            except Exception as ex:
                print(f"r_p={rp:5} e={e:5}: FAILED {type(ex).__name__} {ex}")
                continue
            prec_b, prec_o = dphi_b[2] - 2 * math.pi, dphi_o - 2 * math.pi
            prec_err = abs(prec_b - prec_o) / abs(prec_o)
            per_err = abs(dt_b[2] - t_o) / t_o
            shp_err = max(abs(rp_b - rp_o) / rp_o, abs(ra_b - ra_o) / ra_o)
            v = (prec_err <= 0.01, per_err <= 0.001, shp_err <= 0.01, cross <= 512)
            print(f"r_p={rp:5} e={e:5}  prec_err={prec_err:9.2e} {'PASS' if v[0] else 'FAIL'}"
                  f"  period_err={per_err:9.2e} {'PASS' if v[1] else 'FAIL'}"
                  f"  shape_err={shp_err:9.2e} {'PASS' if v[2] else 'FAIL'}"
                  f"  cross/cyc={cross:6.1f} {'PASS' if v[3] else 'FAIL'}"
                  f"   (prec_o={prec_o:.4f} rad/cyc, L={L:.3f}, E={E:.6f})")

    print()
    print("--- P5: exact cycle repetition at e=0.95, r_p=8, 40 cycles (r1 band 1e-12 rel) ---")
    u0, L2, E = setup_bound(8.0, 0.95)
    L = math.sqrt(L2)
    dphi, dt, cross, _ = run_banded(u0, L2, E, L, 40)
    med = sorted(dphi)[len(dphi) // 2]
    dev = max(abs(x - med) / med for x in dphi)
    medt = sorted(dt)[len(dt) // 2]
    devt = max(abs(x - medt) / medt for x in dt)
    print(f"cycles={len(dphi)}  max rel dev of dphi/cycle={dev:.2e}  of dtime/cycle={devt:.2e}")

    print()
    print("--- P6: massive hyperbolic flybys (light-gate band 1% as reference) ---")
    for rp in (8.0, 10.0, 15.0):
        for E in (1.05, 1.155, 1.414, 2.0):
            try:
                u0, L2 = setup_scatter(rp, E)
            except AssertionError as ex:
                print(f"r_p={rp:5} E={E:6}: skipped ({ex})")
                continue
            L = math.sqrt(L2)
            try:
                ph_b = banded_sweep(u0, L2, E, L)
            except Exception as ex:
                print(f"r_p={rp:5} E={E:6}: banded FAILED {ex}")
                continue
            ph_o = oracle_sweep(u0, L2, h=5e-5 if E >= 1.4 else 1e-4)
            if ph_o is None:
                print(f"r_p={rp:5} E={E:6}: oracle captures (invalid case)")
                continue
            defl_b, defl_o = 2 * ph_b - math.pi, 2 * ph_o - math.pi
            derr = abs(defl_b - defl_o) / defl_o
            vinf = math.sqrt(max(0.0, 1.0 - 1.0 / E / E))
            print(f"r_p={rp:5} E={E:6} v_inf={vinf:.3f}c  defl_exact={defl_o:8.4f} rad  defl_banded={defl_b:8.4f}"
                  f"  err={derr:9.2e} {'PASS(1%)' if derr <= 0.01 else 'FAIL(1%)'}")

    print()
    print("--- controls ---")
    u0, L2, E = setup_bound(8.0, 0.95)
    d1 = oracle_cycle(u0, L2, E, math.sqrt(L2), h=1e-4)[0]
    d2 = oracle_cycle(u0, L2, E, math.sqrt(L2), h=5e-5)[0]
    print(f"oracle Richardson h=1e-4 vs 5e-5: rel diff {abs(d1 - d2) / d1:.2e}")
    u0s, L2s = setup_scatter(8.0, 2.0)
    s1 = oracle_sweep(u0s, L2s, h=1e-4)
    s2 = oracle_sweep(u0s, L2s, h=5e-5)
    print(f"scattering oracle Richardson: rel diff {abs(s1 - s2) / s1:.2e}")
    # banded quadrature convergence: Gauss-8 per segment vs bisection-refined Simpson via half-segments is implicit;
    # instead verify the oracle period against a finer oracle period on one case
    t1 = oracle_cycle(u0, L2, E, math.sqrt(L2), h=1e-4)[1]
    t2 = oracle_cycle(u0, L2, E, math.sqrt(L2), h=5e-5)[1]
    print(f"oracle period Richardson: rel diff {abs(t1 - t2) / t1:.2e}")


if __name__ == "__main__":
    main()
