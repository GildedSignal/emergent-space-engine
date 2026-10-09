#!/usr/bin/env python3
"""The 10^9-in-8GB budget, decomposed. Anchors: repo-measured (H0190, H0210,
components-98bc, law.md) + this run's measurements on the real engine
(`xtask universe --kick-bench`, `--bench`).  Orders of magnitude only."""
import json

# ---- anchors (repo, M1 unless said) ----
KICKS_PER_ORBIT_UNAVG = 32.5      # H0190 K1, low orbit (tides as kicks)
AVERAGING_CUT        = 114.0      # H0190 K2 (32.5 -> 0.285 kicks/orbit)
KICK_US_M1           = 29.0       # H0210 limitation line
PLANE_CADENCE        = 128        # Config::step_log2 = 7 kicks per radial period
TUBE_BYTES           = 16         # law.md
BELT_BITS_PER_BODY   = 0.126      # components-98bc (program, at 2^20)
T_LOW                = 5.4e3      # s, low orbit about an Earth
T_BELT               = 3.15e7     # s, belt body at ~1 AU (T = a^1.5 yr, a=1)
M1_CORES             = 4
M1_BYTES             = 8e9
RTF                  = 100

# ---- this run's measurements (Linux CI box, 8 vCPU shared; orders only) ----
KICK_US_BOX          = 41.8       # kick-bench median (p99 93)
EV_PER_BODY_GAME_S   = 6.1e-2     # bench @71 bodies: (736+77+667+123+6+2680+17+43)/1000 game-s / 71
EV_PER_BODY_GAME_S2  = 3.9e-2     # bench @406 bodies: (4321+8148+87)/800 / 406
BYTES_PER_BODY_SLOPE = 7.13e3     # (406*6813 - 71*5310)/335  (marginal, compiled knots)
HOT_EV_COST_US       = KICK_US_BOX  # engine per-item 20-70 us on this box

print("== 1. The board's '190 cores' re-derived from its own anchors ==")
cores = 1e9 * (KICKS_PER_ORBIT_UNAVG / T_LOW) * KICK_US_M1 * 1e-6
print(f"  1e9 x 32.5 kicks / 5400 s x 29 us = {cores:.0f} cores  (board: ~190) -> same corner:")
print(f"  unaveraged, low-orbit cadence for ALL bodies, rtf 1.")
belt_same = 1e9 * (KICKS_PER_ORBIT_UNAVG / T_BELT) * KICK_US_M1 * 1e-6
print(f"  same bodies at belt cadence instead: {belt_same:.4g} cores ({T_BELT/T_LOW:.1g}x lower).")

print("\n== 2. Measured on the real engine (this box) ==")
print(f"  kick: {KICK_US_BOX} us median (M1: 29); memo exact_hit_rate 0.0 -> nothing shared")
print(f"  hot event rate: {EV_PER_BODY_GAME_S:.1e} / {EV_PER_BODY_GAME_S2:.1e} events/game-s/body (71/406 bodies)")
print(f"  marginal live store: {BYTES_PER_BODY_SLOPE/1e3:.2f} KB/body (BodyRec+plan+cycle knots+history)")
print(f"  tube is {TUBE_BYTES} B -> materialized state is ~{BYTES_PER_BODY_SLOPE/TUBE_BYTES:.0f}x the law's number")

print("\n== 3. Hot-body capacity (the binding pair) ==")
for label, cost_us, ev in [("today, this box", KICK_US_BOX, EV_PER_BODY_GAME_S),
                           ("today, M1 kick cost", KICK_US_M1, EV_PER_BODY_GAME_S),
                           ("+ slack skin 12.6x", KICK_US_M1/12.6, EV_PER_BODY_GAME_S),
                           ("+ averaging (orbit pops only)", KICK_US_M1/12.6, EV_PER_BODY_GAME_S/AVERAGING_CUT)]:
    n = M1_CORES / (RTF * ev * cost_us * 1e-6)
    print(f"  {label:32s} N_hot(rtf100, 4 cores) ~ {n:.2e}")
for label, b in [("today 7.1 KB/body", BYTES_PER_BODY_SLOPE),
                 ("tubes only 16 B", TUBE_BYTES),
                 ("B18 floor ~4 B/body", 4.0)]:
    print(f"  memory ceiling {label:22s} {M1_BYTES/b:.2e} bodies")

print("\n== 4. Cold-body capacity (programs; the 10^9 lives here) ==")
print(f"  1e9 belt bodies as programs: {1e9*BELT_BITS_PER_BODY/8/1e6:.1f} MB")
cpu = 1e9 * (KICKS_PER_ORBIT_UNAVG/AVERAGING_CUT) / T_BELT * KICK_US_M1 * 1e-6 * RTF
print(f"  their kick CPU at rtf 100 (0.28/orbit, 29 us): {cpu:.1e} cores")
sess_orbits = 100*3600*RTF / T_BELT
print(f"  horizon bound: 100 h session at rtf 100 = {sess_orbits:.3f} belt orbits;")
print(f"  even T_Lyapunov = 1e3 orbits -> {sess_orbits/1e3:.1e} e-foldings of individual dispersion: no scar, ever.")

print("\n== 5. H_live for the plane's scene (measured composition, 71 bodies) ==")
kicks_s, enc_s, leavers_s = 736/1000, 123/1000, (17+43)/1000
bits = (kicks_s + enc_s) * 40 + leavers_s * 100   # ~log2 of the changed integer ranges
print(f"  kicks {kicks_s:.2f}/s, encounters {enc_s:.3f}/s, losses {leavers_s:.3f}/s -> ~{bits:.0f} bits/game-s")
