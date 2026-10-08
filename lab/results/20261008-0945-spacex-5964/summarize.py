#!/usr/bin/env python3
"""Extrapolate measured H_live to the 8 GB / 1e9 question. Run after h_live_probe.py main."""
import json

ORBIT_GAME_H = 365.25 * 24 / 100.0     # one 1-AU orbit at rtf 100, in game-hours (87.66)
N9 = 1e9
BUDGET_BITS_PER_BODY = 8 * 8 / N9 * 1e9 # 8 GB = 64 bits/body at 1e9
MC_OVERESTIMATE = 5.24e-3 / 1.25e-3     # MC vs direct-stepped truth on belt0 (4.19x)

rows = json.load(open("h_live_results.json"))
print(f"budget at 1e9: {BUDGET_BITS_PER_BODY:.0f} bits/body; orbit = {ORBIT_GAME_H:.1f} game-h (rtf 100)")
print(f"MC rate correction (direct/MC on belt0): x{1/MC_OVERESTIMATE:.2f}\n")
for r in rows:
    name = r["scene"]
    rate = r.get("enc_rate", 0.0)
    print(f"== {name}: enc_rate MC {rate:.3e}/body/orbit -> corrected {rate/MC_OVERESTIMATE:.3e}; "
          f"kick med da/a {r.get('kick_da_med', 0):.2e}; contacts {r.get('contacts', 0)}")
    if r.get("proximity_fraction") is not None:
        print(f"   proximity: {r['proximity_fraction']*100:.1f}% of bodies have a neighbour within rho")
    for g, d in (r.get("grids") or {}).items():
        b = d["bits_per_body"]
        gb = b * N9 / 8 / 1e9
        per_h = b / ORBIT_GAME_H
        print(f"   [{g}] bits/body@100orb {b:7.3f} | touched {d['touched']*100:5.1f}% | "
              f"at 1e9: {gb:6.3f} GB | creation {per_h:.4f} bits/body/game-h "
              f"({per_h*N9/8/1e6:8.3f} MB/game-h)")
        hist = d.get("bits_hist", [])
        if hist:
            print(f"        bits over refit epochs: {[round(x,2) for x in hist]}")
