#!/usr/bin/env python3
"""The corrected 10^9 encounter ledger (run 20261014-1137-fermi-1738).

Regenerates every number in the dossier from:
  - kick-anchor.jsonl  : THIS box's run of the SHIPPED `cargo run --release -p
                         emergent-encounters -- kick` (n=10^4 anchor, 100 kicks)
  - 90fb's stored cascade.jsonl (cells/verify rows, cited per line)
  - code constants read from this tree (ctx.rs step_log2=7)

Frames: CPU-seconds per GAME-second, and at flying pace rtf 100 (x100).
M1-implied via the frozen M1 anchor (4345.4 us/kick on the same shipped
experiment, 90fb) over THIS box's us_per_kick. Budget: 4 M1 performance cores.
"""
import json, math

G, MSUN = 6.674e-11, 1.989e30
AU = 1.496e11
P_1AU = 2 * math.pi * math.sqrt(AU ** 3 / (G * MSUN))     # 3.156e7 s
P_4YR = 1.26e8                                            # 90fb's belt period
N = 1e9
BUDGET = 4.0
SKIN = 12.6          # board-adopted slack-skin factor (taste log 6 Oct)
RTF_FLY = 100        # the plane's flying pace (B1/367f)

rows = [json.loads(l) for l in open(__file__.replace("ledger2.py", "kick-anchor.jsonl"))]
anchor = [r for r in rows if r.get("exp") == "kick" and r["eps"] == 1e-9][-1]
PAIRS_CELL = anchor["pairs_per_kick"]            # 812.8 (island of 1e4, shipped)
US_PAIR_X86 = anchor["us_per_pair"]              # this box
US_KICK_X86 = anchor["us_per_kick"]
M1F = 4345.4 / US_KICK_X86                       # frozen M1 anchor / this box
US_PAIR = US_PAIR_X86 * M1F                      # M1-implied global pricing
US_PAIR_LOC = 3.95 * M1F                         # cells-local (90fb c6W x86 3.95)
SLACK_SKIP = anchor["slack_skippable_fraction"]

def law(n, X):   # 90fb's measured pairs-per-kick law (<=7% error, n to 1e6, law to 1e7)
    return 0.0346 * n * (1 + X) / (2 * (X - 1))

PAIRS_CONT_W = law(N, 150)    # one contiguous wide belt
PAIRS_CONT_N = law(N, 1.5)    # one contiguous narrow belt

# kick streams per game-second at N=1e9
K_AVG = 0.28                    # orbit-averaged (H0190: 32 -> 0.3 with averaging); 90fb K_AVG
KAPS = (0.28, 32.0, 128.0, 256.0)
streams = {
    "averaged 0.28/orbit (H0190 avg; 90fb K_AVG)": N * K_AVG / P_4YR,          # 2.2/s
    "unaveraged 32/orbit (H0190)":                 N * 32.0 / P_4YR,           # 254/s
    "shipped k=128/orbit, belt at 1 AU":           N * 128.0 / P_1AU,          # 4056/s
    "shipped k=256/orbit, belt at 1 AU":           N * 256.0 / P_1AU,          # 8111/s
}

def cores(kicks_s, pairs, us_pair, skin=SKIN):
    return kicks_s * pairs * us_pair * 1e-6 / skin

print("=" * 100)
print(f"ANCHOR (this box, shipped code): pairs/kick {PAIRS_CELL}  us/pair x86 {US_PAIR_X86}  "
      f"us/kick {US_KICK_X86}  slack_skippable {SLACK_SKIP}")
print(f"M1 factor {M1F:.3f} -> M1 us/pair {US_PAIR:.2f} (global) / {US_PAIR_LOC:.2f} (cells-local, 90fb c6W)")
print(f"Pairs law at 1e9: contiguous wide X=150 {PAIRS_CONT_W:.2e} / narrow X=1.5 {PAIRS_CONT_N:.2e}"
      f"  vs island(1e4) {PAIRS_CELL:.0f}")
print(f"Topology lever {PAIRS_CONT_W/PAIRS_CELL:.0f}x (wide) / {PAIRS_CONT_N/PAIRS_CELL:.0f}x (narrow);"
      f" cadence lever 0.28->128 = {128/K_AVG:.0f}x; skin {SKIN}x; locality {US_PAIR/US_PAIR_LOC:.1f}x")
print("=" * 100)

hdr = f"{'cadence policy (kicks/game-s at 1e9)':46s} | {'islands 812.8':>26s} | {'contiguous X=150':>26s} | {'contiguous X=1.5':>26s}"
print("ENCOUNTER CASCADE, M1-implied cores, skin-on, per GAME-second  (flying pace = x100)", )
print(hdr)
wall = {}
for name, ks in streams.items():
    r = f"{name + f' ({ks:.0f}/s)':46s} |"
    for pairs in (PAIRS_CELL, PAIRS_CONT_W, PAIRS_CONT_N):
        r += f" {cores(ks, pairs, US_PAIR):>11.3g} ({cores(ks,pairs,US_PAIR)*RTF_FLY:>8.3g}) |"
    print(r)
