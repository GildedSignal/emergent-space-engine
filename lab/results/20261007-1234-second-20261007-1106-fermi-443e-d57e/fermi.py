#!/usr/bin/env python3
"""The 10^9 budget from measured anchors (run: python3 fermi.py).

Anchors measured in this run (Linux x86 cloud box; orders of magnitude only):
  bits/event     ~104 (varint, zlib-incompressible; median 20 bits x 4 components)
  residual/body   ~84 bits mean (4 components x ~21), bounded: late/early = 1.09-1.20 over 1 h
  events/body/s   0.010-0.018 at the plane's inner scale (ships on hours-days orbits)
  bytes/body      9846 as held today (tube + residual + compiled trajectory + history)
  settle wall     0.23 s for 3600 game-s, 28 bodies, 3491 events -> <=66 us/event
Machine (M1, from HANDOFF): 8 GB, ~1e10 simple ops/s, ~60 GB/s.
"""
B = 8e9  # bytes
OPS = 1e10
BW = 60e9  # B/s
N = 1e9

bits_event = 104.0
rate_inner = 0.014  # events/body/game-s, measured
resid_body = 84.0  # bits live per body, measured

def period_au(a):  # game seconds (game-second = real second in the plane's units)
    return 3.156e7 * a ** 1.5

print(f"{'term':44s} {'belt 1e9':>14s} {'all-inner 1e9':>14s} {'budget':>10s}")
for name, kicks_orbit in [("unaveraged (32/orbit)", 32), ("averaged (0.3/orbit)", 0.3)]:
    pb = period_au(2.5)
    rate_belt = kicks_orbit / pb
    for label, rate in [("belt", rate_belt), ("inner", rate_inner)]:
        gb_s = N * rate * bits_event / 8
        events_s = N * rate
        if label == "belt":
            belt = (gb_s, events_s)
        else:
            inner = (gb_s, events_s)
    print(f"H_live creation, {name:24s} {belt[0]:>12.1f} B/s {inner[0]/1e6:>12.1f} MB/s   {BW:.0e} B/s")

# capacity terms
print()
print(f"stored, as held today: {9846*N/1e12:.2f} TB  -> {9846*N/B:.0f}x over 8 GB")
print(f"stored, 16 B tube only: {16*N/1e9:.1f} GB -> {16*N/B:.1f}x over 8 GB")
print(f"stored, belt program (0.126 bit/body): {0.126*N/8/1e6:.2f} MB -> {B/(0.126*N/8):.0f}x under")
print(f"live residual if all 1e9 held hot: {resid_body*N/8/1e9:.2f} GB of the 8 GB")
# worst case: zero reabsorption, all inner
fill_s = B * 8 / (N * rate_inner * bits_event)
print(f"zero-reabsorption all-inner fill time for 8 GB: {fill_s:.0f} game-s (measured reabsorption ratio 1.1-1.2/h -> bounded)")
# compute terms
for us in (12.0, 66.0):
    cores = N * rate_inner * us * 1e-6
    print(f"all-inner kick compute at {us:.0f} us/event: {cores:.0f} core.s per game-s (whole M1 ~ {OPS/1e9:.0f} Gops)")
print(f"belt kick compute (1e9 at 2.5 AU, 32/orbit, 66 us): {N*32/period_au(2.5)*66e-6:.2f} core.s per game-s")
# the board's 190-core figure re-derived
print(f"board '190 cores' re-derived: 1e9 x {rate_inner:.3f} ev/body/s x 12 us = {N*rate_inner*12e-6:.0f} cores (inner-scale cadence)")
