#!/usr/bin/env python3
"""Premise red-team falsifier: the view gather at the game's advertised extremes.

Faithful port of crates/universe/src/view.rs::crossing (integer-tick Newton,
ViewCache::guess/put (slope clamped to [0.5, 1.5]), on uniform-motion emitters
in the root frame, c = 1, 1 tick = 1 light-tick = 4.925 us = 1.47 km.

Oracle: g(t) = t + |x(t) - xo| - t_now is strictly increasing in t
(dg/dt = 1 + n.beta > 0 for |beta| < 1), so the last integer tick with
g <= 0 is exactly floor(t_root) with t_root the real root (bisection).
"""
import math, random

TOL = 1e-4
CAP = 64

def make(speed, angle_deg, dist, b_off=0.0):
    a = math.radians(angle_deg)
    x = (dist * math.cos(b_off), dist * math.sin(b_off))
    v = (speed * math.cos(a + b_off), speed * math.sin(a + b_off))
    return x, v

def at(em, t):
    x, v = em
    return (x[0] + v[0] * t, x[1] + v[1] * t)

def g_of(em, t, t_now, xo):
    px, py = at(em, t)
    dist = math.hypot(px - xo[0], py - xo[1])
    return t + dist - t_now, dist, (px, py)

def crossing(em, t_now, xo, guess, reads):
    """Port of view.rs crossing(). Returns (tick, root_real) or None."""
    t = max(0, min(guess, t_now))
    lo = None; hi = None
    for _ in range(CAP):
        reads[0] += 1
        g, dist, pos = g_of(em, t, t_now, xo)
        x, v = em
        d0, d1 = pos[0] - xo[0], pos[1] - xo[1]
        speed = math.hypot(v[0], v[1])
        rad = (d0 * v[0] + d1 * v[1]) / dist if dist > 0 else 0.0
        step = -g / (1.0 + rad)
        if g > 0.0 and t == 0:
            return (0, 0.0)
        if g <= 0.0:
            if g > -(1.0 - speed - TOL) or hi == t + 1:
                return (t, t + step)
            lo = (t, t + step)
        else:
            hi = t
            if lo is not None and lo[0] + 1 == t:
                return lo
        nxt = int(math.floor(t + step))
        if lo is not None:
            nxt = max(nxt, lo[0])
        if hi is not None:
            nxt = min(nxt, hi - 1)
        if nxt == t:
            nxt = t + 1 if g <= 0.0 else t - 1
        t = max(0, min(nxt, t_now))
    return None

def t_root_exact(em, t_now, xo):
    g0 = g_of(em, 0.0, t_now, xo)[0]
    if g0 > 0:
        return None
    if g_of(em, float(t_now), t_now, xo)[0] <= 0:
        return float(t_now)
    lo, hi = 0.0, float(t_now)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g_of(em, mid, t_now, xo)[0] <= 0:
            lo = mid
        else:
            hi = mid
    return lo

def slope_of(em, xo):
    px, py = at(em, 1.0)
    d0, d1 = px - xo[0], py - xo[1]
    dist = math.hypot(d0, d1)
    return 1.0 + (d0 * em[1][0] + d1 * em[1][1]) / dist

def frame(em, t_now, xo, cache):
    reads = [0]
    if cache is not None and cache[0] is not None and cache[0] <= t_now:
        guess = int(math.floor(cache[1] + (t_now - cache[0]) * cache[2]))
    else:
        guess = t_now  # cold: view.rs line 257 unwrap_or(t_now)
    r = crossing(em, t_now, xo, guess, reads)
    if cache is not None and r is not None:
        root = r[1]
        if cache[0] is not None and t_now > cache[0]:
            slope = min(1.5, max(0.5, (root - cache[1]) / (t_now - cache[0])))
        else:
            slope = 1.0
        cache[0], cache[1], cache[2] = t_now, root, slope
    return r, reads[0]

T0 = 300_000_000  # > D so the light has arrived; no pre-first-light path

