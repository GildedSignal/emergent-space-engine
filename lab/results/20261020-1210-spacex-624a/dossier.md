# Dossier — the traversed fraction of a fresh mint (mint-knots od 1, flown)

## Claim

Between a mint and its discard the engine walks a median **14% (cycles) / 0.7%
(passages)** of the knot panels the mint eagerly compiled — **90% of all minted
quadrature panels are never landed in** (fleet arm: 1,104,124 knots minted,
105,241 panels touched) — so a walk-sized (lazy/streaming) compile deletes most
of the 2.7 µs/knot compile wall and the same share of the knot heap, on both
scoreboard rows at once; the over-provisioning is **inverse-sized**: the
≥100-knot mints (40% of all cycle knots, od 2's tail) walk a median **5.1%**.

## Bottleneck

`mint-knots` od 1: "the traversed fraction of a fresh mint before the next
rebind is NOT yet measured (the open experiment)". This decides the lever the
page named (lazy extension vs class-split) for the two rows it unifies: the
kick (75-160 µs vs ~50 ns floor, ~10³·³) and live memory (~5,100 B/body, of
which the compiled orbit ~43 knots × 88 B). Measured answer: the ceiling is
~10× on both; the class split is the wrong lever (both classes over-provision;
the waste tracks walk/cadence, not class).

## Evidence (all from `regen.sh`, ≤ 6 min; Linux/x86 shared box, orders of magnitude only)

Instrument: print-only census in `crates/space/src/orbit.rs` (work/patch.diff,
+189 lines, 0 deletions — purely additive): every minted `OrbitShape` records
class, knots, span; every readout panel landing (`outbound_at` refine panel,
`at_radius`, `crossing_state`) and every passage-tail hit is counted per mint.
Controls on both sides:
- **State-digest-neutral:** the end-state `digest` (the plane's cut digest —
  the physics identity) is bit-identical pristine↔patched on all three arms.
  **Instrument finding:** kick-bench's `replay_digest` is build-sensitive —
  deterministic across repeated runs of one binary (3/3 identical), unmoved by
  an xtask-only layout control (dead 531-byte static), but shifted by any
  crates/space codegen change — so it measures build identity, not behaviour;
  the end-state digest is the identity that binds. (frame-cost's note that a
  patch "deletes the refused/replay_digest fields — the replay-identity
  instrument itself" is the same fragility.)
- **Can pass:** `cargo test --release -p emergent-space mint_census` — a full-period walk reports coverage 0.85+ (1 passed).

| arm | class | mints | knots | never-landed | cov median | cov p90 | cov ≥ 0.9 |
|---|---|---|---|---|---|---|---|
| default (seed 1, rtf 1, 30 s) | cycle | 83 | 1,106 | 83.8% | 20% | 40% | 0 |
| default | passage | 22 | 3,392 | 98.7% | 0.68% | 2.7% | 0 |
| **fleet (seed 1, members 400, rtf 100, 30 s)** | cycle | 18,291 | 1,002,553 | **90.0%** | **14.3%** | 56% | **0** |
| fleet | passage | 676 | 101,571 | **93.5%** | **0.68%** | 21% | 0 |
| seed 3 (held out, rtf 100) | cycle | 2,354 | 95,309 | 89.7% | 20% | 60% | 0 |
| seed 3 | passage | 94 | 14,131 | 93.6% | 0.68% | 21% | 0 |

- **Not one of 21,449 mints reached coverage 0.9** — with the instrument proven
  able to report 0.85+ on a full walk, this is the engine's cadence, not a blind
  instrument: bindings never live a compiled span.
- **Inverse sizing:** fleet cycles ≥ 100 knots (3,025 mints, 399,440 knots =
  40% of cycle knots): coverage median 5.1%, max 26.2%. The 448-knot tail
  compiles ~1.2 ms of quadrature and walks ~5% of it. The eager geometric rule
  (ψ-bands doubling at CAP = π/4, orbit.rs append) sizes the mint by orbit
  *shape*; consumption is sized by *cadence* (time to the next rebind). They
  are unrelated, and no certificate sizes the span.
- **Long lifetimes don't rescue it:** top decile by readouts (50 touches
  cycles / 165 passages): coverage median 20%/24%.
- Passages' tail (compiled to the doll edge, 148 knots median) is the extreme:
  median 4 readouts between mint and discard.

Priced with bd4b's constants (2.7 µs/knot; knots = 85-91% of mint heap):
- fleet arm compile wall ≈ 1.10M knots × 2.7 µs ≈ **3.0 s per 30 s bench**,
  ~90% of it never consumed;
- memory plateau: the same share of the knot heap is never read at panel level.

**Design constraint the census also measures:** binary searches do read
`knots[mid].sum` table-wide (time→phase), so "never landed" prices the exact
per-panel *quadrature* (the expensive node() arithmetic) and the panel-level
reads, not the sum words. A lazy design keeps a searchable spine of exact sums
(e.g. every 8th knot eager: 12.5% upfront + ~10% on landing ≈ 14-23% of the
eager wall → **a 4-7× cut, ceiling 10×**). 5465's regeneration property (knots
regenerable from the key, digest a function of the key not the memo) keeps such
a cache law-neutral.

## Predictions (predictions.md, written before the decisive run)

- P1 cycles median < 30%: **held** (14-20%).
- P2 passages < 50% but above cycles: **half wrong** — 0.68%, *below* cycles;
  my exit-bisection reasoning overestimated passage walking (exit searches use
  `at_radius` as one guess probe, not arc-spanning walks).
- P3 bimodal with a ≥ 0.9 mode: **wrong** — no ≥ 0.9 mode exists at all
  (0 of 21,449); the distribution is short with a mid tail (p90 56%).
- P4 held-out seed within ±10 points: **held** (passages 0.68% both; cycles 14-20%).
- P5 median waste ≥ 60%: **held and exceeded** (90%).

## What would make it wrong

A scene whose bindings live longer than the fleet's (e.g. the belt's
one-kick-per-period cadence — there the cycle may genuinely traverse it all;
NOT measured here, the bench's belt stays unmeasured as before); view decodes
that sample a mint's span at random phases (the census counts them — view is
outside the resolver sample but inside `frame`, so the arms include it — but a
future view that samples phases table-wide would consume sums, not panels);
Adoption cost: one representation change on the knot memo (lazy extension
behind a sums spine), digest-neutral by construction, priced 4-7× on both rows.

Fit with PRINCIPLES: "Compute only surprises" (#3) — the mint is the
non-surprise paid eagerly; "a fix signals the wrong representation" (#19) — the
eager geometric span is sized by the wrong variable (shape, not cadence);
"Rough first, refine when a certificate could break" (#21) — walk-sized
compilation refines exactly when the walk reaches the edge.

## The lens (SpaceX)

Delete-and-rebuild is cheap for a rocket; here the finding *protects* a frozen
law: the lever is not deleting the memo (9edc/225d killed sharing) but cutting
its compiled extent to what the walk consumes — the idiot index of the mint
(panel compile cost ÷ panels walked) is ~10, measured per mint, and it worsens
exactly where the mint is most expensive. What this lens may have missed: the
belt (one-kick-per-period) could legitimately traverse full spans — the
class-split question survives there; and sum-word reads vs panel reads is a
distinction a requirements-first lens almost trampled.

## Commands

`lab/results/20261020-1210-spacex-624a/regen.sh` (≈6 min: two release builds
dominate; runs the control test, three pristine refs, three patched arms,
digest-neutrality check, and prints every number above via `summarize.py`).
Raw JSON: `work/cen-*.json`, `work/ref-*.json`, rows `work/census-fleet-rows.json`.
