#!/usr/bin/env python3
"""The 1e9 budget on the M1, decomposed into walls, from the engine's own measured rates.

Every constant is cited; the only free parameters are the scene (what fraction of bodies
sits in strong-tide low orbits) and the per-event cost, each swept. Orders of magnitude only.

Citations:
  [K1,K2,K6] artifacts/evidence/premise-probe-20260928/GLM_RESULTS.md (H0190):
     32.5 kicks/orbit low orbit (Moon/Sun tides); 0.285 with quadrupole averaging (114x);
     economics: 1.2e-2 calls/s/body at 50 us = 0.6 core per 1e6 ships (K1-style);
                1.0e-4 calls/s/body           = 0.01 core per 1e6 (K2-style).
  [H0210] docs/HISTORY.md: the plane's kicks cost 29 us (recompile-dominated; ~99% recompile).
  [law] docs/law.md: tube = 16 bytes; kicks are integers of the law, orbit-averaged away from
     resonance; the designed kick = integer update + re-anchor at ~0.05 compiles/kick, with the
     cycle memo SHARED across tubes with the same quantized (E, L) key.
  [shipmem] H0209: a perfect convoy costs 488 B per 1e6 ships; belt program 0.126 bits/body
     (gold 20261006 components-98bc, taste log).
  [r8] r8 v2 + q-candidate-degree (taste log): belt 0 = 1.7e6 bodies, 427 encounters per 20
     orbits (~2.6e9 s); work per real encounter ~786 candidate evals, constant at fixed density.
  [M1] board/lens + docs/HANDOFF.md: ~1e10 simple ops/s, 60 GB/s, 8 GB unified, 4 GiB state
     budget, 4P+4E cores ~ 5 effective; plane service RTF 100; approved horizon 3,600 s.
Assumptions (stated, not measured): low orbit = 5,400 s (LEO-class); 1 candidate eval = 3 ns;
per-encounter record = 100 bits; a far body's kick rate is at most the K2-averaged LEO rate.
Inputs: measured on this box by bench.c (fold ns/op, rand16 ns/op).
"""
import sys

# ---- machine (M1) ----
OPS_S      = 1.0e10      # simple ops/s across cores [M1]
BW_S       = 60e9        # B/s sequential [M1]
CORES_EFF  = 5.0         # 4P + 4E in performance-equivalents [M1, assumption]
STATE_B    = 4.0e9       # 4 GiB state budget [M1]
RTF        = 100.0       # the plane's service level [H0210]
SESSION_S  = 3600.0      # one hour of PLAY (wall) = 360,000 game-s at RTF 100

# ---- measured engine rates ----
KICKS_ORBIT_K1 = 32.5    # [K1]
LOW_ORBIT_S    = 5400.0  # LEO-class [assumption]
RATE_K1        = KICKS_ORBIT_K1 / LOW_ORBIT_S        # 6.02e-3 kicks/s/body (game time)
RATE_K2        = RATE_K1 / 114.0                     # [K2] quadrupole averaging
CALL_RATE_K1   = 1.2e-2  # calls/s/body [K6]
CALL_RATE_K2   = 1.0e-4  # calls/s/body [K6]
COST_PLANE     = 29e-6   # s per kick today [H0210]
COST_PROBE     = 50e-6   # s per call in the probe [K6]
TUBE_B         = 16      # B [law]
BELT_BITS      = 0.126   # bits/body [shipmem/gold]
CONVOY_B       = 488.0 / 1e6   # B per ship, perfect convoy [shipmem]
ENC_RATE_BELT0 = 427 / (1.7e6 * 2.6e9)   # encounters/s/body(game) at belt-0 density [r8]
WORK_PER_ENC   = 786.0   # candidate evals per real encounter, fixed density [r8/q-candidate-degree]
EVAL_S         = 3e-9    # s per candidate eval [assumption]
ENC_BITS       = 100.0   # bits per encounter record (pair indices + outcome) [assumption]

# ---- measured on this box (bench.c) ----
FOLD_NS   = float(sys.argv[1]) if len(sys.argv) > 1 else 3.2
RAND16_NS = float(sys.argv[2]) if len(sys.argv) > 2 else 19.6
COST_FOLD_HOT  = FOLD_NS * 1e-9 * 20          # arith+queue floor x20 headroom, hot cycle memo
COST_FOLD_COLD = COST_PLANE * 0.05            # re-anchor: 0.05 compiles/kick [law] x 29 us
RAND16_S  = RAND16_NS * 1e-9                  # per random 16-B tube update, single core
N = 1.0e9

def show(title, lines):
    print(f"\n== {title} ==")
    for k, v in lines:
        print(f"  {k:<56s} {v}")

def cores(rate_per_body_s, n, cost_s, rtf=RTF):
    return n * rate_per_body_s * rtf * cost_s

# ---------------------------------------------------------------- claim check
print("=" * 78)
print("CLAIM CHECK - board: '1e9 orbiting bodies at today's rates ~ 190 cores'")
for label, cost in [("plane kick 29 us [H0210]", COST_PLANE),
                    ("probe call 50 us [K6]", COST_PROBE)]:
    print(f"  1e9 x {RATE_K1:.2e} kicks/s/body x {label:<28s} -> {cores(RATE_K1,1e9,cost,rtf=1):6.0f} cores (RTF 1)")
print(f"  H0190's own row: 0.6 core/1e6 -> {0.6*1000:.0f} cores; averaged 0.01 -> {0.01*1000:.0f} cores")
print("  verdict: 175-600 vs 'about 190' -> claim stands (same wall, <2x at its low end).")

