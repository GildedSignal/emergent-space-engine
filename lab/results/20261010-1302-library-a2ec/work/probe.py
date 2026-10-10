#!/usr/bin/env python3
"""L1 probe: cadence as a per-body certificate (Encke rectification interval)
vs a clock. Toy 2D: test particle (mu=1) on a near-circular orbit, perturbed by a
static secondary (differential tide only). Truth: RK4 fine-step.
Policies propagate the Kepler generator analytically between impulse kicks
dv = a_tide(t_event)*dt. gated-q schedules dt = sqrt(2q/a_bound), a_bound = max
|tide| over the generator orbit (128-point grid, x1.05 margin); fixed-N uses dt=T/N.
Controls: none (negative, must fail big), fixed-256 (positive, must be tiny error).
Oracle: per event, bisect the realized time for the *no-kick* generator (started
from truth at the event epoch) to drift by q; ratio realized/certified.
Run: python3 probe.py  (writes probe-out.json, <60 s per config on lab hardware)"""
import math, json, time, os

TWO_PI = 2.0 * math.pi

def kepler_state(el, dt):
    a, e, w, M0 = el
    n = a ** -1.5
    M = M0 + n * dt
    E = M
    for _ in range(10):
        E -= (E - e * math.sin(E) - M) / (1.0 - e * math.cos(E))
    ca, sa = math.cos(E), math.sin(E)
    x = a * (ca - e); y = a * math.sqrt(1.0 - e * e) * sa
    r = a * (1.0 - e * ca)
    vx = -a * a * n * sa / r; vy = a * a * n * math.sqrt(1.0 - e * e) * ca / r
    cw, sw = math.cos(w), math.sin(w)
    return (x * cw - y * sw, x * sw + y * cw, vx * cw - vy * sw, vx * sw + vy * cw)

def elements(x, y, vx, vy):
    r = math.hypot(x, y); v2 = vx * vx + vy * vy
    a = 1.0 / (2.0 / r - v2)
    if a <= 0.0:
        return None
    rv = x * vx + y * vy
    ex = (v2 - 1.0 / r) * x - rv * vx
    ey = (v2 - 1.0 / r) * y - rv * vy
    e = math.hypot(ex, ey)
    w = math.atan2(ey, ex) if e > 1e-14 else 0.0
    E = math.atan2(rv * math.sqrt(a), a - r)
    M0 = E - e * math.sin(E)
    return (a, e, w, M0)

def tide(x, y, R, ms):
    dx, dy = R - x, -y
    d3 = (dx * dx + dy * dy) ** 1.5
    return (ms * (dx / d3 - 1.0 / (R * R)), ms * dy / d3)

def a_bound(el, R, ms):
    best = 0.0
    step = TWO_PI * el[0] ** 1.5 / 128.0
    for i in range(128):
        x, y, _, _ = kepler_state(el, i * step)
        ax, ay = tide(x, y, R, ms)
        m = math.hypot(ax, ay)
        if m > best: best = m
    return best * 1.05

def truth_run(state0, R, ms, n_orb, spo):
    dt = TWO_PI / spo
    n = n_orb * spo
    x, y, vx, vy = state0
    traj = [(x, y, vx, vy)]
    app = traj.append
    for i in range(n):
        r3 = (x * x + y * y) ** 1.5
        ax1, ay1 = tide(x, y, R, ms); ax1 -= x / r3; ay1 -= y / r3
        k2x = vx + 0.5 * dt * ax1; k2y = vy + 0.5 * dt * ay1
        xm, ym = x + 0.5 * dt * vx, y + 0.5 * dt * vy
        r3m = (xm * xm + ym * ym) ** 1.5
        ax2, ay2 = tide(xm, ym, R, ms); ax2 -= xm / r3m; ay2 -= ym / r3m
        k3x = vx + 0.5 * dt * ax2; k3y = vy + 0.5 * dt * ay2
        xe, ye = x + 0.5 * dt * k2x, y + 0.5 * dt * k2y
        r3e = (xe * xe + ye * ye) ** 1.5
        ax3, ay3 = tide(xe, ye, R, ms); ax3 -= xe / r3e; ay3 -= ye / r3e
        k4x = vx + dt * ax3; k4y = vy + dt * ay3
        xf, yf = x + dt * k3x, y + dt * k3y
        r3f = (xf * xf + yf * yf) ** 1.5
        ax4, ay4 = tide(xf, yf, R, ms); ax4 -= xf / r3f; ay4 -= yf / r3f
        x += dt * (vx + 2 * k2x + 2 * k3x + k4x) / 6.0
        y += dt * (vy + 2 * k2y + 2 * k3y + k4y) / 6.0
        vx += dt * (ax1 + 2 * ax2 + 2 * ax3 + ax4) / 6.0
        vy += dt * (ay1 + 2 * ay2 + 2 * ay3 + ay4) / 6.0
        app((x, y, vx, vy))
    return traj, dt

