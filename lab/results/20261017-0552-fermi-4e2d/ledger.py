#!/usr/bin/env python3
"""The 10^9 budget recomposed (fermi 20261017-0552-4e2d).

Every constant carries its source. Anchors measured by this run are read from
probe.txt (belt_first + the nladder flight); page constants are inlined with
their run ids. M1 = x86 * RATIO (e7ef's anchors: M1 29.3 us vs x86 50 us mixed).
Identity: cores = N * C_ppbi(us/body/interval) / INTERVAL * RTF / 1e6, where
C_ppbi sums the per-event costs of the combs a body fires per interval.
"""
import re

# ---- anchors measured by this run (probe.txt) ----
probe = open(__file__.replace("ledger.py", "probe.txt")).read()
belt_first_p50 = float(re.search(r"belt: \d+ bodies.*p50 (\d+)", probe).group(1))
kicks = int(re.search(r"kicks (\d+)", probe).group(1))
boundaries = int(re.search(r"boundaries (\d+)", probe).group(1))
opens = int(re.search(r"opens (\d+)", probe).group(1))
game_s = float(re.search(r"game ([\d.]+) s", probe).group(1))
# per-event x86 cost on this box: a near-budget clean crest frame (11.95 ms / 242 events)
m = re.search(r"\((\d+), (11\.\d+), (\d+), [\d.]+\)", probe)
frame_ms, frame_ev = float(m.group(2)), int(m.group(3))
C_THISBOX = (frame_ms - 0.4) * 1e3 / frame_ev  # us/event, fixed per-frame part removed

# ---- page constants (cited in dossier.md) ----
N, RTF, CORES = 1e9, 100.0, 4.0
INTERVAL = 28141.5            # the doll grid (3294; 4093; 8ffc; e7ef)
C_KICK, C_BOUND = 51.7, 12.9  # us x86 per kick / boundary event (8ffc)
RATIO = 29.3 / 50.0           # M1/x86 (e7ef)
SPLIT = 8.0                   # BELT_SPLIT (7f97; 98cb flown: first kick x8.000)
SURV_FROZEN = 438 / 712       # 1a46's own belt count: 274/712 deleted, frozen exclusion
SURV_E7EF = 0.39              # e7ef's composed row ("61% belt delete" read as survival 39%)
PLATEAU_KB = 4.95             # b30b kicked-body plateau, kB/body
COMPACT_B = (1.7, 2.4)        # 07b4: self-stirred belt B/live-body
ENGINE_GB, USABLE_GB = 0.5, 6.0
CLIFF_GS = 100.0              # 8792: re-mint cliff between dwell 80 and 100

def cores(c_ppbi_x86):
    return N * (c_ppbi_x86 * RATIO) / INTERVAL * RTF / 1e6

def row(name, c_ppbi_x86, note=""):
    print(f"  {name:<58} {c_ppbi_x86:7.2f} us/B/int   {cores(c_ppbi_x86):8.1f} cores M1   {note}")
    return cores(c_ppbi_x86)

print("== anchors (this run, shipped code, this box) ==")
print(f"belt first item p50 {belt_first_p50:.0f} gs  -> interval {2*belt_first_p50:.0f} gs"
      f"  (record 28,141.5; err {abs(2*belt_first_p50-INTERVAL)/INTERVAL*100:.2f}%)")
print(f"window {game_s:.0f} gs = {game_s/INTERVAL:.4f} intervals: kicks {kicks}, boundaries {boundaries}"
      f" (ratio {kicks/boundaries:.3f}; count parity = the two-comb), opens {opens}")
print(f"per-event x86 this box {C_THISBOX:.1f} us (record anchor 50-52)")
print("\n== CPU ledger at 1e9, rtf 100, M1-equivalent (x86 * %.3f) ==" % RATIO)
row("shipped, kicks only (e7ef's stream)", C_KICK, "the record's ledger row")
two = C_KICK + C_BOUND
row("shipped, two-comb", two, f"+{(two/C_KICK-1)*100:.0f}% (8ffc's correction)")
row("BELT_SPLIT x8 (both combs stretch)", two / SPLIT)
r1 = row("  + hybrid delete, BELT legality (survival 438/712)", two / SPLIT * SURV_FROZEN, "1a46's belt count")
row("  + delete as e7ef composed it (survival 0.39)", two / SPLIT * SURV_E7EF, "e7ef's 5.1-8.65 cores")
row("split x8, boundary comb NOT stretched", C_KICK / SPLIT + C_BOUND, "kick-cadence open 1")
r2 = row("  + delete (frozen legality)", (C_KICK / SPLIT + C_BOUND) * SURV_FROZEN, "")
print(f"    (the boundary-stretch question swings the composed ledger x{r2/r1:.1f})")
req = CORES * INTERVAL / (N * RTF) * 1e6              # M1-us per body per interval at 4 cores
req_x86 = req / RATIO
s_star = two * SURV_FROZEN / req_x86
print(f"\nbudget identity: 4 cores = {req:.3f} us/body/interval (e7ef's 1.13)")
print(f"required split at today's cost, frozen legality: S* = {s_star:.1f}x")
print(f"required mixed cost at split 8, frozen legality: {req*SPLIT/SURV_FROZEN:.1f} us M1 ({req_x86*SPLIT/SURV_FROZEN:.1f} us x86)")

print("\n== memory at 1e9 (the compact wiring) ==")
stock = (N * COMPACT_B[0] / 1e9, N * COMPACT_B[1] / 1e9)
allow = USABLE_GB - stock[1] - ENGINE_GB
for S, tag in [(8.0, "split 8"), (s_star, f"split {s_star:.0f} (CPU-closing)")]:
    mint = N * 2 * SURV_FROZEN / (S * INTERVAL)          # events/game-s
    dstar = allow * 1e9 / (mint * PLATEAU_KB * 1e3)      # gs
    print(f"{tag}: mint {mint:.3e} ev/gs; live at dwell D: {mint*PLATEAU_KB:.0f} kB/gs;"
          f" dwell ceiling D* = {dstar:.0f} gs; window [{CLIFF_GS:.0f}, {dstar:.0f}] gs"
          f" (width x{dstar/CLIFF_GS:.2f})")
mint8 = N * 2 * SURV_FROZEN / (8 * INTERVAL)
diet = allow * 1e9 / (mint8 * 1e3)  # live at 1 kB/body
print(f"with the record diet (live ~1 kB/B): D* = {diet:.0f} gs at split 8 (width x{diet/CLIFF_GS:.1f})")
print(f"compact stock {stock[0]:.1f}-{stock[1]:.1f} GB + engine {ENGINE_GB} GB; live allowance {allow:.1f} GB")

print("\n== the other terms (cited) ==")
print("encounters 0.03-0.6 cores (f0a2, adjudicated; Key::new E absolute Q48 verified in source)")
print("promotion CPU: free (cbc5: the mint IS the kick's compile; demote 0.08 us)")
print(f"genesis one-time: {N*28e-6/3600:.1f} h at today's 28 us/body build (program births delete it, 98bc)")
print("H_live 21 bits/s at 1e9 (4b55 gold): ~0.1 MB/h")
