topic: binet-cells
status: open
closed-by:
valid-while:
updated: 20261015-2041-redteam-0e9d

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

**The kicked half of the same in-cell law is now measured, and its update sentence is
dead at the separatrix (20261015-2041-redteam-0e9d, float64, closed forms + numeric GR
Binet; harness control 2.3e-6).** Design §3's "a kick updates the cycle by a
multiply-add": per-kick cycle error = **(15/8)·(δE/|E|)²** exactly (Newtonian, x =
2√(1+e)·δv/(1−e) at periapsis), so the 1% bar breaks at **e ≥ 0.9616** for
encounter-scale kicks (δv = 1e−3 of periapsis speed), **e ≥ 0.6483** for
deep-passage kicks (1e−2 — B13's regime, the top ~30% of r1's e ≤ 0.9 sampler), and
everywhere for slingshots; the belt's own 2⁻²³ quantum is safe to e = 0.999995.
Storing ∂² (two more numbers per record) widens the band only 2.3× (e ≥ 0.983 / 0.837).
Chaining compounds: after 200 ±1e−3 periapsis kicks the schedule errs 7.1 turns
(fresh-derivative, the design's best reading) and 139 turns (chained record); 18
one-sided kicks eject an e = 0.95 body with the comet 125° wrong on the sky first.
At the GR bound/plunge separatrix (numeric Binet,
E = 0.95, L_sep = 3.5501, window edge +2.0%): **T = 192.7 + 21.8·ln(1/d)** — log
divergence, ∂T/∂L ~ d⁻¹ — a kick with δL = distance-to-boundary errs 4.9%, and a kick
across the boundary makes the multiply-add predict a bound cycle (T = 365) where the
truth is plunge (wrong error *type*, not size). **What survives untouched:** the ring
grid's crossing budget holds into the tail (319 ≤ 512 at e = 0.999; 530 only at
e ≥ 0.99999 — recompile is cheap exactly where the multiply-add dies), and the
shared-record *lookup* is self-similar in relative E-width (T-sensitivity (3/2)·w,
constant in e) — the memo idea stands; only the linear update law breaks. Fix (one
step): a dimensionless recompile trigger |δE|/|E| and |δL|/|L−L_sep| vs √(8·bar/15)
(constants-free, representation not scheduling) — the shipped plane already pays it
implicitly (one full cycle rebind per distinct kick, kick-cadence's record).
**[checker, 0e9d]** This kill is kick-jet's, not new: law.md retired the sentence on
12 October (six golds; "a kick recompiles its cycle exactly"), and kick-jet's record
already holds the constant ((15/8)(δE/(1−E))², 9a04 gold), the
plunge-fabricated-as-bound type error (4978 gold) and the both-ends root-distance
certificate (ee08 gold) — measured on the shipped integer law and the wired plane,
stronger instruments than this float doll. New here only: the periapsis e* table (a
periapsis boundary — apoapsis kicks of the same size err 10⁴–10⁶× less), the T(L)
log-fit constants (a family that exists only for E ≥ √(8/9); the 4.9% headline is
the worst point of a narrow band), and the ring-crossing budget into the tail. The
adoptable residue is a doc sync: representation.md §3 still carries the retired
sentence.

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
- **"A kick updates the cycle by a multiply-add" as a universal law (design §3): the
  error is (15/8)(δE/|E|)² — 16.3% at (e = 0.99, δv = 1e−3), inside r1's sampler
  family and B13's regime; it compounds across kicks and cannot see the plunge class
  change (20261015-2041-redteam-0e9d). Survives its measured domain: belt-quantum kicks
  to e = 0.99999, x ≲ 1e−4 anywhere (control 1.9e−8). Already known when measured:
  kick-jet's golds 4978/9a04/ee08 and law.md's retirement (12 October) — this run
  re-derives it in float, on the draft sentence only. [checker]

## Open directions

1. **Re-freeze r1 with m ∈ {16, 32}, a deterministic near-circular case** (e = 0 at a
   known band offset, where the law is exact) **and a repeat bar the law's integers can
   hold**; then run it for grade at the full 256-seed sampler with no cuts — the lab has
   never graded r1 (H0205's open limitation), and this run plus its check supply the
   expected numbers.
2. **The per-orbit u_k refit** (centre = the orbit's own ū, or advance from the compiled
   mean): deletes the first-order term by construction; needs one measured row to price.
3. **(answered by 20261015-2041-redteam-0e9d)** The multiply-add cycle update on the
   separatrix family, previously unguarded by any rung: measured dead at e ≥ 0.9616
   (encounter kicks) / across the plunge boundary; **no rung catches it — r2 is the
   nearest home** and should add a kicked near-separatrix arm (e ≥ 0.99, x ≥ 0.1)
   judged on per-kick Δt error against the exact recompile, with the benign circular
   row as the control that must pass. The recompile trigger (|δE|/|E| vs √(8·bar/15),
   plus the L-side ratio at the plunge separatrix) is the adoptable form; its cost is
   log-bounded by the ring grid (319 crossings at e = 0.999).

## Contradictions

None. (6765's galaxy-doll page notes near-radial orbits converge algebraically; here
the near-CIRCULAR family is the measured weak flank — different families, composed.
The multiply-add kill and kick-cadence's "one full cycle rebind per kick" on the
shipped plane are the same fact read from two sides: the plane already recompiles, so
the fix prices what is already paid there.)

## Runs
- H0205 checker execution, 29 September (DISPUTED, never graded): m16/m32 pass every r1
  criterion, m8 too coarse, river killed; r1 still lacks a graded verdict.
- 20261015-1450-redteam-fe85 (silver): first-order near-circular law measured (ratio
  1.00, deterministic rows exact); m16 passes the frozen sampler with one seed of
  margin, m8 fails twice; repeat bar exceeded at the frozen horizon; m=16-FAIL headline
  and "never run" premise corrected by the check.
- 20261015-2041-redteam-0e9d (lead: the kill is kick-jet's, already retired in law.md
  12 Oct — 4978/9a04/ee08; new only the e* table, the log-fit constants and the ring
  budget; representation.md §3 needs syncing to law.md): the kicked cycle update
  measured — (15/8)(δE/|E|)² per kick, 1% bar at e ≥ 0.9616 (encounter) / 0.6483 (deep
  passage); compounding 7.1–139 turns per 200 kicks; GR plunge separatrix log-divergent
  with the multiply-add blind to the class change; ring-grid budget and relative-width
  memo lookup both survive; recompile trigger the fix.
