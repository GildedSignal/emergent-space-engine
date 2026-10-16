#!/usr/bin/env python3
"""The stagger's B13/B14-class legality analysis (run 20261016-0504-second-…-917c-c840).

Reads the probe's raw outputs (law-off and law-armed) and an independent float64 RK4
reference integrated from the same starts, and prints:
  - flybys: the assist (ΔE_h, ΔL_h at the reference's SOI exit, B13's rule) per seed,
    law-off and law-armed, each vs the reference (relative), plus the pass flip table;
  - moons: the apsidal precession rate (rad per planet period, hill.rs's estimator) for
    law-off, law-armed and the reference, the escape class at 1.5 R_H for all three,
    and the armed-vs-off rate difference against B14's 10% threshold.
"""
import math, struct, sys

MU, SEP, PR = 1e-3, 5.27e8, 4.84e4
TAU = 2 * math.pi
OM = SEP ** -1.5
P = TAU / OM
TO_ROOT = 1.0 / (1.0 - MU)
SOI = SEP * (MU / 3.0) ** (1.0 / 3.0)
HILL = SOI

f = lambda h: struct.unpack('<d', struct.pack('<Q', int(h, 16)))[0]

def planet(t):
    a = OM * t
    return (SEP * (1 - MU) * math.cos(a), SEP * (1 - MU) * math.sin(a))

def star(t):
    a = OM * t
    return (-SEP * MU * math.cos(a), -SEP * MU * math.sin(a))

def accel(t, s):
    px, py = planet(t)
    sx, sy = star(t)
    rx, ry = s[0] - sx, s[1] - sy
    qx, qy = s[0] - px, s[1] - py
    r3 = (rx * rx + ry * ry) ** 1.5
    q3 = (qx * qx + qy * qy) ** 1.5
    return (-(1 - MU) * rx / r3 - MU * qx / q3, -(1 - MU) * ry / r3 - MU * qy / q3)

def rk4(s0, t0, t1, n, keep=None):
    """Fixed-step RK4 from s0=[x,y,vx,vy] over [t0,t1]; returns list of (t, s)."""
    out = []
    dt = (t1 - t0) / n
    s = list(s0)
    t = t0
    for i in range(n + 1):
        stride = keep or max(1, n // 5120)
        if i % stride == 0 or i == n:
            out.append((t, tuple(s)))
        a1 = accel(t, s)
        s2 = [s[0] + s[2] * dt / 2, s[1] + s[3] * dt / 2, s[2] + a1[0] * dt / 2, s[3] + a1[1] * dt / 2]
        a2 = accel(t + dt / 2, s2)
        s3 = [s[0] + s2[2] * dt / 2, s[1] + s2[3] * dt / 2, s[2] + a2[0] * dt / 2, s[3] + a2[1] * dt / 2]
        a3 = accel(t + dt / 2, s3)
        s4 = [s[0] + s3[2] * dt, s[1] + s3[3] * dt, s[2] + a3[0] * dt, s[3] + a3[1] * dt]
        a4 = accel(t + dt, s4)
        s = [
            s[0] + (s[2] + 2 * s2[2] + 2 * s3[2] + s4[2]) * dt / 6,
            s[1] + (s[3] + 2 * s2[3] + 2 * s3[3] + s4[3]) * dt / 6,
            s[2] + (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]) * dt / 6,
            s[3] + (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1]) * dt / 6,
        ]
        t = t0 + (i + 1) * dt
    return out

def helio(t, s):
    sx, sy = star(t)
    svx = -SEP * MU * OM * math.sin(OM * t)
    svy = SEP * MU * OM * math.cos(OM * t)
    rx, ry = s[0] - sx, s[1] - sy
    vx, vy = s[2] - svx, s[3] - svy
    e = (vx * vx + vy * vy) / 2 - (1 - MU) / math.hypot(rx, ry)
    l = rx * vy - ry * vx
    return e, l

def lcg(seed):
    C, D, M = 6364136223846793005, 1442695040888963407, 1 << 64
    s = (seed * C + D) % M
    def nxt():
        nonlocal s
        s = (s * C + D) % M
        return (s >> 11) / float(1 << 53)
    return nxt

def planet_vel(t):
    a = OM * t
    return (-SEP * (1 - MU) * OM * math.sin(a), SEP * (1 - MU) * OM * math.cos(a))

