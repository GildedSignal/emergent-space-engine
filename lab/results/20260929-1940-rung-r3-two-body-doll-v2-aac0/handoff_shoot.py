#!/usr/bin/env python3
"""Stage 4: handoffs. A figure-eight transfer: a ship on a 1-year symmetric periodic
orbit of the circular restricted problem (star + planet on 1 AU circle + massless ship),
crossing the planet's SOI twice per period, 100 crossings over 50 years.
Reference: RK4 adaptive (half-step agreement 1e-9) on the same model.
Doll: patched star-doll/planet-doll Keplers with invariants re-expressed at each SOI
crossing. Metric: growth exponent of |E_helio_doll(k) - E_helio_ref(k)| across crossings."""
import sys, json, math
import numpy as np
sys.path.insert(0, '.')
from r3lib import GM_STAR, GM_PLANET, SOI, kepler_prop, planet_state

OM = 2.0 * math.pi


def ship_deriv(t, s):
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    px, py = math.cos(OM * t), math.sin(OM * t)
    dx, dy = px - x, py - y
    d3 = (dx * dx + dy * dy) ** 1.5
    ax = -GM_STAR * x / r3 + GM_PLANET * dx / d3
    ay = -GM_STAR * y / r3 + GM_PLANET * dy / d3
    return [vx, vy, ax, ay]


def rk4s(s, t, h):
    k1 = ship_deriv(t, s)
    s2 = [s[i] + 0.5 * h * k1[i] for i in range(4)]
    k2 = ship_deriv(t + 0.5 * h, s2)
    s3 = [s[i] + 0.5 * h * k2[i] for i in range(4)]
    k3 = ship_deriv(t + 0.5 * h, s3)
    s4 = [s[i] + h * k3[i] for i in range(4)]
    k4 = ship_deriv(t + h, s4)
    return [s[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]


def integrate_ship(s0, t_end, tol=1e-11, dtmax=1e-3, dtmin=1e-9):
    s = list(s0); t = 0.0; dt = 1e-3
    n = 0
    while t < t_end - 1e-15:
        if t + dt > t_end:
            dt = t_end - t
        a = rk4s(s, t, dt)
        b = rk4s(rk4s(s, t, 0.5 * dt), t, 0.5 * dt)
        err = max(abs(a[i] - b[i]) for i in range(4))
        if err > tol:
            dt *= 0.5
            if dt < dtmin:
                raise RuntimeError("dt underflow")
            continue
        s = a; t += dt; n += 1
        if err < tol / 50.0 and dt < dtmax:
            dt *= 1.4
    return s


def F(x0, ydot0):
    s0 = [x0, 0.0, 0.0, ydot0]
    s = integrate_ship(s0, 1.0)
    return [s[0] - x0, s[3] - ydot0]


def shoot():
    # ---- Newton shooting for the symmetric periodic orbit
    x0, yd = 1.0 - 0.0042, 4.1
    for it in range(12):
        f0 = F(x0, yd)
        print(f"iter {it}: x0={x0:.8f} yd={yd:.6f} F=({f0[0]:+.3e},{f0[1]:+.3e})", flush=True)
        if abs(f0[0]) < 1e-10 and abs(f0[1]) < 1e-10:
            break
        J = [[0.0] * 2 for _ in range(2)]
        d = 1e-7
        f1 = F(x0 + d, yd); f2 = F(x0, yd + d)
        J[0][0] = (f1[0] - f0[0]) / d; J[0][1] = (f2[0] - f0[0]) / d
        J[1][0] = (f1[1] - f0[1]) / d; J[1][1] = (f2[1] - f0[1]) / d
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        dx = (-f0[0] * J[1][1] + f0[1] * J[0][1]) / det
        dy = (-f0[1] * J[0][0] + f0[0] * J[1][0]) / det
        x0n, ydn = x0 + dx, yd + dy
    try:
        fn = F(x0n, ydn)
        if abs(fn[0]) + abs(fn[1]) > abs(f0[0]) + abs(f0[1]):
            x0n, ydn = x0 + 0.5 * dx, yd + 0.5 * dy
            fn = F(x0n, ydn)
            print("  damped half-step", flush=True)
    except RuntimeError as exn:
        print("  diverged:", exn, flush=True)
        fn = [float('inf'), float('inf')]
    if fn[0] == fn[0] and abs(fn[0]) + abs(fn[1]) < abs(f0[0]) + abs(f0[1]):
        x0, yd = x0n, ydn

    json.dump({"x0": x0, "ydot0": yd}, open('handoff_ic.json', 'w'))
    print("periodic IC:", x0, yd, " SOI:", SOI)

if __name__ == "__main__":
    shoot()