def metrics(snaps, traj, n_orb, spo):
    de_max = dw_max = da_max = 0.0
    dw_end = de_end = 0.0
    w_prev = None
    for k in range(1, n_orb + 1):
        tx, ty, tvx, tvy = traj[k * spo]
        tel = elements(tx, ty, tvx, tvy)
        if tel is None or tel[1] >= 1.0:
            return {"escaped_at_orbit": k}
        ta, te, tw, _ = tel
        px, py, pvx, pvy = snaps[k]
        pel = elements(px, py, pvx, pvy)
        if pel is None or pel[1] >= 1.0:
            return {"policy_escaped_at_orbit": k}
        pa, pe, pw, _ = elements(px, py, pvx, pvy)
        dw = pw - tw
        if w_prev is not None:
            if dw - w_prev > math.pi: dw -= TWO_PI
            elif w_prev - dw > math.pi: dw += TWO_PI
        w_prev = dw
        de, da = pe - te, pa - ta
        de_max = max(de_max, abs(de)); dw_max = max(dw_max, abs(dw)); da_max = max(da_max, abs(da))
        de_end, dw_end = de, dw
    return {"de_max": de_max, "dw_max_deg": math.degrees(dw_max), "da_max": da_max,
            "dw_end_deg_per_orb": math.degrees(dw_end) / n_orb, "de_end": de_end}

def run_policy(el0, R, ms, n_orb, T, q, per_orb, kind, traj=None, fine_dt=None):
    el, t = el0, 0.0
    snaps, ratios, events, escaped = {}, [], 0, False
    while t < n_orb * T:
        if kind == "fixed":
            dt = T / per_orb
        else:
            dt = math.sqrt(2.0 * q / a_bound(el, R, ms))
        x, y, vx, vy = kepler_state(el, dt)
        ax, ay = tide(x, y, R, ms)
        vx += ax * dt; vy += ay * dt
        if traj is not None:
            i0 = min(len(traj) - 1, int(round(t / fine_dt)))
            gel = elements(*traj[i0])
            if gel is not None and gel[1] < 1.0:
                def dev(tt, i0=i0, gel=gel):
                    gx, gy, _, _ = kepler_state(gel, tt)
                    j = i0 + tt / fine_dt
                    j0 = min(len(traj) - 1, int(j)); frac = j - j0
                    j1 = min(len(traj) - 1, j0 + 1)
                    rx = traj[j0][0] + frac * (traj[j1][0] - traj[j0][0])
                    ry = traj[j0][1] + frac * (traj[j1][1] - traj[j0][1])
                    return math.hypot(gx - rx, gy - ry) - q
                lo, hi = 0.0, 2.0 * dt
                if dev(hi) >= 0:
                    for _ in range(25):
                        mid = 0.5 * (lo + hi)
                        if dev(mid) < 0: lo = mid
                        else: hi = mid
                    ratios.append(hi / dt)
                else:
                    ratios.append(2.0)
        nxt = elements(x, y, vx, vy)
        if nxt is None or nxt[1] >= 1.0:
            escaped = True; break
        el = nxt
        t += dt
        events += 1
        k = int(math.floor(t / T + 1e-9))
        if 1 <= k <= n_orb and k not in snaps:
            snaps[k] = kepler_state(el, k * T - t)
    last_k = max(snaps) if snaps else 0
    for k in range(1, n_orb + 1):
        if k not in snaps and k - 1 in snaps:
            st = snaps[k - 1]
            snaps[k] = kepler_state(elements(*st), T)
            last_k = k
    for k in range(1, n_orb + 1):
        if k not in snaps: snaps[k] = kepler_state(el, k * T - t)
    return snaps, events / n_orb, ratios, escaped

