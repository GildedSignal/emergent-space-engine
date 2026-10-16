# Dossier — 20261016-2138-dynamics-217f (dynamics lens)

## Claim

The allocator's rollback feedback (`escalation *= 2` on every rollback, `alloc.rs:1410`) is a
one-way global ratchet with no restoring force: one conflict transient permanently widens every
region's forecast margin (measured frozen at ×4 through 34,000 chronons / 17 stages after two
conflicts), the conflicts self-quench exactly at the derived bound (forecast growth
`margin·E·vmax + (E−1)` ≥ achievable speed), and the permanent tax is paid as planned merges
that fresh anchors must then avoid (77–90 avoided/stage post-conflict vs 1–2 on the identical
geometry without conflicts — regions parked at merge windows, serialized, released); a
10-line decay mirror (halve at every conflict-free sync grid, env `ES_DECAY`, off = shipped
verbatim) restores the equilibrium at **bit-identical outcome digests**.

## Bottleneck

Not a board headline but principle 12's own object ("the algorithm that allocates the work…
it's the most important one") and principle 13 ("errors never compound"): no wiki page has
ever measured rollback/AIMD/stride/regroup dynamics (grep over all 31 pages: zero hits; the
allocator's scheduling was graded once, "idiot index 1.01", 825f, on conflict-free scenes).
The ratchet is the scan-queue latch's shape (69f3) found in the allocator: a monotone gate
with no decay. Gain: deletes the permanent over-margin class at 10 lines and prices the
conflict channel for billion-scale scenes, where regions are many and promise-breaking
accelerations (encounters, burns) are the norm.

## Evidence

Shipped code, public API only for the trajectories (staged `run_to`; per-stage counters —
`run_to` resets them; `speed_escalation` is current state). Conflict factory derived, not
fitted: a Fermi cannon (light body between two closing heavy bouncers, m 16384:1, ~2× per
bounce — measured 64 → 16384 quanta/chronon within 200 chronons on the bare stepper) aimed
at quiet 8-body clusters; `min_region: 1` (config knob) so clusters stay separate regions.

Newtonian battery (`batteryn`, 4 cells 8000 units apart, staggered ignitions; regen.sh):

| stage (2000 chr) | rollbacks | escal | merges avoided |
|---|---|---|---|
| 1 | 2 | 4.0 | 20 |
| 2–5 | 0 | 4.0 | 43→71 |
| 13–17 | 0 | **4.0 frozen** | 78→78/stage |

- Two conflicts at ignition, then **zero rollbacks forever** — the quench: after the
  conflicts, forecast growth 2·E·vmax ≥ any post-anchor speed, so no promise can break again.
- Escalation frozen at 4.0 through stage 17; **stride AIMD restores** (p50 back at the
  256-chronon sync grid) while escalation never does: same controller family, one
  self-heals, one latches (P3 held).
- The permanent tax: `merges_avoided` 77–90/stage vs **1–2/stage on the same geometry under
  the relativistic law** (battery, zero conflicts) — every avoided merge was a plan the
  over-wide margin forced and the fresh anchor had to undo; between plan and avoid the
  regions are parked (`Park::Wait`) at a merge window they then don't hold (P6's honest form:
  not throughput collapse — splits re-fine the partition, measured 4→32 regions — but a
  standing serialization tax of ~80 forced sync points per 2000 chronons).
- Relativistic battery (`battery`, 8000-unit cells; `batteryr`, 600-unit near cells): **zero
  rollbacks in any geometry** — at c-cap the conflict window is one stride (≤ c·stride ≈ 256
  units) and the plan catches everything else; P1's quench held with the conflicts never
  firing at all (stronger than the 1–2 predicted for the far scene; the near scene's 2–4
  predicted conflicts did not fire — the first post-ignition anchor closes the window).
- Decay arm (`ES_DECAY=1`): conflicts still fire when real (stage 1: 1 rollback), escalation
  returns to 1.0 by stage 2 and rides the boundary (bounded cycle, not a ratchet; P5 held),
  and the final world and outcome digests are **bit-identical to the shipped arm**
  (`964ee2e03c0b…` / `74db660c2e68…`, both arms) — the certificate holds; the ratchet moves
  scheduling, never results (P4 held).
- Instrument identity: staged `run_to` + `Report` fields only; no allocator line touched by
  the instrument (the example is new; the alloc.rs change is the ES_DECAY arm itself,
  default-off).

## Predictions

`predictions.md` was written before the battery runs (the mechanism, the quench bound, the
AIMD contrast, digest invariance). Held: quench (P1, stronger than stated — zero relativistic
conflicts), the Newtonian conflicts + frozen latch (P2's first half), AIMD-vs-ratchet
asymmetry (P3), digest invariance (P4), the decay cycle (P5). Missed, reported as held-out
honesty: P2's "region collapse toward 1" — splits re-fined the partition (4→32 regions), so
the latch's cost is the standing avoided-merge tax, not permanent single-region collapse;
P6's ≥2× throughput gap was not measured as stated (replaced by the avoided-merge tax and
utilisation columns; wall comparisons on a loaded box mislead by ±45%, b583's lesson).

## What would make it wrong

- The tax reading: `merges_avoided` counts plans undone by fresh anchors; if the parked-wait
  window costs nothing (regions would have idled anyway under the goal cap), the ratchet is
  harmless in batch — the frames harness (deadline misses, present rate) is the decisive
  surface, not flown here.
- Scale: 44 bodies, 4–8 workers. At billion-scale region counts the over-margin couples
  differently (every pair plans earlier); the quench bound itself is scale-free but the
  avoided-merge rate is not measured beyond this scene.
- The relativistic zero-conflict result is geometry-specific by construction (one-stride
  window); a scene with sub-stride-scale regions (dense belts) could still fire conflicts
  under Law::Relativistic — untested.

## Cost of adopting, fit with PRINCIPLES

Adoption is the 10-line decay mirror (or a per-region escalation — the ratchet is global but
conflicts are local; a slow region far from a conflict inherits ×2 margin forever, which is
the wrong locality). PRINCIPLES: "Errors never compound" (the margin compounds: ×2 per
conflict, never undone); "local laws" (the escalation is global state); "the simulation
decides, heuristics schedule" (the ratchet is a heuristic answering a measurement the
forecast could make directly: margin from c/vmax at genesis). One law at every scale: the
same decay mirror the belt's kick cadence and TCP's window live by.

## The lens

Dynamics missed the workload question: I built the cheapest bifurcation instrument, not a
flown scene, so the result prices the mechanism, not the game's real conflict rate. The
checker should fly the frames harness (`run_frames`, deadline misses) on a conflict-prone
scene — that is the named next experiment.

## Commands

`lab/results/20261016-2138-dynamics-217f/regen.sh` (each flight ≤ 60 s; ~4 min total
including build). Raw tables: the run log above; re-run any arm with
`cargo run -p emergent-allocator --release --offline --example ratchet -- <scene> 17 2000 1`.
