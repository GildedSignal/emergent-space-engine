"""Gravity assists: 64 flybys of the moving planet, b log-uniform in
[1.5, 50] planet radii, v_inf = 10 km/s in units of sqrt(GM_star/1 AU).

Entry state (both law and reference start identically on the sphere of
influence): relative position r_rel = (R_SOI, 0), hyperbolic velocity with
impact parameter b: v_t = b v_inf / R_SOI, v_r = -sqrt(v_inf^2 + 2 mu/R_SOI
- v_t^2). Heliocentric dv = v(exit) - v(entry), each configuration at its own
exit event (first outgoing SOI crossing).
"""
import json
import math

from common import MU_PLANET, R_PLANET_AU, R_SOI, V_INF, sample_cases
from nbary import (deriv, helio_state, kepler_propagate, planet_state,
                   rk4_step)


def entry_state(b):
    v_t = b * V_INF / R_SOI
    v_r = -math.sqrt(V_INF ** 2 + 2.0 * MU_PLANET / R_SOI - v_t * v_t)
    p, pv = planet_state(0.0)
    r_ship = (p[0] + R_SOI, p[1])
    v_ship = (pv[0] + v_r, pv[1] + v_t)
    y0 = (0.0, 0.0, 0.0, 0.0, p[0], p[1], pv[0], pv[1],
          r_ship[0], r_ship[1], v_ship[0], v_ship[1])
    return y0


def run_ref_flyby(b, h_bg=2e-3, c_enc=250.0, max_t=1.0):
    y = entry_state(b)
    y_entry = tuple(y)
    t = 0.0

    def g(yy):
        return math.hypot(yy[8] - yy[4], yy[9] - yy[5]) - R_SOI

    prev = g(y)
    while t < max_t:
        d = math.hypot(y[8] - y[4], y[9] - y[5])
        h = min(h_bg, math.sqrt(d ** 3 / MU_PLANET) / c_enc)
        nxt = rk4_step(y, h)
        cur = g(nxt)
        if cur > 0 and prev <= 0 and t > 1e-9:
            lo, hi = t, t + h
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                ym = rk4_step(y, mid - t)
                if g(ym) > 0:
                    hi = mid
                else:
                    lo = mid
            yout = rk4_step(y, 0.5 * (lo + hi) - t)
            return 0.5 * (lo + hi), y_entry, yout
        y = nxt
        t += h
        prev = cur
    return None


def law_flyby(b):
    y0 = entry_state(b)
    (hx, hy), (hvx, hvy) = helio_state(y0)
    p, pv = planet_state(0.0)
    r_rel = (hx - p[0], hy - p[1])
    v_rel = (hvx - pv[0], hvy - pv[1])
    t_guess = 2.0 * R_SOI / V_INF * 3.0

    def sep(dt):
        rr, _ = kepler_propagate(r_rel, v_rel, MU_PLANET, dt)
        return math.hypot(rr[0], rr[1])

    lo, hi = 0.0, t_guess
    while sep(hi) < R_SOI:
        hi *= 1.5
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if sep(mid) > R_SOI:
            hi = mid
        else:
            lo = mid
    dt_out = 0.5 * (lo + hi)
    rr, vv = kepler_propagate(r_rel, v_rel, MU_PLANET, dt_out)
    p2, pv2 = planet_state(dt_out)
    dvx = vv[0] - v_rel[0]
    dvy = vv[1] - v_rel[1]
    return (dvx, dvy), dt_out


def main():
    _, b_rplanet = sample_cases()
    rows = []
    worst = 0.0
    for k, br in enumerate(b_rplanet):
        b = br * R_PLANET_AU
        (dv_lx, dv_ly), _ = law_flyby(b)
        out = run_ref_flyby(b)
        t_out, y_in, y_out = out
        ivx = y_in[10] - y_in[6] - 0.0
        ivy = y_in[11] - y_in[7]
        ovx = y_out[10] - y_out[6]
        ovy = y_out[11] - y_out[7]
        dv_rx, dv_ry = ovx - ivx, ovy - ivy
        err = math.hypot(dv_lx - dv_rx, dv_ly - dv_ry)
        mag = math.hypot(dv_rx, dv_ry)
        rel = err / mag
        worst = max(worst, rel)
        rows.append(dict(k=k, b_rplanet=br, dv_law=[dv_lx, dv_ly],
                         dv_ref=[dv_rx, dv_ry], rel_err=rel, t_out=t_out))
    npass = sum(1 for r in rows if r["rel_err"] <= 0.01)
    print(f"assist passes: {npass}/64, worst rel err {worst:.4f}")
    for r in rows:
        if r["rel_err"] > 0.004:
            print(f"  k={r['k']:2d} b={r['b_rplanet']:6.2f} R_p rel_err={r['rel_err']:.4f}")
    with open("assists.json", "w") as f:
        json.dump(rows, f)


if __name__ == "__main__":
    main()
