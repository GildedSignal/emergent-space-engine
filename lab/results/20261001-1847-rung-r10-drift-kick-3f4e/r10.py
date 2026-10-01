#!/usr/bin/env python3
"""Rung r10: the compiled drift plus kicks, with a smooth changeover (SyMBA, restricted form).

CR3BP in canonical units: star mass 1-mu, planet mu on a unit circle (sep = 1), G = M = 1,
Omega = 1, planet period 2*pi. All state vectors are barycentric inertial [x, y, vx, vy];
the split integrators work heliocentric (exact conversion through the star's analytic circle).

Configs:
  truth      DOP853 rtol 1e-12, barycentric inertial (planet interior regularized as a uniform
             sphere, as xtask/src/behave/restricted.rs does).
  wh-fixed   Wisdom-Holman: Kepler drift about the star + planet kicks (direct+indirect), fixed
             base step H = 2*pi/N, no changeover.
  symba      DLL98 restricted: the smooth changeover Kbar(d) (1 far / 0 near, band [1, 2] R_H)
             splits each base step into a far chunk (star drift + planet kicks, DKD) of duration
             Kbar*H and a near chunk (exact two-body drift about the planet + tidal kicks, DKD
             sub-stepped at H/2^j with j from the local planetocentric period). The dominant body
             follows the changeover; no hard switch anywhere.
  soi-switch events3's negative: hard state-selected switch of the dominant body at the sphere of
             influence, base step H throughout.

Cases (sampler Python random.Random(20261011), rules ported from xtask/src/behave):
  B12 16 ships   mu = 1e-3, >= 20 SOI crossings in 200 planet periods (search ported from
                 handoff.rs), Jacobi error sampled every P/8.
  B14 256 moons  128 circular births + 128 eccentric (e0 <= 0.3), a in [0.2, 0.9] R_H, prograde
                 even / retrograde odd, 50 planet periods, sampled every P/64.
  r4 v3 resonant 2:1 and 3:2, mu in {3e-5, 3e-4, 3e-3}, detuned by {-1/3, 0, +1/3} of
                 W = 2.5 mu^(2/3), e0 = 0.02, phases 4 deg and 172 deg, 200 synodic periods.
"""

import json
import math
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

TAU = 2.0 * math.pi
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- scene


class Scene:
    def __init__(self, mu, sep=1.0, planet_radius=4.84e4 / 5.27e8):
        self.mu = mu
        self.sep = sep
        self.omega = sep ** -1.5
        self.period = TAU * sep ** 1.5
        self.hill = sep * (mu / 3.0) ** (1.0 / 3.0)
        self.soi = sep * mu ** 0.4
        self.r_pl = planet_radius * sep  # uniform-sphere interior for the truth

    def planet(self, t):
        c, s = math.cos(t * self.omega), math.sin(t * self.omega)
        r, v = self.sep * (1.0 - self.mu), self.sep * (1.0 - self.mu) * self.omega
        return (r * c, r * s), (-v * s, v * c)

    def star(self, t):
        c, s = math.cos(t * self.omega), math.sin(t * self.omega)
        r, v = self.sep * self.mu, self.sep * self.mu * self.omega
        return (-r * c, -r * s), (v * s, -v * c)

    def planet_distance(self, t, s):
        (px, py), _ = self.planet(t)
        return math.hypot(s[0] - px, s[1] - py)

    def jacobi(self, t, s):
        (sx, sy), _ = self.star(t)
        (px, py), _ = self.planet(t)
        r1 = math.hypot(s[0] - sx, s[1] - sy)
        r2 = math.hypot(s[0] - px, s[1] - py)
        return (2.0 * (1.0 - self.mu) / r1 + 2.0 * self.mu / r2
                + 2.0 * self.omega * (s[0] * s[3] - s[1] * s[2])
                - (s[2] * s[2] + s[3] * s[3]))

    def barycentric(self, t, rel):
        (px, py), (vx, vy) = self.planet(t)
        return [rel[0] + px, rel[1] + py, rel[2] + vx, rel[3] + vy]

    def relative(self, t, s):
        (px, py), (vx, vy) = self.planet(t)
        return [s[0] - px, s[1] - py, s[2] - vx, s[3] - vy]

    # heliocentric helpers (the planet's heliocentric place is the unit circle times sep)
    def helio(self, t, s):
        (sx, sy), (svx, svy) = self.star(t)
        return [s[0] - sx, s[1] - sy, s[2] - svx, s[3] - svy]

    def from_helio(self, t, h):
        (sx, sy), (svx, svy) = self.star(t)
        return [h[0] + sx, h[1] + sy, h[2] + svx, h[3] + svy]

    def helio_planet(self, t):
        c, s = math.cos(t * self.omega), math.sin(t * self.omega)
        return (self.sep * c, self.sep * s), (-self.sep * self.omega * s, self.sep * self.omega * c)

