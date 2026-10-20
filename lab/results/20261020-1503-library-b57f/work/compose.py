#!/usr/bin/env python3
"""The ask's three prices: composition on page constants only (every input cited).

Sources (page constants):
  [9ed1]  checker: answer bill 4.2-4.4 us/BODY at every rung (442.9 ms @1e5,
          847.8 @2e5, 1273.5 @3e5); en=178 on the worst 3e5 answer; ms/en 6.2-7.15
          vs 0.1-1 normal; TTL-proof; "at 1e9 one such answer is ~4 ks".
  [a31c]  era 27.9k gs at rtf 400 => 69.75 s era wall budget; kick comb at 1e9
          12.75 h/era = 658x budget (45.9 us/kick); boundary comb 2.39 h = 123x.
  [f102]  47.8% of burn captures are duplicate asks at ~44 us; no change-signal
          coarser than the candidate set certifies a duplicate (0 hits at every
          measured grain); direction (d) dead as stated.
  [0e9c/d7d1] walked/kept per capture: plane 72.7 walked / 32.5 kept; seam (N=3000)
          1841 walked per bail / 333 kept; 10^3 burn 1070 / 344; formation doll
          551.25 walked (K-sized doll); candidates identical both arms.
  [0346]  co-orbital gold: every real encounter lies within partner rank 4 along
          the orbit; phase-neighbour certificate at O(n*k).
  [be73]  the pin's compare form 0.34% of budget at 10^6 vs the shipped walk form
          124.93%: "the form, not the policy, carries the cost".
"""
US_BODY_LO, US_BODY_HI = 4.2e-6, 4.4e-6      # s per body per answer  [9ed1]
ERA_BUDGET_S = 69.75                          # era wall budget at rtf 400 [a31c]
KICK_COMB_1E9_S = 12.75 * 3600                # kick comb per era at 1e9 [a31c]
RANK_K = 4                                    # partner rank bound [0346]

print("== P2: the walk at 1e9 (kill bar [50,75]) ==")
for n in (1e5, 2e5, 3e5, 1e9):
    lo, hi = n * US_BODY_LO, n * US_BODY_HI
    print(f"  N={n:.0e}: one answer = {lo:.4g}-{hi:.4g} s"
          + (f" = {lo/ERA_BUDGET_S:.4g}-{hi/ERA_BUDGET_S:.4g}x the 69.75 s era budget" if n == 1e9 else ""))
meas = {1e5: 442.9e-3, 2e5: 847.8e-3, 3e5: 1273.5e-3}
for n, m in meas.items():
    print(f"  cross-check N={n:.0e}: law {n*US_BODY_LO*1e3:.0f}-{n*US_BODY_HI*1e3:.0f} ms vs measured {m*1e3:.1f} ms"
          f" -> ratio {m/(n*US_BODY_LO):.2f}-{m/(n*US_BODY_HI):.2f}")

print("== P3: discard asymmetry (walked population-proportional, kept scene-local) ==")
scenes = [  # (scene, walked, kept/answered)
    ("plane (N=0)",        72.7,   32.5),   # [0e9c]
    ("10^3 burn",          1070.0, 344.0),  # [0e9c]
    ("seam N=3000/bail",   1841.0, 333.0),  # [0e9c]
    ("3e5 answer (en)",    3e5,    178.0),  # [9ed1]
]
for name, w, k in scenes:
    print(f"  {name:20s} walked {w:>10.4g}  kept/answered {k:>7.4g}  discard {w/k:>10.4g}")
import math
ws = [math.log10(s[1]) for s in scenes]; ks = [math.log10(s[2]) for s in scenes]
print(f"  walked spans {10**(max(ws)-min(ws)):.4g}x across scenes; kept spans {10**(max(ks)-min(ks)):.4g}x")
for kept_at_1e9, tag in ((178.0, "en=178 class"), (333.0, "seam's 333 kept")):
    print(f"  1e9 discard with kept={kept_at_1e9:.0f} ({tag}): {1e9/kept_at_1e9:.3g}")

print("== the two exits, priced ==")
print(f"  (a) incremental answering: maintenance rides per-body events; the belt's kick comb at")
print(f"      1e9 is {KICK_COMB_1E9_S/ERA_BUDGET_S:.0f}x the era budget [a31c], and f102 measured NO")
print(f"      change-signal below the candidate set certifies an unchanged answer (0 hits at every")
print(f"      grain) -> the maintenance signal does not exist; per-body maintenance is the 658x wall.")
print(f"  (b) the tier: ask cost O(k), k<={RANK_K} [0346]; the seam is wired (universe.rs:469);")
print(f"      scheduling is exact integer arithmetic (crates/encounters, dioph).")
print(f"  be73's law generalized to the freeze channel: the form (walk vs compare/rank), not the")
print(f"      policy (TTL, stagger, cadence), carries the cost: 0.34% vs 124.93% at 10^6 on the pin.")

print("== the regime partition (dimensionless, radial.rs's own sentence) ==")
print("  out-of-band dolls: window misses the doll's registered range -> apsidal filter already O(few)")
print("  in-band (player inside the belt): 'the caller reads every body as before' -> the tier's k-window")
print("  the partition number: window-vs-registration coverage, already computed by ctx.radial.candidates")