print("=== P1: warm readouts per emitter per frame (100 frames) ===")
for label, speed, ang in [("static", 0.0, 0.0), ("slow 0.01 tr", 0.01, 90.0),
                          ("b9 transverse", 0.9, 90.0), ("b9 head-on", 0.9, 180.0),
                          ("b9 receding", 0.9, 0.0), ("b99 transverse", 0.99, 90.0),
                          ("b99 head-on", 0.99, 180.0), ("b9999 transverse", 0.9999, 90.0)]:
    for F in (64, 670):
        em = make(speed, ang, 2.91e8 if abs(ang-180.0)<1 else 2e8)
        cache = [None, 0.0, 1.0]
        tot = 0; mx = 0
        t = T0
        for f in range(100):
            t += F
            r, n = frame(em, t, (0.0, 0.0), cache)
            tot += n; mx = max(mx, n)
        print(f"  {label:16s} F={F:4d}  mean readouts {tot/100:5.2f}  max {mx}")

print("=== P1b: warm readouts, moving observer (0.9c lateral), b9 transverse ===")
em = make(0.9, 90.0, 2e8)
cache = [None, 0.0, 1.0]
t = T0; tot = 0
for f in range(100):
    t += 670
    xo = (0.9 * 670 * f, 0.0)
    r, n = frame(em, t, xo, cache)
    tot += n
print(f"  moving observer F=670: mean readouts {tot/100:.2f}")

print("=== P2/P4: correctness vs exact tick; cold and foreign (wrong by 1e5) ===")
bad = 0; total = 0; worst_reads = 0; nones = 0
for speed in (0.0, 0.1, 0.9, 0.99, 0.9999, 0.99999):
    for ang_deg in (0, 45, 90, 135, 180):
        for dist in (1e3, 1e6, 1e8):
            for guess_kind in ("cold", "foreign+", "foreign-"):
                em = make(speed, math.radians(ang_deg), dist)
                t_now = T0
                tr = t_root_exact(em, t_now, (0.0, 0.0))
                if tr is None:
                    continue
                want = int(math.floor(tr))
                if guess_kind == "cold":
                    guess = t_now
                else:
                    guess = max(0, min(t_now, want + (100_000 if guess_kind == "foreign+" else -100_000)))
                reads = [0]
                r = crossing(em, t_now, (0.0, 0.0), guess, reads)
                total += 1
                worst_reads = max(worst_reads, reads[0])
                if r is None:
                    nones += 1; bad += 1
                elif r[0] != want:
                    bad += 1
                    if bad < 8:
                        print(f"    MISMATCH speed={speed} ang={ang_deg} D={dist:.0e} {guess_kind}: got {r[0]} want {want}")
print(f"  cases {total}, wrong-or-dropped {bad}, worst readouts {worst_reads}, None {nones}")

print("=== P2b: acceptance window (analytic) ===")
for speed in (0.9, 0.99, 0.999, 0.9999, 0.99999):
    w = 1.0 - speed - TOL
    print(f"  speed {speed:8f}: window {w:+.2e} -> {'EMPTY (first-readout path unreachable)' if w <= 0 else 'non-empty'}")

print("=== P3: tick quantization -> apparent angular error (px, 1080p, 90 deg FOV) ===")
PX = (math.pi / 2.0) / 1920.0
for D_ticks in (1e3, 1e4, 1e5, 1e8):
    err = 0.9 * 1.0 / D_ticks
    print(f"  D={D_ticks:.0e} ticks ({D_ticks*1.47:.3e} km): {err/PX:9.4f} px per tick of quantization")
print(f"  D* (1 px per tick, v=0.9): {0.9/PX:.3e} ticks = {0.9/PX*1.47:.3e} km")

print("=== P5: one-crossing monotonicity sweep (1e5 cases) ===")
random.seed(11)
viol = 0; dmin = 10.0
for _ in range(100_000):
    sp = random.uniform(0.0, 0.9999)
    a = random.uniform(0, 2 * math.pi)
    b = random.uniform(0, 2 * math.pi)
    em = make(sp, a * 180 / math.pi, 1e6, b)
    s = slope_of(em, (0.0, 0.0))
    dmin = min(dmin, s)
    if s <= 0.0:
        viol += 1
print(f"  min dg/dt over sweep: {dmin:.6f} (must be > 0); violations {viol}")

print("=== extra: true root-advance rate vs the [0.5,1.5] clamp, approachers ===")
for speed in (0.5, 0.9, 0.99, 0.999):
    em = make(speed, 180.0, 2.91e8)
    s_true = 1.0 / slope_of(em, (0.0, 0.0))
    print(f"  approaching {speed}: dt_root/dt_now = {s_true:10.3f}  clamp caps at 1.5")
