#!/usr/bin/env python3
"""The 10^9 budget, one law: events/wall-second = N * e * R / P.

cores_needed = N * e * (R/P) * t_event   (1 core delivers 1 core-second per wall second)
bandwidth    = events/wall-s * bytes_touched (M1 ~60 GB/s)
memory       = programs + tubes + scars <= 4 GiB state budget (8 GB unified minus OS/GPU/app)

Measured anchors (this box, 2026-10-11 06:20 UTC, load 0.1, 8 vCPU x86; OoM only):
  t_event today (plane kick/item resolves): ship 69 us, fleet 18-25 us -> t_today = 30e-6 s
  t_event target (memo hit: table + queue): 0.1-0.3 us               -> t_hit  = 0.2e-6 s
  10^9-ship scene RSS: 106 MB = 0.85 bit/ship; density view 25-37 ms/frame on 3.9 cores
  M1 envelope (board): ~1e10 simple ops/s across cores, ~60 GB/s, 8 GB unified.

Scene rows: (fraction of 10^9, period P in simulated seconds, events per orbit e).
e = kicks/orbit + encounters/orbit. H0190: 32 kicks (0.3 averaged). r8 v2: 1.1 encounters/body/orbit.
R = rtf = simulated seconds per wall second (game speed).
"""
M1_CORES = 4.0
BW_GB_S = 60.0
BYTES_TOUCHED = 96  # tube 16 B + queue entry + memo line, OoM


def row(name, frac, P, e, R, t_event, N=1e9):
    n = N * frac
    rate = n * e * R / P          # events per wall second
    cores = rate * t_event        # core-seconds per wall second = cores
    bw = rate * BYTES_TOUCHED / 1e9
    verdict = "OK" if cores <= M1_CORES else f"OVER x{cores/M1_CORES:.0f}"
    if bw > BW_GB_S:
        verdict += f" +BW x{bw/BW_GB_S:.0f}"
    print(f"{name:38s} rate={rate:9.3g}/s cores={cores:9.3g}  bw={bw:7.2f} GB/s  {verdict}")


print(f"{'scene (N=1e9)':38s} {'events/wall-s':>14s} {'M1 cores':>10s} {'mem-bw':>9s}")
print("--- t_event = 30 us (measured today: a kick resolves a recompile) ---")
row("belt P=5.2yr, e=1.4, R=100", 1.0, 1.6e8, 1.4, 100, 30e-6)
row("all in hour orbits, e=1.4, R=100", 1.0, 5.4e3, 1.4, 100, 30e-6)
row("190-cores scene: P=5.4e3s, e=32, R=1", 1.0, 5.4e3, 32, 1, 30e-6)
print("--- t_event = 0.2 us (memo hit: the law's intended kick) ---")
row("belt P=5.2yr, e=1.4, R=100", 1.0, 1.6e8, 1.4, 100, 0.2e-6)
row("all in hour orbits, e=1.4, R=100", 1.0, 5.4e3, 1.4, 100, 0.2e-6)
row("190-cores scene: P=5.4e3s, e=32, R=1", 1.0, 5.4e3, 32, 1, 0.2e-6)
row("worst case: e=32, P=5.4e3s, R=100", 1.0, 5.4e3, 32, 100, 0.2e-6)

print("\n--- the M1 event ceiling (compute and bandwidth cross) ---")
for t in (30e-6, 1e-6, 0.2e-6):
    c, b = M1_CORES / t, BW_GB_S * 1e9 / BYTES_TOUCHED
    print(f"t_event={t*1e6:5.1f} us: compute ceiling {c:.3g}/s, bandwidth ceiling {b:.3g}/s -> {min(c,b):.3g} events/s")

print("\n--- memory: the scar budget at 1e9 ---")
state_bits = 4 * 2**30 * 8
per_ship = state_bits / 1e9
prog_bits = 0.85
print(f"state budget {per_ship:.0f} bits/ship; programs measured {prog_bits:.2f} b ({100*prog_bits/per_ship:.1f}%); scars get {per_ship-prog_bits:.0f} bits/ship")
for scar_bits in (8, 32, 128):
    print(f"scar {scar_bits:3d} b -> {(per_ship-prog_bits)*1e9/scar_bits:.2g} scars = {(per_ship-prog_bits)/scar_bits:.2f} per body per session")
orbit_wall_h = 1.6e8 / 100 / 3600
print(f"belt orbit at rtf 100 = {orbit_wall_h:.0f} wall-hours; every body scars once per orbit (32 b):")
print(f"  session ends after {(per_ship-prog_bits)/32/1.1:.1f} orbits = {(per_ship-prog_bits)/32/1.1*orbit_wall_h:.0f} wall-hours")
print(f"  3% of encounters scar: {(per_ship-prog_bits)/32/(1.1*0.03):.0f} orbits = {(per_ship-prog_bits)/32/(1.1*0.03)*orbit_wall_h/24:.0f} wall-days")
