# Autoresearch log — run 20261006-1436-autoresearch-cdf8

Artifact: `PlayerNeighbourhood::find` (`crates/universe/src/encounter.rs`), the plane's exact
encounter check (bottleneck #4 of the plane's measured list). Metric: ns per item, median over
48 sweeps, release build, alternating call order to cancel warm-cache bias. Behaviour constraint:
the encounter list must stay bit-identical (`outputs_identical=true` in every line of the bench).

## Round 0 — baseline + profile

- Hypothesis (H0): the per-item cost is dominated by the tube decode (`other.cartesian(t)`).
- Measurement (`baseline.txt`): A (sparse circular belt, 401 bodies) 1496 ns/item, decode share
  1358 (91%); B (clustered eccentric) 3524, decode 3332 (94%); P (the plane, 28 bodies) 1248.
  `binding_at` is 20–34 ns/item — nothing. H0 held.

## Round 1 — exact band pre-filter (REVERTED)

- Hypothesis (H1): the tube's key bounds the body's distance from the doll's centre
  ([periapsis, apoapsis]; speed ≤ periapsis speed), so a body whose whole band stays farther than
  `near` of the player over the interval can be skipped before the decode. All steps padded away
  from rejection (residual and sub-quantum turn read from the binding).
- Change: `bands()` + skip test in `find` (saved: `round1-filter-encounter.rs`).
- Bug found on the way: capping the speed bound at `Scalar::ONE` (for null keys) clamped every
  body's bound to c, making the margin ~1e8 and rejecting nothing. Fixed to apply only to
  `key.null`.
- Measurement (clean build, alternating order):
  - A: 445 vs 1495 ns/item — 3.4×; 18424/18800 items (98%) rejected, outputs bit-identical.
  - B: 3880 vs 3450 — 12% SLOWER (bands computed, nothing rejected: eccentric clustered bands
    all overlap the player).
  - HO3: 3807 vs 3384 — +8% (pass-through overhead only).
  - P (the plane): **outputs differ** — 47 vs 69 encounters, 0 vs 19 contacts. Kill criterion
    (pre-registered: any output bit changes ⇒ revert) fired. REVERTED.
- Root cause, measured with an in-loop self-check (`UNSAFE SKIP: j=16 r_lo=1.4126e9
  r_hi=1.4249e9 x_hi=1.2426e9 margin=1.0765e8 actual_hit=true`): the body's readout distance from
  the doll's centre (~1.24e9) is BELOW its key's periapsis (1.41e9). For secondaries the tube is
  the pair's relative orbit (H0213: "a secondary's tube is the relative orbit"), not an orbit
  about the doll's origin — the band invariant is false for that class of binding. The filter
  needs a per-binding "centred on the doll's origin" condition (test-particle tubes only).

## Stopped

One round; the pre-registered kill criterion fired, so the change is reverted and the loop stops
(the lens's 10% rule never became the binding constraint). Best sound configuration: the
original finder plus this bench.

## What the loop produced

1. A bench (`crates/universe/examples/enc_bench.rs`) that A/Bs any future finder against a
   verbatim replica of today's loop with bit-identity checks and per-item timings, on six scenes
   including the plane itself — the instrument for whoever picks up bottleneck #4.
2. A falsified premise with its exact boundary: the radius-band pre-filter is sound and 3.4× on
   sparse circular belts, useless-to-harmful on eccentric clusters, and unsound on the plane
   today because secondaries' tubes are relative orbits. The fix is a flag, not a redesign.
3. A bench-methodology trap, hit and closed: A/B both ways (the first find of a pair warms the
   cycle memo; a one-sided order inflates the second caller by ~3×).
