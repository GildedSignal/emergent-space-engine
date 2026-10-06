# Predictions (written before the held-out runs)

Tuning happened only on the training case: seed 4242, σ_e 0.1, κ 1e-5, n 400, 8 epochs,
slack 0.5, widen 2.0 (result: setups 8.0× down, wall 6.8× down, misses 0, extras 0,
3,879/3,879 encounters). All cases below were not run when this file was written.

Common shape: n 400, ρ 0.01, a ∈ [0.9, 1.1], 8 epochs, arm `skin` with slack 0.5, widen 2.0
unless stated. "Ratio" = baseline setups / skin setups (same as setup_evals ratio here, since
one setup costs the same in both arms).

| Case | Setup | Prediction |
|---|---|---|
| H1 | seed 777, σ_e 0.1, κ 1e-5 | zero re-setups after epoch 0 (per_epoch_setups = [ncand, 0×7]); ratio ≈ 8; **misses = 0**; extras ≤ 20 (widened windows may catch an extra genuine minimum; exact checks decide, so extras are real encounters); skin wall ≤ 0.25 × baseline wall |
| H2 | seed 313, σ_e 0.2, κ 1e-5 | same as H1; extras may be larger (wider eccentricities → wider arcs); **misses = 0** |
| H3 | seed 909, σ_e 0.1, κ 1e-3 (churn stress, 100× stronger kicks) | re-setups appear (per_epoch_setups > 0 after epoch 0) but total setups ≤ 3 × ncand (ratio ≥ 2.7); **misses = 0** (validity fires at slack 0.5 while widening covers 2.0, i.e. 4× the allowed drift) |
| C1 | κ = 0 (no kicks), seed 4242 | per_epoch_setups = [ncand, 0×7]; misses = 0 AND extras = 0 (no drift at all → same passages proposed up to widening); ratio = 8 |
| C2 | κ 1e-3, slack 0.5, **widen 0** (negative control) | **misses > 0**: stale windows/anchors hide real encounters. If misses = 0 here, the comparison is insensitive and the run is VOID |
| C3 | κ 1e-5, slack 1e-9 (negative control) | validity always fails → re-setup every epoch: setups = 8 × ncand (ratio 1), misses = 0 (degenerates to baseline); skin wall ≈ baseline wall |

## What would kill the mechanism

1. Any miss > 0 in H1/H2/H3 with widen ≥ 4 × slack: the validity envelope is unsound — a pair
   whose elements drifted less than the slack can hold an encounter its widened cached window
   no longer covers. Kill the slack/widen pairing rule (not caching itself).
2. C2 showing misses = 0: the miss detector cannot see staleness → VOID, all zero-miss claims
   unearned.
3. H3: if re-setups explode (setups > 6 × ncand) the churn regime pays wake-re-pay like the
   killed deferral, and the skin only helps in quiet regimes — still true but a much weaker
   claim; report honestly.
4. Skin run_evals > baseline setup savings (wall ratio ≥ 1): widened windows cost more in exact
   checks than they save in setups → kill widen = 2.0, try smaller.
