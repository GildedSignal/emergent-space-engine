#!/usr/bin/env python3
"""Band-triggered kicks vs fixed-cadence kicks under a real third-body tide.

Body: mu=1, a=1, e in {0.6, 0.9}, starts at periapsis. Perturber: m_p on a
circular orbit a_p, same plane. Truth: RK4, dt = T/nsteps. Generator: exact
Kepler from the last kick (the engine's drift tube). A kick re-anchors the
generator to the truth state. Policies:
  fixed(j): kick every T/j (law.md today: kicks at a fixed step in phase)
  band(w):  kick at the first check where |r_true - r_gen| > w
"""
import json, math, sys

MU = 1.0
TWO_PI = 2.0 * math.pi

def accel(x, y, t, mp, ap, kep_on=True):
    ax = ay = 0.0
    if kep_on:
        r = math.hypot(x, y)
        f = -MU / (r * r * r)
        ax += f * x; ay += f * y
    if mp > 0.0:
        th = TWO_PI * t / (TWO_PI * math.sqrt(ap ** 3))  # n_p*t
        xp = ap * math.cos(th); yp = ap * math.sin(th)
        dx = xp - x; dy = yp - y
        d3 = (dx * dx + dy * dy) ** 1.5
        rp3 = ap ** 3
        ax += mp * (dx / d3 - xp / rp3)
        ay += mp * (dy / d3 - yp / rp3)
    return ax, ay

def truth(e, mp, ap, orbits, nsteps_per_orbit):
    dt = TWO_PI / nsteps_per_orbit
    rp0 = 1.0 - e
    x = rp0; y = 0.0
    v0 = math.sqrt(MU * (1.0 + e) / (1.0 - e))
    vx = 0.0; vy = v0
    n = orbits * nsteps_per_orbit
    traj = []
    for i in range(n + 1):
        t = i * dt
        traj.append((t, x, y, vx, vy))
        ax, ay = accel(x, y, t, mp, ap)
        k1x, k1y = vx, vy
        ax2, ay2 = accel(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, t + 0.5 * dt, mp, ap)
        k2x, k2y = vx + 0.5 * dt * ax, vy + 0.5 * dt * ay
        ax3, ay3 = accel(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, t + 0.5 * dt, mp, ap)
        k3x, k3y = vx + 0.5 * dt * ax2, vy + 0.5 * dt * ay2
        ax4, ay4 = accel(x + dt * k3x, y + dt * k3y, t + dt, mp, ap)
        k4x, k4y = vx + dt * ax3, vy + dt * ay3
        x += dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x)
        y += dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y)
        vx += dt / 6.0 * (ax + 2 * ax2 + 2 * ax3 + ax4)
        vy += dt / 6.0 * (ay + 2 * ay2 + 2 * ay3 + ay4)
    # energy drift check (Kepler part)
    e0 = 0.5 * v0 * v0 - MU / rp0
    xf, yf, vxf, vyf = traj[-1][1:5]
    e1 = 0.5 * (vxf * vxf + vyf * vyf) - MU / math.hypot(xf, yf)
    return traj, abs((e1 - e0) / e0)

def kepler_gen(t0, x0, y0, vx0, vy0, t):
    """Exact two-body propagation of the kick state to time t (2-D)."""
    r0 = math.hypot(x0, y0)
    v2 = vx0 * vx0 + vy0 * vy0
    a = 1.0 / (2.0 / r0 - v2 / MU)  # mu=1
    rv = x0 * vx0 + y0 * vy0
    ex = (v2 - 1.0 / r0) * x0 - rv * vx0
    ey = (v2 - 1.0 / r0) * y0 - rv * vy0
    e = math.hypot(ex, ey)
    w = math.atan2(ey, ex) if e > 1e-12 else 0.0
    cw, sw = math.cos(w), math.sin(w)
    xp = cw * x0 + sw * y0; yp = -sw * x0 + cw * y0
    vxp = cw * vx0 + sw * vy0; vyp = -sw * vx0 + cw * vy0
    b = a * math.sqrt(max(1.0 - e * e, 1e-18))
    E0 = math.atan2(yp / b, xp / a + e)
    M0 = E0 - e * math.sin(E0)
    n = 1.0 / (a * math.sqrt(a))
    M = M0 + n * (t - t0)
    M = (M + math.pi) % TWO_PI - math.pi
    E = M if e < 0.8 else math.pi
    for _ in range(60):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        d = f / fp
        if d > 0.4: d = 0.4
        if d < -0.4: d = -0.4
        E -= d
        if abs(d) < 1e-14: break
    cE, sE = math.cos(E), math.sin(E)
    xpf = a * (cE - e); ypf = b * sE
    vf = math.sqrt(MU / a) / (1.0 - e * cE)
    vxpf = -vf * sE; vypf = vf * b / a * cE
    return (cw * xpf - sw * ypf, sw * xpf + cw * ypf,
            cw * vxpf - sw * vypf, sw * vxpf + cw * vypf)

