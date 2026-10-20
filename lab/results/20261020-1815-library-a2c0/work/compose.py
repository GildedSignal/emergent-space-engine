#!/usr/bin/env python3
"""compose.py — the answer channel's 1e9 bill under the carry bound (23a6), and the
single-doll era ledger. Composition only: every constant is page-cited; no flight.
Pages: lab/wiki/nladder.md (23a6, a0a1, 9ed1, 8365, ca63, a31c entries)."""
import math

# ---- page-cited constants -----------------------------------------------------
# 23a6 (second author on a0a1), nladder.md line ~12:
COLD_US = 3.86          # us/body, the one cold lump per flight
SKIP_COLD = 0.109       # cold-lump skip fraction (10.9%)
WARM_MEAN = 0.041       # us/body, warm belt-wide answers (best 0.030)
WARM_BEST = 0.030
N_ANSWERS = 41          # belt-wide answers in the flight
FLIGHT_GS = 30_000.0    # the 1e5 flight length
SKIP_MEAN_PUB = 0.9755  # published mean skip over 4.1e6 bound decisions
CAP_ALL_US = 0.267      # us/body, capture ALL-walk, 1e5 (OFF arm)
CUT3E5_GS = 19_500.0    # 23a6's 3e5 canonical cut
# a0a1 (taleb), nladder.md line ~14:
READ_LAW = (4.17, 4.5)  # us/body, the cartesian read law (answer walk)
CAP_CHANNEL_MS = 2_986.0  # capture-channel ms over 3,107 captures at 1e5
CAP_ALL_MS_1E5 = 28.9     # one ALL-walk at 1e5
ALLWALKS_3E5 = 126         # counted ALL-walks at 3e5 (checker: 125; band kept)
# 9ed1 (taleb), nladder.md: staggered and off arms both:
LAMBDA = 4.889e-5        # kicks/body/gs at 1e5
# 8365 (second author on 0a46):
ERA_GS = 27_900.0        # gs per era (the ships' shared clock period)
# a31c (library), nladder.md line ~19:
ERA_BUDGET_S = 69.75     # s of wall per era at rtf 400 (27,900/400)
KICK_COMB_H = 12.75      # h/era at 1e9 (45.9 us/kick)
BOUNDARY_COMB_H = 2.39   # h/era at 1e9 (deleted by a31c's arm; kept row for reference)
# the target:
N = 1e9
FRAME_BUDGET_MS = 12.0

def h(sec): return sec / 3600.0

print("== P1: the cold point prices a miss-read (both-sided control)")
c_read = COLD_US / (1.0 - SKIP_COLD)
print(f"  miss-read from 23a6's cold lump: {c_read:.2f} us/body"
      f"  | a0a1's law {READ_LAW[0]}-{READ_LAW[1]}  | inside law: "
      f"{READ_LAW[0] <= c_read <= READ_LAW[1]} (ratio to band edges "
      f"{c_read/READ_LAW[1]:.2f}-{c_read/READ_LAW[0]:.2f})")

print("== P2: the memo's dirty-per-kick ratio delta, from the warm point")
gap = FLIGHT_GS / N_ANSWERS
lam_gap = LAMBDA * gap
print(f"  uniform inter-answer gap {gap:.0f} gs -> kicks/body/gap {lam_gap:.4f}")
for cc in (0.0, 0.02):
    for w, name in ((WARM_MEAN, "mean"), (WARM_BEST, "best")):
        miss = (w - cc) / c_read
        delta = -math.log1p(-miss) / lam_gap if 0 < miss < 1 else float("nan")
        print(f"  c_check={cc:.2f} warm {name} {w:.3f}: miss {100*miss:.2f}%"
              f" -> delta {delta:.3f}")
d_lo, d_hi = 0.05, 0.30   # fitted band across the four corners
print(f"  fitted band delta in [{d_lo}, {d_hi}] (letter: < 0.5) ;"
      f" registered alternative delta=1 with clustered gaps")

print("== P3: the published mean skip is the warm+cold mixture")
warm_skip = 1.0 - (WARM_MEAN / c_read)          # c_check = 0 reading
mix = ((N_ANSWERS - 1) * warm_skip + SKIP_COLD) / N_ANSWERS
print(f"  warm-only skip {100*warm_skip:.1f}% ; mixture over {N_ANSWERS} answers"
      f" {100*mix:.1f}% vs published {100*SKIP_MEAN_PUB:.2f}%"
      f" (|diff| {abs(mix-SKIP_MEAN_PUB)*100:.2f} pp)")

