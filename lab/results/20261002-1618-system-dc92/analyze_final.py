#!/usr/bin/env python3
"""Final analysis: consumes results-ctl.json, results-main.json,
results-decisive.json. (Supersedes the analyze.py of the same folder, which
assumed -- wrongly -- that the recorded rmax was the apoapsis.)"""
import json, math, sys
import numpy as np
from scipy.integrate import quad

def schw_advance(M, rmin, rmax):
    g = lambda r: 1 - 2 * M / r
    A = g(rmin) / (rmin * rmin); B = g(rmax) / (rmax * rmax)
    L2 = (g(rmin) - g(rmax)) / (B - A)
    E2 = g(rmin) * (1 + L2 / (rmin * rmin))
    L = math.sqrt(L2)
    V = lambda r: E2 - g(r) * (1 + L2 / (r * r))
    f = lambda r: L / (r * r) / math.sqrt(max(V(r), 1e-300))
    phi = 2 * quad(f, rmin, rmax, points=[rmin, rmax], limit=400)[0]
    return phi - 2 * math.pi

d = json.load(open("results-decisive.json"))
r, n = d["river"], d["newtonian"]
a = (r["rmin"] + r["rmax"]) / 2
e = (r["rmax"] - r["rmin"]) / (r["rmax"] + r["rmin"])
p = a * (1 - e * e)
gr = r["slope_peri"] - n["slope_peri"]
monopole_1pn = 6 * math.pi * 0.03 / p
monopole_exact = schw_advance(0.03, r["rmin"], r["rmax"])
out = dict(
    realized=dict(a=a, e=e, p=p),
    river_slope=r["slope_peri"], river_slope_apo=r["slope_apo"],
    newtonian_slope=n["slope_peri"], newtonian_slope_apo=n["slope_apo"],
    GR_correction=gr,
    monopole_1pn=monopole_1pn, monopole_exact_allPN=monopole_exact,
    excess_over_monopole=gr - monopole_exact,
    ratio_gr_over_1pn=gr / monopole_1pn,
    orbit_shape=dict(river_rmin=r["rmin"], newtonian_rmin=n["rmin"],
                     river_rmax=r["rmax"], newtonian_rmax=n["rmax"]),
    drift_diagnostics=dict(dE_max=r["dE_max"], dL_max=r["dL_max"],
                           note="dL 7.5% of L: ray-selection outliers; "
                                "slope noise ~0.05 rad (apo-vs-peri spread)"),
)
print(json.dumps(out, indent=1, default=float))
json.dump(out, open("analysis-final.json", "w"), indent=1, default=float)