def truth_states(scene, s0, times, rtol=1e-12):
    """States at `times` (all >= 0, ascending), barycentric. None: no answer."""
    from scipy.integrate import solve_ivp
    mu, rpl = scene.mu, scene.r_pl
    om = scene.omega

    def eom(t, y):
        c, s = math.cos(t * om), math.sin(t * om)
        sx, sy = -mu * c, -mu * s
        px, py = (1.0 - mu) * c, (1.0 - mu) * s
        x, y, vx, vy = y
        d1x, d1y = x - sx, y - sy
        d2x, d2y = x - px, y - py
        r1 = math.sqrt(d1x * d1x + d1y * d1y)
        r2 = math.sqrt(d2x * d2x + d2y * d2y)
        f2 = mu / max(r2, rpl) ** 3
        return (vx, vy,
                -(1.0 - mu) * d1x / r1 ** 3 - f2 * d2x,
                -(1.0 - mu) * d1y / r1 ** 3 - f2 * d2y)

    times = np.asarray(times)
    sol = solve_ivp(eom, (0.0, float(times[-1])), list(s0), method="DOP853",
                    rtol=rtol, atol=1e-14, t_eval=times)
    if not sol.success or sol.y.shape[1] != len(times):
        return None
    return sol.y.T, sol.nfev


def truth_states_escape(scene, s0, times, rtol, stop_hill):
    """Like truth_states but stops at the first escape past stop_hill Hill radii.
    Returns (states, nfev, escaped)."""
    from scipy.integrate import solve_ivp
    mu, rpl = scene.mu, scene.r_pl
    om = scene.omega
    lim = stop_hill * scene.hill

    def eom(t, y):
        c, s = math.cos(t * om), math.sin(t * om)
        sx, sy = -mu * c, -mu * s
        px, py = (1.0 - mu) * c, (1.0 - mu) * s
        x, y, vx, vy = y
        d1x, d1y = x - sx, y - sy
        d2x, d2y = x - px, y - py
        r1 = math.sqrt(d1x * d1x + d1y * d1y)
        r2 = math.sqrt(d2x * d2x + d2y * d2y)
        f2 = mu / max(r2, rpl) ** 3
        return (vx, vy,
                -(1.0 - mu) * d1x / r1 ** 3 - f2 * d2x,
                -(1.0 - mu) * d1y / r1 ** 3 - f2 * d2y)

    def beyond(t, y):
        c, s = math.cos(t * om), math.sin(t * om)
        return math.hypot(y[0] - (1.0 - mu) * c, y[1] - (1.0 - mu) * s) - lim

    beyond.terminal = True
    beyond.direction = 1.0
    times = np.asarray(times)
    sol = solve_ivp(eom, (0.0, float(times[-1])), list(s0), method="DOP853",
                    rtol=rtol, atol=1e-14, t_eval=times, events=beyond)
    if not sol.success:
        return None
    escaped = bool(sol.status == 1)
    return sol.y.T, sol.nfev, escaped


# ---------------------------------------------------------------- universal-variable Kepler drift


