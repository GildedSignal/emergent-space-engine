"""Scan for a regular 2:1 resonant transfer: 100 SOI crossings, gentle
conjunctions, reference reproducible to 1e-9 (regularity check via half-step).

Ship: interior 2:1 ellipse, a_s = 2^(-2/3), apoapsis r_apo = 1 - d_r, started
at apoapsis at longitude theta_a (behind the planet at longitude 0). The
planet catches the ship near apoapsis once per planet period.
"""
import math

from common import MU_PLANET, R_SOI
from nbary import deriv, rk4_step

A_S = 2.0 ** (-2.0 / 3.0)


def initial_state(d_r, theta_a):
    r_apo = 1.0 - d_r
    e = r_apo / A_S - 1.0
    v_apo = math.sqrt(2.0 / r_apo - 1.0 / A_S)
    r0 = (r_apo * math.cos(theta_a), r_apo * math.sin(theta_a))
    v0 = (v_apo * -math.sin(theta_a), v_apo * math.cos(theta_a))
    return r0, v0, e


def scan_point(d_r, theta_a, t_end, h_bg=0.002, c_enc=120.0):
    r0, v0, e = initial_state(d_r, theta_a)
    y = (0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, r0[0], r0[1], v0[0], v0[1])
    t = 0.0
    prev = math.hypot(r0[0] - 1.0, r0[1]) - R_SOI
    crossings = 0
    min_d = 1e9
    t_first100 = None
    while t < t_end:
        d = math.hypot(y[8] - y[4], y[9] - y[5])
        h = min(h_bg, math.sqrt(d ** 3 / MU_PLANET) / c_enc)
        y = rk4_step(y, h)
        t += h
        d = math.hypot(y[8] - y[4], y[9] - y[5])
        min_d = min(min_d, d)
        cur = d - R_SOI
        if (cur > 0) != (prev > 0):
            crossings += 1
            if crossings == 100:
                t_first100 = t
        prev = cur
    return crossings, t_first100, min_d


if __name__ == "__main__":
    import sys
    t_end = float(sys.argv[1]) if len(sys.argv) > 1 else 20 * 2 * math.pi
    for d_r in (0.002, 0.003, 0.004, 0.005):
        for theta_a in (-0.02, -0.05, -0.1, -0.2):
            c, tf, md = scan_point(d_r, theta_a, t_end)
            print(f"d_r={d_r:.3f} theta_a={theta_a:+.2f}: crossings={c:3d} "
                  f"t100={tf if tf is None else round(tf,1)} min_d/R_SOI={md/R_SOI:.3f}")
