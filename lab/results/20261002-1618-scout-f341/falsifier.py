#!/usr/bin/env python3
"""Scout falsifier: fewer kicks per orbit at the same behaviour (run 20261002-1618-scout-f341).

Plane baseline (crates/universe/src/step.rs): exact Kepler drift (a tube is read, never
stepped: free) + DKD kicks of weight H at the interval midpoint, H = P/64 in the drift's
phase; a kick evaluates the tide and rebinds. The falsifier replicates this in floats.

Candidate: Gauss-node Picard collocation of the kick layer (GP-s). One window per radial
period, s Gauss-Legendre nodes; node impulses J_i = w_i H a_tide(r(t_i)) iterated to a
fixed point (warm-started from the previous window). Converged limit = collocation of the
tide on the self-consistent trajectory (order 2s per window); later nodes feel earlier
nodes' impulses, the phase feedback that r4's fixed-arc first-order kicks lacked.
Accounting: kicks per orbit = s * mean sweeps (each sweep is s tide evaluations); drifts
are free, as in the engine.

Cases: M1 tune/smoke (e0=0.05, 0.3 R_H), M2 held-out (e0=0.3, 0.3 R_H), M3 held-out
(e0=0.3, 0.6 R_H), F1 flyby (B13-like), R1/R2 2:1 resonance nominal/detuned (B17-like).
Truth: the same split at 2048 (moons) / 1024 (resonance) / 8192 (flyby) kicks per orbit,
with a finer control verifying convergence. Negative control: LF-8/16.

Usage: python3 falsifier.py [--smoke]
"""
import json
import math
import os
import sys
import time

T0 = time.time()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

GAUSS = {
    2: ((0.21132486540518713, 0.7886751345948129), (0.5, 0.5)),
    3: ((0.1127016653792583, 0.5, 0.8872983346207417), (5.0 / 18.0, 4.0 / 9.0, 5.0 / 18.0)),
    4: ((0.06943184420297371, 0.33000947820757187, 0.6699905217924282, 0.9305681557970263),
        (0.17392742256872693, 0.3260725774312731, 0.3260725774312731, 0.17392742256872693)),
}

# ---------------------------------------------------------------- Kepler: exact drift


def _C(z):
    if z > 1e-6:
        return (1.0 - math.cos(math.sqrt(z))) / z
    if z < -1e-6:
        return (math.cosh(math.sqrt(-z)) - 1.0) / (-z)
    return 0.5 - z / 24.0 + z * z / 720.0


def _S(z):
    if z > 1e-6:
        s = math.sqrt(z)
        return (s - math.sin(s)) / (s * s * s)
    if z < -1e-6:
        s = math.sqrt(-z)
        return (math.sinh(s) - s) / (s * s * s)
    return 1.0 / 6.0 - z / 120.0 + z * z / 5040.0


def prop(r, v, mu, dt):
    """Exact two-body propagation (universal variables; F'(chi) = |r| so Newton is safe)."""
    r0 = math.hypot(r[0], r[1])
    v2 = v[0] * v[0] + v[1] * v[1]
    alpha = 2.0 / r0 - v2 / mu
    vr0 = (r[0] * v[0] + r[1] * v[1]) / r0
    sq = math.sqrt(mu)
    chi = sq * dt * (alpha if alpha > 0.0 else 1.0 / r0)
    for _ in range(80):
        z = alpha * chi * chi
        C, S = _C(z), _S(z)
        F = (r0 * vr0 / sq) * chi * chi * C + (1.0 - alpha * r0) * chi ** 3 * S + r0 * chi - sq * dt
        rr = chi * chi * C + (r0 * vr0 / sq) * chi * (1.0 - z * S) + r0 * (1.0 - z * C)
        d = F / rr
        chi -= d
        if abs(d) <= 1e-13 * (1.0 + abs(chi)):
            break
    z = alpha * chi * chi
    C, S = _C(z), _S(z)
    f = 1.0 - chi * chi / r0 * C
    g = dt - chi ** 3 / sq * S
    rx, ry = f * r[0] + g * v[0], f * r[1] + g * v[1]
    rn = math.hypot(rx, ry)
    fd = sq / (r0 * rn) * chi * (z * S - 1.0)
    gd = 1.0 - chi * chi / rn * C
    return (rx, ry), (fd * r[0] + gd * v[0], fd * r[1] + gd * v[1])


def osc(r, v, mu):
    """Planar osculating (a, e, varpi, M) — elliptic only for M."""
    rn = math.hypot(r[0], r[1])
    v2 = v[0] * v[0] + v[1] * v[1]
    a = 1.0 / (2.0 / rn - v2 / mu)
    rv = r[0] * v[0] + r[1] * v[1]
    k = v2 / mu - 1.0 / rn
    ex, ey = k * r[0] - rv / mu * v[0], k * r[1] - rv / mu * v[1]
    e = math.hypot(ex, ey)
    varpi = math.atan2(ey, ex) if e > 1e-11 else 0.0
    M = float("nan")
    if 0.0 < e < 0.999 and a > 0.0:
        cosE = (1.0 - rn / a) / e
        sinE = rv / (e * math.sqrt(mu * a))
        E = math.atan2(sinE, cosE)
        M = E - e * math.sin(E)
    return a, e, varpi, M