def sep_angle(t, x, y, ap):
    Tp = TWO_PI * math.sqrt(ap ** 3)
    thp = TWO_PI * (t % Tp) / Tp
    thb = math.atan2(y, x)
    d = (thb - thp + math.pi) % TWO_PI - math.pi
    return abs(d)

def run_band(traj, w, step, ap, conj_win=math.radians(45.0)):
    """step = index stride between checks (1 -> every stored step)."""
    kicks = 0; maxd = 0.0; near_conj = 0
    tk = traj[0][0]; xk, yk, vxk, vyk = traj[0][1:5]
    first_gap = None; last_kick_i = 0
    for i in range(step, len(traj), step):
        t, x, y, vx, vy = traj[i]
        gx, gy, _, _ = kepler_gen(tk, xk, yk, vxk, vyk, t)
        d = math.hypot(x - gx, y - gy)
        if d > maxd: maxd = d
        if d > w:
            kicks += 1
            if sep_angle(t, x, y, ap) < conj_win: near_conj += 1
            if first_gap is None: first_gap = i - last_kick_i
            last_kick_i = i
            tk = t; xk, yk, vxk, vyk = x, y, vx, vy
    orbits = traj[-1][0] / TWO_PI
    return dict(policy='band', w=w, check_stride=step, kicks_per_orbit=kicks / orbits,
                max_dev=maxd, frac_near_conj=(near_conj / kicks) if kicks else None,
                kicks=kicks, orbits=orbits)

def run_fixed(traj, j, step, ap):
    dt_kick = TWO_PI / j
    kicks = 0; maxd = 0.0; next_t = traj[0][0] + dt_kick
    tk = traj[0][0]; xk, yk, vxk, vyk = traj[0][1:5]
    for i in range(step, len(traj), step):
        t, x, y, vx, vy = traj[i]
        gx, gy, _, _ = kepler_gen(tk, xk, yk, vxk, vyk, t)
        d = math.hypot(x - gx, y - gy)
        if d > maxd: maxd = d
        if t >= next_t:
            kicks += 1
            next_t += dt_kick
            tk = t; xk, yk, vxk, vyk = x, y, vx, vy
    orbits = traj[-1][0] / TWO_PI
    return dict(policy='fixed', j=j, kicks_per_orbit=kicks / orbits, max_dev=maxd,
                kicks=kicks, orbits=orbits)

def main():
    mp, ap = 3e-3, 2.2
    out = {'runs': []}
    NSTEP = 8192; ORB = 10
    for e in (0.6, 0.9):
        traj, edrift = truth(e, mp, ap, ORB, NSTEP)
        print(f"# e={e}: truth RK4 T/{NSTEP}, {ORB} orbits, |dE/E|={edrift:.2e}", flush=True)
        base = dict(e=e, energy_drift=edrift)
        for j in (4, 8, 16, 32, 64, 128, 256, 512):
            r = run_fixed(traj, j, 2, ap); r.update(base); out['runs'].append(r)
            print(f"fixed j={j:4d}: kicks/orbit={r['kicks_per_orbit']:7.2f} maxdev={r['max_dev']:.3e}", flush=True)
        # band at fine check (T/4096): stored grid is T/8192, stride 2
        for w in (3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1):
            r = run_band(traj, w, 2, ap); r.update(base)
            out['runs'].append(r)
            fc = 'n/a' if r['frac_near_conj'] is None else f"{r['frac_near_conj']:.2f}"
            print(f"band w={w:.0e}: kicks/orbit={r['kicks_per_orbit']:7.2f} maxdev={r['max_dev']:.3e} near_conj={fc}", flush=True)
        # sizing: same w, coarse check (T/1024 -> stride 8) vs fine (stride 1)
        w0 = 3e-3
        for stride, tag in ((8, 'mean-rate check'), (1, 'peak-rate check')):
            r = run_band(traj, w0, stride, ap); r.update(base); r['sizing'] = tag
            out['runs'].append(r)
            print(f"band w={w0:.0e} [{tag}]: maxdev/w={r['max_dev'] / w0:6.2f} kicks/orbit={r['kicks_per_orbit']:7.2f}", flush=True)
    # controls: no perturber, e=0.6
    traj0, ed0 = truth(0.6, 0.0, ap, ORB, NSTEP)
    print(f"# control e=0.6 m_p=0: |dE/E|={ed0:.2e}", flush=True)
    rb = run_band(traj0, 3e-3, 2, ap); rb.update(e=0.6, control='no-surprise'); out['runs'].append(rb)
    rf = run_fixed(traj0, 64, 2, ap); rf.update(e=0.6, control='no-surprise'); out['runs'].append(rf)
    print(f"control band: kicks={rb['kicks']} (predict 0); control fixed j=64: kicks={rf['kicks']}", flush=True)
    json.dump(out, open('metrics.json', 'w'), indent=1)
    print("wrote metrics.json")

if __name__ == '__main__':
    main()
