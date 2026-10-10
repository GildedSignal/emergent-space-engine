#!/usr/bin/env python3
"""The 10^9 budget on one M1-class machine, from measured constants only.

Inputs (regenerable):
  kick-bench.json     xtask universe --kick-bench --seconds 20          (this box)
  bench-rtf100.json   xtask universe --bench --rtf 100 --seconds 20     (this box)
Constants from the record (docs/HISTORY.md H0190; board 30 Sept; law.md; plane.md):
  32.5 kicks per low orbit unaveraged, 0.285 averaged (K2's 114x), low orbit T = 5.4e3 s
  belt a = 3 AU -> T = 1.64e8 s; 427 encounters / 1844 bodies / 20 orbits = 0.012/body/orbit
  tube floor 16 B; components-98bc gold: 0.126 bits per smooth-belt body
Machine (HANDOFF): ~1e10 simple ops/s across cores (~8 effective), ~60 GB/s, 8 GB unified,
4 GiB approved sim budget. Orders of magnitude only (Linux/x86 box; integrator re-measures).
"""
import json, pathlib

R = pathlib.Path(__file__).parent
kick = json.load(open(R / "kick-bench.json"))
plane = json.load(open(R / "bench-rtf100.json"))

T_KICK_US = kick["kick_us"]["median"]          # per DISTINCT kick = one cycle compile
T_KICK_LEAVER_US = kick["kick_us_leavers"]["median"]
BYTES_BODY_PLANE = plane["bytes_per_body"]
CORES = 8.0
RTF = 100.0                                    # game-seconds per real second

def kicks_per_rs(n, per_orbit, period_s):
    return n * per_orbit / period_s * RTF

def row(name, rate):
    cost = rate * T_KICK_US * 1e-6             # core-seconds per real second
    print(f"{name:<42} {rate:>10.3g} kicks/s   {cost:>9.3g} core-s/s   {cost/CORES:>7.3g} machine")
    return cost

print(f"t_kick (distinct, median)      = {T_KICK_US:.1f} us   (leavers {T_KICK_LEAVER_US:.0f} us)")
print(f"memo hit on distinct kicks     = exact {kick['memo']['exact_hit_rate']}, "
      f"quantized {kick['memo']['quantized_hit_rate']}  (3 seeds)")
print(f"bytes/body shipped plane       = {BYTES_BODY_PLANE}")
print(f"events/s whole plane @rtf100   = {plane['events_per_second']:.0f} on {plane['bodies']} bodies; "
      f"frame cpu p50 {plane['frame_cpu_ms']['p50']:.1f} ms, rtf lowest 1% {plane['rtf']['lowest_1pct']:.1f}\n")

print("--- kick compute at 1e9 bodies, rtf 100 ---")
c1 = row("all low orbit, unaveraged (32.5/orbit)", kicks_per_rs(1e9, 32.5, 5.4e3))
c2 = row("all low orbit, averaged (0.285/orbit)", kicks_per_rs(1e9, 0.285, 5.4e3))
c3 = row("belt 3 AU, unaveraged (32/orbit)", kicks_per_rs(1e9, 32, 1.64e8))
c4 = row("belt 3 AU, averaged (0.3/orbit)", kicks_per_rs(1e9, 0.3, 1.64e8))
cap = CORES / (T_KICK_US * 1e-6)
print(f"\naffordable distinct kicks/s on {CORES:.0f} cores = {cap:.3g}")
print(f"  -> low-orbit population cap at that cost, averaged: "
      f"{cap / kicks_per_rs(1, 0.285, 5.4e3):.3g} bodies")
print(f"  -> t_kick needed for 1e9 low-orbit averaged on {CORES:.0f} cores: "
      f"{CORES / kicks_per_rs(1e9, 0.285, 5.4e3) * 1e9:.3g} ns/kick")

print("\n--- storage at 1e9 bodies ---")
for name, b in (("tube floor (law.md)", 16), ("shipped plane store", BYTES_BODY_PLANE)):
    print(f"{name:<28} {b:>8.4g} B/body -> {b*1e9/2**30:>7.3g} GiB  "
          f"({b*1e9/2**30/8:+.2f}x of 8 GB, {b*1e9/2**30/4:+.2f}x of 4 GiB budget)")
pb = 0.126 / 8
print(f"{'population program (gold)':<28} {pb:>8.4g} B/body -> {pb*1e9/2**20:>7.3g} MiB  "
      f"({pb*1e9/2**30/8:+.2f}x of 8 GB)")

print("\n--- H_live, belt creation at 1e9 (bits per game-second) ---")
for bits_per_scar in (32, 128):
    rate = 0.012 / 1.64e8 * 1e9 * bits_per_scar
    print(f"scar {bits_per_scar:>3} bits: {rate:>8.3g} bits/game-s "
          f"({rate*RTF/8/1e6:>8.3g} MB per real second at rtf {RTF:.0f})")