def _stumpff(z):
    """(c0, c1, c2, c3) Stumpff functions."""
    if abs(z) < 1e-2:
        z2 = z * z
        c0 = 1.0 - z / 2 + z2 / 24 - z * z2 / 720
        c1 = 1.0 - z / 6 + z2 / 120 - z * z2 / 5040
        c2 = 0.5 - z / 24 + z2 / 720 - z * z2 / 40320
        c3 = 1.0 / 6.0 - z / 120 + z2 / 5040 - z * z2 / 362880
        return c0, c1, c2, c3
    if z > 0:
        sz = math.sqrt(z)
        c0, c1 = math.cos(sz), math.sin(sz) / sz
    else:
        sz = math.sqrt(-z)
        c0, c1 = math.cosh(sz), math.sinh(sz) / sz
    c2, c3 = (1.0 - c0) / z, (1.0 - c1) / z
    return c0, c1, c2, c3


def kepler_drift(GM, x, y, vx, vy, dt):
    """Exact two-body advance by dt. Returns (x, y, vx, vy). Raises on failure."""
    sqgm = math.sqrt(GM)
    r0 = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    alpha = 2.0 / r0 - v2 / GM  # 1/a
    rdv = x * vx + y * vy
    A = rdv / sqgm
    B = 1.0 - alpha * r0
    tgt = sqgm * dt

    def F(ch):
        z = alpha * ch * ch
        _, _, c2, c3 = _stumpff(z)
        return A * ch * ch * c2 + B * ch ** 3 * c3 + r0 * ch - tgt

    def Fp(ch):
        z = alpha * ch * ch
        _, c1, c2, _ = _stumpff(z)
        return A * ch * c1 + B * ch * ch * c2 + r0

    ch = tgt / r0  # decent universal start
    ok = False
    for _ in range(100):
        f = F(ch)
        fp = Fp(ch)
        if fp == 0.0:
            break
        step = f / fp
        ch -= step
        if abs(step) <= 1e-15 * max(1.0, abs(ch)):
            ok = abs(F(ch)) <= 1e-14 * max(1e-3, abs(tgt))
            if ok:
                break
            break  # converged or hopeless; refine by bisection if needed
    if not ok:  # safeguarded bisection (F is monotone in ch)
        lo, hi = min(0.0, ch), max(0.0, ch)
        while F(hi) < 0:
            hi = 2 * hi + 1e-8
            if hi > 1e12:
                raise RuntimeError("kepler bracket")
        while F(lo) > 0:
            lo = 2 * lo - 1e-8
            if lo < -1e12:
                raise RuntimeError("kepler bracket")
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if F(mid) < 0:
                lo = mid
            else:
                hi = mid
        ch = 0.5 * (lo + hi)
    z = alpha * ch * ch
    _, _, c2, c3 = _stumpff(z)
    f = 1.0 - ch * ch * c2 / r0
    g = dt - ch ** 3 * c3 / sqgm
    xn, yn = f * x + g * vx, f * y + g * vy
    rn = math.hypot(xn, yn)
    fd = sqgm * ch * (z * c3 - 1.0) / (r0 * rn)
    gd = 1.0 - ch * ch * c2 / rn
    return xn, yn, fd * x + gd * vx, fd * y + gd * vy


# ---------------------------------------------------------------- the split integrators

# base steps per planet period (divisible by 8 for B12's P/8, by 64 for B14's P/64, and by the
# resonant grids: 2:1 P1/8 = 12 H, 3:2 P1/8 = 16 H)
NSTEPS = 192
S_LOCAL = 110.0     # target force evals per planetocentric orbit in the near region
MAX_DEPTH = 14      # deepest recursion level: H / 2^14
SMOOTH = lambda u: u * u * u * (10.0 + u * (-15.0 + 6.0 * u))  # C2 smoothstep


def symba_Kbar(scene, d):
    """1 far (>= 2 R_H), 0 near (<= 1 R_H), C2-smooth between."""
    lo, hi = scene.hill, 2.0 * scene.hill
    if d >= hi:
        return 1.0
    if d <= lo:
        return 0.0
    return SMOOTH((d - lo) / (hi - lo))


