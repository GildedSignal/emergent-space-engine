#!/usr/bin/env python3
# Premise probe, economics (GLM, 28 Sep 2026): position calls per second per body from
# kicks and re-anchors, scaled to a million ships in low Earth orbit. Rates are the
# measured K1/K2 numbers (glm_k1.py, glm_k2.py): K1 32.48 kicks/orbit, K2 0.285/orbit,
# LEO period 5544.6 s. A re-anchor = one element solve + one conic propagation,
# counted as ~2 position-equivalent calls (1 to 3 is the honest range). The engine
# budget is G2.5a: median 50 us per position call, so 0.3 core at 1x real time for
# 1M ships means <= 6e3 calls/s total. Python timings below are proxies only.
import math, time, os

GM_E = 3.986004418e14; R0 = 6.771e6
N0 = math.sqrt(GM_E/R0**3); P = 2.0*math.pi/N0
K1_RATE = 32.48/P          # kicks/s/body, measured
K2_RATE = 0.2853/P         # kicks/s/body, measured
CALLS_PER_ANCHOR = 2.0

def elems(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx*vx + vy*vy
    a = GM_E/(2.0*GM_E/r - v2); rv = x*vx + y*vy; q = v2 - GM_E/r
    ex = (q*x - rv*vx)/GM_E; ey = (q*y - rv*vy)/GM_E
    e = math.hypot(ex, ey); w = math.atan2(ey, ex)
    nu = math.atan2(y, x) - w
    Ea = 2.0*math.atan2(math.sqrt(1.0-e)*math.sin(0.5*nu), math.sqrt(1.0+e)*math.cos(0.5*nu))
    return a, e, w, Ea - e*math.sin(Ea)

def prop(st, t):
    a, e, w, M0, t0 = st
    M = M0 + math.sqrt(GM_E/(a*a*a))*(t - t0)
    Ea = M
    for _ in range(8): Ea -= (Ea - e*math.sin(Ea) - M)/(1.0 - e*math.cos(Ea))
    cE = math.cos(Ea); sE = math.sin(Ea)
    b = a*math.sqrt(1.0-e*e); r = a*(1.0-e*cE); g = math.sqrt(GM_E*a)/r
    xp = a*(cE-e); yp = b*sE; vxp = -g*sE; vyp = g*(b/a)*cE
    cw = math.cos(w); sw = math.sin(w)
    return xp*cw-yp*sw, xp*sw+yp*cw, vxp*cw-vyp*sw, vxp*sw+vyp*cw

# Python proxy timing: element solve + propagation (one re-anchor's arithmetic)
st = (6.771e6, 1e-7, 0.3, 0.0, 0.0)
t0 = time.time()
n = 200000
for i in range(n):
    x, y, vx, vy = prop(st, i*0.1)
    elems(x, y, vx, vy)
us = (time.time()-t0)/n*1e6
print(f"econ: Python proxy re-anchor arithmetic = {us:.1f} us (proxy only; engine target 50 us/call, Rust+certified ladder)")
for name, rate in (("K1 tides-as-kicks", K1_RATE), ("K2 averaged-tides formula", K2_RATE)):
    per_body = rate*CALLS_PER_ANCHOR
    total = per_body*1e6
    cores = total*50e-6
    print(f"econ: {name}: {rate:.2e} kicks/s/body -> {per_body:.2e} position-calls/s/body; "
          f"1M ships -> {total:.2e} calls/s -> {cores:.2f} core at 50 us/call")
print(f"econ: per ship, one kick every {1.0/K1_RATE:.0f} s (K1) / {1.0/K2_RATE:.0f} s (K2)")
print(f"econ: load={os.getloadavg()[0]:.2f}")
