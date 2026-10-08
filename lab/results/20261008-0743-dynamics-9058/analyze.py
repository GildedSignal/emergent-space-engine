#!/usr/bin/env python3
"""Analyze cadence sweep: growth exponents (B12-style), bounded amplitudes, drift rates."""
import glob, os
import numpy as np

rows = []
for path in sorted(glob.glob("data/*.csv")):
    name = os.path.basename(path)[:-4]
    d = np.genfromtxt(path, delimiter=",", names=True, skip_header=0)
    t = d["t_jup"]; cj = d["cj_err"]; ee = d["e_err"]; pom = d["pom_err"]; truth = d["cj_truth_drift"]
    lo = max(2, len(t) // 10)  # last decade
    def slope(y):
        y = np.maximum(y, 1e-300)
        sl = np.polyfit(np.log10(t[lo:]), np.log10(y[lo:]), 1)[0]
        return sl
    # unwrap pom error for a drift-rate fit (rad per Jup orbit)
    dp = np.diff(pom); dp = (dp + np.pi) % (2 * np.pi) - np.pi
    pomu = np.concatenate([[pom[0]], pom[0] + np.cumsum(dp)])
    rate = np.polyfit(t[lo:], pomu[lo:], 1)[0]
    rows.append(dict(name=name, exp_cj=slope(cj), exp_e=slope(ee),
                     max_cj=np.max(cj[lo:]), max_e=np.max(ee[lo:]),
                     pom_rate=rate, truth_floor=np.max(truth)))

hdr = f"{'run':<22}{'exp_CJ':>7}{'exp_e':>7}{'max_CJ':>10}{'max_e':>10}{'pom_rate':>10}{'truth':>9}"
print(hdr); print("-" * len(hdr))
for r in sorted(rows, key=lambda r: r["name"]):
    print(f"{r['name']:<22}{r['exp_cj']:>7.2f}{r['exp_e']:>7.2f}{r['max_cj']:>10.2e}"
          f"{r['max_e']:>10.2e}{r['pom_rate']:>10.2e}{r['truth_floor']:>9.1e}")
