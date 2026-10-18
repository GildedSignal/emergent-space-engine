# Predictions (written before the decisive run)

Question: does the seen stream's content law (cc75's coast census) survive the burning player,
and is the burn's far-field churn observer-side (aberration, a K-independent recompose of a
stored record) or emitter-side (a churn that forces the K-walk every frame)?

Held-out cases (not tuned on): the burn arm at every K, the stride-5 deltas at 1e5, and the
shift (patina) churn. Controls: the coast arm must reproduce cc75/62c1's statics.

- **P1 (control, cc75):** at 1e4 coast, far rows (light-seconds ≥ 100) ≥ 1.2e4, occupied sky
  cells at θ_f = 8e-3 = 785-786 (capacity 2π/θ_f), alone-in-cell fraction < 0.01; the near set
  (light-seconds < 100) 340-360 rows.
- **P2 (control, 62c1/649c):** coast per-frame far-row churn is pixel-static: ≥ 99% of far rows
  stay in their sky cell across consecutive frames, at every K flown (1e3-1e5).
- **P3 (the wildcard, decomposition):** under continuous L8 burn at 1e4, the per-frame change of
  the *displayed* direction (aberrated) is dominated by the observer's β change, and the
  *emitter-side* change (angle of `offset`, the root-frame direction: parallax + light-cone
  sweep + emitter motion) stays below θ_f/10 for ≥ 99% of far rows. **KILL:** if > 1% of far
  rows move emitter-side by more than θ_f in one census interval, the burn's churn is not a
  recompose and the record over the cold store cannot serve the wildcard.
- **P4 (aggregate churn):** the number of sky cells whose far-row count changes per census
  interval stays ≤ 5% of occupied cells under L8 burn (≤ 0.5% coast) — the re-binning is local,
  not a global re-hash.
- **P5 (K-law):** the *fraction* of far rows changing cell per interval is K-flat under burn
  (set by dβ/θ_f, not by N). If the fraction grows with K, something besides aberration drives it.
- **P6 (patina):** per-frame |Δ ln shift| of far rows under burn has p99 ≤ 0.02 (the Doppler
  swing is slow); coast p99 ≤ 1e-3.

Physical basis: a belt body at 2-3 AU moves at ~3e-4 c; per frame its emission point moves
~3e-4 ls, which at 1e3 ls distance is ~3e-7 rad of angle — far below θ_f. The observer's
aberration under burn changes every direction by ~|dβ| per frame, independent of the row's
distance. So the burn's churn should be one global transform (O(cells) to recompose), not a
per-body walk.