def far_accel(scene, t, h):
    """Planet direct + indirect term, heliocentric. One force evaluation."""
    (px, py), _ = scene.helio_planet(t)
    dx, dy = h[0] - px, h[1] - py
    dd = math.hypot(dx, dy)
    f = scene.mu / max(dd, scene.r_pl) ** 3
    return [-f * dx - scene.mu * px, -f * dy - scene.mu * py]


def tide_accel(scene, t, h):
    """Star's tidal field in the planet's (accelerating) frame, heliocentric components."""
    (px, py), _ = scene.helio_planet(t)
    r = math.hypot(h[0], h[1])
    k = (1.0 - scene.mu) / r ** 3
    return [-k * h[0] + (1.0 - scene.mu) * px, -k * h[1] + (1.0 - scene.mu) * py]

S_LOCAL = 96.0      # target force evals per planetocentric orbit in the near region

def drift_star(scene, h, dt):
    h[0], h[1], h[2], h[3] = kepler_drift(1.0 - scene.mu, h[0], h[1], h[2], h[3], dt)


def drift_pair(scene, t, h, dt):
    (px, py), (pvx, pvy) = scene.helio_planet(t)
    h[0], h[1], h[2], h[3] = kepler_drift(scene.mu, h[0] - px, h[1] - py, h[2] - pvx, h[3] - pvy, dt)
    (px, py), (pvx, pvy) = scene.helio_planet(t + dt)
    h[0] += px
    h[1] += py
    h[2] += pvx
    h[3] += pvy


def near_level(scene, d):
    """Recursion level j: step H/2^j <= (planetocentric period)/S_LOCAL."""
    if d <= 0.0:
        return MAX_DEPTH
    need = S_LOCAL * math.sqrt(scene.mu / d ** 3) / NSTEPS
    if need <= 1.0:
        return 0
    return min(MAX_DEPTH, max(1, math.ceil(math.log2(need))))


class Runner:
    """Steps a massless body, recording states at exact sample times (grids are step-aligned)."""

    def __init__(self, scene, s0, config, H, n_steps):
        self.scene, self.config, self.H, self.n = scene, config, H, n_steps
        self.h = list(scene.helio(0.0, s0))
        self.t = 0.0
        self.evals = 0
        self.cached_far = None  # accel value at the current (t, h), far form
        self.step_index = 0

    def _far_chunk(self, dur, sc=None):
        sc = sc or self.scene
        a = self.cached_far
        if a is None:
            a = far_accel(sc, self.t, self.h)
            self.evals += 1
        self.h[2] += a[0] * dur / 2
        self.h[3] += a[1] * dur / 2
        drift_star(sc, self.h, dur)
        self.t += dur
        a2 = far_accel(sc, self.t, self.h)
        self.evals += 1
        self.h[2] += a2[0] * dur / 2
        self.h[3] += a2[1] * dur / 2
        self.cached_far = a2  # valid at (t, h) for a following far chunk

    def _near_chunk(self, dur, substeps):
        sc = self.scene
        t_end = self.t + dur
        a = tide_accel(sc, self.t, self.h)
        self.evals += 1
        while self.t < t_end - 1e-15:
            (px, py), _ = sc.helio_planet(self.t)
            d = math.hypot(self.h[0] - px, self.h[1] - py)
            step = self.H / (1 << near_level(sc, d)) if substeps else self.H
            step = min(step, t_end - self.t)
            self.h[2] += a[0] * step / 2
            self.h[3] += a[1] * step / 2
            drift_pair(sc, self.t, self.h, step)
            self.t += step
            a = tide_accel(sc, self.t, self.h)
            self.evals += 1
            self.h[2] += a[0] * step / 2
            self.h[3] += a[1] * step / 2
    def step(self):
        sc = self.scene

        if self.config == "wh-fixed":
            self._far_chunk(self.H)
            return
        if self.config == "soi-switch":
            (px, py), _ = sc.helio_planet(self.t)
            d = math.hypot(self.h[0] - px, self.h[1] - py)
            if d > sc.soi:
                self._far_chunk(self.H)
            else:
                self.cached_far = None
                self._near_chunk(self.H, substeps=False)
            return
        if self.config == "symba":
            (px, py), _ = sc.helio_planet(self.t)
            d = math.hypot(self.h[0] - px, self.h[1] - py)
            K = symba_Kbar(sc, d)
            tf = K * self.H
            if tf > 0.0:
                self._far_chunk(tf)
                if tf < self.H:  # blended step: the cache no longer matches a plain next step
                    pass
            else:
                self.cached_far = None
            if self.H - tf > 0.0:
                self.cached_far = None
                self._near_chunk(self.H - tf, substeps=True)
            return
        raise ValueError(self.config)

    def run(self, sample_steps):
        """sample_steps: sorted iterable of step indices (states after those steps)."""
        want = sorted(set(sample_steps))
        out = []
        wi = 0
        for i in range(self.n):
            self.step()
            if wi < len(want) and want[wi] == i + 1:
                out.append((self.t, self.scene.from_helio(self.t, self.h)))
                wi += 1
        return out, self.evals


