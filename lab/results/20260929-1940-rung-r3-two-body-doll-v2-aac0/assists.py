#!/usr/bin/env python3
"""Stage 3: gravity assists. 64 flybys of the moving planet; doll vs N-body reference.
dv is heliocentric v(T_END) - v(0) at MATCHED epochs (T_END = 0.25 yr), so the
comparison isolates the flyby treatment rather than the sun's arc bending."""
import sys, json, math, random
import numpy as np
sys.path.insert(0, '.')
from r3lib import (GM_STAR, GM_PLANET, SOI, R_EARTH_AU, PLANET_OMEGA, kepler_prop,
                   planet_state, rk4)

D0 = 0.05          # AU, start distance from planet (far field)
T_END = 0.25       # yr, matched final epoch (flyby over by ~0.14)
VINF = 0.633       # AU/yr ~ 3 km/s, planet-relative approach speed along -x

rng = random.Random(20261002)
bvals = []
for i in range(64):
    b = math.exp(rng.uniform(math.log(1.5), math.log(50.0))) * R_EARTH_AU
    bvals.append(b if i % 2 == 0 else -b)   # alternate leading/trailing side


def reference(r0_rel, v0_rel):
    (px, py), (pvx, pvy) = planet_state(0.0)
    s = [0.0, 0.0, px, py, px + r0_rel[0], py + r0_rel[1],
         0.0, 0.0, pvx, pvy, pvx + v0_rel[0], pvy + v0_rel[1]]
    t = 0.0
    dt = 1e-3
    trace = []
    prevd = math.hypot(*r0_rel)
    inside = False
    while t < T_END - 1e-12:
        dt = min(dt, T_END - t)
        a = rk4(s, dt)
        b2 = rk4(rk4(s, 0.5 * dt), 0.5 * dt)
        err = max(abs(a[i] - b2[i]) for i in range(12))
        if err > 1e-9:
            dt *= 0.5
            continue
        sold = list(s)
        s = a
        t += dt
        d = math.hypot(s[4] - s[2], s[5] - s[3])
        if (d < SOI) != inside:
            lo, hi = 0.0, dt
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                sm = rk4(sold, mid)
                dm = math.hypot(sm[4] - sm[2], sm[5] - sm[3])
                if (dm < SOI) == inside:
                    lo = mid
                else:
                    hi = mid
            sm = rk4(sold, 0.5 * (lo + hi))
            trace.append((t - dt + 0.5 * (lo + hi), list(sm)))
            inside = not inside
        if err < 1e-11 and dt < 2e-3:
            dt *= 1.4
    v_start = (pvx + v0_rel[0], pvy + v0_rel[1])
    return v_start, (s[10], s[11]), trace


def doll(r0_rel, v0_rel):
    t = 0.0
    (px, py), (pvx, pvy) = planet_state(t)
    r = (px + r0_rel[0], py + r0_rel[1])
    v = (pvx + v0_rel[0], pvy + v0_rel[1])
    v_start = v
    inside = math.hypot(*r0_rel) < SOI

    def dist_rel(rr, tt):
        (qx, qy), _ = planet_state(tt)
        return math.hypot(rr[0] - qx, rr[1] - qy)

    legs = 0
    while t < T_END - 1e-12:
        if inside:
            legs += 1
            (qx, qy), (qvx, qvy) = planet_state(t)
            rr0 = (r[0] - qx, r[1] - qy)
            vv0 = (v[0] - qvx, v[1] - qvy)
            thi = min(0.2, T_END - t)
            while True:                        # bracket the exit
                rm, vm = kepler_prop(rr0, vv0, thi, GM_PLANET)
                if math.hypot(*rm) > SOI or thi > T_END - t - 1e-12:
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
            dtl = min(0.5 * (lo + hi), T_END - t)
            rm, vm = kepler_prop(rr0, vv0, dtl, GM_PLANET)
            t += dtl
            (qx, qy), (qvx, qvy) = planet_state(t)
            r = (rm[0] + qx, rm[1] + qy)
            v = (vm[0] + qvx, vm[1] + qvy)
            inside = math.hypot(*rm) < SOI
        else:
            # star-doll leg to SOI entry or to T_END, whichever first
            t_hit = None
            tscan = 0.0
            step = 2e-3
            while tscan < T_END - t - 1e-12:
                tscan += step
                rs, vs = kepler_prop(r, v, tscan, GM_STAR)
                if dist_rel(rs, t + tscan) < SOI:
                    t_hit = tscan
                    break
            if t_hit is None:
                rs, vs = kepler_prop(r, v, T_END - t, GM_STAR)
                r, v = rs, vs
                t = T_END
                break
            lo, hi = t_hit - step, t_hit
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                rs, vs = kepler_prop(r, v, mid, GM_STAR)
                if dist_rel(rs, t + mid) > SOI:
                    lo = mid
                else:
                    hi = mid
            rs, vs = kepler_prop(r, v, 0.5 * (lo + hi), GM_STAR)
            r, v = rs, vs
            t += 0.5 * (lo + hi)
            inside = True
    return v_start, v, legs


results = []
for _ib, b in enumerate(bvals):
    if _ib % 8 == 0: print("seed", _ib, flush=True)
    r0_rel = (D0, -b)
    v0_rel = (-VINF, 0.0)
    v_s_r, v_e_r, trace = reference(r0_rel, v0_rel)
    dv_ref = (v_e_r[0] - v_s_r[0], v_e_r[1] - v_s_r[1])
    v_s_d, v_e_d, nleg = doll(r0_rel, v0_rel)
    dv_dol = (v_e_d[0] - v_s_d[0], v_e_d[1] - v_s_d[1])
    err = math.hypot(dv_dol[0] - dv_ref[0], dv_dol[1] - dv_ref[1]) / math.hypot(*dv_ref)
    # planet-relative turn angle from the reference trace
    if len(trace) >= 2:
        vin = (trace[0][1][10] - trace[0][1][8], trace[0][1][11] - trace[0][1][9])
        vout = (trace[1][1][10] - trace[1][1][8], trace[1][1][11] - trace[1][1][9])
        sp = (vin[0] * vout[0] + vin[1] * vout[1]) / (math.hypot(*vin) * math.hypot(*vout))
        turn = math.degrees(math.acos(max(-1.0, min(1.0, sp))))
    else:
        turn = float('nan')
    results.append(dict(b=abs(b), err=err, dv_ref=math.hypot(*dv_ref), turn=turn, legs=nleg))

errs = np.array([r['err'] for r in results])
babs = np.array([r['b'] for r in results])
turns = np.array([r['turn'] for r in results])
print(f"assist_pass_fraction = {(errs <= 0.01).mean():.4f}")
print(f"median err = {np.median(errs):.3e}  max = {errs.max():.3e} at b/R_E = {babs[errs.argmax()]/R_EARTH_AU:.1f}")
print(f"turn angles: {np.nanmin(turns):.1f} to {np.nanmax(turns):.1f} deg")
print(f"|dv_ref| range: {np.array([r['dv_ref'] for r in results]).min():.3f} to {np.array([r['dv_ref'] for r in results]).max():.3f} AU/yr")
json.dump(results, open('assists.json', 'w'), indent=0)
