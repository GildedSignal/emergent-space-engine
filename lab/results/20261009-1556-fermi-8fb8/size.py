#!/usr/bin/env python3
"""Sizing: bits/body, the 10^9 verdict, and the kill boundary, from the MC laws.

Measured laws (seed 1, verified on held-out seeds by analyze.py):
  tied body   : H_A(k)     = 0.5*log2(k) + c_A,   c_A = H_A(1 rounded) ~ 4.2..5.5
  multiset    : H_mult(k)  ~ 0.25*log2(k) + c_M   (quarter-power coupling)
Constants scale with log2(sigma_1/delta): +1 bit per halving of delta or sigma_1.
"""
import json
import numpy as np

GB = 8 * 1024**3
NBODY = 10**9
BUDGET = GB * 8 / NBODY  # bits per body at 10^9 in 8 GB  (8 bytes)

LAM = 1.1          # encounters per body per orbit (r8 v2, belt 0)
TORB_GAME_S = 1e4  # game-seconds per orbit at the plane's compression (param)
D = 5              # kicked elements (a, e, i, Omega, omega)


def laws(kern="gauss"):
    rows = json.load(open(f"mc_seed1_{kern}.json"))
    k = np.array([np.log2(r["k"]) for r in rows[6:]])
    ha = np.array([r["H_A"] for r in rows[6:]])
    hm = np.array([r["H_multiset"] for r in rows[6:]])
    sa = np.polyfit(k, ha, 1)
    sm = np.polyfit(k, hm, 1)
    return {"slope_A": sa[0], "icept_A": sa[1],
            "slope_M": sm[0], "icept_M": sm[1]}


def bits_per_body(L, k, f_tie, d=D):
    tied = d * (L["slope_A"] * np.log2(k) + L["icept_A"])
    mult = d * (L["slope_M"] * np.log2(k) + L["icept_M"])
    return mult + f_tie * tied + 0.13  # + program bits


def main():
    print(f"budget: {BUDGET:.1f} bits/body (10^9 in 8 GB, counting bits)")
    L = laws("gauss")
    print(f"gauss law: H_A = {L['slope_A']:.3f}*log2k + {L['icept_A']:.2f}; "
          f"H_mult = {L['slope_M']:.3f}*log2k + {L['icept_M']:.2f}  (per element, sigma1/delta=8)")
    print(f"{'f_tie':>8} {'k=2^10':>16} {'k=2^13':>16} {'k=2^16':>16} {'k=2^20':>16}")
    for f in (1.0, 1e-1, 1e-3, 1e-6):
        cells = []
        for k in (1 << 10, 1 << 13, 1 << 16, 1 << 20):
            b = bits_per_body(L, k, f)
            cells.append(f"{b:7.1f}b {b*NBODY/8/GB:5.2f}GB")
        print(f"{f:>8} " + " ".join(cells))
    # kill boundary: all-tied (f=1) crossing the budget
    for f in (1.0, 1e-1, 1e-3):
        lo, hi = 2.0, 60.0
        for _ in range(60):
            mid = (lo * hi) ** 0.5
            if bits_per_body(L, 2 ** mid, f) > BUDGET:
                hi = mid
            else:
                lo = mid
        k = 2 ** lo
        orb = k / LAM
        print(f"f_tie={f:g}: budget crossed at k={k:.1e} encounters "
              f"({orb:.1e} orbits = {orb*TORB_GAME_S/3.15e7:.1g} game-years at T_orb=1e4 s)")
    # traffic: raw distinction creation rate at 10^9 bodies
    hk = 5.05  # measured kick-stream entropy, gauss, sigma1/delta = 8
    for torb in (1e3, 1e4):
        rate = NBODY * LAM * hk / torb / 8 / 1e6  # MB per game-second
        print(f"creation traffic at 10^9: {rate:.2f} MB/game-s (T_orb={torb:.0e} s); "
              f"retained at k=2^13: {bits_per_body(L, 1<<13, 1e-3)/ (LAM*2**13*hk)*100:.4f}%")


if __name__ == "__main__":
    main()
