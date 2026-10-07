#!/usr/bin/env python3
"""The 1e9 budget, REPUBLISHED (second author) with the checker's two named fixes:

(1) the plane's per-kick fold cost is now MEASURED on distinct kicks (xtask universe
    --kick-bench, 3 seeds, RTF 100 and 1) instead of synthetic: whole kick, the
    fresh-compile share on the rebinds' own keys, and both memo hit rates;
(2) every frontier row is intersected with the resident-tube memory wall
    (strong-tide population x 16 B <= 4 GB state budget).

Citations beyond budget.py's (unchanged, see orig/budget.py):
  [measured] this run: kickbench-s{1,2,3}-rtf{100,1}.json (shipped harness
    `xtask universe --kick-bench`), decompose-out.txt (fresh Orbit::compile on the
    rebinds' own keys, same replay loop), compile-out.txt (compile grid).
"""
import sys

# ---- machine (M1) ----
OPS_S      = 1.0e10
BW_S       = 60e9
CORES_EFF  = 5.0
STATE_B    = 4.0e9        # 4 GB state budget [M1]
RTF        = 100.0
SESSION_S  = 3600.0

# ---- engine rates (unchanged from the original) ----
KICKS_ORBIT_K1 = 32.5
LOW_ORBIT_S    = 5400.0
RATE_K1        = KICKS_ORBIT_K1 / LOW_ORBIT_S   # 6.02e-3 kicks/s(game)/body
RATE_K2        = RATE_K1 / 114.0                # 5.28e-5
CALL_RATE_K2   = 1.0e-4
RATE_PLANE     = 8.0e-3   # [measured] plane scene, distinct kicks / ship-game-seconds:
                         # 8.15e-3 / 7.28e-3 / 7.42e-3 (seeds 1/2/3, decompose-out.txt) --
                         # ABOVE the LEO K1 rate: today's battle scene is the adversarial cadence
TUBE_B         = 16
BELT_BITS      = 0.126
CONVOY_B       = 488.0 / 1e6
ENC_RATE_BELT0 = 427 / (1.7e6 * 2.6e9)
WORK_PER_ENC   = 786.0
EVAL_S         = 3e-9
ENC_BITS       = 100.0

# ---- MEASURED on this box (this run; x86 orders of magnitude, integrator re-measures M1) ----
KICK_US_MADE    = 35.0    # kickbench s1/s2/s3 rtf100: 35.0/34.8/35.0 median (29 us on M1 [H0210])
KICK_US_LEAVER  = 92.0    # 91.9/72.1/89.4 median; p99 393/371/378
KICK_US_LEAV99  = 390.0   # p99 tail
COMPILE_US_MADE = 3.7     # fresh Orbit::compile on the rebinds' own keys (weak-field cycles)
COMPILE_US_LEAV = 50.0    # 62.2/43.3/46.1 (cycles; passages' own compile not counted)
COMPILE_US_GRID = 34.7    # (p,e) grid median; p99 171 (strong field, e=0.99)
HIT_EXACT       = 0.0     # exact-key memo hit rate on DISTINCT kicks, every seed/rtf (3108 rebinds)
HIT_QUANT       = 0.955   # 12+12-bit law memo key: 0.9547/0.9509/0.9571 (RTF 100); a LAW CHANGE [law]
JET_COMPILES    = 0.05    # compiles/kick of the adopted design (jet + exact re-anchor) [law]

COST_PLANE    = KICK_US_MADE   * 1e-6                 # today's kick, measured
COST_DESIGNED = JET_COMPILES * COMPILE_US_GRID * 1e-6 # 1.74 us: jet re-anchor (both reuse designs agree)
COST_DESIGNED_FLEET = JET_COMPILES * COMPILE_US_LEAV * 1e-6  # 2.5 us on leaver-like keys
N_MEM = STATE_B / TUBE_B                               # 2.5e8 strong-tide bodies: the tube-memory wall

def show(title, lines):
    print(f"\n== {title} ==")
    for k, v in lines:
        print(f"  {k:<56s} {v}")

def cores(rate, n, cost):
    return n * rate * RTF * cost

print("=" * 78)
print("MEASURED (this box, shipped harness `xtask universe --kick-bench`, distinct kicks)")
show("the plane's real kick", [
    ("whole kick, made ships",  f"{KICK_US_MADE:.0f} us median (29 us on M1 [H0210])"),
    ("whole kick, fleet leavers", f"{KICK_US_LEAVER:.0f} us median, p99 {KICK_US_LEAV99:.0f} us"),
    ("fresh compile on the rebind's own key", f"made {COMPILE_US_MADE:.1f} us (11% of kick); leavers {COMPILE_US_LEAV:.0f} us (48-57%; passages extra)"),
    ("compile grid median / p99", f"{COMPILE_US_GRID:.1f} / 171 us (p = 2^4..2^24 M, e = 0..0.99)"),
    ("cycle-memo hit rate, EXACT key", f"{HIT_EXACT:.0%}  (3 seeds x 2 rtf, 3108 distinct rebinds) -> the hot-memo corner is dead"),
    ("cycle-memo hit rate, quantized key", f"{HIT_QUANT:.1%}  (law change: re-rounding random-walks the orbit [law: Not adopted])"),
])
show("the two reachable reuse designs (measured ingredients)", [
    ("jet + exact re-anchor (adopted [law])", f"{JET_COMPILES} x {COMPILE_US_GRID:.1f} us = {COST_DESIGNED*1e6:.2f} us/kick"),
    ("quantized cell (NOT adopted)", f"(1-{HIT_QUANT:.3f}) x {COMPILE_US_GRID:.1f} us = {(1-HIT_QUANT)*COMPILE_US_GRID:.2f} us/kick"),
    ("agreement", "both land 1.6-1.8 us: the designed fold is ~2 us, NOT the 64 ns hot corner"),
])

