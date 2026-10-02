#!/usr/bin/env python3
"""JANUS-style integer reversibility on the changeover (run 20261001-2353-q-changeover-e04a).

Question (the lens): may the switch depend on the state without breaking reversibility?

Integer core: DKD with constant-velocity drifts, H = P/512 (fine enough that the base
map's Jacobi error is bounded far below the switching effects; the WH Kepler drift is
replaced by free flight so every map is an exact integer map -- JANUS proper uses the WH
split; the changeover argument is independent of the drift's form). Positions q in units
of sep/2^44, momenta p in units of (sep/2^44) per half-step. Kick impulses are
round(c * f(q)) with f evaluated in float from exact integer q. Every branch decision is
made at the step's symmetric mid-state, where the backward (p-flip) run sees the same
positions. Reversal = JANUS's own test: negate momenta, run the same code, negate again,
compare bit for bit.

Laws (same core, same forces, only the switching differs):
  smooth    the SyMBA weights of the separation (position-only, no branch: one law).
  heaviside a position-only selector between two different maps: outside 1 R_H the
            planet impulse is applied once at the mid-state (map A); inside, it is
            split into two half-impulses at 1/4 and 3/4 of the interval (map B).
            Both maps are exact integer maps and individually p-flip symmetric.
  radial    the same selector, but it also requires the pair to be approaching
            (dot(rel v, rel x) < 0): a velocity-dependent branch.
"""
import math, json

LQ = 2.0 ** -44
MU = 1e-3
GMS = 1.0 - MU
P = 2.0 * math.pi
RH = (MU / 3.0) ** (1.0 / 3.0)
SOI = MU ** 0.4
NST = 512
H = P / NST
HQ = H / 2
CK = int(round(H * HQ / LQ))   # DKD full-step kick: dv = a*H -> dp = a*H*HQ/LQ
SH = [SOI * 2.0 ** (1 - l) for l in range(4)]
SC = 2.0 ** 44   # planet position in integer quanta

def planet_rel(q0, q1, t):
    px, py = math.cos(t) * SC, math.sin(t) * SC
    return (q0 - px) * LQ, (q1 - py) * LQ

def planet_force(q0, q1, t):
    dx, dy = planet_rel(q0, q1, t)
    r = math.hypot(dx, dy)
    return (-MU * dx / r ** 3, -MU * dy / r ** 3)

def star_force(q0, q1):
    r = math.hypot(q0, q1) * LQ
    return (-GMS * q0 * LQ / r ** 3, -GMS * q1 * LQ / r ** 3)

def Bfun(r, l):
    y = (r - SH[l] * 0.5) / (SH[l] * 0.5)
    return 0.0 if y <= 0 else (1.0 if y >= 1 else y * y * (3 - 2 * y))

def Wfun(r, l, L=4):
    w = 1.0
    for i in range(min(l, L)):
        w *= 1.0 - Bfun(r, i)
        if w == 0.0:
            return 0.0
    if l < L:
        w *= Bfun(r, l)
    return w

def depth(r):
    vmax = 1.0   # position-only reach bound (fixed constant, no velocity)
    d = 0
    for l in range(4):
        if r < SH[l] + vmax * H:
            d = l + 1
    return d

def kick_imp(q, t, w):
    """Total impulse (star+planet shares scaled by w for the planet) at integer q, time t."""
    sx, sy = star_force(q[0], q[1])
    px, py = planet_force(q[0], q[1], t)
    return (int(round(CK * sx)), int(round(CK * sy)),
            int(round(CK * w * px)), int(round(CK * w * py)))