print("(each cell: per game-second, and in parentheses at flying pace rtf 100; budget 4 cores)")
print()
print("MAX RTF ON 4 CORES (90fb's own bottom-line metric), skin-on, global pricing:")
for name, ks in streams.items():
    r = f"  {name:46s}"
    for pairs in (PAIRS_CELL, PAIRS_CONT_W, PAIRS_CONT_N):
        c = cores(ks, pairs, US_PAIR)          # per game-second
        rtf = BUDGET / c if c > 0 else float("inf")
        r += f"  {min(rtf, 1e9):>10.3g}"
    print(r + "   [islands / wide / narrow]")
print(f"  [90fb's own row: 'max rtf on 4 cores: averaged + skin' = 5,216 at CELL geometry — the")
print("   '0.966/0.077 per cell' was the partitioned TOTAL, not a per-cell rate]")
print()
print("=" * 100)
print("AUDIT OF THE PUBLISHED NUMBERS")
print("=" * 100)
ks_avg = streams["averaged 0.28/orbit (H0190 avg; 90fb K_AVG)"]
# 90fb's composition
casc_pair_cell = PAIRS_CELL * US_PAIR * 1e-6
print(f"90fb '0.966 per cell' = kicks_s(all 1e9, averaged, rtf100 = {ks_avg*RTF_FLY:.0f}/s) x one island wake"
      f" ({PAIRS_CELL:.0f} x {US_PAIR:.2f} us = {casc_pair_cell*1e3:.2f} ms)")
print(f"   = {ks_avg*RTF_FLY*casc_pair_cell:.3f} cores  == the PARTITIONED TOTAL (all islands). It is not a per-cell rate.")
print(f"effb '7.7e3 skin / 9.66e4 no-skin' = that x 1e5 cells  -> bills the billion's kick stream once per cell.")
print(f"Structural identity: 1e5 cells x {PAIRS_CELL:.0f} = {1e5*PAIRS_CELL:.2e} pairs ~ contiguous pair count"
      f" ({PAIRS_CONT_W:.2e}-{PAIRS_CONT_N:.2e}),")
print(f"   so effb's magnitude lands inside the CONTIGUOUS+averaged+skin+rtf100 cell of the cube"
      f" ({cores(ks_avg,PAIRS_CONT_W,US_PAIR)*RTF_FLY:.2e}-{cores(ks_avg,PAIRS_CONT_N,US_PAIR)*RTF_FLY:.2e}) by identity,")
print(f"   not by the cell arithmetic written. The published label ('working point = 1e5 cells') contradicts the number.")
print()
print("THE KICK TERM IN THE SAME FRAMES (effb's own constants, made consistent):")
for nm, rate_per_body, us in (("shipped 231 us", 128 / P_1AU, 231.0),
                              ("Carlson 30 us", 128 / P_1AU, 30.0),
                              ("key arm 0.11 us (b29a)", 128 / P_1AU, 0.11)):
    c = N * rate_per_body * us * 1e-6
    print(f"  {nm:26s} {c:9.3g} cores/game-s   {c*RTF_FLY:9.3g} at flying pace")
print("  [effb's ledger: kick term at rtf 1 (0.12-1.09 cores) vs encounter term carrying 90fb's rtf 100")
print("   inside the 0.077 -> the published '7,051x the kick term' mixes frames by 100x]")
print()
print("THE 'WIRED WALL' (H0216's held-out number, recomputed):")
C_W = 0.0346 * (1 + 150) / (2 * (150 - 1))     # law coefficient, contiguous wide X=150
walls = []
for name, ks_rate in (("averaged 0.28/orbit", K_AVG / P_4YR), ("unaveraged 32/orbit", 32.0 / P_4YR),
                      ("shipped k=128/orbit", 128.0 / P_1AU)):
    c_body = ks_rate * PAIRS_CELL * US_PAIR * 1e-6 / SKIN   # per body per game-second (islands)
    w_isl = BUDGET / c_body
    w_con = math.sqrt(BUDGET * SKIN / (ks_rate * C_W * US_PAIR * 1e-6))  # contiguous: cost ~ N^2
    walls.extend([w_isl / RTF_FLY, w_con / math.sqrt(RTF_FLY)])
    print(f"  {name:24s} islands: {w_isl:.2e} (rtf1) / {w_isl/RTF_FLY:.2e} (fly)   "
          f"contiguous-wide: {w_con:.2e} (rtf1) / {w_con/math.sqrt(RTF_FLY):.2e} (fly)")
print("  [contiguous cost is quadratic in N: pairs/kick = C_W*N; islands linear]")
print(f"  [effb's held-out '~5.2e5 skin-on' inherits the hybrid composition; the honest flying-pace walls span")
print(f"   {min(walls):.1e} to {max(walls):.1e} bodies — the wiring's step_log2 + topology choices are worth ~{max(walls)/min(walls):.0e}x]")
