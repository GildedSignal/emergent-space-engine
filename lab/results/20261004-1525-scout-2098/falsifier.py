#!/usr/bin/env python3
"""Falsifier: how few kicks per orbit hold B14's apsidal precession (10%)?

Hill regime: test-particle moon (a_m=1, e0) around a planet (GM=1), perturbed
by the parent 'sun' (mass ratio mu) on a circular orbit at a_s=(3 mu)^{1/3}/f.
The split is the engine's (law.md): exact Kepler drift (the compiled tube) +
tide kicks at a fixed step in the drift's own phase (n kicks per moon orbit).

Methods:
  plain   KDK (kick h/2, drift h, kick h/2), sun phase at kick time
  corr3   plain + WHFast 3rd-order symplectic corrector (start/end/outputs)
  corr5   same, 5th-order corrector (Rein & Tamayo 2015 coefficients)
  fr4     Forest-Ruth 4th-order composition (4 force evals / step)
  avg     double-averaged disturbing function (the H0190/r9 method; control)

Reference: plain at 512 kicks/orbit (checked vs 1024 on one case).
Cost metric: tide-force evaluations per moon orbit.
"""
import math, json, sys

TWOPI = 2.0 * math.pi
MU = 1.0e6
E0 = 0.10
A1 = 0.41833001326703777398908601289259374469640768464934
A2 = 0.83666002653407554797817202578518748939281536929867
B31 = -0.024900596027799867499350357910273437184309981229127
B51 = -0.0083001986759332891664501193034244790614366604097090
B52 = 0.041500993379666445832250596517122395307183302048545
W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W0 = -2.0 ** (1.0 / 3.0) * W1

class Escape(Exception):
    pass

class Sim:
    __slots__ = ('x', 'y', 'vx', 'vy', 't', 'fevals', 'a_s', 'n_s', 'th0')
    def __init__(self, f, e0=E0, a_m=1.0):
        self.a_s = (3.0 * MU) ** (1.0 / 3.0) / f * a_m
        self.n_s = math.sqrt(1.0 + MU) / self.a_s ** 1.5
        self.th0 = 0.6
        self.t = 0.0
        self.fevals = 0
        # start at periapsis
        n = 1.0 / a_m ** 1.5
        v = math.sqrt((1.0 + e0) / (a_m * (1.0 - e0)))
        self.x = a_m * (1.0 - e0); self.y = 0.0
        self.vx = 0.0; self.vy = v

    def tide(self, x, y, t):
        self.fevals += 1
        th = self.th0 + self.n_s * t
        c, s = math.cos(th), math.sin(th)
        sx, sy = self.a_s * c, self.a_s * s
        dx, dy = sx - x, sy - y
        d2 = dx * dx + dy * dy
        d = math.sqrt(d2)
        s2 = self.a_s * self.a_s
        return MU * (dx / (d2 * d) - c / s2), MU * (dy / (d2 * d) - s / s2)

    def kick(self, dt, t=None):
        ax, ay = self.tide(self.x, self.y, self.t if t is None else t)
        self.vx += ax * dt; self.vy += ay * dt

    def drift(self, dt):
        """Exact Kepler drift about GM=1."""
        self.t += dt
        x, y, vx, vy = self.x, self.y, self.vx, self.vy
        r = math.hypot(x, y)
        v2 = vx * vx + vy * vy
        rv = x * vx + y * vy
        a = 1.0 / (2.0 / r - v2)
        if a <= 0.0:
            raise Escape('hyperbolic')
        hz = x * vy - y * vx
        ex = (v2 - 1.0 / r) * x - rv * vx
        ey = (v2 - 1.0 / r) * y - rv * vy
        e = math.hypot(ex, ey)
        if e >= 0.995:
            raise Escape('e=%.3f' % e)
        om = math.atan2(ey, ex)
        n = 1.0 / a ** 1.5
        # eccentric anomaly now
        E0 = math.atan2((y * ex - x * ey) / (e * hz) if False else 0.0, 1.0)
        sE = (rv / math.sqrt(a)) / e
        cE = (1.0 - r / a) / e
        E = math.atan2(sE, cE)
        M = E - e * math.sin(E) + n * dt
        M = M % TWOPI
        E = M if e < 1e-12 else (math.pi if M > math.pi else M)
        for _ in range(100):
            f = E - e * math.sin(E) - M
            dE = f / (1.0 - e * math.cos(E))
            E -= dE
            if abs(dE) < 1e-15:
                break
        cE, sE = math.cos(E), math.sin(E)
        px = a * (cE - e)
        py = a * math.sqrt(1.0 - e * e) * sE
        Edot = n / (1.0 - e * cE)
        pvx = -a * sE * Edot
        pvy = a * math.sqrt(1.0 - e * e) * cE * Edot
        co, so = math.cos(om), math.sin(om)
        self.x = co * px - so * py
        self.y = so * px + co * py
        self.vx = co * pvx - so * pvy
        self.vy = so * pvx + co * pvy

    def elements(self):
        x, y, vx, vy = self.x, self.y, self.vx, self.vy
        r = math.hypot(x, y)
        v2 = vx * vx + vy * vy
        rv = x * vx + y * vy
        a = 1.0 / (2.0 / r - v2)
        ex = (v2 - 1.0 / r) * x - rv * vx
        ey = (v2 - 1.0 / r) * y - rv * vy
        e = math.hypot(ex, ey)
        om = math.atan2(ey, ex) % TWOPI
        return a, e, om

    # --- WHFast corrector Z operator: drift(a h); kick(-b h); drift(-2a h);
    #     kick(+b h); drift(a h)  (kepler_step/interaction_step pattern) ---
    def zop(self, aa, bb):
        t0 = self.t          # canonical operator at frozen time
        self.drift(aa)
        self.kick(-bb, t0)
        self.drift(-2.0 * aa)
        self.kick(bb, t0)
        self.drift(aa)
        assert abs(self.t - t0) < 1e-12

    def corrector(self, h, order, inv):
        if order == 3:
            self.zop(inv * A1 * h, -inv * B31 * h)
            self.zop(-inv * A1 * h, inv * B31 * h)
        else:
            self.zop(-inv * A2 * h, -inv * B51 * h)
            self.zop(-inv * A1 * h, -inv * B52 * h)
            self.zop(inv * A1 * h, inv * B52 * h)
            self.zop(inv * A2 * h, inv * B51 * h)

    def step_plain(self, h):
        self.drift(0.5 * h)
        self.kick(h)          # sun phase at step midpoint
        self.drift(0.5 * h)

    def step_fr4(self, h):
        self.kick(W1 * 0.5 * h)
        self.drift(W1 * h)
        self.kick((W0 + W1) * 0.5 * h)
        self.drift(W0 * h)
        self.kick((W0 + W1) * 0.5 * h)
        self.drift(W1 * h)
        self.kick(W1 * 0.5 * h)

