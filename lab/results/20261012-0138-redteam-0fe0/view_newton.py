#!/usr/bin/env python3
"""Red-team 20261012-0138, attack A3 (the view gathered at the past light cone).

representation.md §2: "Each visible tube crosses the observer's past light cone once;
Newton's method finds the crossing, starting from the previous frame's." r6 judges the
*cost* (iterations per frame); nothing judges the behaviour at relativistic emitters.

The root function F(t_e) = (t_o - t_e) - |x_e(t_e)| has F' = -1 - x_hat . v_e, which
degenerates to -(1 - beta_radial) when the emitter runs straight at the observer. Newton
on a nearly-flat region overshoots. Emitter: circular orbit of radius R at orbital speed
beta (the game's compact-object neighbourhoods), observer at distance D on the x axis,
60 FPS. Warm start: the previous frame's root.

Counts Newton iterations per frame (capped at 64) for beta in {0.1, 0.5, 0.9, 0.99}.
"""
import math

R, D, FPS, CAP = 100.0, 1000.0, 60.0, 64

def emitter(t, beta):
    w = beta / R
    return (R * math.cos(w * t), R * math.sin(w * t))

def F(te, to, beta):
    x, y = emitter(te, beta)
    return (to - te) - math.hypot(x - D, y)

def run(beta, seconds=8.0):
    # cold start: bisect the first frame to machine precision
    def solve_bisect(to):
        lo, hi = to - (D + 2 * R) - 1, to
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if F(mid, to, beta) > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    prev = solve_bisect(0.0)
    iters, frames = [], 0
    to = 0.0
    while to < seconds:
        to += 1.0 / FPS
        te, k = prev, 0
        while k < CAP:
            x, y = emitter(te, beta)
            r = math.hypot(x - D, y)
            # F' = -1 - (x-D)/r * vx - y/r * vy
            w = beta / R
            vx, vy = -R * w * math.sin(w * te), R * w * math.cos(w * te)
            fp = -1.0 - ((x - D) * vx + y * vy) / r
            f = (to - te) - r
            step = f / fp
            te -= step
            k += 1
            if abs(step) < 1e-13 * max(1.0, abs(te)):
                break
        iters.append(k)
        prev = te
        frames += 1
    mean = sum(iters) / len(iters)
    tail = sorted(iters)[int(0.99 * len(iters)) - 1]
    return mean, max(iters), tail, iters.count(CAP)

print(f"{'beta':>6} {'mean it/frame':>14} {'p99':>5} {'max':>5} {'capped@64':>10}")
for beta in (0.1, 0.5, 0.9, 0.99, 0.999):
    mean, mx, p99, capped = run(beta)
    print(f"{beta:>6} {mean:>14.2f} {p99:>5} {mx:>5} {capped:>10}")