def apsidal_rate(times, states):
    varpi = []
    for t, s in zip(times, states):
        px, py = planet(t)
        pvx, pvy = planet_vel(t)
        w = (s[0] - px, s[1] - py, s[2] - pvx, s[3] - pvy)
        r2 = w[0] * w[0] + w[1] * w[1]
        v2 = w[2] * w[2] + w[3] * w[3]
        rv = w[0] * w[2] + w[1] * w[3]
        k = v2 - MU / math.sqrt(r2)
        ex, ey = k * w[0] - rv * w[2], k * w[1] - rv * w[3]
        if not math.hypot(ex, ey) > 1e-9 * MU:
            return None
        ang = math.atan2(ey, ex)
        if not varpi:
            varpi.append(ang)
            continue
        jump = (ang - varpi[-1]) % TAU
        if jump > math.pi:
            jump -= TAU
        if abs(jump) > math.pi / 2:
            return None
        varpi.append(varpi[-1] + jump)
    u = [t / P for t in times]
    n = len(u)
    mu_ = sum(u) / n
    mv = sum(varpi) / n
    num = sum((a - mu_) * (b - mv) for a, b in zip(u, varpi))
    den = sum((a - mu_) ** 2 for a in u)
    return num / den

# ---- flybys ----
def parse_flyby(p):
    rows = {}
    for ln in open(p):
        toks = ln.strip().split()
        if not toks or toks[0] != 'flyby':
            continue
        i = int(toks[1])
        d = {'q': float(toks[2].split('=')[1][:-1]), 'vinf': float(toks[3].split('=')[1]), 'psi': float(toks[4].split('=')[1])}
        j = toks.index('start') + 5
        d['start'] = [f(x) for x in toks[j - 4:j]]
        while j < len(toks) - 1 and toks[j].startswith('t'):
            t = toks[j]
            if j + 1 < len(toks) and toks[j + 1] == 'LOST':
                d[t] = None
                j += 2
                continue
            d[t] = [f(x) for x in toks[j + 1:j + 5]]
            d['E' + t[1:]] = f(toks[j + 5][2:])
            d['L' + t[1:]] = f(toks[j + 6][2:])
            j += 7
        rows[i] = d
    return rows

def ref_exit(s0):
    """B13's rule: the first time after coming within SOI that r_planet exceeds 1.5 SOI, within one period."""
    traj = rk4(s0, 0.0, P, 120000, keep=60)
    entered = False
    for idx, (t, s) in enumerate(traj):
        px, py = planet(t)
        r = math.hypot(s[0] - px, s[1] - py)
        if not entered and r <= SOI:
            entered = True
        if entered and r > 1.5 * SOI:
            # refine by bisection with a fine integration over the last coarse step
            t0 = traj[idx - 1][0]
            fine = rk4(traj[idx - 1][1], t0, t, 240)
            for tf, sf in fine:
                px, py = planet(tf)
                if math.hypot(sf[0] - px, sf[1] - py) > 1.5 * SOI:
                    return tf, sf, r
            return t, s, r
    return None, None, None

print('== B13-class probe: the assist at the reference exit (law-off vs law-armed vs RK4 reference) ==')
off = parse_flyby(sys.argv[1] + '/probe_flyby_off.txt')
arm = parse_flyby(sys.argv[1] + '/probe_flyby_armed.txt')
print(f"{'seed':>4} {'q(r)':>6} {'v_inf':>9}  {'ref ΔE':>10} {'off err':>9} {'armed err':>10}  {'ref ΔL':>10} {'off err':>9} {'armed err':>10}")
flips = 0
for i in sorted(off):
    q, vinf = off[i]['q'], off[i]['vinf']
    tx, sref, _ = ref_exit(off[i]['start'])
    if tx is None:
        print(f"{i:>4} {q:>6.2f} {vinf:9.2e}  reference never exits (excluded class)")
        continue
    # judge BOTH the law and the reference at the same fixed time (0.2 P): between the SOI exit
    # and 0.2 P the planet's far pull keeps changing E_h, so exit-time vs 0.2P would not cancel.
    full = rk4(off[i]['start'], 0.0, 0.2 * P, 120000, keep=2000)
    t2000 = min(full, key=lambda ts: abs(ts[0] - 0.2 * P))
    eref, lref = helio(t2000[0], t2000[1])
    e_exit, _ = helio(tx, sref)
    e0, l0 = helio(0.0, off[i]['start'])
    print(f"      [ref E_h drift exit->0.2P: {abs(eref - e_exit) / max(abs(e_exit - e0), 1e-300):.2e} of the assist]")
    dE_ref, dL_ref = eref - e0, lref - l0
    # the law's assist: its own E,L at the first probe sample past the reference exit (the
    # assist is complete there; the off and armed arms use the same sample time)
    best_t = min((t for t in ('0.2', '0.4', '0.6', '0.8', '1.0') if tx <= float(t) * P), default=None)
    cells = ['', '']
    ok = [False, False]
    for k, d in enumerate((off[i], arm[i])):
        t = best_t
        while t is not None and d.get('t' + t) is None:
            t = next((x for x in ('0.4', '0.6', '0.8', '1.0') if float(x) > float(t) and d.get('t' + x) is not None), None)
        if t is None:
            cells[k] = 'LOST'.rjust(9) + ' ' + 'LOST'.rjust(10)
            continue
        eA, lA = d['E' + t], d['L' + t]
        dE, dL = eA - e0, lA - l0
        de = abs(dE - dE_ref) / max(abs(dE_ref), 1e-300)
        dl = abs(dL - dL_ref) / max(abs(dL_ref), 1e-300)
        cells[k] = f"{de:9.2e} {dl:10.2e}"
        ok[k] = de <= 1e-2 and dl <= 1e-2
    print(f"{i:>4} {q:>6.2f} {vinf:9.2e}  {dE_ref:10.3e} {cells[0]}  {dL_ref:10.3e} {cells[1]}  {'FLIP' if False else ''}")
    if ok[0] != ok[1] and (off[i].get('t0.2') is not None or arm[i].get('t0.2') is not None):
        flips += 1
        print(f"      ^ FLIP at the 1% threshold (off pass={ok[0]}, armed pass={ok[1]})")