print("== P4: the 1e9 extension is cadence-bound; the total is not")
for d in (d_lo, d_hi, 1.0):
    stale_era = 1.0 - math.exp(-d * LAMBDA * ERA_GS)
    single = stale_era * c_read * N / 1e6                      # s, one answer/era
    per_era = d * LAMBDA * ERA_GS * c_read * N / 1e6           # s, any cadence
    print(f"  delta={d:.2f}: era staleness {100*stale_era:.0f}% ; single warm-at-era"
          f" answer {single:,.0f} s = {single/ERA_BUDGET_S:.1f}x budget ;"
          f" per-era read bill (cadence-invariant) {per_era:,.0f} s"
          f" = {per_era/ERA_BUDGET_S:.1f}x budget = {h(per_era):.2f} h")
closure = (ERA_GS / gap) * WARM_MEAN * N / 1e6
print(f"  closure: {ERA_GS/gap:.0f} answers/era x 41 s = {closure:,.0f} s"
      f" (must land on the delta~0.27 branch above)")

print("== P5: the single-doll 1e9 era ledger (rtf 400, budget"
      f" {ERA_BUDGET_S} s = {h(ERA_BUDGET_S)*1000:.1f} ms-equivalents)")
aw_1e5 = CAP_CHANNEL_MS / CAP_ALL_MS_1E5 * (ERA_GS / FLIGHT_GS)   # upper bound
aw_3e5 = ALLWALKS_3E5 * (ERA_GS / CUT3E5_GS)                       # counted
walk_s = CAP_ALL_US * N / 1e6
cap_lo, cap_hi = aw_1e5 * walk_s, aw_3e5 * walk_s
ans_lo, ans_hi = d_lo * LAMBDA * ERA_GS * c_read * N / 1e6, d_hi * LAMBDA * ERA_GS * c_read * N / 1e6
kick = KICK_COMB_H * 3600
tot_lo, tot_hi = kick + cap_lo + ans_lo, kick + cap_hi + ans_hi
print(f"  capture ALL-walks: {aw_1e5:.0f}/era (1e5 upper bound) - {aw_3e5:.0f}/era"
      f" (counted 3e5) x {walk_s:.0f} s = {h(cap_lo):.1f}-{h(cap_hi):.1f} h/era"
      f" = {cap_lo/ERA_BUDGET_S:.0f}-{cap_hi/ERA_BUDGET_S:.0f}x budget,"
      f" each ONE {walk_s:.0f}-s frame on the player's item")
print(f"  kick comb (a31c): {KICK_COMB_H:.2f} h/era = {kick/ERA_BUDGET_S:.0f}x ;"
      f" boundary comb deleted (kept: {BOUNDARY_COMB_H:.2f} h)")
print(f"  answer reads with the bound: {h(ans_lo):.2f}-{h(ans_hi):.2f} h/era"
      f" = {ans_lo/ERA_BUDGET_S:.1f}-{ans_hi/ERA_BUDGET_S:.1f}x budget")
print(f"  TOTAL {h(tot_lo):.1f}-{h(tot_hi):.1f} h/era ="
      f" {tot_lo/ERA_BUDGET_S:,.0f}-{tot_hi/ERA_BUDGET_S:,.0f}x budget ;"
      f" answer share {100*ans_lo/tot_hi:.1f}-{100*ans_hi/tot_lo:.1f}% ;"
      f" capture share {100*cap_lo/tot_hi:.0f}-{100*cap_hi/tot_lo:.0f}% ;"
      f" kick share {100*kick/tot_lo:.0f}-{100*kick/tot_hi:.0f}%")

print("== P6: the capture walk already busts the frame below every flown rung")
x = FRAME_BUDGET_MS * 1e3 / CAP_ALL_US
print(f"  0.267 us/body x N > 12 ms at N > {x:.2e} ; measured anchor 28.9 ms at 1e5"
      f" -> {28.9e3/1e5:.3f} us/body (band 0.25-0.30)")
