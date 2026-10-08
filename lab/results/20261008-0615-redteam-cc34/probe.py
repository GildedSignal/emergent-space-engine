#!/usr/bin/env python3
"""redteam-cc34: does the fixed-tolerance resonance switch survive a chirp?

Planar circular restricted 3-body, interior 2:1, mu = 3e-4 (r4's range).
truth    = full unaveraged RK4 (star fixed, perturber on a circle, drag -k v).
switched = the design's shape: secular-averaged elements OUTSIDE the fixed
           tolerance W (law.md #29 gate, W = 2.5 mu^(2/3), r4 v3's width),
           exact integration INSIDE (the design's best in-resonance law).
Pure float probe: orders of magnitude, outcome labels, ratios.
"""
import math, json

MU = 3e-4
GMS = 1.0 - MU          # star GM (perturber GM = MU), total = 1
AP, NP = 1.0, 1.0       # perturber circle
W_REL = 2.5 * MU ** (2.0 / 3.0)          # fixed tolerance, relative da/a
A_RES = 0.5 ** (2.0 / 3.0)
K_DRAG = 2.38e-5                         # ~300 particle orbits to cross 4W
T_LIB_ORB = 3.14                          # ~1 orbit in time units at a_res


def accel(x, y, vx, vy, t, lp0, unaveraged=True):
    ax = ay = 0.0
    if unaveraged:
        px, py = AP * math.cos(t + lp0), AP * math.sin(t + lp0)
        dx, dy = px - x, py - y
        r = math.hypot(x, y)
        d = math.hypot(dx, dy)
        ax += -GMS * x / (r * r * r) + MU * dx / (d * d * d)
        ay += -GMS * y / (r * r * r) + MU * dy / (d * d * d)
    ax += -K_DRAG * vx
    ay += -K_DRAG * vy
    return ax, ay


def rk4(x, y, vx, vy, t, h, lp0, unaveraged=True):
    k1x, k1y = vx, vy
    a1x, a1y = accel(x, y, vx, vy, t, lp0, unaveraged)
    k2x, k2y = vx + 0.5 * h * a1x, vy + 0.5 * h * a1y
    a2x, a2y = accel(x + 0.5 * h * k1x, y + 0.5 * h * k1y, k2x, k2y, t + 0.5 * h, lp0, unaveraged)
    k3x, k3y = vx + 0.5 * h * a2x, vy + 0.5 * h * a2y
    a3x, a3y = accel(x + 0.5 * h * k2x, y + 0.5 * h * k2y, k3x, k3y, t + 0.5 * h, lp0, unaveraged)
    k4x, k4y = vx + h * a3x, vy + h * a3y
    a4x, a4y = accel(x + h * k3x, y + h * k3y, k4x, k4y, t + h, lp0, unaveraged)
    return (x + h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x),
            y + h / 6 * (k1y + 2 * k2y + 2 * k3y + k4y),
            vx + h / 6 * (a1x + 2 * a2x + 2 * a3x + a4x),
            vy + h / 6 * (a1y + 2 * a2y + 2 * a3y + a4y))


def elems(x, y, vx, vy):
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2 / GMS)
    ex = (v2 / GMS - 1.0 / r) * x - (x * vx + y * vy) * vx / GMS
    ey = (v2 / GMS - 1.0 / r) * y - (x * vx + y * vy) * vy / GMS
    e = math.hypot(ex, ey)
    wpi = math.atan2(ey, ex)
    # true longitude
    lam = math.atan2(y, x)
    nu = lam - wpi
    c, s = math.cos(nu), math.sin(nu)
    E = math.atan2(math.sqrt(1 - e * e) * s, e + c)
    M = E - e * math.sin(E)
    return a, e, wpi, wpi + M