def run_candidate(scene, s0, config, T_end, sample_times):
    """States at sample_times; returns (states, force_evals) or None."""
    H = scene.period / NSTEPS
    n_steps = int(round(T_end / H))
    H = T_end / n_steps
    # map sample times to step indices
    idx = [int(round(t / H)) for t in sample_times]
    for t, k in zip(sample_times, idx):
        if abs(k * H - t) > 1e-9 * max(1.0, t):
            raise RuntimeError(f"sample grid not step-aligned: {t} vs {k * H}")
    r = Runner(scene, s0, config, H, n_steps)
    try:
        samples, evals = r.run(idx)
    except (RuntimeError, OverflowError, ValueError):
        return None
    return samples, evals


# ---------------------------------------------------------------- case samplers (Python random.Random(20261011))


def b12_candidates(rng, n):
    """(side, k, alpha) ported from sample.rs handoffs()."""
    out = []
    for _ in range(n):
        side = 1.0 if rng.random() < 0.5 else -1.0
        k = 1.5 + 1.5 * rng.random()
        alpha = math.radians(30.0 + 300.0 * rng.random())
        out.append((side, k, alpha))
    return out


def b12_ship(scene, side, k, alpha):
    """Circular barycentric orbit at radius sep*(1 + side*k*R_H/sep), angle alpha from the planet."""
    r = 1.0 + side * scene.hill / scene.sep * k
    v = r ** -0.5
    return [r * math.cos(alpha), r * math.sin(alpha), -v * math.sin(alpha), v * math.cos(alpha)]


def b14_births(rng, n_circ=128, n_ecc=128):
    """[(a_hill, phase, e0)], circular births first; even index prograde, odd retrograde."""
    out = [(0.2 + 0.7 * rng.random(), TAU * rng.random(), 0.0) for _ in range(n_circ)]
    out += [(0.2 + 0.7 * rng.random(), TAU * rng.random(), 0.3 * rng.random()) for _ in range(n_ecc)]
    return out


def b14_moon_state(scene, a_hill, phase, e0, prograde):
    a = a_hill * scene.hill
    s, c = math.sin(phase), math.cos(phase)
    r = a * (1.0 - e0)
    v = math.sqrt(scene.mu * (1.0 + e0) / (a * (1.0 - e0))) * (1.0 if prograde else -1.0)
    return scene.barycentric(0.0, [r * c, r * s, -v * s, v * c])


def resonant_cases():
    """r4 v3's resonant cases (resonance.rs): 36 of them."""
    out = []
    for j, exact in [(1, 2.0), (2, 1.5)]:
        for mu in (3e-5, 3e-4, 3e-3):
            W = 2.5 * mu ** (2.0 / 3.0)
            for d in (-1.0 / 3.0, 0.0, 1.0 / 3.0):
                for k, m0 in enumerate((math.radians(4.0), math.radians(172.0))):
                    out.append({"name": f"{j+1}:{j} mu {mu:.0e} detune {d:+.2f} phase {k}",
                                "j": j, "mu": mu, "ratio": exact * (1.0 + d * W),
                                "e0": 0.02, "m0": m0})
    return out


