# Predictions — 20261018-2040-dynamics-834e (written before the decisive sweep)

Pilot already seen (seeds 1–3, n=400, vmax=2^17, φ ≤ 0.6): rate matches free Enskog
(cross-section = swept width 2·reach = 4r; the in-code `nu_enskog` column of the pilot
JSONL is 2× too small — fixed before the decisive run), Fano1 ≤ 1 everywhere seen,
frames flat (p99/p50 ≤ 1.08), distinct-partner fraction collapsing with φ. Below,
"held-out" = seeds 5/6, n=1600, vmax arms, and the φ ∈ {0.7, 0.78} arms still running
when this was written.

- **P1 (positive control, instrument).** At φ = 0.05 the measured per-body rate is
  within ±10% of free-flight kinetic theory ν_free = (φ/π)·4·g_H·⟨|w|⟩/Q (g_H at 0.05
  ≈ 1.06). Pilot: 1.009. If any dilute arm leaves ±10%, the counting instrument is
  broken and the run is VOID.
- **P2 (rate law vs Henderson).** measured/Henderson stays < 0.85 for all φ ≥ 0.7
  (the cold ordered start cages and backscatters; equilibrium Henderson over-counts
  contact correlation). It will NOT rise above 1.15 anywhere: no jamming-driven
  rate divergence below φ = 0.78 in a cold-started formation-like gas.
- **P3 (no avalanche).** Fano1 < 1 for every arm with φ ≤ 0.78, all seeds including
  5/6 and n=1600 (anti-bunching: the consumed rule + quasi-periodic cage
  recollisions dominate). Kill "no avalanche" if any arm shows Fano1 > 1.5.
- **P4 (flat frames).** p99/p50 per-chronon ops < 1.15 everywhere, and the largest
  per-tick contact component < n/20 (< 20 at n=400, < 80 at n=1600) for all φ ≤ 0.78:
  no percolation cliff in the per-chronon contact graph below jamming, because
  ν_per_body < 0.5/chronon never approaches engagement. Kill if any component > n/10.
- **P5 (speed linearity).** At φ = 0.3, ν/⟨|w|⟩ is constant within ±5% across
  vmax ∈ {2^15, 2^16, 2^17, 2^18} (Enskog: rate linear in mean closing speed).
- **P6 (scale invariance).** ν per body and Fano1 at n=1600 match n=400 within ±10%
  at the same φ (no N-dependence of the rate law; the cost cliff, if any, is in ops
  per chronon, not per body).
- **P7 (the one burst class).** max_batch ~ n events appear at φ ≥ 0.45 but are
  wall-flash batches (coherent wall hits, O(1) flips each): maxops/p50 stays
  < 1.2 wherever max_batch > 100. If a pairs-driven batch of > n/10 fires with
  maxops/p50 > 2, that is a real contact avalanche and P3/P4 die with it.