def state(a, e, wpi, M):
    E = M
    for _ in range(60):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    x = a * (math.cos(E) - e)
    y = a * math.sqrt(1 - e * e) * math.sin(E)
    ca, sa = math.cos(wpi), math.sin(wpi)
    x, y = ca * x - sa * y, sa * x + ca * y
    n = math.sqrt(GMS / a ** 3)
    vf = n * a / (1 - e * math.cos(E))
    vx = -vf * math.sin(E)
    vy = vf * math.sqrt(1 - e * e) * math.cos(E)
    vx, vy = ca * vx - sa * vy, sa * vx + ca * vy
    return x, y, vx, vy


def truth_run(a0, e0, lp0, t_end, h_over_T=1 / 120.0, entry_frac=0.0):
    x, y, vx, vy = state(a0, e0, 0.0, 0.0)
    t, h = 0.0, h_over_T * 2 * math.pi * math.sqrt(a0 ** 3 / GMS)
    best = [None, None]
    a_tr, e_tr, phi_tr = [], [], []
    e_thr = 0.1 * e0 + 0.002
    while t < t_end:
        x, y, vx, vy = rk4(x, y, vx, vy, t, h, lp0)
        t += h
        if int(t / h) % 4 == 0:
            a, e, wpi, lam = elems(x, y, vx, vy)
            phi = math.remainder(2 * (t + lp0) - lam - wpi, 2 * math.pi)
            a_tr.append(a); e_tr.append(e); phi_tr.append(phi)
            if best[0] is None and abs(e - e0) > e_thr:
                best[0] = t
                best[1] = abs(a - A_RES) / A_RES / W_REL
    n3 = 3 * len(a_tr) // 4
    rng = max(phi_tr[n3:]) - min(phi_tr[n3:])
    cap = rng < math.pi
    return dict(captured=cap, e_final=e_tr[-1], a_final=a_tr[-1],
                e_max=max(e_tr), entry_t=best[0], entry_over_W=best[1],
                phi_range=rng)


def calibrate(a_c, e0=0.05, orbits=200):
    """measure g(a) = d(wpi)/dt and dn(a): secular rates outside the island.
    Drag off: the averaged branch applies the drag itself (no double count)."""
    global K_DRAG
    K_DRAG, k0 = 0.0, K_DRAG
    x, y, vx, vy = state(a_c, e0, 0.0, 0.0)
    t, h = 0.0, (2 * math.pi * math.sqrt(a_c ** 3 / GMS)) / 120.0
    t_end = orbits * 2 * math.pi * math.sqrt(a_c ** 3 / GMS)
    n0 = math.sqrt(GMS / a_c ** 3)
    ts, ws, ls = [], [], []
    while t < t_end:
        x, y, vx, vy = rk4(x, y, vx, vy, t, h, 0.0)
        t += h
        if int(t / h) % 8 == 0:
            a, e, wpi, lam = elems(x, y, vx, vy)
            if ts:
                wpi += 2 * math.pi * round((ws[-1] - wpi) / (2 * math.pi))
                d = lam - n0 * t
                d += 2 * math.pi * round((ls[-1] - d) / (2 * math.pi))
            else:
                d = lam
            ts.append(t); ws.append(wpi); ls.append(d)
    K_DRAG = k0
    def slope(ys):
        n = len(ys); sx = sum(ts) / n; sy = sum(ys) / n
        b = sum((ts[i] - sx) * (ys[i] - sy) for i in range(n)) / sum((ti - sx) ** 2 for ti in ts)
        return b
    return slope(ws), slope(ls)