# ---------------------------------------------------------------- moon (Hill tide) cases


class MoonScene:
    """Planet-centred frame; star of mass mu_s at a_p on a circular orbit at rate n_p.
    Tide (the kick layer): -mu_s (r-R_s)/|r-R_s|^3 - mu_s R_s/a_p^3 (direct + indirect)."""

    def __init__(self, a_m_frac, e0):
        self.mu_p, self.mu_s, self.a_p = 1.0, 1000.0, 1000.0
        self.n_p = math.sqrt((self.mu_s + self.mu_p) / self.a_p ** 3)
        self.R_H = self.a_p * (self.mu_p / (3.0 * self.mu_s)) ** (1.0 / 3.0)
        self.a_m = a_m_frac * self.R_H
        self.e0 = e0
        rp = self.a_m * (1.0 - e0)
        vm = math.sqrt(self.mu_p * (1.0 + e0) / (1.0 - e0) / self.a_m)
        self.state0 = ((rp, 0.0), (0.0, vm))
        self.P0 = 2.0 * math.pi * math.sqrt(self.a_m ** 3 / self.mu_p)

    def star(self, t):
        th = self.n_p * t
        c, s = math.cos(th), math.sin(th)
        return (self.a_p * c, self.a_p * s), (-self.a_p * self.n_p * s, self.a_p * self.n_p * c)

    def tide(self, r, t):
        Rs, _ = self.star(t)
        dx, dy = r[0] - Rs[0], r[1] - Rs[1]
        d3 = (dx * dx + dy * dy) ** 1.5
        k = -self.mu_s / d3
        ki = -self.mu_s / self.a_p ** 3
        return (k * dx + ki * Rs[0], k * dy + ki * Rs[1])

    def jacobi(self, r, v, t):
        mu_s, mu_p, n = self.mu_s, self.mu_p, self.n_p
        Rs, Vs = self.star(t)
        G = (mu_s / (mu_s + mu_p),)  # barycentre offset along Rs
        gx, gy = G[0] * Rs[0], G[0] * Rs[1]
        gvx, gvy = G[0] * Vs[0], G[0] * Vs[1]
        qx, qy = r[0] - gx, r[1] - gy
        wvx, wvy = v[0] - gvx + n * qy, v[1] - gvy - n * qx  # rotate by -n t
        th = n * t
        c, s = math.cos(th), math.sin(th)
        px, py = c * qx + s * qy, -s * qx + c * qy
        p2 = px * px + py * py
        v2 = wvx * wvx + wvy * wvy
        r1 = math.hypot(r[0] - Rs[0], r[1] - Rs[1])
        rp = math.hypot(r[0], r[1])
        return n * n * p2 + 2.0 * mu_s / r1 + 2.0 * mu_p / rp - v2


def lf_moon(sc, nk, T_end, sample_dt):
    """The plane's law in floats: DKD, H = P(a)/nk in phase, rebind each kick."""
    r, v = sc.state0
    t, kicks = 0.0, 0
    samples = []
    nxt = 0.0
    while True:
        while nxt <= t + 1e-9 and nxt <= T_end:
            rr, vv = (r, v) if abs(t - nxt) < 1e-12 else prop(r, v, sc.mu_p, nxt - t)
            a, e, w, _ = osc(rr, vv, sc.mu_p)
            samples.append((t if abs(t - nxt) < 1e-12 else nxt, a, e, w, sc.jacobi(rr, vv, nxt)))
            nxt += sample_dt
        if t >= T_end:
            break
        a, ee, _, _ = osc(r, v, sc.mu_p)
        if a <= 0.0 or ee >= 0.9999 or math.isnan(a):
            samples.append((t, a, ee, 0.0, sc.jacobi(r, v, t)))
            return samples, kicks / (T_end / sc.P0), True
        P = 2.0 * math.pi * math.sqrt(a ** 3 / sc.mu_p)
        H = P / nk
        rm, vm = prop(r, v, sc.mu_p, H / 2.0)
        at = sc.tide(rm, t + H / 2.0)
        v = (vm[0] + at[0] * H, vm[1] + at[1] * H)
        r, v = prop(rm, v, sc.mu_p, H / 2.0)
        t += H
        kicks += 1
    return samples, kicks / (T_end / sc.P0), False


