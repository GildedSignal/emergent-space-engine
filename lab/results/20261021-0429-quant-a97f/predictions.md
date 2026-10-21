# Predictions — 20261021-0429-quant-a97f (written before the counterfactual analysis; the 2,700 flight is still running)

Question (calendar od 4): the post-mixing standing worst-window load excess (measured max/μ 1.54–1.92 vs Poisson floor 1.378±0.080 at 2,700; 1.83 vs 1.185 at 11,700 — the checker's flights) — is its source (a) shear-neighbour correlation (step is a smooth function of a, tight-in-a pairs stay phase-locked and were born train-correlated), or (b) step-law discreteness (exact/near commensurability collisions on the integer step lattice)?

Instrument: the 45c0 genesis census (reused verbatim, plus a per-generation full dump `census_*.tsv`: id, due, step, a). Counterfactual arms rotate the extracted post-mixing state forward with constant steps (due += k·s) and recompute the 64-window load:

- A0 identity — calibration against the measured later censuses;
- A1 step-shuffle — permute steps among ships (breaks a↔s pairing, keeps the step multiset);
- A2 jitter 10⁻⁵ — breaks exact lattice collisions, shear perturbation ≤ 1.5×10⁻⁴ periods over 15 fires;
- A3 jitter 10⁻³ — breaks near-locking at the one-window scale;
- A4 phase-random — the floor control.

Controls on both sides: A4 must return the Poisson floor (else the instrument is broken and the run is VOID); A0 must reproduce the measured loads (else the constant-step model is invalid and no counterfactual runs).

## Pre-registered predictions

- P1 (calibration): A0 reproduces measured max/μ at g = 26–35 within ±0.15. Conf 0.7. Fails → the excess is being made by step news, not carried state; counterfactuals void.
- P2 (the fork): A1 removes ≥ 50% of the excess over the Poisson floor (shear/correlation source). Conf 0.55. Survives → source is in the step multiset's lattice, not the pairing.
- P3 (discreteness): A2 removes < 20% (exact commensurability is minor); A3 removes ≥ 40% only if near-locking at window scale matters. Conf 0.5.
- P4 (pair evidence): co-firing pairs in the hottest windows have median |Δa| < 0.5× the random-pair median (a-neighbours). Conf 0.65.
- P5 (persistence): per-window load autocorrelation over one generation > 0.3 in A0, ≈ 0 in A4. Conf 0.6.
- P6 (scaling consequence, stated only if P2/P4 hold): the excess at 11,700 vs 2,700 tracks the tight-pair count per window, and the 10⁹ worst-frame multiplier is quoted as the pair-count scaling, a bound not a point.

A result that kills both P2 and P3 (neither arm moves the excess) with P1/P4-controls passing is itself the finding: the excess is carried in the phase pattern itself (the train's frozen remnant in locked pairs), priced by D1 persistence.