def switched_run(a0, e0, lp0, t_end, g_fit, dn_fit):
    """averaged elements outside W, exact inside. Returns outcome + log."""
    a, e, wpi, M = a0, e0, 0.0, 0.0
    lam = wpi + M
    t, dt = 0.0, 0.25
    log = []
    while t < t_end:
        n = math.sqrt(GMS / a ** 3)
        g = g_fit(a); dn = dn_fit(a)
        det = abs(2 * NP - (n + dn) - g)
        if det <= 1.5 * W_REL * n:            # inside tolerance: exact law
            break
        lam += (n + dn) * dt
        wpi += g * dt
        a *= math.exp(-2 * K_DRAG * (1 + 0.5 * e * e) * dt)
        t += dt
        log.append((t, a, e))
    x, y, vx, vy = state(a, e, wpi, lam - wpi)
    h = (2 * math.pi * math.sqrt(a ** 3 / GMS)) / 120.0
    a_tr, e_tr, phi_tr = [], [], []
    while t < t_end:
        x, y, vx, vy = rk4(x, y, vx, vy, t, h, lp0)
        t += h
        if int(t / h) % 4 == 0:
            aa, ee, ww, ll = elems(x, y, vx, vy)
            phi = math.remainder(2 * (t + lp0) - ll - ww, 2 * math.pi)
            a_tr.append(aa); e_tr.append(ee); phi_tr.append(phi)
    n3 = 3 * len(a_tr) // 4
    rng = max(phi_tr[n3:]) - min(phi_tr[n3:])
    return dict(captured=rng < math.pi, e_final=e_tr[-1], a_final=a_tr[-1],
                e_max=max(e_tr + [e]), switch_t=log[-1][0] if log else 0.0,
                switch_det_over_W=abs(log[-1][1] - A_RES) / A_RES / W_REL if log else 0.0,
                phi_range=rng)


def main():
    out = {}
    # calibration of the averaged branch's secular rates (outside island)
    a1, a2 = A_RES * 1.10, A_RES * 1.17   # far-field: secular rates only
    g1, dn1 = calibrate(a1); g2, dn2 = calibrate(a2)
    def g_fit(a):  s = (g2 - g1) / (a2 - a1);  return g1 + s * (a - a1)
    def dn_fit(a): s = (dn2 - dn1) / (a2 - a1); return dn1 + s * (a - a1)
    out['calibration'] = dict(g=[g1, g2], dn=[dn1, dn2])
    t_end = 1200 * T_LIB_ORB
    a0 = A_RES * (1 + 2 * W_REL)
    rows = []
    for e0 in (0.005, 0.05, 0.2):
        for lp0 in (0.0, math.pi):
            tr = truth_run(a0, e0, lp0, t_end)
            sw = switched_run(a0, e0, lp0, t_end, g_fit, dn_fit)
            rows.append(dict(e0=e0, lp0=lp0, truth=tr, switched=sw))
            print(f"e0={e0:6g} lp0={lp0:5g}  TRUTH cap={tr['captured']!s:5} "
                  f"e_fin={tr['e_final']:.4g} entry/W={tr['entry_over_W'] if tr['entry_over_W'] else -1:6.2f}   "
                  f"SWITCH cap={sw['captured']!s:5} e_fin={sw['e_final']:.4g} "
                  f"switch@W={sw['switch_det_over_W']:.2f}")
    out['rows'] = rows
    # slow chirp (K/4): adiabatic side, where the libration island width rules
    global K_DRAG
    K_DRAG /= 4.0
    t_slow = 2.2 * t_end
    for e0 in (0.05, 0.2):
        tr = truth_run(a0, e0, 0.0, t_slow)
        sw = switched_run(a0, e0, 0.0, t_slow, g_fit, dn_fit)
        rows.append(dict(e0=e0, lp0='slow', truth=tr, switched=sw))
        print(f"SLOW e0={e0:6g}           TRUTH cap={tr['captured']!s:5} "
              f"e_fin={tr['e_final']:.4g} a_fin={tr['a_final']:.5g} entry/W={tr['entry_over_W'] if tr['entry_over_W'] else -1:6.2f}   "
              f"SWITCH cap={sw['captured']!s:5} e_fin={sw['e_final']:.4g} a_fin={sw['a_final']:.5g}")
    K_DRAG *= 4.0
    # convergence: e0=0.2, lp0=0, half step
    tr_h2 = truth_run(a0, 0.2, 0.0, t_end, h_over_T=1 / 240.0)
    out['convergence'] = dict(base=rows[4]['truth'], half=tr_h2)
    print("convergence e0=0.2:", rows[4]['truth']['captured'], tr_h2['captured'],
          f"e_fin {rows[4]['truth']['e_final']:.4g} vs {tr_h2['e_final']:.4g}")
    with open('probe-out.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
