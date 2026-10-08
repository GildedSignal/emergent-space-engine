# Predictions (written before the scaling runs)

Baseline measured (shipped code, rtf=1, 30 s, 39 bodies + 48 fleet members):
frame CPU p50 3.30 ms; view_gather p50 2.37 ms (74.2% share), view_json 0.53 (14.6%),
wire 0.24 (6.7%), engine 0.15 (4.5%, but max 11.8 ms). At rtf=100: engine p99 5.24 ms,
36/1800 overflow frames, rtf lowest 1% = 17.

Code reading (not yet measured): `gather_with` (crates/universe/src/view.rs) runs
`for i in 0..u.n_bodies()` with a Newton light-cone crossing per body (1–3 `state_rate`
readouts each: doll-chain walk + checked-Scalar ramp) and then loops every fleet member
(velocity extrapolation + one `String` clone per seen emitter). No distance, brightness
or change culling anywhere in the loop.

## Held-out cases (not tuned on)

1. **Bodies scaling** (12 → 120 → 1200 star ships, members fixed at 48): view_gather p50
   grows linearly in body count, slope 20–90 µs per body per frame (the crossing path).
   At 1200 ships the gather alone is 25–100 ms: over the 16.7 ms frame budget by itself,
   with the engine still inside its 5 ms budget.
2. **Members scaling** (48 → 1600 → 6400, ships fixed): view_gather grows linearly in
   members with slope 0.3–2 µs per member (extrapolation + String alloc), i.e. cheaper
   per head than a body's crossing. The fleet member loop is the cheaper of the two O(N)
   terms.
3. **Shares invert only at high rtf**: at rtf=100 the engine's p99 reaches its 5 ms
   budget (measured: 5.24 ms, 36 overflow frames) while the gather stays flat per frame —
   the engine tail, not the gather, is what pulls rtf's lowest 1% down to ~17.

## What would falsify the constraint claim

- If view_gather stays flat as bodies grow 100× (some culling or cache I missed), the
  constraint moves back to the engine's kick tail and my claim is wrong.
- If the engine's overflow at rtf=100 grows to dominate frame CPU share (>50%) before
  the gather does at the plane's own scale, the engine is the constraint even at rtf=1
  scale and the view is a later problem.
