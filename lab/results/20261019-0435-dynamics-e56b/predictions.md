# Predictions — 20261019-0435-dynamics-e56b

Written before the decisive grid. Scene: `--scene mixed` (one coherent n/2 fleet at drift
q/4 crossing a thermal n/2 belt at cloudvmax = q/16, band [1.5e, 2.5e], Bounce box;
`--boxscale` moves only the far wall). Geometry says: at v = q/4 one box unit costs 4
chronons, so the fleet's oscillation period is 8·w and it crosses the band twice per
oscillation — **predicted contacts-hump spacing = 4·w chronons** (n=400 bs2 w=450 → 1800;
n=1600 bs2 w=870 → 3480; n=6400 bs2 w=1710 → 6840; n=1600 bs1 w=435 → 1740; bs3 w=1305 →
5220). Wall-hit humps (the fleet bouncing) sit between contacts humps, same 4·w clock.

- **P1 (mechanism).** Every bounce arm shows the 4·w clock in BOTH series (walls and
  contacts), spacing within ±15% of the median, contacts humps interleaved between wall
  humps. KILL: no periodicity, or spacing not tracking w — then the modulation is not
  wall-driven and "wall-reflection train" dies as the mechanism.
- **P2 (period law).** spacing/w = 4.0 ± 0.3 across n ∈ {400, 1600, 6400} (16× in n) and
  boxscale ∈ {1, 2, 3}.
- **P3 (amplitude).** Hump peak above the cloud-only baseline (`--nofleet` control) is
  CONSTANT across recurrences: last/first ≥ 0.7 (a wall-driven limit cycle; the fleet does
  not measurably ablate in the belt). Alternative branch, reported as such: decaying
  ≥ 2× over ≥ 4 humps → ringdown, and "the fleet stays coherent forever" is wrong.
- **P4 (duty).** Worst 64-ch window / late mean grows with boxscale (duty cycle falls):
  bs1 < bs2 < bs3; F64_late in bounce arms >> the cloud-only control's (~1-3).
- **P5 (free space).** `--free`: exactly one crossing season, then flat — late windows
  within ±25% of constant, late mean ≈ the nofleet control's late mean ±30%, walls = 0.
  KILL: recurrence in free space → the persistence is not the wall's.
- **P6 (unit cost).** Excess contacts per fleet body per crossing ≈ 0.4·per_row (90b7's
  one-shot figure), same order at every n.
- **P7 (seeds).** Seed 2 arms agree with seed 1 in spacing (±15%) and amplitude class.

Verdict rule: the wall-reflection train stands only if P1 ∧ P2 ∧ P5 hold. Controls on both
sides: nofleet (cloud alone, must show NO humps — flat) and the free arm (one season).
A control that fails voids the instrument.