def main():
    out, t_start = {}, time.time()
    for cfg, R, ms in [("A_R3_ms0.01", 3.0, 0.01), ("B_R1.5_ms0.03", 1.5, 0.03),
                       ("B2_R2_ms0.02", 2.0, 0.02), ("B3_R2.2_ms0.012", 2.2, 0.012), ("B4_R2.6_ms0.01", 2.6, 0.010)]:
        n_orb, spo, T, q = 200, 4096, TWO_PI, 2e-4
        el0 = (1.0, 0.05, 0.0, 0.0)
        tw = time.time()
        traj, fine_dt = truth_run(kepler_state(el0, 0.0), R, ms, n_orb, spo)
        res = {"truth_s": round(time.time() - tw, 1), "n_orb": n_orb, "q": q}
        snaps_none = {k: kepler_state(el0, k * T) for k in range(1, n_orb + 1)}
        res["none"] = {**metrics(snaps_none, traj, n_orb, spo), "kicks_per_orbit": 0.0}
        for pol, kw in [("fixed_256", dict(kind="fixed", per_orb=256)),
                        ("fixed_32", dict(kind="fixed", per_orb=32)),
                        ("fixed_8", dict(kind="fixed", per_orb=8)),
                        ("gated_q", dict(kind="gated", per_orb=None))]:
            snaps, kpo, ratios, esc = run_policy(el0, R, ms, n_orb, T, q,
                                                 traj=traj if pol == "gated_q" else None,
                                                 fine_dt=fine_dt, **kw)
            m = metrics(snaps, traj, n_orb, spo)
            m["kicks_per_orbit"] = kpo
            if esc: m["escaped"] = True
            if ratios:
                rs = sorted(ratios)
                m["oracle_over_certified_median"] = rs[len(rs) // 2]
                m["oracle_over_certified_p10"] = rs[len(rs) // 10]
                m["oracle_censored_frac"] = sum(1 for r in rs if r >= 2.0) / len(rs)
            res[pol] = m
        out[cfg] = res
        json.dump(out, open(os.path.join(os.path.dirname(__file__), "probe-out.json"), "w"), indent=1)
        print(f"== {cfg} truth={res['truth_s']}s")
        for pol, m in res.items():
            if pol in ("truth_s", "n_orb", "q") or m is None: continue
            if "escaped_at_orbit" in m or "policy_escaped_at_orbit" in m:
                print(f"  {pol:10s} ESCAPED: {m}"); continue
            extra = (f" oracle/cert med={m['oracle_over_certified_median']:.2f}"
                     f" p10={m['oracle_over_certified_p10']:.2f}"
                     f" cen={m['oracle_censored_frac']:.2f}") if "oracle_over_certified_median" in m else ""
            print(f"  {pol:10s} kicks/orb={m['kicks_per_orbit']:8.2f} de_max={m['de_max']:.2e}"
                  f" dw_max={m['dw_max_deg']:9.3f} deg da_max={m['da_max']:.2e}"
                  f" dw/orb={m['dw_end_deg_per_orb']:8.4f} deg{extra}")
    out["_wall_s"] = round(time.time() - t_start, 1)
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "probe-out.json"), "w"), indent=1)
    print("wall", out["_wall_s"], "s")

if __name__ == "__main__":
    main()
