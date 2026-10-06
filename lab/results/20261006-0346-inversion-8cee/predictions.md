# Predictions — written before the decisive runs (only `ctrl-coorbital` had run)

Scenes not run yet: `highe-align`, `highe-rand` (N=240, a∈[1,1.2], e∈[0.60,0.95], ϖ=0 vs random,
λ random, ρ=1e-3, horizon 10 orbits), `formation`, `wall` (N=240, a=1±4e-4, e≤0.02, ϖ=0, λ random
vs clustered in ±0.3, ρ=1e-3, horizon 20 orbits). None of these can come out of `make_belt`
(it caps e at 0.5), so no frozen verification belt has ever tested e > 0.5 or an aligned-apsis
formation. Judges: the crate's own truth (radial pairs, conservative advancement) for the full
horizon, plus my dense fixed-grid third opinion (comparison minima + golden refine, Halley states;
no sign-change brackets) on a strided pair sample over 3–4 orbits.

Controls already run: `ctrl-coorbital` → missed 0, false 0, three-way agreement (also
`dense_missed_by_truth` 0 — the truth is not the broken one there).

## Predictions

1. **High-e misses (main).** At least one highe scene has missed > 0 against the crate's own
   truth. Mechanism I expect: a Cross section's window comes from a second-order Taylor with
   SAFETY = 1.1; at high eccentricity the neglected third order (curvature × s³, s the synodic
   offset at the crossing) exceeds the 10% margin, the true minimum lands outside the window, and
   the method — by design — evaluates nothing there. The demotion guard (window ≤ half the
   passage-overlap cap) may rescue it; if missed = 0 everywhere, prediction 3 carries the result.
2. **Where.** If misses exist, `highe-align` (crossings near the common periapsis, curvature
   maximal) misses at least as many as `highe-rand`.
3. **High-e cost inversion (fallback).** If missed = 0 in both highe scenes, then evals per
   reported encounter is ≥ 5× the ctrl baseline (numeric Wide windows dominate: tangency-adjacent
   geometry at high e demotes Cross sections and pays ~1e3 state evals each, the cost the
   q-candidate-degree silver measured as 91% of its total at 10⁶).
4. **False reports at high e.** g-noise terraces (Δr·Δv touching its noise floor without a
   minimum) are not co-orbital-specific: at least one false report appears in the highe scenes
   (r8 v3 found exactly one in a co-orbital belt; high-e crossing minima are flatter).
5. **Fleet correctness.** `formation`/`wall`: missed 0 (Full sections are padded, merged-Wide
   windows are computed rigorously), false 0; `radial_not_cone` = 0 in every scene (the ε_u
   candidate tolerance holds even at e ≤ 0.95).
6. **Fleet cost.** Work per real encounter in `formation`/`wall` is ≥ 10× a phase-mixed belt
   baseline: nearly identical orbits make every pair a Wide/Full section with expensive setup, and
   `wall` (clustered phases) has far fewer encounters paying for the same setup, so its
   evals_per_enc and checks_per_enc are the highest of all scenes.

## What would invalidate the instrument

A control failing (missed ≠ 0 or false ≠ 0 on ctrl scenes), or `dense_missed_by_truth` > 0 on
sampled frames where truth and method agree (would mean my dense scanner, not the crate, is the
outlier). Any miss claim must also be missed by the dense opinion on its frame, or be validated
pair-by-pair with the dense full-horizon scan.