def gp_moon(sc, s, T_end, sample_dt, wpo=1):
    """Gauss-node Picard collocation: wpo windows per orbit, s nodes, warm-started impulses."""
    nodes, ws = GAUSS[s]
    r, v = sc.state0
    t, ev = 0.0, 0
    samples, sweeps = [], []
    J = [(0.0, 0.0)] * s
    nxt = 0.0
    while True:
        while nxt <= t + 1e-9 and nxt <= T_end:
            rr, vv = (r, v) if abs(t - nxt) < 1e-12 else prop(r, v, sc.mu_p, nxt - t)
            a, e, w, _ = osc(rr, vv, sc.mu_p)
            samples.append((t if abs(t - nxt) < 1e-12 else nxt, a, e, w, sc.jacobi(rr, vv, nxt)))
            nxt += sample_dt
        if t >= T_end:
            break
        a, ee, _, _ = osc(r, v, sc.mu_p)
        if a <= 0.0 or ee >= 0.9999 or math.isnan(a):
            samples.append((t, a, ee, 0.0, sc.jacobi(r, v, t)))
            return samples, ev / (T_end / sc.P0), (sum(sweeps) / len(sweeps) if sweeps else 0.0), True
        P = 2.0 * math.pi * math.sqrt(a ** 3 / sc.mu_p)
        H = P / wpo
        sw = 0
        while True:
            cur, tprev = (r, v), t
            rs = []
            for i in range(s):
                cprev = nodes[i - 1] if i else 0.0
                ri, vi = prop(*cur, sc.mu_p, (nodes[i] - cprev) * H)
                rs.append((ri, t + nodes[i] * H))
                cur = (ri, (vi[0] + J[i][0], vi[1] + J[i][1]))
            re, ve = prop(*cur, sc.mu_p, (1.0 - nodes[-1]) * H)
            Jn = []
            for i in range(s):
                at = sc.tide(rs[i][0], rs[i][1])
                Jn.append((ws[i] * H * at[0], ws[i] * H * at[1]))
            diff = max(max(abs(Jn[i][0] - J[i][0]), abs(Jn[i][1] - J[i][1])) for i in range(s))
            scale = max(max(abs(x), abs(y)) for (x, y) in Jn) + 1e-300
            J = Jn
            sw += 1
            ev += s
            if diff <= 1e-12 * scale or sw >= 40:
                # final rebuild with the converged impulses (drifts only: free)
                cur = (r, v)
                for i in range(s):
                    cprev = nodes[i - 1] if i else 0.0
                    ri, vi = prop(*cur, sc.mu_p, (nodes[i] - cprev) * H)
                    cur = (ri, (vi[0] + J[i][0], vi[1] + J[i][1]))
                re, ve = prop(*cur, sc.mu_p, (1.0 - nodes[-1]) * H)
                break
        r, v = re, ve
        t += H
        sweeps.append(sw)
    return samples, ev / (T_end / sc.P0), sum(sweeps) / len(sweeps), False



def unwrap(xs):
    res = [xs[0]]
    for i in range(1, len(xs)):
        d = xs[i] - xs[i - 1]
        res.append(res[-1] + d - 2.0 * math.pi * round(d / (2.0 * math.pi)))
    return res


def linfit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx if sxx else float("nan")


def y4_moon(sc, macro_per_orbit, T_end, sample_dt):
    """Yoshida 4th-order triple jump of DKD steps (weights w1,w2,w3; w2 < 0).
    Three kicks per macro step; the extra/negative drifts are free (exact Kepler)."""
    cbrt2 = 2.0 ** (1.0 / 3.0)
    w = (1.0 / (2.0 - cbrt2), -cbrt2 / (2.0 - cbrt2), 1.0 / (2.0 - cbrt2))
    r, v = sc.state0
    t, kicks = 0.0, 0
    samples = []
    nxt = 0.0
    while True:
        while nxt <= t + 1e-9 and nxt <= T_end:
            rr, vv = (r, v) if abs(t - nxt) < 1e-12 else prop(r, v, sc.mu_p, nxt - t)
            a, e, wp, _ = osc(rr, vv, sc.mu_p)
            samples.append((nxt, a, e, wp, sc.jacobi(rr, vv, nxt)))
            nxt += sample_dt
        if t >= T_end:
            break

        a, ee, _, _ = osc(r, v, sc.mu_p)
        if a <= 0.0 or ee >= 0.9999 or math.isnan(a):
            samples.append((t, a, ee, 0.0, sc.jacobi(r, v, t)))
            return samples, kicks / (T_end / sc.P0), True
        P = 2.0 * math.pi * math.sqrt(a ** 3 / sc.mu_p)
        H = P / macro_per_orbit
        for wi in w:
            rm, vm = prop(r, v, sc.mu_p, wi * H / 2.0)
            at = sc.tide(rm, t + wi * H / 2.0)
            v = (vm[0] + at[0] * wi * H, vm[1] + at[1] * wi * H)
            r, v = prop(rm, v, sc.mu_p, wi * H / 2.0)
            t += wi * H
            kicks += 1
    return samples, kicks / (T_end / sc.P0), False


