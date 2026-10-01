"""Convergence of the truth: 24 seeds (spread over a/R_H, both senses)
re-integrated at rtol=atol=1e-13 with a different sampling grid; classes and
precession rates must agree with the 1e-12 reference.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp
from common import (MU, RH, T_END, make_seeds, init_state, cr3bp,
                    rot_to_inert, osc, prec_rate, secular_z)
from cands import TS


def run(seed, rtol):
    sol = solve_ivp(cr3bp, (0.0, T_END), init_state(seed), method="DOP853",
                    rtol=rtol, atol=rtol, t_eval=TS)
    u_rot = (sol.y[0] - (1 - MU)) + 1j * sol.y[1]
    uin, vin = rot_to_inert(u_rot, sol.y[2] + 1j * sol.y[3], sol.t)
    a_os, e_os, z = osc(uin, vin)
    escaped = bool(a_os[-1] <= 0.0 or abs(u_rot[-1]) > 2.0 * RH)
    zs = secular_z(TS, z)
    trim = 40
    return escaped, prec_rate(TS[trim:-trim], zs[trim:-trim])


seeds = make_seeds()
sel = [seeds[i] for i in range(0, 256, 11)]
with open("truth.json") as f:
    truth = {r["i"]: r for r in json.load(f)}
with open("table.json") as f:
    tab = {r["i"]: r for r in json.load(f)}
bad_cls = bad_nu = 0
worst = 0.0
for s in sel:
    esc13, nu13 = run(s, 1e-13)
    if esc13 != truth[s["i"]]["escaped"]:
        bad_cls += 1
        print(f"seed {s['i']}: class differs 1e-13 vs 1e-12")
    nu12 = tab[s["i"]]["nu_truth"]
    if nu13 is not None and nu12:
        worst = max(worst, abs(nu13 - nu12) / abs(nu12))
        if abs(nu13 - nu12) > 0.1 * abs(nu12):
            bad_nu += 1
print(f"convergence: {len(sel)} seeds, class mismatches {bad_cls}, "
      f"precession mismatches {bad_nu}, worst rel nu change {worst:.2%}")
