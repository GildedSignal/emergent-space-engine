# Predictions (held-out: seeds 2, 3, 4, 5 in `jet` mode; all tuning on seed 1)

Bench: `bench jet <seed>` in this folder (standalone crate, path deps, no crate edited).
The universe is driven exactly as the prior run's `kick` mode (900 frames, rtf 100, unlimited
budget, settle); digests must therefore equal the prior record's on seeds 2-3.

The question this run answers (the checker's named gold experiment, cheapest decisive parts):
can any reuse of a compiled cycle across the plane's kicks be bit-identical, what would the
re-anchored jet re-anchor on, and what does reuse cost per use against the fresh compile.

1. **Exact reuse never hits.** Over consecutive fired-kick pairs: exact `OrbitKey` repeats 0,
   exact `ShapeKey` repeats 0 (I allow ≤ 2 accidental hits); ShapeMemo first-encounter hits
   ≤ 1% of fired kicks, on every seed.
2. **The shipped quantized boundary does hit.** QuantizedMemo first-encounter hits ≥ 85% of
   fired kicks; MemoCode equality on consecutive pairs ≥ 90%; weak-branch shapes (compactness
   collapsed to zero) = 100% of fired kicks.
3. **No bit-identical reuse across a key step.** Between a body's consecutive compiled orbits:
   cycle increments (period, advance, proper period) bit-equal on ≤ 2 pairs, quarter-period
   state reads bit-equal on ≤ 2 pairs, per seed; the relative period change between consecutive
   keys has p50 in [10⁻¹⁰, 10⁻⁷] — far above the Scalar ulp (2.2×10⁻¹⁹), i.e. no rounding
   slack absorbs it.
4. **The jet's re-anchor never fires in the plane.** Per-kick key drift |dln| p50 in [10⁻¹⁰, 10⁻⁷],
   p95 ≤ 10⁻⁶; the accumulated signed drift crosses √(floor/C) = 7.3×10⁻⁴ zero times in 900
   frames on every seed (floor 10⁻⁶, C = 1.9 from red-team 20261006-0346).
5. **Reuse per use is ≥ 10× cheaper than the compile it replaces**: shape-hit/quant-hit ≤ 5 µs
   per call against a compile line of ≥ 30 µs on this box; compile stays 60–96% of the isolated
   `from_state` rebind (band, shared box; the point estimate moves run to run).
6. **Digests regenerate**: `jet` prints the same digest as the prior record's `kick` mode on
   seeds 2 and 3 (f8f522a9…, 2c5685c6…), and `kick`/`frame` modes reproduce heldout.txt.
7. **Sweep**: for fixed eccentricity the weak-branch compile (p ≥ 2¹⁸) has the same knot count
   at every p (the shape key collapses compactness to zero); compile cost grows with e — at
   e = 0.995 at least 3× the e = 0 cost at the same p.

Kill criteria for my claim: exact-reuse hits ≥ 5% on any seed (then a bit-identical memo
exists and the refutation dies), or bit-identity across a key step on ≥ 5% of pairs (then
rounding slack absorbs reuse and the digest-identical jet becomes conceivable).
