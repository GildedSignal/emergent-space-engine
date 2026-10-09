#!/usr/bin/env python3
"""Premise 5 micro-check: 'each visible tube crosses the observer's past light cone
once; Newton from the previous frame's crossing finds it.' Flat spacetime, float64.
Observer burns 0 -> 0.9c (and jinks); emitters on circular orbits up to beta 0.3.
Truth: bisection on f(tau) = t_obs - tau - |x_obs - x_em(tau)|. Newton seeded from
the previous frame's root. Counts iterations, wrong roots, and crossing count."""
import math, random

random.seed(20261009)
c = 1.0
N_em = 100
# emitters: circular orbits, radius 5..60, speed beta 0..0.3, random phase/center
ems = []
for i in range(N_em):
    R = random.uniform(5, 60)
    beta = random.uniform(0, 0.3)
    om = beta * c / R
    ph = random.uniform(0, 2 * math.pi)
    cx, cy = random.uniform(-40, 40), random.uniform(-40, 40)
    ems.append((R, om, ph, cx, cy))

def x_em(i, tau):
    R, om, ph, cx, cy = ems[i]
    return (cx + R * math.cos(om * tau + ph), cy + R * math.sin(om * tau + ph))

def x_obs(t):
    # observer: burn along x with turn-overs (jink), |a| up to ~2/s proper-ish
    v = 0.9 * math.tanh(t / 3.0)          # ramp to 0.9c
    jink = 0.05 * math.sin(1.7 * t)       # hard transverse jinking
    return (v * t, 8.0 * math.sin(0.9 * t) + 40.0 * jink * t)

def f(i, t_obs, tau):
    ox, oy = x_obs(t_obs)
    ex, ey = x_em(i, tau)
    return (t_obs - tau) - math.hypot(ox - ex, oy - ey)

frames = [k * 0.05 for k in range(400)]   # 20 s at 20 Hz
prev = [0.0] * N_em
max_it = 0
wrong = 0
multi = 0
for t_obs in frames:
    ox, oy = x_obs(t_obs)
    for i in range(N_em):
        # crossing count by dense sign scan
        ts = [t_obs - 130.0 + k * 0.13 for k in range(1000)]
        vals = [f(i, t_obs, tau) for tau in ts]
        ncross = sum(1 for a, b in zip(vals, vals[1:]) if a * b <= 0)
        if ncross != 1:
            multi += 1
        # truth by bisection on [t_obs-130, t_obs]
        lo, hi = t_obs - 130.0, t_obs - 1e-9
        flo = f(i, t_obs, lo)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f(i, t_obs, mid) > 0:
                lo = mid
            else:
                hi = mid
        tau_true = 0.5 * (lo + hi)
        # Newton from previous frame's root
        tau = max(prev[i], 1e-6)
        it = 0
        for it in range(1, 60):
            ex, ey = x_em(i, tau)
            dx, dy = ox - ex, oy - ey
            R = math.hypot(dx, dy)
            # df/dtau = -1 + n.v_em
            Rdot = -( -dx * 0 - dy * 0)  # emitters move; approximate v numerically
            h = 1e-7
            ex2, ey2 = x_em(i, tau + h)
            vx, vy = (ex2 - ex) / h, (ey2 - ey) / h
            df = -1.0 + (dx * vx + dy * vy) / R
            step = f(i, t_obs, tau) / df
            tau -= step
            if abs(step) < 1e-12:
                break
        prev[i] = tau
        max_it = max(max_it, it)
        if abs(tau - tau_true) > 1e-6:
            wrong += 1
print(f"frames={len(frames)} emitters={N_em} checks={len(frames)*N_em}")
print(f"non-single crossings: {multi}")
print(f"Newton wrong roots: {wrong}")
print(f"max Newton iterations: {max_it}")
