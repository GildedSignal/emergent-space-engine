# Dossier — 20261017-1447-dynamics-fd35 (dynamics lens)

## Claim

The finality race is a **state property, not a sampling fate**: on shipped code with a
print-only instrument, every realized conflict restores *exactly* at the published tick
(8,213 certify clashes over 45 arm-processes: `fin_hi − s0` min = max = **0**), the armed margin —
how far publication leads the deepest restorable truth an in-flight stride can still hit —
is measurable at every publish (HAZ), every certify (PRE), and every rollback (RB/FIRE),
so **a draw with armed ≤ 0 at every publish and D ≤ 0 at every certify cannot fire the
finality assert**: the engine-side fix's test can be a state certificate, not Monte Carlo
across windows (allocator-ratchet open direction 7, answered).

## Bottleneck

`lab/wiki/allocator-ratchet.md` direction 7: "making incidence a prediction instead of a
sampled draw would turn the fix's test into a certificate." The engine-side
publish/rollback boundary fix is confirmed necessary at protocol strength (01e7, bc0f);
until now its only test was incidence sampling (fat-tailed across windows, invisible at
endpoints). This run supplies the state quantity the fix can be tested against. No 10×
compute claim: this deletes the *test cost* (N-arm Monte Carlo) and names the exact
condition the fix must maintain.

## Evidence (all numbers from `regen.sh`, shipped tree + `work/patch.diff`)

Instrument (print-only, ~150 lines in `crates/allocator/src/alloc.rs` + the
`examples/race.rs` driver; no engine line touched):
- **HAZ** at every publish: `F` = max published `fin_hi`, `S` = deepest live truth start,
  `g = F − S`, and **A** = the per-pair armed margin: max over (busy stride B) × (live
  truth L) with B's hard-speed reach hull not separated from L's box, of
  `fin_hi(desc(B) ∪ desc(L)) − min(s_B, s_L)` (descendants = superset of rollback's
  snapshot closure).
- **PRE** before every certify (same lock hold, same measured box, same separation
  predicate): `D` = the largest `fin_hi − s0` the upcoming clash would restore. `D > 0`
  ⟺ the assert will fire (modulo the closure superset).
- **RB/FIRE** inside rollback: the exact assert inputs, before the untouched assert.

Arms (one process each; `race <n> <seed> <min_region> <rate> <s> <win> <smax> <vmax> <sp> <sab> <ahead>`):
- churn-loaded (n=3000×4 clusters, sp=40, vmax=64, sab=3, min=1, rate=2400, ahead=1.0):
  seeds 11/15/21/2 (+replicates 11/15) — the scene-start band where the page's frames
  crashes lived (742 genesis regions, present pinned at 12/s, ~1,300 rollbacks per 4-s arm).
- fast-dispersal (n=1000, sp=100, vmax=160, sab=3, rate=600): seeds 11/15/21/2 (+reps).
- controls: min_region=32 (4 rollbacks vs ~1,300 — the knob deletes conflicts, 326×);
  single gas vmax=2 (2,000 single-body regions, 0 rollbacks — the no-conflict class).
- probe h_128_60 (vmax=128, sp=60, no sabotage): the **armed episode**.

Results (`analyze.py matrix`):
1. **The equality law.** 2,515 clashes in the 14 matrix arms (8,213 over all 45 arm
   processes): `minD = maxD = 0`, every RB margin `m = 0`. Publication is *pinned at the
   contact boundary*: finality's coalescing (`alone_at`) and the certificate's separation
   (`certify`) agree exactly on the contact tick. No clash ever arrives with slack
   (no negative D): publication never lags a restorable conflict either — the coupled
   system sits on the boundary as an attractor, both sides pushing onto it.
2. **The armed episode (the race seen in state).** h_128_60: one pair (busy region b2 ×
   truth t1, s=1792), margin A = 48 → 128 over 10 publishes (F 1840 → 1920 while S
   stuck at 1792), then resolved **by pruning**: at p=98 every truth aged out (S = −1)
   and b2's stride certified clean. Zero rollbacks in that whole arm. The race has two
   resolution channels — conflict (fires iff A > 0 at contact) and pruning (the hazard
   evaporates) — and incidence is the probability the first channel wins while armed.
3. **The negative certificate.** Across all 45 arm-processes: `fires = 0`, `posA = 4/13,034`
   publishes (all four in the one probe arm), every PRE `D ≤ 0`. Armed ≤ 0 at every
   publish + D ≤ 0 at every certify ⇒ the assert is unreachable for the draw — decided
   from state, not from surviving N windows. Replicate check (seed 11 churn): rollback
   counts move with the schedule (1,305 vs 1,326 — incidence is wall-clock-raced, as
   bc0f found) but the equality law holds in both (all D = 0, maxA = 0).
4. **The fix's cost on these classes** is the armed margin it must refuse: ≤ 128
   chronons once (10 publishes) in the dispersal probe, ≤ 48–96 in churn, 0 elsewhere —
   a hold-publication fix loses at most one burst of lead here.

## Predictions

`predictions.md` was written before the matrix. P1 (0 fires in 14 arms) **held**; P2
(armed never positive in matrix arms) **held** (the probe arm's 4 positive publishes are
the armed episode, outside the matrix); P3 (the equality law, exact) **held**; P4
(min_region=32 ≈ 0 rollbacks) **held approximately** (4 vs ~1,300); P5 (a fire shows
armed > 0 first) **untested — nothing fired**.

## What would make it wrong

- The positive direction (crash ⇒ armed > 0 at an earlier publish) is untested: I did
  not reproduce a firing assert in this window (0/45 arm-processes vs the page's 7/12 on their
  selfchurn harness, which lives on their branch). My scenes are faithful *classes*
  (scene-start churn, dispersal) but not their exact draw; the instrument's positive
  side needs one reproduction on their harness — the named next experiment.
- `PRE D > 0 ⟺ fire` is proven only against my descendants-superset closure; no D > 0
  event was ever observed to compare against a real assert (a false-positive closure
  would over-arm, never miss a fire — the safe direction, but its sharpness at contact
  is unmeasured).
- The armed margin uses the law's hard speed for reach (sound upper bound); a violating
  law sample would void light-cone finality wholesale (`lightcone = None`), outside this
  analysis.

## Cost of adopting, fit with PRINCIPLES

The patch is print-only and behind nothing (test harness only; ~150 lines). A production
version is the fix's own gate: "never publish past the deepest restorable truth an
in-flight stride can hit" — which is exactly "armed ≤ 0 maintained by construction", the
state the fix must hold. PRINCIPLES 12 ("the algorithm that allocates the work… the most
important one") and 13 ("errors never compound"): the equality law shows the shipped
scheduler already pins the boundary; the fix only has to refuse the excursions. Principle
2: the certificate judges the representation (state), not the sampling.

## The lens

The dynamics lens found the attractor (boundary equality) and the excursion channels
(conflict vs pruning) but spent its window reconstructing the crashing scene class; the
positive-side prediction (lead time before a fire) remains one reproduction away. What
the lens may have missed: the geometry of *why* the two mechanisms agree exactly
(`alone_at`'s per-part v-growth vs `certify`'s hull-over-stride) — a derivation worth
one focused run, since it is the soundness argument the fix will be written against.
