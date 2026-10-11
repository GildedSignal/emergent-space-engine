#!/usr/bin/env python3
"""Kick-cadence probe: fixed vs significance-gated tidal kicks.

Planar circular restricted 3-body, primary GM=1 at origin, parent mu=1e-3 on a
circular orbit R=1. Kernel = Wisdom-Holoman split: exact Kepler drift under the
primary + tidal kick (incl. indirect term) applied at the interval midpoint.
Cost metric = number of field evaluations (events). Scheme A: fixed interval.
Scheme B: per-body interval from a relative field-change rule using only the
last two evaluations (no extra field evals for the decision).

Usage: sim.py <out.json> <A|B|ref> <param>   (param = kicks per parent orbit, or theta)
"""
import math, random, sys, time

MU_P = 1e-3
NB = math.sqrt(1.0 + MU_P)          # parent mean motion (R = 1)
T_ORB = 2.0 * math.pi / NB          # parent orbital period
HORIZON = 100.0 * T_ORB

def tide_dot(x, y, vx, vy, t):
    """Analytic time-derivative of the tidal field (no finite-difference delay)."""
    nt = NB * t
    c, s = math.cos(nt), math.sin(nt)
    vpx, vpy = -NB * s, NB * c
    wx, wy = x - c, y - s
    d2 = wx * wx + wy * wy
    d3 = d2 ** 1.5
    d5 = d3 * d2
    ex, ey = vx - vpx, vy - vpy
    wd = wx * ex + wy * ey
    return (-MU_P * (ex / d3 - 3 * wx * wd / d5) - MU_P * vpx,
            -MU_P * (ey / d3 - 3 * wy * wd / d5) - MU_P * vpy)

NBODY = 32
MUP = MU_P / (1.0 + MU_P)           # mass fraction, barycenter shift

TAU_MIN = T_ORB / 1024.0
TAU_MAX = T_ORB / 4.0
SAMPLE_DT = T_ORB / 4.0
NWIN = 100                          # rate windows (one parent orbit each)

def tide(x, y, t):
    c, s = math.cos(NB * t), math.sin(NB * t)
    dx, dy = c - x, s - y
    d3 = (dx * dx + dy * dy) ** 1.5
    return MU_P * (dx / d3 - c), MU_P * (dy / d3 - s)

def jacobi1(x, y, vx, vy, t):
    """Barycentric-rotation Jacobi (expected exact)."""
    c, s = math.cos(NB * t), math.sin(NB * t)
    bx, by = x - MUP * c, y - MUP * s
    r = math.hypot(x, y)
    d = math.hypot(x - c, y - s)
    wrx, wry = vx + NB * y, vy - NB * x       # v - n zhat x r
    return (NB * NB * (bx * bx + by * by) + 2.0 / r + 2.0 * MU_P / d
            - (wrx * wrx + wry * wry))

def jacobi2(x, y, vx, vy, t):
    """Variant without the barycenter shift (control on the oracle formula)."""
    c, s = math.cos(NB * t), math.sin(NB * t)
    r = math.hypot(x, y)
    d = math.hypot(x - c, y - s)
    wrx, wry = vx + NB * y, vy - NB * x
    return (NB * NB * (x * x + y * y) + 2.0 / r + 2.0 * MU_P / d
            - (wrx * wrx + wry * wry))

def drift(x, y, vx, vy, dt):
    """Exact Kepler drift under GM=1 (elements -> advance -> state)."""
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    if e < 1e-12:
        e = 1e-12
        ex, ey = e, 0.0
    om = math.atan2(ey, ex)
    sq = math.sqrt(max(1.0 - e * e, 1e-18))
    nb = a ** -1.5
    cosE = (1.0 - r / a) / e
    sinE = rv / (e * math.sqrt(a))
    E = math.atan2(sinE, cosE)
    M = E - e * math.sin(E) + nb * dt
    E = M
    for _ in range(6):
        E -= (E - e * math.sin(E) - M) / (1.0 - e * math.cos(E))
    cE, sE = math.cos(E), math.sin(E)
    den = 1.0 - e * cE
    px = a * (cE - e)
    py = a * sq * sE
    pvx = -a * nb * sE / den
    pvy = a * sq * nb * cE / den
    co, so = math.cos(om), math.sin(om)
    return (px * co - py * so, px * so + py * co,
            pvx * co - pvy * so, pvx * so + pvy * co, a, e)

def elements(x, y, vx, vy):
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    om = math.atan2(ey, ex)
    E = math.atan2(rv / (max(e, 1e-12) * math.sqrt(a)), (1.0 - r / a) / max(e, 1e-12))
    L = om + E - e * math.sin(E)
    return a, e, (L + math.pi) % (2 * math.pi) - math.pi

