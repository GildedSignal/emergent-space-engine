#!/usr/bin/env python3
"""Extrapolation and verdict arithmetic from hlive.json (run after hlive_probe.py)."""
import json
import numpy as np

R = json.load(open("hlive.json"))
try:
    R["kicks"] = json.load(open("kicks.json"))
except FileNotFoundError:
    pass
A1 = 3.156e7          # seconds in one a=1 orbit (year), a = 1 AU around 1 Msun
RTF = 100.0           # the plane's flying speed
GB = 8.0              # goal memory
BUDGET = 4.0          # HANDOFF's approved state budget, GiB
SESSION_H = 1.0       # the approved session length, hours

print("== measured rates (events per body per a=1 orbit) ==")
for k in ("B18b_N2e3", "B18b_N1e4", "B18b_N5e4", "loE_N1e4", "r8box_mid", "r8box_lo"):
    if k not in R:
        continue
    r = R[k]["events_per_body_per_a1orbit"]
    print(f"{k:12s} N={R[k]['N']:6d} rate(1e-4)={r['1e-04']:.3e} "
          f"rate(1e-5)={r['1e-05']:.3e} slope={R[k]['b_slope']:.3f}")

# --- N scaling: rate/N should saturate (mean field) ---
print("\n== rate / N (per body per orbit per unit N) ==")
pts = [(R[k]["N"], R[k]["events_per_body_per_a1orbit"]["1e-04"]) for k in ("B18b_N2e3", "B18b_N1e4", "B18b_N5e4")]
for n, r in pts:
    print(f"  N={n:6d}: {r/n:.3e}")
exponent = (np.log(pts[2][1]) - np.log(pts[0][1])) / (np.log(pts[2][0]) - np.log(pts[0][0]))
print(f"  fitted exponent over N=2e3..5e4: {exponent:.3f}")
r_per_N = pts[2][1] / pts[2][0]     # the saturated value (largest N)
rate1e9 = r_per_N * 1e9
print(f"  extrapolated rate(rho=1e-4) at N=1e9: {rate1e9:.3e} per body per a=1 orbit")

# --- contact channel at 1e9, one belt ---
R_SHIP = 4.4e-10     # 100 m ship at a=1.5 AU (belt units)
slope = 1.0
c_per_body_per_orbit_a1 = rate1e9 * (R_SHIP / 1e-4) ** slope
print(f"\n== contacts at 1e9 in ONE B18b belt ==")
print(f"  contact rate: {c_per_body_per_orbit_a1:.3e} per body per a=1 orbit")
print(f"                {c_per_body_per_orbit_a1 * 1.84:.3e} per body per own orbit (a=1.5 AU)")
for au, name in ((1.5, "belt at 1.5 AU"), (0.05, "close-in belt at 0.05 AU")):
    P_yr = au ** 1.5
    sim_s_per_play_h = SESSION_H * 3600 * RTF
    orbits_per_h = sim_s_per_play_h / (P_yr * A1)
    ch = c_per_body_per_orbit_a1 * orbits_per_h
    print(f"  {name}: P={P_yr:.4g} yr; orbits/play-hour={orbits_per_h:.3e}; "
          f"contacts/body/hour={ch:.3e}; total/hour={ch*1e9:.3e}; "
          f"individuated fraction/hour={1-np.exp(-ch):.2%}")
    for bits in (64, 128):
        gb_per_h = ch * 1e9 * bits / 8 / 1e9
        print(f"    at {bits} bits/survivor: {gb_per_h:.3f} GiB/hour -> wall at {BUDGET} GiB: "
              f"{BUDGET/gb_per_h if gb_per_h > 0 else float('inf'):.1f} h (immortal ships, no reabsorption)")

# --- r8 anchor ---
print("\n== r8 v2 belt-0 anchor ==")
truth = 427 / (1e4 * 20)
for k in ("r8box_lo", "r8box_mid"):
    if k in R:
        r1e4 = R[k]["events_per_body_per_a1orbit"]["1e-04"]
        # rate(rho) = r(1e-4) * rho/1e-4 (slope ~1); rho implied by the truth:
        rho_impl = 1e-4 * truth / r1e4
        print(f"  {k}: rate(1e-4)={r1e4:.3e}; r8 truth {truth:.3e} implies rho={rho_impl:.2e} "
              f"(r8 box: [1e-5, 3e-4])")

# --- kicks: the quantum table ---
print("\n== kick entropy table (bits per encounter participant, b<1e-4) ==")
for name, v in R["kicks"].items():
    print(f"  {name:22s} bits={v['bits']:7.3f} subquantum={v['subquantum_frac']:.4f} n={v['n']}")
