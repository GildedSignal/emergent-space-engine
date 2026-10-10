#!/usr/bin/env python3
"""Independent verification of missed pairs: pure-python Kepler from dumped elements.
Elements: [a, e, pom, period(ticks), tp(ticks)]; TAU*2^32 ticks per time unit."""
import json, math

TAU = 2 * math.pi
TICKS = 4294967296.0

def body(a, e, pom, period, tp):
    n = TAU * TICKS / period
    # a stored on Body is derived from n; use it directly
    return (a, e, pom, period, tp, n)

def state(b, t):
    a, e, pom, period, tp, n = b
    M = ((t * TICKS - tp) / period) * TAU
    E = M
    for _ in range(80):
        f = E - e * math.sin(E) - M
        fp = 1 - e * math.cos(E)
        d = f / fp
        E -= d
        if abs(d) < 1e-15:
            break
    cE, sE = math.cos(E), math.sin(E)
    r = a * (1 - e * cE)
    xv = a * (cE - e)
    yv = a * math.sqrt(1 - e * e) * sE
    ke = n * a / r
    cp, sp = math.cos(pom), math.sin(pom)
    return (xv * cp - yv * sp, xv * sp + yv * cp, ke * (-sE) * cp - ke * (math.sqrt(1-e*e) * cE) * sp,
            ke * (-sE) * sp + ke * (math.sqrt(1-e*e) * cE) * cp)

def mind(bi, bj, t_end, ns=400000):
    best, bt = float('inf'), 0.0
    for s in range(ns):
        t = t_end * s / ns
        pi, pj = state(bi, t), state(bj, t)
        d = math.hypot(pi[0] - pj[0], pi[1] - pj[1])
        if d < best:
            best, bt = d, t
    # golden refine
    lo, hi = max(0.0, bt - 2 * t_end / ns), min(t_end, bt + 2 * t_end / ns)
    phi = 0.6180339887498949
    c, dd = hi - phi * (hi - lo), lo + phi * (hi - lo)
    fc, fd = None, None
    def f(t):
        pi, pj = state(bi, t), state(bj, t)
        return math.hypot(pi[0] - pj[0], pi[1] - pj[1])
    fc, fd = f(c), f(dd)
    for _ in range(90):
        if fc < fd:
            hi, dd, fd = dd, c, fc
            c = hi - phi * (hi - lo); fc = f(c)
        else:
            lo, c, fc = c, dd, fd
            dd = lo + phi * (hi - lo); fd = f(dd)
    m = f(0.5 * (lo + hi))
    return (min(best, m), bt)

if __name__ == '__main__':
    import sys
    for line in open(sys.argv[1]):
        d = json.loads(line)['missmap']
        rho, orbits = d['rho'], d['orbits']
        t_end = orbits * TAU
        print(f"scene rho={rho} orbits={orbits}")
        for e in d['detail'][:4]:
            bi = body(*e['el_i']); bj = body(*e['el_j'])
            dm, tm = mind(bi, bj, t_end)
            ok = dm < rho
            print(f"  pair {e['pair']} rust_d={e['d']:.4e} py_d={dm:.4e} t={tm:.4f} sub-rho={ok} verdict={e['v']}")
