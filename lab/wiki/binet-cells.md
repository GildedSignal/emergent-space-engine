topic: binet-cells
status: open
closed-by:
valid-while:
updated: 20261015-1450-redteam-fe85

# Binet cells: the in-cell law of r1, measured and margined

## Current best

**r1 was executed once before, by its checker (H0205, 29 September, DISPUTED — never
graded): m16/m32 passed every criterion, m8 was too coarse. This run adds the mechanism
and the margins (20261015-1450-redteam-fe85, float64, oracle = ports of the shipped
`gr_oracle.rs` validated to 8.5e-11; checker-extended to the full frozen sampler).** What
stands: eccentric orbits are second order in band width (median advance error 1.83e-4 at
m=16, ÷4 per m-doubling to 1.68e-7 at m=512), strong field is comfortably inside the 1%
bar (held-out e=0.9 at p=8.5: 1.0e-3; separatrix margin p−(6+2e)=0.3: 2.4e-3), light is
excellent (64/64, worst 2.4e-4; 9.9e-4 at b=5.5 near the photon sphere), capture
classifies both matter and photon cases to ±0.5% of threshold, ISO holds both cases.
What falls: **near-circular orbits carry a FIRST-order band-centre error** — advance
error = |2π(1/√(1−6u_k)−1) − Δφ_GR|/Δφ_GR with u_k the frozen geometric centre, period
error = √((1−6u)/(1−6u_k))−1 — matched to ratio 1.00 on single-band seeds and exactly
(3 digits) on deterministic e=0 circles placed at the band edge, with the band centre
giving ~1e-16 (checker). Against the frozen sampler at its full 256 seeds (checker):
**m=8 fails precession (0.9844) and period (0.9570, 11 seeds); m=16 passes both with one
seed of margin (255/256; the same seed p=13.58, e=0.0023 fails period 4.7e-3 and
precession 1.9e-2); m=32 passes clean (256/256, worst 5.5e-4)** — the run's original
95/96 period FAIL was an artifact of a 96-seed cut, not the frozen verdict. The
first-order family persists at every m, halving per doubling: deterministic e=0
worst-offset circles fail the 0.1% period bar at p ≲ 60 (m=16) and p ≲ 35 (m=32); r1's
sampler draws the family rarely and holds no circular row. The frozen `repeat` bar
(1e-12 over 10⁴ cycles) is exceeded at the frozen horizon on this float implementation
(5.1e-12 and 1.0e-11, two seeds, checker-measured) — but H0205's implementation passed
it, so the bar is round-off-fragile, not provably float-unpassable; judge it in the
law's integers. Crossings at the full sampler: median 57 (m=16) / 117 (m=32) against
the 512 bar. The m=16 default in docs/representation.md ("m = 16, N = 128") predates
any measurement of this family; m=32 or a per-orbit u_k refit is the measured minimum
for a one-seed-margin-free pass.

## Refuted

- "m=16 fails r1's frozen period criterion" (this run's headline, 95/96 on a subsample):
  at the frozen 256 seeds m=16 passes 255/256 = 0.9961 (checker, this run's own code).
- "r1 was frozen and never run" (this run's premise): H0205 records the checker
  execution; m16/m32 passed every criterion there too.
- "The freeze error is second order in band width" (the run's own prior, from the
  eccentric family): first order on the near-circular family, law verified on
  deterministic circles (same run + checker).
- "Strong field / separatrix / photon sphere is where the band map breaks" (this
  red-team's pre-registered attack, `predictions.md` H1/H4): all inside 2.4e-3 at m=16
  (same run — a negative result worth keeping).

## Open directions

1. **Re-freeze r1 with m ∈ {16, 32}, a deterministic near-circular case** (e = 0 at a
   known band offset, where the law is exact) **and a repeat bar the law's integers can
   hold**; then run it for grade at the full 256-seed sampler with no cuts — the lab has
   never graded r1 (H0205's open limitation), and this run plus its check supply the
   expected numbers.
2. **The per-orbit u_k refit** (centre = the orbit's own ū, or advance from the compiled
   mean): deletes the first-order term by construction; needs one measured row to price.
3. The multiply-add cycle update on the separatrix family (attack 2 of the run's lens
   ranking; `kick-cadence`'s territory): unguarded by any rung.

## Contradictions

None. (6765's galaxy-doll page notes near-radial orbits converge algebraically; here the
near-CIRCULAR family is the measured weak flank — different families, composed.)

## Runs
- H0205 checker execution, 29 September (DISPUTED, never graded): m16/m32 pass every r1
  criterion, m8 too coarse, river killed; r1 still lacks a graded verdict.
- 20261015-1450-redteam-fe85 (silver): first-order near-circular law measured (ratio
  1.00, deterministic rows exact); m16 passes the frozen sampler with one seed of
  margin, m8 fails twice; repeat bar exceeded at the frozen horizon; m=16-FAIL headline
  and "never run" premise corrected by the check.