def moon_metrics(samples, P0, skip_orbits=30):
    ts = [s[0] for s in samples]
    es = [s[2] for s in samples]
    ws = unwrap([s[3] for s in samples])
    Js = [s[4] for s in samples]
    i0 = next((i for i, t in enumerate(ts) if t >= skip_orbits * P0), max(1, len(ts) // 2))
    prec = linfit(ts[i0:], ws[i0:]) * P0  # rad per orbit
    stable = all(0.002 < e < 0.95 for e in es) and abs(es[-1] - es[0]) < 0.5

    dj = max(abs(J - Js[0]) for J in Js) / abs(Js[0])
    # growth exponent on |J - J0| (B12-style), over the samples above a floor
    ys = [math.log10(max(abs(J - Js[0]), 1e-17)) for J in Js]
    expo = linfit(ts, ys) * P0
    emax_dev = max(abs(e - e) for e in es)  # placeholder, replaced by caller vs truth
    return dict(prec_rad_per_orbit=prec, stable=stable, jacobi_rel_drift=dj,
                jacobi_exponent_per_orbit=expo, e_final=es[-1], e_max=max(es), e_min=min(es))


def interp_truth(ts_tr, vals_tr, t):
    if t <= ts_tr[0]:
        return vals_tr[0]
    if t >= ts_tr[-1]:
        return vals_tr[-1]
    lo, hi = 0, len(ts_tr) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ts_tr[mid] <= t:
            lo = mid
        else:
            hi = mid
    f = (t - ts_tr[lo]) / (ts_tr[hi] - ts_tr[lo])
    return vals_tr[lo] * (1.0 - f) + vals_tr[hi] * f


# ---------------------------------------------------------------- resonance cases


class ResScene:
    """Two planets about a star (mu_s = 1, masses m). Kick layer: direct + indirect
    of the other planet; drift: exact Kepler about the star (heliocentric frame)."""

    def __init__(self, m, a, e, lam):
        self.m, self.a, self.e, self.lam = m, a, e, lam
        self.mu_s = 1.0

    def state0(self):
        r, v = [], []
        for m, a, e, lam in zip(self.m, self.a, self.e, self.lam):
            w = lam  # start at longitude of periapsis offset: place at varpi=lam, M=0
            rp = a * (1.0 - e)
            vm = math.sqrt(self.mu_s * (1.0 + e) / (1.0 - e) / a)
            c, s = math.cos(w), math.sin(w)
            r.append((rp * c, rp * s))
            v.append((-vm * s, vm * c))
        return r, v

    def kick(self, i, rs, ts_unused=None):
        out = [0.0, 0.0]
        ri = rs[i]
        for j in range(len(rs)):
            if j == i:
                continue
            rj = rs[j]
            dx, dy = ri[0] - rj[0], ri[1] - rj[1]
            d3 = (dx * dx + dy * dy) ** 1.5
            rj3 = (rj[0] ** 2 + rj[1] ** 2) ** 1.5
            out[0] += -self.m[j] * dx / d3 - self.m[j] * rj[0] / rj3
            out[1] += -self.m[j] * dy / d3 - self.m[j] * rj[1] / rj3
        return out


def res_lf(sc, nk, T_end, sample_dt, P1):
    r, v = sc.state0()
    t = [0.0, 0.0]
    tnow = 0.0
    samples = []
    kicks = [0, 0]
    nxt = 0.0
    while True:
        while nxt <= tnow + 1e-9 and nxt <= T_end:
            row = [nxt]
            for i in range(2):
                if abs(t[i] - nxt) < 1e-12:
                    rr, vv = r[i], v[i]
                else:
                    rr, vv = prop(r[i], v[i], sc.mu_s, nxt - t[i])
                a, e, w, M = osc(rr, vv, sc.mu_s)
                lam = w + M if not math.isnan(M) else float("nan")
                row += [a, e, w, lam]
            samples.append(row)
            nxt += sample_dt
        if tnow >= T_end:
            break
        i = 0 if t[0] <= t[1] else 1
        a, _, _, _ = osc(r[i], v[i], sc.mu_s)
        P = 2.0 * math.pi * math.sqrt(a ** 3 / sc.mu_s)
        H = P / nk
        # drift i to its kick time, read j there (a tube read: exact)
        ri, vi = prop(r[i], v[i], sc.mu_s, H / 2.0)
        tj = t[1 - i]
        rj, _ = prop(r[1 - i], v[1 - i], sc.mu_s, t[i] + H / 2.0 - tj)
        at = sc.kick(i, [ri, rj])
        vi = (vi[0] + at[0] * H, vi[1] + at[1] * H)
        r[i], v[i] = prop(ri, vi, sc.mu_s, H / 2.0)
        t[i] += H
        kicks[i] += 1
        tnow = min(t)
    kicks_per_orbit = (kicks[0] / (T_end / P1) + kicks[1] / (T_end / (2.0 * P1))) / 2.0
    return samples, kicks_per_orbit


def res_gp(sc, s, T_end, sample_dt, P1, wpm=1):
    nodes, ws = GAUSS[s]
    r, v = sc.state0()
    t = 0.0
    samples = []
    ev = 0
    sweeps = []
    J = [[(0.0, 0.0)] * s for _ in range(2)]
    nxt = 0.0
    while True:
        while nxt <= t + 1e-9 and nxt <= T_end:
            row = [nxt]
            for i in range(2):
                rr, vv = (r[i], v[i]) if abs(t - nxt) < 1e-12 else prop(r[i], v[i], sc.mu_s, nxt - t)
                a, e, w, M = osc(rr, vv, sc.mu_s)
                lam = w + M if not math.isnan(M) else float("nan")
                row += [a, e, w, lam]
            samples.append(row)
            nxt += sample_dt
        if t >= T_end:
            break
        H = P1 / wpm  # window = a fraction of the inner period
        sw = 0
        while True:
            cur = [(r[0], v[0]), (r[1], v[1])]
            rs_nodes = [[None] * s for _ in range(2)]
            ends = []
            for i in range(2):
                c = cur[i]
                for k in range(s):
                    cprev = nodes[k - 1] if k else 0.0
                    rk, vk = prop(*c, sc.mu_s, (nodes[k] - cprev) * H)
                    rs_nodes[i][k] = rk
                    c = (rk, (vk[0] + J[i][k][0], vk[1] + J[i][k][1]))
                re, ve = prop(*c, sc.mu_s, (1.0 - nodes[-1]) * H)
                ends.append((re, ve))
            diff = scale = 0.0
            for i in range(2):
                Jn = []
                for k in range(s):
                    at = sc.kick(i, [rs_nodes[0][k], rs_nodes[1][k]])
                    Jn.append((ws[k] * H * at[0], ws[k] * H * at[1]))
                for k in range(s):
                    diff = max(diff, abs(Jn[k][0] - J[i][k][0]), abs(Jn[k][1] - J[i][k][1]))
                    scale = max(scale, abs(Jn[k][0]), abs(Jn[k][1]))
                J[i] = Jn
            sw += 1
            ev += 2 * s
            if diff <= 1e-12 * (scale + 1e-300) or sw >= 40:
                for i in range(2):
                    c = (r[i], v[i])
                    for k in range(s):
                        cprev = nodes[k - 1] if k else 0.0
                        rk, vk = prop(*c, sc.mu_s, (nodes[k] - cprev) * H)
                        c = (rk, (vk[0] + J[i][k][0], vk[1] + J[i][k][1]))
                    ends[i] = prop(*c, sc.mu_s, (1.0 - nodes[-1]) * H)
                break
        for i in range(2):
            r[i], v[i] = ends[i]
        t += H
        sweeps.append(sw)
    return samples, ev / (T_end / P1), sum(sweeps) / len(sweeps)


def res_metrics(samples, skip=10):
    ts = [row[0] for row in samples]
    e1 = [row[2] for row in samples]
    lam1 = [row[4] for row in samples]
    lam2 = [row[8] for row in samples]
    w1 = [row[3] for row in samples]
    pump = max(e1[i] for i in range(len(ts)) if ts[i] >= skip)
    th = unwrap([(2.0 * l2 - l1 - w) for l1, l2, w in zip(lam1, lam2, w1)])
    rng = max(th) - min(th)
    if rng > 1.5 * 2.0 * math.pi:
        return dict(pump=pump, regime="circulating")
    return dict(pump=pump, regime="librating", amp=rng / 2.0)


# ---------------------------------------------------------------- flyby case


class FlybyScene:
    """B13-like: a ship's hyperbolic passage of a planet, resolved in the planet's doll.
    Drift: exact hyperbolic Kepler about the planet. Kick layer: the star's tide.
    Window: twice the leg from start (2 R_SOI) through periapsis (step.rs)."""

    def __init__(self):
        self.mu_p, self.mu_s, self.a_p = 1.0, 1000.0, 1000.0
        self.n_p = math.sqrt((self.mu_s + self.mu_p) / self.a_p ** 3)
        self.R_SOI = self.a_p * (self.mu_p / self.mu_s) ** 0.4
        self.vinf = 0.77
        self.rperi = 5.0
        ah = -self.mu_p / self.vinf ** 2
        self.ah = ah
        self.e = 1.0 - self.rperi / ah
        p = -ah * (self.e ** 2 - 1.0)
        r0 = 2.0 * self.R_SOI
        cnu = (p / r0 - 1.0) / self.e
        nu = -math.acos(cnu)  # incoming branch
        self.r0mag = r0
        # state at nu (periapsis along +x, rotated by phi0)
        self.phi0 = 0.7
        vr = math.sqrt(self.mu_p / p) * self.e * math.sin(nu)
        vt = math.sqrt(self.mu_p / p) * (1.0 + self.e * math.cos(nu))
        c, s = math.cos(nu), math.sin(nu)
        r_local = (r0 * c, r0 * s)
        v_local = (vr * c - vt * s, vr * s + vt * c)
        cp, sp = math.cos(self.phi0), math.sin(self.phi0)
        rot = lambda q: (q[0] * cp - q[1] * sp, q[0] * sp + q[1] * cp)
        self.state0 = (rot(r_local), rot(v_local))
        # time from start to periapsis (Kepler: hyperbolic anomaly)
        F = 2.0 * math.atanh(math.sqrt((self.e - 1.0) / (self.e + 1.0)) * math.tan(nu / 2.0))
        self.leg = -math.sqrt((-ah) ** 3 / self.mu_p) * (self.e * math.sinh(F) - F)
        self.window = 2.0 * self.leg

    def star(self, t):
        th = self.n_p * t
        return (self.a_p * math.cos(th), self.a_p * math.sin(th))

    def tide(self, r, t):
        Rs = self.star(t)
        dx, dy = r[0] - Rs[0], r[1] - Rs[1]
        d3 = (dx * dx + dy * dy) ** 1.5
        k = -self.mu_s / d3
        ki = -self.mu_s / self.a_p ** 3
        return (k * dx + ki * Rs[0], k * dy + ki * Rs[1])

    def helio(self, r, v, t):
        Rs = self.star(t)
        Vs = (-self.a_p * self.n_p * math.sin(self.n_p * t), self.a_p * self.n_p * math.cos(self.n_p * t))
        rh = (r[0] - Rs[0], r[1] - Rs[1])
        vh = (v[0] - Vs[0], v[1] - Vs[1])
        E = 0.5 * (vh[0] ** 2 + vh[1] ** 2) - self.mu_s / math.hypot(*rh)
        L = rh[0] * vh[1] - rh[1] * vh[0]
        return E, L


def flyby_run(sc, kind, n_or_s, windows=1):
    r, v = sc.state0
    t = 0.0
    ev = 0
    W = sc.window
    if kind == "lf":
        H = W / n_or_s
        while t < W:
            rm, vm = prop(r, v, sc.mu_p, H / 2.0)
            at = sc.tide(rm, t + H / 2.0)
            v = (vm[0] + at[0] * H, vm[1] + at[1] * H)
            r, v = prop(rm, v, sc.mu_p, H / 2.0)
            t += H
            ev += 1
        sweeps = float("nan")
    else:
        s = n_or_s
        nodes, ws = GAUSS[s]
        H = W / windows
        J = [(0.0, 0.0)] * s
        sws = []
        while t < W - 1e-9:
            sw = 0
            while True:
                cur = (r, v)
                rs = []
                for i in range(s):
                    cprev = nodes[i - 1] if i else 0.0
                    ri, vi = prop(*cur, sc.mu_p, (nodes[i] - cprev) * H)
                    rs.append((ri, t + nodes[i] * H))
                    cur = (ri, (vi[0] + J[i][0], vi[1] + J[i][1]))
                re, ve = prop(*cur, sc.mu_p, (1.0 - nodes[-1]) * H)
                Jn = []
                for i in range(s):
                    at = sc.tide(rs[i][0], rs[i][1])
                    Jn.append((ws[i] * H * at[0], ws[i] * H * at[1]))
                diff = max(max(abs(Jn[i][0] - J[i][0]), abs(Jn[i][1] - J[i][1])) for i in range(s))
                scale = max(max(abs(x), abs(y)) for (x, y) in Jn) + 1e-300
                J = Jn
                sw += 1
                ev += s
                if diff <= 1e-12 * scale or sw >= 40:
                    cur = (r, v)
                    for i in range(s):
                        cprev = nodes[i - 1] if i else 0.0
                        ri, vi = prop(*cur, sc.mu_p, (nodes[i] - cprev) * H)
                        cur = (ri, (vi[0] + J[i][0], vi[1] + J[i][1]))
                    re, ve = prop(*cur, sc.mu_p, (1.0 - nodes[-1]) * H)
                    break
            r, v = re, ve
            t += H
            sws.append(sw)
        sweeps = sum(sws) / len(sws)
    E0, L0 = sc.helio(sc.state0[0], sc.state0[1], 0.0)
    E1, L1 = sc.helio(r, v, W)
    a_out, e_out, _, _ = osc(r, v, sc.mu_p)
    return dict(kicks=ev, sweeps=sweeps, dE=E1 - E0, dL=L1 - L0, a_out=a_out, e_out=e_out)


# ---------------------------------------------------------------- driver


def run_moon_case(tag, frac, e0, orbits, schemes, truth_n=2048, control_n=None):
    print(f"\n== {tag}: moon a={frac} R_H, e0={e0}, {orbits} orbits ==")
    sc = MoonScene(frac, e0)
    T = orbits * sc.P0
    sdt = sc.P0 / 4.0
    res = {}
    smp, kpo, esc_tr = lf_moon(sc, truth_n, T, sdt)
    ts = [x[0] for x in smp]
    skip = min(30, int(orbits) // 4)
    m = moon_metrics(smp, sc.P0, skip_orbits=skip)
    res["truth"] = dict(kicks_per_orbit=kpo, escaped=esc_tr, **m)
    print(f"  truth LF-{truth_n}: prec={m['prec_rad_per_orbit']:+.6e} rad/orbit "
          f"Jdrift={m['jacobi_rel_drift']:.2e} stable={m['stable']} escaped={esc_tr}")
    if control_n and not esc_tr:
        smp2, _, _ = lf_moon(sc, control_n, min(T, 60 * sc.P0), sdt)
        m2 = moon_metrics(smp2, sc.P0, skip_orbits=skip)
        rel = abs(m2["prec_rad_per_orbit"] - m["prec_rad_per_orbit"]) / abs(m["prec_rad_per_orbit"])
        res["truth_control"] = dict(kicks_per_orbit=control_n, prec=m2["prec_rad_per_orbit"], rel_dev=rel)
        print(f"  control LF-{control_n} (60 orbits): rel precession dev {rel:.2e}")
    e_tr = [x[2] for x in smp]
    for label, kind, n, wpo in schemes:
        if kind == "lf":
            smp, kpo, esc = lf_moon(sc, n, T, sdt)
            extra = {}
        elif kind == "y4":
            smp, kpo, esc = y4_moon(sc, n, T, sdt)
            extra = {}
        else:
            smp, kpo, msw, esc = gp_moon(sc, n, T, sdt, wpo=wpo)
            extra = dict(mean_sweeps=msw)
        m = moon_metrics(smp, sc.P0, skip_orbits=skip)
        row = dict(kicks_per_orbit=kpo, escaped=esc, classify_ok=(esc == esc_tr),
                   jacobi_rel_drift=m["jacobi_rel_drift"],
                   jacobi_exponent=m["jacobi_exponent_per_orbit"],
                   stable=m["stable"], e_final=m["e_final"], **extra)
        if esc == esc_tr and not esc:
            e_dev = max(abs(s[2] - interp_truth(ts, e_tr, s[0])) for s in smp)
            prec_err = abs(m["prec_rad_per_orbit"] - res["truth"]["prec_rad_per_orbit"]) / abs(res["truth"]["prec_rad_per_orbit"])
            row["prec_err"] = prec_err
            row["e_dev_max"] = e_dev
            note = f"prec_err {prec_err*100:7.3f}%  e_dev {e_dev:.2e}"
        elif esc and esc_tr:
            row["escape_t"] = smp[-1][0]
            note = f"escaped at t={smp[-1][0]:.0f} (truth t={ts[-1]:.0f})"
        else:
            note = "MISCLASSIFIED vs truth (B14 first clause fails)"
        res[label] = row
        sw = f" sweeps~{extra['mean_sweeps']:.2f}" if extra else ""
        print(f"  {label:>10}: {kpo:7.2f} kicks/orbit  {note}  "
              f"Jdrift {m['jacobi_rel_drift']:.1e}{sw}")
    return res


def run_res_case(tag, detune, orbits, schemes, truth_n=1024):
    print(f"\n== {tag}: 2:1 resonance mu=1e-4, detune {detune}, {orbits} inner orbits ==")
    a2 = 2.0 ** (2.0 / 3.0) * (1.0 + detune)
    sc = ResScene([1e-4, 1e-4], [1.0, a2], [0.02, 0.02], [0.0, math.pi / 3.0])
    P1 = 2.0 * math.pi
    T = orbits * P1
    sdt = P1 / 4.0
    res = {}
    smp, kpo = res_lf(sc, truth_n, T, sdt, P1)
    m = res_metrics(smp)
    res["truth"] = dict(kicks_per_orbit=kpo, **m)
    print(f"  truth LF-{truth_n}: pump e1max={m['pump']:.5f} regime={m['regime']}"
          + (f" amp={m.get('amp', float('nan')):.3f}" if m["regime"] == "librating" else ""))
    if tag == "R1":
        smp2, _ = res_lf(sc, 2048, min(T, 80 * P1), sdt, P1)
        m2 = res_metrics(smp2)
        res["truth_control"] = dict(pump=m2["pump"], regime=m2["regime"], amp=m2.get("amp"))
        print(f"  control LF-2048 (80 orbits): pump={m2['pump']:.5f} regime={m2['regime']}")
    for label, kind, n, wpm in schemes:
        if kind == "lf":
            smp, kpo = res_lf(sc, n, T, sdt, P1)
            extra = {}
        else:
            smp, kpo, msw = res_gp(sc, n, T, sdt, P1, wpm=wpm)
            extra = dict(mean_sweeps=msw)
        m = res_metrics(smp)
        pump_ratio = m["pump"] / res["truth"]["pump"]
        row = dict(kicks_per_orbit=kpo, pump=m["pump"], pump_ratio=pump_ratio, regime=m["regime"], **extra)
        if m["regime"] == res["truth"]["regime"] == "librating":
            row["amp_ratio"] = m["amp"] / res["truth"]["amp"]
        res[label] = row
        sw = f" sweeps~{extra['mean_sweeps']:.2f}" if extra else ""
        ar = f" amp_ratio {row.get('amp_ratio', float('nan')):.3f}" if "amp_ratio" in row else ""
        print(f"  {label:>10}: {kpo:7.2f} kicks/orbit  pump_ratio {pump_ratio:.3f}  "
              f"{m['regime']}{ar}{sw}")
    return res


def run_flyby():
    print("\n== F1: flyby (planet doll, periapsis 5 radii, v_inf ~0.77 v_orbit) ==")
    sc = FlybyScene()
    res = {}
    res["truth"] = flyby_run(sc, "lf", 8192)
    tr = res["truth"]
    print(f"  truth LF-8192: dE={tr['dE']:+.6e} dL={tr['dL']:+.6e} e_out={tr['e_out']:.6f}")
    for label, kind, n, windows in [("LF-64", "lf", 64, 1), ("LF-16", "lf", 16, 1),
                                    ("GP-3", "gp", 3, 1), ("GP-4", "gp", 4, 1),
                                    ("GP-4x4", "gp", 4, 4)]:
        row = flyby_run(sc, kind, n, windows)
        row["dE_err"] = abs(row["dE"] - tr["dE"]) / abs(tr["dE"])
        row["dL_err"] = abs(row["dL"] - tr["dL"]) / abs(tr["dL"])
        res[label] = row
        print(f"  {label:>7}: kicks {row['kicks']:4d}  dE_err {row['dE_err']*100:6.3f}%  "
              f"dL_err {row['dL_err']*100:6.3f}%  sweeps~{row['sweeps']:.2f}")
    return res


def main():
    smoke = "--smoke" in sys.argv
    R = {"machine": dict(cpus=__import__("os").cpu_count(), t=time.strftime("%Y-%m-%dT%H:%M:%S")),
         "kick_bench_note": "cloud x86; orders of magnitude only"}
    if smoke:
        R["M1"] = run_moon_case("M1", 0.3, 0.05, 12,
                                [("LF-64", "lf", 64, 1), ("GP-3", "gp", 3, 1),
                                 ("Y4-12", "y4", 4, 1), ("GP-3x4", "gp", 3, 4)],
                                truth_n=512, control_n=1024)
    else:
        moon_schemes = [
            ("LF-64", "lf", 64, 1), ("LF-32", "lf", 32, 1), ("LF-16", "lf", 16, 1),
            ("LF-8", "lf", 8, 1),
            ("Y4-6", "y4", 2, 1), ("Y4-12", "y4", 4, 1), ("Y4-24", "y4", 8, 1),
            ("GP-3x1", "gp", 3, 1), ("GP-4x4", "gp", 4, 4), ("GP-3x8", "gp", 3, 8),
            ("GP-4x8", "gp", 4, 8),
        ]
        res_schemes = [
            ("LF-64", "lf", 64, 1), ("LF-32", "lf", 32, 1), ("LF-16", "lf", 16, 1),
            ("LF-8", "lf", 8, 1),
            ("GP-4x1", "gp", 4, 1), ("GP-4x2", "gp", 4, 2), ("GP-3x4", "gp", 3, 4),
        ]
        R["M1"] = run_moon_case("M1", 0.3, 0.05, 120, moon_schemes, truth_n=2048, control_n=4096)
        R["M2"] = run_moon_case("M2 (held-out)", 0.3, 0.3, 120, moon_schemes, truth_n=2048)
        R["M3"] = run_moon_case("M3 (held-out)", 0.6, 0.3, 120, moon_schemes, truth_n=2048)
        R["R1"] = run_res_case("R1", 0.0, 200, res_schemes, truth_n=1024)
        R["R2"] = run_res_case("R2", -1.0 / 3.0 * 2.5 * (1e-4) ** (2.0 / 3.0), 200, res_schemes, truth_n=1024)
        R["F1"] = run_flyby()
    R["elapsed_s"] = time.time() - T0
    with open(OUT, "w") as f:
        json.dump(R, f, indent=1)
    print(f"\nelapsed {R['elapsed_s']:.1f}s -> {OUT}")


if __name__ == "__main__":
    main()