# ---------------------------------------------------------------- kick walls
print("\n" + "=" * 78)
print(f"WALLS AT N=1e9 (RTF {RTF:.0f}, budget {CORES_EFF:.0f} eff. cores, {STATE_B/1e9:.0f} GB state)")
for name, rate_b, cost, note in [
    ("S1 adversarial: all 1e9 strong-tide, K1 cadence, plane 29 us",
     RATE_K1, COST_PLANE, "unaveraged + today's fold"),
    ("S1b same, free 200 ns fold", RATE_K1, 200e-9, "compute still dead"),
    ("S1c same, K2 averaged, fold {hot:.0f} ns (hot memo)".format(hot=COST_FOLD_HOT*1e9),
     RATE_K2, COST_FOLD_HOT, "fits with 15x margin"),
    ("S1d same, K2 averaged, fold {cold:.0f} ns (cold re-anchor)".format(cold=COST_FOLD_COLD*1e9),
     RATE_K2, COST_FOLD_COLD, "1.6x OVER: the cycle memo must be hot"),
    ("S2 all 1e9 charged K2-averaged LEO rate (absurd upper bound for far bodies)",
     CALL_RATE_K2, COST_FOLD_HOT, "true belt rate unmeasured; a lead"),
]:
    c = cores(rate_b, N, cost)
    show(name, [("kick compute", f"{c:8.2f} cores  ({c/CORES_EFF:9.3g}x budget)  [{note}]")])

# realistic galaxy scene: 1e9 belt (weak tide) + 1e7 fleet strong-tide (unaveraged, ships
# and chaotic regions are never averaged [law]) + player
for pop, cadence, cost, lbl in [
    (1e7, RATE_K1, COST_FOLD_HOT, "fleet 1e7 strong-tide, K1 cadence, hot fold"),
    (1e7, RATE_K1, COST_FOLD_COLD, "fleet 1e7 strong-tide, K1 cadence, cold re-anchor"),
]:
    c = cores(cadence, pop, cost)
    show(f"galaxy scene: {lbl}", [("kick compute", f"{c:8.2f} cores  ({c/CORES_EFF:9.3g}x budget)")])

# random-access wall (the one ops/s misses): each kick touches one 16-B tube at random
for name, rate_b in [("S1 unaveraged", RATE_K1), ("S1c averaged", RATE_K2),
                     ("S2 K2 all bodies", CALL_RATE_K2)]:
    ops_s = N * rate_b * RTF
    cap = CORES_EFF / RAND16_S
    show(f"random-access: {name}", [("tube updates/s vs 5-core capacity",
        f"{ops_s:9.3e}/s vs {cap:9.3e}/s  -> {ops_s/cap:9.3g}x")])

# bandwidth
for name, ev, bper, rtf in [("S2 events (all 1e9, K2 rate)", CALL_RATE_K2 * N, 2*TUBE_B, RTF),
                            ("full sweep per frame (60 Hz, 1e9 tubes)", 60.0, N*TUBE_B, 1.0)]:
    bw = ev * bper * rtf
    show(f"bandwidth: {name}", [("bytes/s vs M1 60 GB/s", f"{bw:9.3e} B/s -> {bw/BW_S:9.3g}x")])

# memory + H_live
show("memory (galaxy scene)", [
    ("bulk: 1e9 belt programs @0.126 bits", f"{N*BELT_BITS/8/1e6:8.1f} MB"),
    ("live tubes: 1% of 1e9 @16 B",         f"{0.01*N*TUBE_B/1e9:8.2f} GB"),
    ("live tubes: 0.1% of 1e9 @16 B",       f"{0.001*N*TUBE_B/1e9:8.2f} GB"),
    ("convoy floor for 1e6 fleet ships",    f"{1e6*CONVOY_B/1e3:8.1f} kB"),
])
enc_s = N * ENC_RATE_BELT0 * RTF            # wall-clock encounters/s at fixed density
show("H_live (galaxy scene, folded kicks)", [
    ("encounters/s (wall) at belt-0 density scaled", f"{enc_s:8.3e}/s"),
    ("bits/s from encounters @100 bits",             f"{enc_s*ENC_BITS:8.3e} bits/s"),
    ("encounter compute (786 evals each)",           f"{enc_s*WORK_PER_ENC*EVAL_S:8.3e} cores"),
    ("growth over an hour of play (encounters)",     f"{enc_s*ENC_BITS*SESSION_S/8:8.1f} B"),
])
for pop, cadence in [(1e6, RATE_K1), (1e7, RATE_K1), (1e7, RATE_K2), (1e8, RATE_K2)]:
    grow = pop * cadence * RTF * TUBE_B * SESSION_S   # B per hour of play if kicks SCAR
    show(f"H_live if kicks scar (no fold): pop {pop:.0e}, {'K1' if cadence==RATE_K1 else 'K2'} cadence", [
        ("growth per hour of play", f"{grow/1e9:8.3g} GB/h  ({'BREAKS 4 GiB' if grow > STATE_B else 'bounded'})")])

# ---------------------------------------------------------------- frontier
print("\n" + "=" * 78)
print("FRONTIER: max strong-tide population N* = CORES_EFF / (cadence x RTF x cost)")
for lbl, r_, c_ in [("K1 cadence, hot fold", RATE_K1, COST_FOLD_HOT),
                    ("K2 averaged, hot fold", RATE_K2, COST_FOLD_HOT),
                    ("K2 averaged, cold re-anchor (1.5 us)", RATE_K2, COST_FOLD_COLD),
                    ("K1 cadence, plane 29 us", RATE_K1, COST_PLANE)]:
    print(f"  {lbl:<38s} N* = {CORES_EFF/(r_*RTF*c_):9.3e} strong-tide bodies")