def run(f, n_kicks, method, horizon_po):
    """horizon_po: horizon in planet orbits (sun periods)."""
    s = Sim(f)
    T = TWOPI                       # moon period (a=1)
    Tp = TWOPI / s.n_s              # planet (sun) period
    h = T / n_kicks
    cor = method.startswith('corr')
    order = 3 if method == 'corr3' else 5
    if cor:
        s.corrector(h, order, +1.0)   # real -> mapping
    out = []
    n_orb = int(horizon_po * Tp / T)
    try:
        k = 0
        next_out = 0.0
        while k * h < horizon_po * Tp:
            if method == 'fr4':
                s.step_fr4(h)
            else:
                s.step_plain(h)
            k += 1
            if s.t >= next_out:            # sample once per moon orbit
                if cor:
                    s.corrector(h, order, -1.0)  # mapping -> real
                out.append((s.t,) + s.elements())
                if cor:
                    s.corrector(h, order, +1.0)
                next_out += T
    except Escape as ex:
        return {'class': 'escape', 'why': str(ex), 'samples': len(out)}
    if cor:
        s.corrector(h, order, -1.0)
    return {'class': 'bound', 'samples': out,
            'fevals_per_orbit': s.fevals / (s.t / T)}

def precession_rate(samples):
    """Linear fit of unwrapped periapsis angle vs t; discards first 20%."""
    ts = [s[0] for s in samples]
    oms = [s[3] for s in samples]
    unw = [oms[0]]
    for i in range(1, len(oms)):
        d = oms[i] - oms[i - 1]
        while d > math.pi: d -= TWOPI
        while d < -math.pi: d += TWOPI
        unw.append(unw[-1] + d)
    k0 = len(ts) // 5
    ts, unw = ts[k0:], unw[k0:]
    nt = len(ts)
    if nt < 5:
        return None
    st = sum(ts) / nt; su = sum(unw) / nt
    num = sum((t - st) * (u - su) for t, u in zip(ts, unw))
    den = sum((t - st) ** 2 for t in ts)
    return num / den