def init_bodies():
    rng = random.Random(20261011)
    bodies = []
    for i in range(NBODY):
        a = 0.25 + 0.30 * rng.random()
        e = 0.4 * rng.random()
        lam = 2 * math.pi * rng.random()
        om = 2 * math.pi * rng.random()
        f = 2 * math.pi * rng.random()          # true anomaly
        p = a * (1 - e * e)
        r = p / (1 + e * math.cos(f))
        x = r * math.cos(om + f); y = r * math.sin(om + f)
        h = math.sqrt(max(p, 1e-18))
        vr = h / p * e * math.sin(f)
        vt = h / r
        vx = vr * math.cos(om + f) - vt * math.sin(om + f)
        vy = vr * math.sin(om + f) + vt * math.cos(om + f)
        bodies.append((x, y, vx, vy, a, e))
    return bodies

def run(scheme, param):
    bodies = init_bodies()
    out = []
    for bi, (x0, y0, vx0, vy0, a0, e0) in enumerate(bodies):
        x, y, vx, vy = x0, y0, vx0, vy0
        t = 0.0
        if scheme in ('B', 'C'):
            tau = T_ORB / 128.0
        elif scheme == 'D':
            tau = 2.0 * math.pi / (param * abs(NB - a0 ** -1.5))  # kicks per synodic period
        else:
            tau = T_ORB / param
        apx = apy = None
        j10 = jacobi1(x, y, vx, vy, 0.0)
        j20 = jacobi2(x, y, vx, vy, 0.0)
        d1 = d2 = 0.0
        amag_last = 1.0
        events = 0
        wins = [0] * NWIN
        samples = []
        nxt = SAMPLE_DT
        ok = True
        while t < HORIZON:
            if scheme == 'A':
                tau = T_ORB / param
            x, y, vx, vy, _, _ = drift(x, y, vx, vy, tau / 2.0)
            tm = t + tau / 2.0
            ax, ay = tide(x, y, tm)
            adx = ady = None
            if scheme == 'C':
                adx, ady = tide_dot(x, y, vx, vy, tm)
            vx += ax * tau; vy += ay * tau
            x, y, vx, vy, _, _ = drift(x, y, vx, vy, tau / 2.0)
            t += tau
            events += 1
            w = int(t / T_ORB)
            if 0 <= w < NWIN:
                wins[w] += 1
            if t >= nxt:
                d1 = max(d1, abs(jacobi1(x, y, vx, vy, t) - j10) / abs(j10))
                d2 = max(d2, abs(jacobi2(x, y, vx, vy, t) - j20) / abs(j20))
                samples.append((t, d1))
                nxt += SAMPLE_DT
            if apx is not None and scheme == 'B':
                da = math.hypot(ax - apx, ay - apy)
                amag = math.hypot(ax, ay)
                amag_last = amag
                nu = param * amag * tau / max(da, 1e-18)
                tau = min(max(nu, TAU_MIN), TAU_MAX)
            elif scheme == 'C' and adx is not None:
                amag = math.hypot(ax, ay)
                da = math.hypot(adx, ady)
                nu = param * amag / max(da, 1e-18)
                tau = min(max(nu, TAU_MIN), TAU_MAX)
            apx, apy = ax, ay
            if events > 400000:
                ok = False
                break
        a_f, e_f, L_f = elements(x, y, vx, vy) if ok else (float('nan'),) * 3
        tb = 2 * math.pi * a0 ** 1.5
        win_max = max(wins) / (T_ORB / tb)
        out.append(dict(a0=a0, e0=e0, events=events, ok=ok,
                        rate=events / (HORIZON / tb), win_max=win_max,
                        d1=d1, d2=d2, samples=samples,
                        a_f=a_f, e_f=e_f, L_f=L_f))
    return out

def summarize(res):
    ds = sorted(r['d1'] for r in res if r['ok'])
    rs = sorted(r['rate'] for r in res if r['ok'])
    wm = sorted(r['win_max'] for r in res if r['ok'])
    n = len(ds)
    med = ds[n // 2]
    p90 = ds[int(0.9 * (n - 1))]
    return dict(median_d1=med, p90_d1=p90,
                mean_rate=sum(rs) / len(rs),
                mean_winmax=sum(wm) / len(wm),
                ratio_winmax_rate=(sum(wm) / len(wm)) / (sum(rs) / len(rs)))

if __name__ == '__main__':
    outpath, scheme, param = sys.argv[1], sys.argv[2], float(sys.argv[3])
    t0 = time.time()
    res = run(scheme, param)
    summ = summarize(res)
    summ.update(scheme=scheme, param=param, wall=time.time() - t0)
    import json
    json.dump(dict(summary=summ, bodies=res), open(outpath, 'w'))
    print(scheme, param, json.dumps(summ))
