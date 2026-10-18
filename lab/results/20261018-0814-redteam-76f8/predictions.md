# Predictions (written before the sweep runs)

Target premise: docs/representation.md L70–76 — two evaluation orders of one event
graph, sparse where "events per cell per light-crossing ≪ 1", dense (lockstep) where
that number "is near 1". Identity is guarded (r5, r5-starve); **the crossover — the
density at which lockstep becomes cheaper than the sparse core — has never been
measured.** The only datapoints (r5's bonus) are one density (the battle scene's fixed
5q spacing): sparse wins 28× at 2500 bodies.

Falsifier: `crates/engine/tests/xdense.rs` — my own seeded scenes on shipped code
(`Chronon` vs `EventCore`, law `es-lattice-relativistic-v1`, q = 1024, radius q/2 for
all bodies so the packing floor is exact), digests asserted equal in every cell. Two
scene families plus controls:

- **Gas** (the sustained-K probe): a boxed hot gas, grid spacing s ∈ {8q, 5q, 3q, 2q,
  1.5q, 1.25q, 1.0q} × genesis speed q/speed_div, speed_div ∈ {8, 4, 2}. The container
  confines (a battle scrum / cluster core), so K stays high for the whole horizon.
- **Slam** (the battle shape): two jittered grids closing at q/8 each, spacing swept,
  with and without shared fleet velocities (the sparse core's velocity classes).
- **Miss control**: the slam with the fleets offset so they never meet.

c = 1 quantum per chronon in this law (`check_speed_limit`: |k|² < q²), so a q×q
cell's light-crossing time is exactly one chronon: the doc's K is events per q²-cell
per chronon, and I report contacts per body per chronon alongside it.

## The predictions

- **P1 (miss control):** with zero contacts over the same horizon, the sparse core
  costs < 5% of lockstep (its calendar sits idle; lockstep re-bins n bodies every
  chronon, Ω(n log n · T)).
- **P2 (the crossover exists inside the physical range):** in the boxed gas the
  per-order walls cross somewhere between s = 3q and s = 1.0q at speed_div 4 — i.e. at
  a packing the game can reach (a ground-in scrap, touching bodies), lockstep wins on
  the CPU arm. Predicted crossover band: 0.02–0.3 contacts per body per chronon.
  Falsified if sparse stays ahead at s = 1.0q (touching, the physical floor) at every
  speed, or if lockstep already wins at s = 5q (then the battle scene's own density
  would have been dense-side and the r5 bonus reading is an artifact of the empty
  tail).
- **P3 (N does not move it):** at fixed density the winner does not flip between
  N = 400 and N = 6400 (both costs ~linear in N at fixed contact rate; only the sort's
  log n differs). Falsified if the crossover density shifts by more than one spacing
  step per 4× N.
- **P4 (fleets never reach it):** the slam in formation mode (one velocity per fleet →
  the sparse core's classes make the fleet's internals free) stays sparse-side at every
  spacing, and the non-formation slam stays sparse-side at every spacing ≥ 2q — the
  crossing is a transient, and post-contact dispersion drops K below the line. Falsified
  if any slam spacing crosses.
- **P5 (units):** both orders' `Metrics.ops` tell the same story as the walls (ops
  ratio within ~2× of the wall ratio in every cell) — if ops and walls disagree in
  direction anywhere, the instrument, not the premise, is suspect.

## What each outcome would mean

- P2 holds and P4 holds: the dense order's premise **survives with a measured domain**
  — confined grinds at near-touching packing only; no battle-shaped scene reaches it.
  The doc's Knudsen split is then right but its "battles" example is wrong-side.
- P2 fails (sparse wins everywhere ≥ s = q): the dense order's CPU arm has **no
  physical domain** — one order suffices at every reachable density on scalar CPUs,
  and the premise dies by deletion (principle 1: the best part is no part) unless the
  GPU/NEON arm can show a vectorization win inside the leftover band.
- P2 holds and P4 fails: the crossover is inside the game's own battles — the dense
  order is load-bearing exactly as written.

Held out: the gas cells at speed_div 2 (highest K), the N-sweep at s = 1.5q, and the
formation-slam row are tuned on none of these numbers; they are decided by the run.