def step(law, q, t, sign, state):
    """One DKD interval forward (sign=+1) or with flipped momenta (sign=-1).
    All branch decisions are made on q at the mid-state (identical in both directions)."""
    q = list(q)
    if sign < 0:
        q[2], q[3] = -q[2], -q[3]
    # drift half
    q[0] += q[2]; q[1] += q[3]
    tm = t + H / 2
    r = math.hypot(*planet_rel(q[0], q[1], tm))
    if law == "smooth":
        for l in range(depth(r) + 1):
            w = Wfun(r, l)
            if w == 0.0:
                continue
            kx, ky, jx, jy = kick_imp(q, tm, w / 4 ** l)
            # all layers fire at the mid-state with their time share h_l = H/4^l
            q[2] += jx; q[3] += jy
            state["events"] += 1 if l >= 1 else 0
        kx, ky, _, _ = kick_imp(q, tm, 0.0)
        q[2] += kx; q[3] += ky
    elif law == "heaviside":
        if r >= RH:   # map A: one planet impulse at mid
            kx, ky, jx, jy = kick_imp(q, tm, 1.0)
            q[2] += kx + jx; q[3] += ky + jy
        else:         # map B: star at mid (planet at start time t, a different map)
            kx, ky, _, _ = kick_imp(q, tm, 0.0)
            q[2] += kx; q[3] += ky
            fx, fy = planet_force(q[0], q[1], t)
            q[2] += int(round(CK * fx)); q[3] += int(round(CK * fy))
            state["events"] += 1
    else:  # radial: velocity-dependent branch
        dx, dy = planet_rel(q[0], q[1], tm)
        vx, vy = q[2] * LQ / HQ, q[3] * LQ / HQ
        pvx, pvy = -math.sin(tm), math.cos(tm)
        approaching = dx * (vx - pvx) + dy * (vy - pvy) < 0
        if approaching and r < RH:
            kx, ky, _, _ = kick_imp(q, tm, 0.0)
            fx, fy = planet_force(q[0], q[1], t)
            q[2] += kx + int(round(CK * fx)); q[3] += ky + int(round(CK * fy))
        else:
            kx, ky, jx, jy = kick_imp(q, tm, 1.0)
            q[2] += kx + jx; q[3] += ky + jy
    # drift half
    q[0] += q[2]; q[1] += q[3]
    if sign < 0:
        q[2], q[3] = -q[2], -q[3]
    return q

def jacobi(q, t):
    x, y = q[0] * LQ, q[1] * LQ
    vx, vy = q[2] * LQ / HQ, q[3] * LQ / HQ
    px, py = math.cos(t), math.sin(t)
    r1 = math.hypot(x, y); r2 = math.hypot(x - px, y - py)
    return 0.5 * (vx * vx + vy * vy) - GMS / r1 - MU / r2 - (x * vy - y * vx)

def run(law, q0, nsteps=60000):
    st = {"events": 0}
    q = list(q0)
    c0 = jacobi(q, 0.0)
    worst = 0.0
    for k in range(nsteps):
        q = step(law, q, k * H, +1, st)
        if k % 8 == 0:
            worst = max(worst, abs((jacobi(q, (k + 1) * H) - c0) / c0))
    qf = list(q)
    # JANUS reversal: flip momenta, run the same code, flip back
    for k in range(nsteps - 1, -1, -1):
        q = step(law, q, k * H, -1, st)
    rev = q == list(q0)
    return rev, worst, st["events"], qf

if __name__ == "__main__":
    out = {}
    a = 1.0 + 2 * RH
    e = 0.08
    p_ = a * (1 - e * e)
    r0 = p_ / (1 + e)              # periapsis start
    hh = math.sqrt(GMS * p_)
    vpr = hh / r0
    q0 = [int(round(r0 / LQ)), 0, 0, int(round(vpr * HQ / LQ))]
    for law in ["smooth", "heaviside", "radial"]:
        rev, worst, nev, qf = run(law, q0)
        out[law] = dict(bit_reversible=rev, worst_rel_jacobi=worst, events=nev)
        print(f"{law:9s} p-flip retrace={rev}  worst|dC/C|={worst:.2e}  switch events={nev}")
    json.dump(out, open("janus.json", "w"), indent=1)
