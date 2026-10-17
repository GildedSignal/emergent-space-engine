topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261016-2138-dynamics-217f

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The rollback controller has no restoring force, and the conflict process quenches itself
exactly at the derived bound (20261016-2138-dynamics-217f, dynamics lens, shipped
`crates/allocator` + public-API trajectory instrument; patch = the `ratchet` example and the
default-off `ES_DECAY` arm).** `escalation *= 2` at every rollback (`alloc.rs:1410`) is
global (one conflict doubles every region's margin) and never decays. Conflict factory
(derived, not fitted): a Fermi cannon — a light body between two closing m=16384 bouncers,
~2× per bounce, measured 64→16384 quanta/chronon within 200 chronons on the bare stepper —
outruns the per-stride forecast (margin·vmax from the last anchor) into a neighbour region's
true box before any planned merge catches it. Newtonian battery (4 cells, staggered
ignitions, 17 stages × 2000 chronons): conflicts fire at ignition only (1–4 rollbacks,
run-to-run timing-nondeterministic — the checker's identical reruns latched ×2, ×2 and ×4;
the fix phase saw ×16), then zero forever — the
quench, because forecast growth `margin·E·vmax + (E−1)` ≥ any achievable post-anchor speed
makes promises unbreakable — while escalation froze at its ignition power of 2 through stage
17 and the checker's 40-stage run (80,000 chronons; digest-identical across arms at both
horizons; stride AIMD
restored to the 256-chronon grid in the same run: one controller of the pair self-heals, the
other latches). The tax: `merges_avoided` 72–90/stage latched — but the ×50 contrast against
the 1–2/stage relativistic twin is law-confounded: the decay arm at escalation 1.0 on the
**same Newtonian scene** still pays ~54/stage, so the ratchet-attributable component is
~×1.5, and the checker's flight of the frames harness (60 Hz, rates 15k/30k, 3 reps/arm)
shows no shipped-vs-decay deadline-miss separation at 44 bodies — the tax is unproven where
the player feels it (regions
parked at planned merge windows that fresh anchors then undo). The decay arm's own cost:
re-opening the window refires conflicts (6 rollbacks / 10,832 wasted ops at stage 1 vs 2 /
5,656 shipped in the regen run). Under `Law::Relativistic` no
geometry tried fired any conflict — including the checker's 200-unit cells, closer than the
author's 600: at c-cap the conflict window is one stride (≤ c·stride ≈
256 units) and the plan catches the rest; no relativistic geometry has ever latched the
ratchet. The 10-line decay mirror (`ES_DECAY`: halve the
escalation at every conflict-free sync grid; off = shipped verbatim) restores the equilibrium
— conflicts still fire when real, escalation rides the boundary at 1–2 instead of freezing —
at **bit-identical outcome digests** to the shipped arm (`964ee2e0…`/`74db660c2e`, both arms):
the certificate moves scheduling, never results. Splits re-fine the partition after the
coarsening (4→32 regions; one checker rerun sat at 9 regions for ~6 stages, so this too is
one sample), so the latch's measured cost is the standing avoided-merge tax,
not permanent region collapse. min_region=1 (config knob) throughout so clusters stay
separate regions.

## Refuted

- **"The rollback response is a controller"**: it is half a controller — the AIMD stride
  half restores (+1/accepted, halved on rollback), the escalation half only doubles; measured
  frozen at its ignition power of 2 for 32,000 (author) and 80,000 (checker) chronons after
  the last conflict; the exponent itself is a nondeterministic sample, 2–16 across runs
  (20261016-2138-dynamics-217f).
- **"Rollbacks cascade"** (the lens's branching-ratio worry): measured self-quenching — each
  rollback widens every forecast, so conflicts go extinct at the derived bound; the danger is
  the permanent over-margin, not a cascade (20261016-2138-dynamics-217f).
- **"Conflicts are a Newtonian-law pathology, so nothing needs measuring"**: the mechanism is
  law-independent (any post-anchor acceleration past margin·vmax breaks a promise); the
  relativistic quench is a one-stride window, not an absence — sub-stride-scale region
  geometries are unmeasured (20261016-2138-dynamics-217f; the checker's 200-unit-cell probe,
  closer than any author scene, still fired zero).

## Open directions

1. **The frames-harness flight** (this run's named next experiment): conflict-prone scene
   under `run_frames` — deadline misses, present rate, buffer — shipped arm vs `ES_DECAY`,
   pricing the avoided-merge tax where the player feels it. Batch mode can hide it (regions
   idle under the goal cap anyway). **Checker's first flight: no separation** — deadline
   misses shipped [1,1,1]/[5,8,1] vs decay [1,1,1]/[7,1,1] at rates 15k/30k, 44 bodies,
   noise-dominated; a tax must beat this bar at scale before adoption is worth more than
   hygiene.
2. **Per-region escalation**: the ratchet is global but conflicts are local; a slow region
   far from a conflict inherits ×2 forever. The decay mirror is the 10-line fix; locality is
   the representation fix (PRINCIPLES: "local laws").
3. **Margin from the law, not from history**: the quench bound says the safe margin is
   `c/vmax` at genesis — the escalation state may be deletable outright for relativistic
   scenes (margin 2 + c-cap already made every tried geometry conflict-free).
4. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far, including this one, is a synthetic cannon.

## Contradictions

None open.

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
  global, permanent, self-quenching conflicts, AIMD the only restoring half; decay mirror
  digest-identical.
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
  reproduced and extended (80k chronons, 200-unit relativistic cells); tax magnitude
  law-confounded (~×1.5 same-scene, not ×50), frames flight shows no separation at 44 bodies,
  latch exponent nondeterministic across runs.