def avg_rate(f, e0=E0, a_m=1.0, horizon_po=None):
    """r9's control: single average over the moon's mean anomaly, sun resolved.
    (The planar double average is exactly constant: the 2D circular average of
    1/|s-r| carries only the n=0 multipole for r < a_s.) Integrates the
    secular Lagrange equations for (e, varpi) with lambda_s = n_s t.
    Returns sampled (t, a, e, varpi) like the kick runs."""
    a_s = (3.0 * MU) ** (1.0 / 3.0) / f
    n_s = math.sqrt(1.0 + MU) / a_s ** 1.5
    n = 1.0 / a_m ** 1.5
    NG = 48
    xs = [((i + 0.5) / NG) for i in range(NG)]  # uniform (periodic) nodes

    def phi(e, om, lam):
        """<R>_M at fixed sun longitude lam."""
        tot = 0.0
        for i in range(NG):
            M = TWOPI * xs[i]
            E = M
            for _ in range(60):
                fE = E - e * math.sin(E) - M
                dE = fE / (1.0 - e * math.cos(E))
                E -= dE
                if abs(dE) < 1e-14: break
            px = a_m * (math.cos(E) - e)
            py = a_m * math.sqrt(1 - e * e) * math.sin(E)
            co, so = math.cos(om), math.sin(om)
            x, y = co * px - so * py, so * px + co * py
            c, s2 = math.cos(lam), math.sin(lam)
            dx, dy = a_s * c - x, a_s * s2 - y
            d = math.sqrt(dx * dx + dy * dy)
            tot += MU * (1.0 / d - (x * c + y * s2) / (a_s * a_s))
        return tot / NG  # uniform-in-M average, weight pi/NG each / 2pi

    def derivs(t, e, om):
        lam = 0.6 + n_s * t  # same sun phase convention as Sim
        de = 1e-6
        Rep = phi(e + de, om, lam); Rem = phi(e - de, om, lam)
        Rop = phi(e, om + de, lam); Rom = phi(e, om - de, lam)
        dRde = (Rep - Rem) / (2 * de)
        dRdom = (Rop - Rom) / (2 * de)
        k = math.sqrt(1 - e * e) / (n * a_m * a_m * e)
        return k * dRde, -k * dRdom

    dt = 0.05 / n  # ~70 steps per moon orbit
    e, om, t = e0, 0.0, 0.0
    samples = []
    Tp = TWOPI / n_s
    while t < (horizon_po or 20.0) * Tp:
        om0, e0_ = om, e
        # RK2 midpoint
        wp, ep = derivs(t, e, om)
        wm, em = derivs(t + 0.5 * dt, e + 0.5 * dt * ep, om + 0.5 * dt * wp)
        om = om0 + dt * wm
        e = e0_ + dt * em
        t += dt
        if e >= 0.995 or e < 1e-6:
            return {'class': 'escape', 'why': 'e=%.3f' % e, 'samples': samples}
        samples.append((t, a_m, e, om % TWOPI))
    return {'class': 'bound', 'samples': samples}

def main():
    results = []
    for f in (0.2, 0.3, 0.4):
        horizon = 20.0
        ref_run = run(f, 512, 'plain', horizon)
        ref = precession_rate(ref_run['samples']) if ref_run['class'] == 'bound' else None
        results.append({'f': f, 'ref': ref})
        print('f=%.2f  ref rate=%.6g rad/orbit  (%d samples)' %
              (f, ref, len(ref_run['samples'])))
        for method in ('plain', 'corr3', 'corr5', 'fr4'):
            for nk in (32, 16, 8, 6, 4, 3, 2, 1):
                rr = run(f, nk, method, horizon)
                if rr['class'] != 'bound':
                    print('  %-6s nk=%-3d ESCAPE/%s' % (method, nk, rr['why']))
                    results.append({'f': f, 'method': method, 'nk': nk,
                                    'class': 'escape'})
                    continue
                rate = precession_rate(rr['samples'])
                ef = rr['samples'][-1][2]
                err = abs(rate - ref) / abs(ref) if ref and rate else None
                fe = rr['fevals_per_orbit']
                results.append({'f': f, 'method': method, 'nk': nk,
                                'class': 'bound', 'rate': rate, 'relerr': err,
                                'efinal': ef, 'fevals_per_orbit': fe})
                print('  %-6s nk=%-3d rate=%.6g  relerr=%.3g  e_end=%.4f  fev/orb=%.1f'
                      % (method, nk, rate, err, ef, fe))
        ar = avg_rate(f, horizon_po=horizon)
        if ar['class'] != 'bound':
            print('  avg    ESCAPE/%s' % ar['why'])
        else:
            arate = precession_rate(ar['samples'])
            aerr = abs(arate - ref) / abs(ref) if ref else None
            print('  avg    rate=%.6g  relerr=%.3g  e_end=%.4f' %
                  (arate, aerr, ar['samples'][-1][2]))
            results.append({'f': f, 'method': 'avg', 'relerr': aerr,
                            'rate': arate})
    json.dump(results, open('lab/results/20261004-1525-scout-2098/results.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
