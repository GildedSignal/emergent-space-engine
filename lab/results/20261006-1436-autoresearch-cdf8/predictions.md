# Predictions (written before the loop; held-out cases marked)

Artifact: `PlayerNeighbourhood::find` (crates/universe/src/encounter.rs), the plane's exact
encounter check — bottleneck #4 of the plane's measured list (190 µs per item).
Metric: ns per item (one item = one candidate body checked), release build, deterministic scenes.
Constraint (must hold everywhere, not a prediction): the returned encounter list — pairs, order,
ticks, contact bits — is bit-identical to the baseline on every scene and sweep.

## Hypotheses

- H0 (profile): the per-item cost is dominated by `other.cartesian(t)` (the tube decode: Kepler
  solve in exact Scalar arithmetic), not by `binding_at` (an Arc clone) or the integer `hit`.
- H1 (the change): an exact band pre-filter — the tube's key gives the radius band
  [periapsis, apoapsis] (or [periapsis, outer_radius] for a passage) and the speed bound
  (periapsis speed); with the residual's own magnitude and the turn's quantum added as padding,
  a body whose band cannot bring it within `near` of the player over the interval
  (|d| − |w| > near, with |w| ≤ (v_hi + |v|)·h by triangle inequality) is skipped before any
  decode. Conservative in every step, so it can only skip pairs the predicate would reject.

## Predictions on tuning scenes (I may look at these)

- P1: sparse belt (400 ships, radii log-spread over [1.5e8, 6e8] root units, one player at 3e8):
  ≥ 80% of items rejected before decode; ns/item drops ≥ 5×.
- P2: clustered belt (50 of 400 ships in one tight phase cluster so real encounters exist):
  ns/item within +15% of baseline (the filter must not slow down the pass-through case much).

## Held-out (will not tune on; run once at the end)

- HO1 (10× bodies, same distribution): ns/item within 2× of the 400-body value — the filter is
  O(1) per item, no hidden scaling with N.
- HO2 (eccentric, e = 0.5·2^48 in Q48): wider bands reject less; I predict ≥ 40% still rejected
  and ≥ 2× on ns/item. Bit-identity must hold.
- HO3 (tight cluster everywhere — every body inside the band of every other): ns/item ≤ baseline
  +20% (worst case for the filter: nothing rejected, padding arithmetic paid on every item).

## Kill criteria

- If H0 is false (decode < 50% of item cost), the band filter cannot reach 2×: revert it and
  pivot the loop to the integer fast path (skip the Scalar↔integer round-trips in the closure).
- If the filter changes any output bit on any scene: revert, the change is a law change, not a cost cut.
- Stop after three consecutive rounds gaining < 10% (lens rule).