print("\n" + "=" * 78)
print(f"WALLS AT N=1e9 (RTF {RTF:.0f}, {CORES_EFF:.0f} eff. cores, {STATE_B/1e9:.0f} GB state)")
for name, pop, rate, cost, note in [
    ("S1 adversarial: all 1e9 strong-tide, K1, today's kick", 1e9, RATE_K1, COST_PLANE, "measured 35 us"),
    ("S1c same, K2 averaged, DESIGNED fold 1.74 us", 1e9, RATE_K2, COST_DESIGNED, "compute 1.8x OVER (was '15x under' at the dead 64 ns corner)"),
    ("S1c-mem same scene, memory-legal pop 2.5e8", N_MEM, RATE_K2, COST_DESIGNED, "tubes fill the 4 GB budget: memory binds"),
    ("realistic: 1e7 fleet at the plane MEASURED cadence, designed", 1e7, RATE_PLANE, COST_DESIGNED, "13.9 cores: 2.8x OVER: the realistic fleet does NOT fit at any legal fold"),
    ("realistic capped: 3.6e6 fleet (compute N* at measured cadence)", 3.6e6, RATE_PLANE, COST_DESIGNED, "4.99 cores: exactly budget"),
    ("realistic-hard: 1e7 fleet, LEO cadence K1, designed", 1e7, RATE_K1, COST_DESIGNED, "10.4 cores: 2.1x OVER"),
    ("S2 all 1e9 far bodies at K2-averaged LEO rate, designed fold", 1e9, CALL_RATE_K2, COST_DESIGNED, "3.5x OVER: even the absurd upper bound no longer 'fits'"),
    ("S2-mem same, memory-legal pop 2.5e8", N_MEM, CALL_RATE_K2, COST_DESIGNED, "0.87 core: fits once memory-legal"),
]:
    c = cores(rate, pop, cost)
    show(name, [("kick compute", f"{c:8.2f} cores  ({c/CORES_EFF:9.3g}x budget)  [{note}]")])

print("\n" + "=" * 78)
print("FRONTIER: max strong-tide population, compute vs the resident-tube memory wall")
print(f"  memory wall: {N_MEM:.3e} bodies (4 GB / 16 B tube)")
for lbl, r_, c_ in [
    ("K1 cadence, today's kick (measured 35 us)", RATE_K1, COST_PLANE),
    ("K1 cadence, designed fold 1.74 us",         RATE_K1, COST_DESIGNED),
    ("plane MEASURED cadence 8e-3, designed fold", RATE_PLANE, COST_DESIGNED),
    ("K2 averaged, designed fold 1.74 us",        RATE_K2, COST_DESIGNED),
    ("K2 averaged, dead hot corner 64 ns",        RATE_K2, 64e-9),
]:
    n_c = CORES_EFF / (r_ * RTF * c_)
    n = min(n_c, N_MEM)
    bind = "COMPUTE" if n_c < N_MEM else "MEMORY"
    print(f"  {lbl:<40s} N* = {n:9.3e}   ({bind} binds; compute alone said {n_c:9.3e})")

print("\n" + "=" * 78)
print("THE SWING (representation only), at the memory-legal adversarial population 2.5e8")
for lbl, rate, cost in [("today: K1 + 35 us measured kick", RATE_K1, COST_PLANE),
                        ("designed: K2 + 1.74 us jet fold", RATE_K2, COST_DESIGNED)]:
    c = cores(rate, N_MEM, cost)
    print(f"  {lbl:<40s} {c:9.3g} cores ({c/CORES_EFF:9.3g}x budget)")
sw_today = cores(RATE_K1, N_MEM, COST_PLANE)
sw_des   = cores(RATE_K2, N_MEM, COST_DESIGNED)
print(f"  swing = {sw_today/sw_des:.3e}x  = averaging 114x x kick/fold 20x; the original's 5.2e4x needed the dead 64 ns corner")

print("\n" + "=" * 78)
print("WHAT THE ORIGINAL GOT WRONG, AND WHAT SURVIVES")
show("corrections", [
    ("'hot fold 64 ns' corner", "dead: exact-key hit rate 0.0 on every distinct-kick run"),
    ("'S1c fits compute 15x under' (all 1e9 strong-tide)", f"machine-false twice over: 1.8x OVER compute at the reachable fold, and {1e9*TUBE_B/1e9:.0f} GB of tubes vs 4 GB"),
    ("'recompile-dominated' [H0210]", "11% on made kicks, 48-57% on leavers (this scene); the rest is readout/forces/fit"),
    ("realistic 1e7 fleet 'fits 13x'", "dead: measured plane cadence 8e-3 (> K1!) x reachable fold = 2.8x OVER; compute N* at that cadence is 3.6e6 ships"),
    ("'no wall is set by N'", "one is: resident tubes cap strong-tide bodies at 2.5e8 whatever the fold costs"),
])
show("survives (orders unchanged)", [
    ("the swing", f"{sw_today/sw_des:.0f}x (3 orders), 22x below the original's 5.2e4x: the 64 ns corner was unreachable"),
    ("other walls", "bandwidth, encounters, belt memory, H_live folding bound: unchanged inputs, unchanged margins"),
    ("tail (principle 12)", f"designed fold p99/kick ~ 0.05 x 171 us = {0.05*171:.1f} us, 5x its mean: the allocator must budget re-anchor bursts"),
    ("determinism", "shipped harness digests stable per seed; refused 0 everywhere"),
])
