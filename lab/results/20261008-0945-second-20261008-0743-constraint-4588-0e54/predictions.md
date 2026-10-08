# Predictions (written before the decisive matrix; tuned only on seed-1 smoke runs at 5 s)

Runs decided: `quantum_view 15 <rtf> <seed> 5 <members> <quantum>` for
(m48, rtf 1, 1080p), (m48, rtf 100, 1080p), (m400, rtf 100, 1080p),
(m48, rtf 100, 4k), (m48, rtf 10000, 1080p), (m48, rtf 10000, 4k),
(m400, rtf 100, 4k, seed 7). All on the shared Linux box; orders of magnitude only.

1. **The gate does not pass as specified.** The near population (fresh battle handoffs
   ~5–10 milli-light-seconds out, and near ships) breaches the distance-family quanta
   (age / light_seconds / offset) even under the curvature-guarded first-order hold:
   I predict FAIL in every configuration, worst err/quantum ≈ 5–20 on age/light_seconds,
   concentrated on kind 3 and kind 4 rows, ≤ ~10 % of served-row checks. The far population
   (planets, moons, distant ships) holds every field under one quantum.
2. **The author's 82.7 % quiet does not survive an all-field gate.** With all ten `Seen`
   fields gated at the display quantum, the servable fraction at 1080p is ≈ 20–35 % of
   rows at m48 rtf 100 (fleet-loop rows are unservable — no sound cheap basis — and near
   rows churn), not 54–83 %.
3. **The realized saving is real but below the claim.** At m48 rtf 100 I predict
   0.3–0.55 ms/frame off a 0.8–0.9 ms gather (~1.5–1.8× gather). At m400 rtf 100 the
   fleet dominates the row count, so the saving stays ≈ 0.5–0.9 ms — NOT the author's
   predicted 1.4–2 ms/frame; the cache buys body-row compute, and bodies are the minority
   of rows in a fleet battle.
4. **rtf and quantum sweep.** At rtf 1 the served fraction is the highest of the matrix
   (≈ 40–60 % of body rows; drifts are 100× smaller). At 4k the served fraction roughly
   halves. At rtf 10⁴ the engine's kicks flood the bases; served < 10 % and the cache is
   irrelevant there (the author's crossover bracket stands).

If (1) fails — the gate passes everywhere — the claim upgrades to gold with the cache built.
If (3) overshoots (saving ≥ 1.4 ms at m400), the presentation-memo lever is confirmed at
scale even with the fleet excluded.