print(f"threshold flips (off -> armed at 1e-2): {flips}")

# ---- moons ----
def parse_moon_raw(p):
    series = {}
    for ln in open(p):
        toks = ln.split()
        if toks[0] != 'raw':
            continue
        i = int(toks[1])
        series.setdefault(i, []).append((float(toks[3]), [f(x) for x in toks[4:8]]))
    meta = {}
    for ln in open(p):
        toks = ln.split()
        if toks[0] == 'moon' and toks[1].isdigit():
            meta[int(toks[1])] = toks
    return series, meta

print()
print('== B14-class probe: apsidal precession (rad/planet-period) and class at 1.5 R_H, 10 planet periods ==')
so, mo = parse_moon_raw(sys.argv[1] + '/probe_moon_off.txt')
sa, ma = parse_moon_raw(sys.argv[1] + '/probe_moon_armed.txt')
# reproduce the probe's LCG to get each moon's exact start
rng = lcg(0x5EED_0002)
starts = {}
for i in range(8):
    a_h = 0.2 + 0.7 * rng()
    e0 = [0.0, 0.15, 0.3][i % 3]
    pro = i % 2 == 0
    phase = TAU * rng()
    a = a_h * HILL
    r = a * (1 - e0)
    v = math.sqrt(MU * (1 + e0) / r) * (1 if pro else -1)
    px, py = planet(0.0)
    pvx = -SEP * (1 - MU) * OM * 0.0
    pvy = SEP * (1 - MU) * OM * 1.0
    starts[i] = [px + r * math.cos(phase), py + r * math.sin(phase), pvx - v * math.sin(phase), pvy + v * math.cos(phase)]
print(f"{'seed':>4} {'a/H':>5} {'e0':>4} {'pro':>3}  {'rate off':>12} {'rate armed':>12} {'rate ref':>12} {'|a-off|/ref':>11} {'esc o/a/r':>10}")
for i in sorted(so):
    to, ss = zip(*so[i])
    ta, sa_ = zip(*sa[i])
    ref = rk4(starts[i], 0.0, 10 * P, 128000, keep=200)
    tr = [t for t, s in ref]
    sr = [s for t, s in ref]
    ro = apsidal_rate(to, ss)
    ra = apsidal_rate(ta, sa_)
    rr = apsidal_rate(tr, sr)
    def esc(ts, sts):
        return any(math.hypot(s[0] - planet(t)[0], s[1] - planet(t)[1]) > 1.5 * HILL for t, s in zip(ts, sts))
    eo, ea, er = esc(to, ss), esc(ta, sa_), esc(tr, sr)
    def fmt(x):
        return f"{x:12.5e}" if x is not None else "    none    "
    da = abs(ra - ro) / abs(rr) if (ra is not None and ro is not None and rr not in (None, 0)) else float('nan')
    print(f"{i:>4} {float(mo[i][2].split('=')[1][:-1]):>5.2f} {float(mo[i][3].split('=')[1]):>4.2f} {mo[i][4].split('=')[1]:>3}  {fmt(ro)} {fmt(ra)} {fmt(rr)} {da:11.2e} {str(eo)[0]}/{str(ea)[0]}/{str(er)[0]}")
