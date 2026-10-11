#!/usr/bin/env python3
"""The 10^9 budget on one 8 GB M1, decomposed into compute / bandwidth / capacity,
grounded in measured constants. Orders of magnitude only (Linux/x86 host).

Sources (all measured in this repo unless noted):
  KICK_US_RAW  = 29   us  - H0210 plane limitation ("kicks cost 29 us")
  SETUP_FRAC   = 0.92     - gold 20261006-0737-components-4643 (92% of per-kick
                            evals is window setup) -> kick floor ~2.3 us
  KICKS_ORBIT  = 32.5     - H0190 K1 (Kepler parent + Moon/Sun tides as kicks)
  AVG_FACTOR   = 114      - H0190 K2 (quadrupole averaging, first order)
  PROG_BITS    = 0.126    - gold components-98bc (smooth belt, bijective program)
  TUBE_BYTES   = 16       - law.md contract ("the 16-byte tube")
  ENC_BO       = 0.0207   - THIS RUN, steady n=1000 rho=1e-3 sigma_e=1e-2 (414 hits
                            / 20 orbits / 1000 bodies); r8 v2's 427 encounters
                            over 20 orbits on belt 0 = 0.0214 (same config, other seed)
  M1: 8 GB unified (~5 GB usable for the sim), ~60 GB/s, ~10^10 simple ops/s (board).
  Times: LEO period 5.4e3 s; belt orbit at a~1.2 (a in [1,1.5]) ~1.26 y ~ 4.0e7 s.
"""
import math

# ---- machine
GB = 1e9
USABLE = 5 * GB              # bytes the sim may hold
BANDWIDTH = 60 * GB          # bytes/s
CORE_NS = 1e9                # one core = 1e9 ns of serial work per second
M1_CORES = 4                 # performance cores (board counts ~1e10 simple ops/s)

# ---- engine constants (see docstring)
KICK_US_RAW, SETUP_FRAC = 29.0, 0.92
KICK_US_FIXED = KICK_US_RAW * (1 - SETUP_FRAC)          # 2.32 us
KICKS_ORBIT, AVG_FACTOR = 32.5, 114.0
KICKS_ORBIT_AVG = KICKS_ORBIT / AVG_FACTOR              # 0.285
PROG_BITS, TUBE_BYTES = 0.126, 16
ENC_BO = 0.0207                                          # scars/body/orbit, belt-0 config

N = 1e9
FPS = 60.0

def row(label, value, unit, cap="", margin=""):
    print(f"{label:<58}{value:>14.3g} {unit:<10}{cap:<14}{margin}")

print(f"=== 10^9 bodies on one M1: which term breaks first? ===")
print(f"(kick floor {KICK_US_FIXED:.2f} us = {KICK_US_RAW} us x (1-{SETUP_FRAC}); "
      f"averaged kicks {KICKS_ORBIT_AVG:.3f}/orbit = {KICKS_ORBIT}/{AVG_FACTOR:.0f})\n")

# ---------------- compute ----------------
print("--- COMPUTE (cores of serial event work) ---")
for name, period_s, k_orbit in [("LEO (worst)", 5.4e3, KICKS_ORBIT),
                                ("LEO averaged", 5.4e3, KICKS_ORBIT_AVG),
                                ("belt (typical)", 4.0e7, KICKS_ORBIT),
                                ("belt averaged", 4.0e7, KICKS_ORBIT_AVG)]:
    ev_s = N * k_orbit / period_s                    # kicks/s over all bodies
    for tag, us in [("today 29us", KICK_US_RAW), ("fixed 2.3us", KICK_US_FIXED)]:
        cores = ev_s * us / 1e6 / CORE_NS * CORE_NS  # us per event -> cores
        cores = ev_s * us * 1e-6
        row(f"{name}, {tag}", cores, "cores",
            f"vs {M1_CORES}", f"{cores/M1_CORES:.2g}x")
# the 190-core claim, re-derived from first principles:
leo_today = N * KICKS_ORBIT / 5.4e3 * KICK_US_RAW * 1e-6
print(f"\nBoard's 'about 190 cores' re-derived: 1e9 x 32.5/5400s x 29us = {leo_today:.0f} cores  OK")
enc_s = N * ENC_BO / 4.0e7                            # real encounters/s, fixed density
row("encounters found+judged (10k ops each, 100x rtf)", enc_s * 100 * 1e4 / 1e10, "cores",
    "vs 4", "")

# ---------------- bandwidth ----------------
print("\n--- BANDWIDTH (60 GB/s) ---")
row("events/s cap at 64 B/event", BANDWIDTH / 64, "ev/s")
row("belt events at 100x rtf (kicks avg + encounters)",
    N * (KICKS_ORBIT_AVG / 4.0e7 + ENC_BO / 4.0e7) * 100, "ev/s", "", "clears")
full_sweep = N * 64                                    # one read pass over all bodies
row("one full read pass", full_sweep / BANDWIDTH, "s")
per_frame = BANDWIDTH / FPS / N
row("bytes per body per 16.7 ms frame", per_frame, "B", "", "=> no full-sweep/frame")

# ---------------- capacity ----------------
print("\n--- CAPACITY (5 GB usable = 40 bits/body at 1e9) ---")
row("tube store (16 B/body)", N * TUBE_BYTES / GB, "GB", "vs 5 GB",
    f"{N*TUBE_BYTES/GB/5:.1f}x OVER")
row("program store (0.126 bits/body)", N * PROG_BITS / 8 / GB, "GB", "vs 5 GB",
    f"{5/(N*PROG_BITS/8/GB):.0f}x margin")
row("one pending event per body (16 B)", N * 16 / GB, "GB", "vs 5 GB",
    f"{N*16/GB/5:.1f}x OVER -> queue must be sublinear")
lookahead_orbits = 0.1
row(f"queue at {lookahead_orbits} orbit lookahead (encounters in flight)",
    N * ENC_BO * lookahead_orbits * 16 / GB, "GB", "vs 5 GB", "clears")

print("\n--- H_live: scar arithmetic at the measured belt rate ---")
scar_bits = TUBE_BYTES * 8
create_bits_bo = ENC_BO * scar_bits
row("scar bits created per body per orbit", create_bits_bo, "bits")
budget_bits = USABLE * 8 / N
row("total budget", budget_bits, "bits/body")
row("unreabsorbed scars fill the budget after", budget_bits / create_bits_bo, "orbits")
row("  ... = years of game time at a=1.2 AU", budget_bits / create_bits_bo * 1.26, "years")
row("recompile cadence to hold scars under 10% of budget",
    0.1 * budget_bits / create_bits_bo, "orbits")
row("scar creation rate at 1x rtf (belt)", N * ENC_BO / 4.0e7, "scars/s")
row("scar creation rate at 100x rtf (belt)", N * ENC_BO / 4.0e7 * 100, "scars/s")
row("bytes/s of unreabsorbed scar growth at 100x rtf",
    N * ENC_BO / 4.0e7 * 100 * TUBE_BYTES, "B/s")

# ---------------- sensitivity: what flips the verdict ----------------
print("\n--- SENSITIVITY (what must move 10x to change the verdict) ---")
print("compute: belt scale has >=4 orders of margin; LEO needs the 114x averaging")
print("         (already measured valid there) else 14 cores vs 4.")
print("bandwidth: only a per-frame full sweep breaks (64x over) -> 'no ticks' is law.")
print("capacity: breaks TODAY at 3.2x (tubes) and 3.2x (linear queue); saved only by")
print("          programs + sublinear queue + reabsorption. THE binding term.")
