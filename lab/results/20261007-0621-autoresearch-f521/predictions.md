# Predictions (written before the decisive held-out run)

Artifact: `crates/encounters` (the Binet-cone + Diophantine first-hit encounter finder, r8 v3 line).
Metric: setup cost per candidate pair — `setup_ns_per_pair` and Kepler solves per pair — at n = 10 000,
sigma_e = 0.01, rho = 1e-4 (the `scale n` / `kick` belt). Baseline (this machine, this build):
8 348 ns/pair, 20.26 f-call evals/pair = 40.5 Kepler solves/pair; 87% of setup evals sit in
`d_of_s`'s fixed 33-sample arc scan; 54% of window-advancement calls have d < 16 rho (the
geometric tail of conservative advancement).

Changes under test (each rigorous — windows stay supersets, the exact per-passage check is untouched):
1. Cache j's arc states per window invocation (j's tau-grid does not depend on s).
2. Local Lipschitz constant for the s-advancement (i's speed bound over the anomaly range it
   actually traverses, not the whole-orbit vmax).

## Held-out cases (not tuned on)

- `verify a b c long`: missed = 0 on every set, false-positive rate unchanged (windows are
  supersets by construction; the exact check is unchanged). Predicted: missed 0, false <= baseline + 0.
- `scale n` at n = 30 000 and 100 000: same relative gain as at 10 000 (the change is per-pair,
  not per-belt). Predicted: setup_evals_per_pair 9.69 -> ~5.5 (30k), 5.16 -> ~3.0 (100k).
- `kick` (n = 10 000, horizon 1000 orbits): us_per_kick drops by the same fraction as setup
  evals (the gold components-4643 finding says 92% of per-kick evals are window setup);
  slack_skippable_fraction unchanged (certificates' budgets are recomputed the same way).

## Point predictions at n = 10 000 (tuning case)

- setup_ns_per_pair: 8 348 -> <= 5 500 ns (>= 1.5x).
- Kepler solves per pair: 40.5 -> <= 27.
- Hits per pair-orbit unchanged (4.546e-5 within 1%); checks_per_hit <= 1.3 (window edges may
  shift by a few ticks; the exact check still decides).

## What would make it wrong

- If refine's share (off-grid, uncached) eats the gain: expected refine share ~13% of evals,
  it caps the cut at ~1.8x on the scan bucket.
- If j's states were NOT actually s-independent: the math says f(tau) = rel(i(mi + n(tau-s)), j(mj + n tau));
  j depends on tau only. If verify shows misses, the caching is buggy, not the idea.
- If the local Lipschitz bound is unsound: any missed encounter in verify long kills it (revert).

## Structural change that would beat this (the lens blind spot)

The tail exists because the s-advancement uses a whole-orbit Lipschitz constant while the true
local slope of D(s) is the relative approach rate (~0.09 vmax here). A per-pair second-order
window model (as `cross_window` already does for transversal crossings) extended to tangential
pairs would remove the tail entirely instead of halving its per-step cost.
