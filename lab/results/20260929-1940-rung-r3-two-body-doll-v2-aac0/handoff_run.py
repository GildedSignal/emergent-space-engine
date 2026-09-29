#!/usr/bin/env python3
"""Stage 4b: 50-year handoff comparison. Reference (RK4, half-step 1e-9, restricted
exact N-body: star + planet circular + massless ship) vs patched doll.
Metric: growth exponent of heliocentric energy error across the 100 SOI crossings."""
import sys, json, math
import numpy as np
sys.path.insert(0, '.')
from r3lib import GM_STAR, GM_PLANET, SOI, kepler_prop, planet_state
from handoff_shoot import ship_deriv, rk4s

OM = 2.0 * math.pi
ic = json.load(open('handoff_ic.json'))
X0, YD0 = ic['x0'], ic['ydot0']
NYEARS = 120

# ---------------- reference with crossing events ----------------
s = [X0, 0.0, 0.0, YD0]
t = 0.0
dt = 1e-3
crossings = []            # (t, state)
inside = math.hypot(s[0] - 1.0, s[1]) < SOI
tmax = NYEARS * 1.0
while t < tmax - 1e-12:
    if t + dt > tmax:
        dt = tmax - t
    a = rk4s(s, t, dt)
    b = rk4s(rk4s(s, t, 0.5 * dt), t, 0.5 * dt)
    err = max(abs(a[i] - b[i]) for i in range(4))
    if err > 1e-9:
        dt *= 0.5
        continue
    sold = list(s)
    s = a
    t += dt
    px, py = math.cos(OM * t), math.sin(OM * t)
    d = math.hypot(s[0] - px, s[1] - py)
    if (d < SOI) != inside:
        lo, hi = 0.0, dt
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            sm = rk4s(sold, t - dt, mid)
            pxm, pym = math.cos(OM * (t - dt + mid)), math.sin(OM * (t - dt + mid))
            dm = math.hypot(sm[0] - pxm, sm[1] - pym)
            if (dm < SOI) == inside:
                lo = mid
            else:
                hi = mid
        tc = t - dt + 0.5 * (lo + hi)
        sm = rk4s(sold, t - dt, 0.5 * (lo + hi))
        crossings.append((tc, list(sm)))
        inside = not inside
    if err < 1e-11 and dt < 2e-3:
        dt *= 1.3
print("reference crossings:", len(crossings), flush=True)
if len(crossings) < 100:
    print("WARNING: fewer than 100 crossings")

# ---------------- patched doll ----------------
def run_doll(s0, tmax):
    r = (s0[0], s0[1]); v = (s0[2], s0[3]); t = 0.0
    inside = math.hypot(r[0] - 1.0, r[1]) < SOI
    ev = []
    guard = 0
    while t < tmax - 1e-12 and len(ev) < 200:
        guard += 1
        if guard > 400:
            break
        if inside:
            (px, py), (pvx, pvy) = planet_state(t)
            rr0 = (r[0] - px, r[1] - py)
            vv0 = (v[0] - pvx, v[1] - pvy)
            thi = min(0.3, tmax - t)
            while True:
                rm, vm = kepler_prop(rr0, vv0, thi, GM_PLANET)
                if math.hypot(*rm) > SOI or thi >= tmax - t - 1e-12:
                    break
                thi *= 1.5
            lo, hi = 0.0, thi
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                rm, vm = kepler_prop(rr0, vv0, mid, GM_PLANET)
                if math.hypot(*rm) < SOI:
                    lo = mid
                else:
                    hi = mid
            dtl = min(0.5 * (lo + hi), tmax - t)
            rm, vm = kepler_prop(rr0, vv0, dtl, GM_PLANET)
            t += dtl
            (px, py), (pvx, pvy) = planet_state(t)
            r = (rm[0] + px, rm[1] + py)
            inside = math.hypot(*rm) < SOI
            v = (vm[0] + pvx, vm[1] + pvy)
            t_hit = None
            tscan = 0.0
            step = 5e-4
            while tscan < tmax - t - 1e-12:
                tscan += step
                rs, vs = kepler_prop(r, v, tscan, GM_STAR)
                px, py = math.cos(OM * (t + tscan)), math.sin(OM * (t + tscan))
                if math.hypot(rs[0] - px, rs[1] - py) < SOI:
                    t_hit = tscan
                    break
            if t_hit is None:
                rs, vs = kepler_prop(r, v, tmax - t, GM_STAR)
                r, v, t = rs, vs, tmax
                break
            lo, hi = t_hit - step, t_hit
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                rs, vs = kepler_prop(r, v, mid, GM_STAR)
                px, py = math.cos(OM * (t + mid)), math.sin(OM * (t + mid))
                if math.hypot(rs[0] - px, rs[1] - py) > SOI:
                    lo = mid
                else:
                    hi = mid
            rs, vs = kepler_prop(r, v, 0.5 * (lo + hi), GM_STAR)
            r, v = rs, vs
            t += 0.5 * (lo + hi)
            inside = True
            ev.append((t, r, v))
    return ev

doll_ev = run_doll([X0, 0.0, 0.0, YD0], tmax)
print("doll crossings:", len(doll_ev), flush=True)

def E_hel(r, v):
    return 0.5 * (v[0]**2 + v[1]**2) - GM_STAR / math.hypot(*r)

n = min(len(crossings), len(doll_ev))
k = np.arange(1, n + 1)
dE = np.array([abs(E_hel(er, ev) - E_hel(cr[1], cr[1][2:])) for cr, (tr, er, ev) in
               zip(crossings[:n], doll_ev[:n])])
lam = np.polyfit(k, np.log(dE), 1)[0]
print(f"handoff_energy_growth_exponent = {lam:.4f}")
print(f"first |dE| = {dE[0]:.3e}  last = {dE[-1]:.3e}  max = {dE.max():.3e}")
json.dump({"lam": lam, "dE": dE.tolist(), "cross_t": [c[0] for c in crossings[:n]],
           "doll_t": [e[0] for e in doll_ev[:n]],
           "ref_xy": [c[1][:2] for c in crossings[:n]],
           "doll_xy": [e[1] for e in doll_ev[:n]],
           "ship_path": None}, open('handoff_data.json', 'w'))

# also store a coarse reference path for the picture
path = []
s = [X0, 0.0, 0.0, YD0]; t = 0.0; dt = 2e-3
while t < 6.0:
    s = rk4s(s, t, dt); t += dt
    path.append((s[0], s[1]))
json.dump(path, open('handoff_path6yr.json', 'w'))
print("saved handoff data")