def resonant_start(scene, case):
    """Kepler orbit about the star, periapsis along +x (port of resonance.rs start())."""
    n1 = case["ratio"] * scene.omega
    a = ((1.0 - scene.mu) / (n1 * n1)) ** (1.0 / 3.0)
    e, m0 = case["e0"], case["m0"]
    ea = m0
    for _ in range(50):
        ea -= (ea - e * math.sin(ea) - m0) / (1.0 - e * math.cos(ea))
    se, ce = math.sin(ea), math.cos(ea)
    px, py = a * (ce - e), a * math.sqrt(1.0 - e * e) * se
    f = n1 * a / (1.0 - e * ce)
    vx, vy = -f * se, f * math.sqrt(1.0 - e * e) * ce
    (sx, sy), (svx, svy) = scene.star(0.0)
    return [sx + px, sy + py, svx + vx, svy + vy]


def resonant_times(scene, case):
    p1 = TAU / (case["ratio"] * scene.omega)
    synodic = 1.0 / (1.0 / p1 - 1.0 / scene.period)
    dt = p1 / 8.0
    n = int(math.ceil(200.0 * synodic / dt))
    return [k * dt for k in range(1, n + 1)]


# ---------------------------------------------------------------- metrics ports


def growth_exponent(err):
    """Port of xtask/src/behave/fit.rs growth_exponent (last 90%, 16 log windows, LSQ slope)."""
    err = list(err)
    n = len(err)
    first = max(n // 10, 1)
    if n <= first or any(not math.isfinite(e) for e in err):
        return float("nan")
    pts, used = [], 0
    for jj in range(16):
        a = first if jj == 0 else int(round(first * (n / first) ** (jj / 16)))
        b = n if jj == 16 else int(round(first * (n / first) ** ((jj + 1) / 16)))
        a = min(a, n)
        b = min(b, n)
        if b <= a:
            continue
        used += 1
        top = max(abs(e) for e in err[a:b])
        if top > 0.0:
            pts.append((math.log(math.sqrt(a * (b - 1))), math.log(top)))
    if used < 8:
        return float("nan")
    if not pts:
        return 0.0
    if len(pts) < 3:
        return float("nan")
    m = len(pts)
    mx = sum(p[0] for p in pts) / m
    my = sum(p[1] for p in pts) / m
    num = sum((p[0] - mx) * (p[1] - my) for p in pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    return num / den


def apsides_series(scene, times, states):
    """Unwrapped planetocentric periapsis longitudes, or None where undefined."""
    out = []
    for t, s in zip(times, states):
        w = scene.relative(t, s)
        r2 = w[0] * w[0] + w[1] * w[1]
        v2 = w[2] * w[2] + w[3] * w[3]
        rv = w[0] * w[2] + w[1] * w[3]
        k = v2 - scene.mu / math.sqrt(r2)
        ex, ey = k * w[0] - rv * w[2], k * w[1] - rv * w[3]
        if not math.hypot(ex, ey) > 1e-9 * scene.mu:
            return None
        varpi = math.atan2(ey, ex)
        if not out:
            out.append(varpi)
            continue
        jump = (varpi - out[-1]) % TAU
        if jump > math.pi:
            jump -= TAU
        elif jump < -math.pi:
            jump += TAU
        if abs(jump) > math.pi / 2:
            return None
        out.append(out[-1] + jump)
    return out if out else None


def apsidal_rate(scene, times, states):
    """Radians per planet period, or None."""
    varpi = apsides_series(scene, times, states)
    if varpi is None:
        return None
    u = [t / scene.period for t in times]
    n = len(u)
    mu_ = sum(u) / n
    mv = sum(varpi) / n
    num = sum((a - mu_) * (b - mv) for a, b in zip(u, varpi))
    den = sum((a - mu_) ** 2 for a in u)
    return num / den if den > 0 else None


def resonant_series(scene, j, times, states):
    """Unwrapped resonant angle phi = (j+1) lp - j ls - varpi_s, plus e(t) about the star."""
    phis, es = [], []
    for t, s in zip(times, states):
        (px, py), (pvx, pvy) = scene.star(t)
        x, y, vx, vy = s[0] - px, s[1] - py, s[2] - pvx, s[3] - pvy
        r2 = x * x + y * y
        v2 = vx * vx + vy * vy
        rv = x * vx + y * vy
        k = v2 - (1.0 - scene.mu) / math.sqrt(r2)
        ex, ey = k * x - rv * vx, k * y - rv * vy
        es.append(math.hypot(ex, ey) / (1.0 - scene.mu))
        varpi = math.atan2(ey, ex)
        (plx, ply), _ = scene.helio_planet(t)
        lp = math.atan2(ply, plx)
        ls = math.atan2(y, x)
        phi = (j + 1) * lp - j * ls - varpi
        phis.append(phi)
    # proper unwrap
    unw = [phis[0]]
    for p in phis[1:]:
        d = (p - unw[-1]) % TAU
        if d > math.pi:
            d -= TAU
        unw.append(unw[-1] + d)
    return unw, es


# ---------------------------------------------------------------- unit sanity checks


def self_test():
    rng = random.Random(1)
    # 1. Kepler drift: energy + roundtrip over random conics
    for _ in range(300):
        GM = rng.uniform(0.001, 2.0)
        x, y = rng.uniform(-2, 2), rng.uniform(-2, 2)
        r = math.hypot(x, y)
        v = math.sqrt(rng.uniform(0.2, 1.8) * GM / r)
        ang = rng.uniform(0, TAU)
        vx, vy = v * math.cos(ang), v * math.sin(ang)
        e0 = 0.5 * (vx * vx + vy * vy) - GM / r
        L0 = x * vy - y * vx
        dt = rng.uniform(-3, 3)
        xn, yn, vxn, vyn = kepler_drift(GM, x, y, vx, vy, dt)
        e1 = 0.5 * (vxn * vxn + vyn * vyn) - GM / math.hypot(xn, yn)
        L1 = xn * vyn - yn * vxn
        assert abs(e1 - e0) < 1e-12 * max(1, abs(e0)), (e0, e1)
        assert abs(L1 - L0) < 1e-12 * max(1, abs(L0))
        xb, yb, vxb, vyb = kepler_drift(GM, xn, yn, vxn, vyn, -dt)
        err = max(abs(xb - x), abs(yb - y), abs(vxb - vx), abs(vyb - vy))
        assert err < 1e-10, err
    # 2. truth vs wh-fixed on a smooth ship (far from the planet): states close after 2 periods
    sc = Scene(1e-3)
    s0 = b12_ship(sc, 1.0, 30.0, math.radians(120))
    times = [k * sc.period / 64 for k in range(1, 129)]
    ref = truth_states(sc, s0, times, rtol=1e-13)[0]
    cand = run_candidate(sc, s0, "wh-fixed", times[-1], times)
    d = max(max(abs(a - b) for a, b in zip(r, c)) for r, c in zip(ref, [s for _, s in cand[0]]))
    assert d < 2e-5, d
    # 3. symba far body equals wh-fixed step-for-step
    r1 = Runner(sc, s0, "wh-fixed", sc.period / NSTEPS, 8)
    r2_ = Runner(sc, s0, "symba", sc.period / NSTEPS, 8)
    r1.run([])
    r2_.run([])
    e = max(abs(a - b) for a, b in zip(r1.h, r2_.h))
    assert e < 1e-15, e
    # 4. growth exponent port: power laws
    for alpha in (0.0, 0.5, 1.0):
        g = growth_exponent([1e-9 * max(k, 1.0) ** alpha for k in range(10_000)])
        assert abs(g - alpha) < 1e-3, (alpha, g)
    assert growth_exponent([0.0] * 1000) == 0.0
    print("self-test OK")


if __name__ == "__main__":
    self_test()
