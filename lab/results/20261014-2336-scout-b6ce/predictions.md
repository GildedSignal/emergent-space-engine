# Predictions (written before the decisive run)

Scene: float replica of the in-band scan (625b/d7e3/c481's ruin) — belt of the ladder's
own generator (a U[2,3) AU, e Rayleigh(0.07) re-drawn above 0.4, doll 0), player circular
2.5 AU in doll 0, burn cadence: one minted scan per 83 game-s for 16,000 game-s (193 mints,
the 625b protocol). Two window anchors for R (the `near` radius the shipped scan keeps to):
R_code = 2^10·(2·ship radius) = 0.176 AU (derived from `Scalar::raw(34, 8)` root units,
ENCOUNTER_LOG2 = 10), and R_count = 0.037 AU (back-solved from c481's ~21 encounters/mint
at 10⁵ under my surface-density estimate — the anchor check below).

Held-out cases (not tuned on):

- **P1 (shipped shape):** the shipped radial tier (16 bins/octave over radius) returns
  `None` (walk all) at essentially every in-band mint; candidates ≈ N_belt (>99%), at both
  10⁵ and 10⁶. Structural: the belt is a thin shell; any in-band window covers >25% of it.
- **P2 (anchor):** truth encounters/mint at 10⁵ with R_code lands within ~3× of the record's
  ~21/mint (4,032 encounters / 193 mints). If it lands ≫ (say >10×), my R_code derivation is
  wrong and the R_count arm carries the claim; I will say so.
- **P3 (the tier):** a key index — sort by mean longitude L(t0) within (mean-anomaly M,
  geometric-e) buckets, all keys exactly linear or constant between kicks — finds every
  truth hit (zero misses at every sampled mint, both N, both R) with candidates ≤ 2% of N
  at R_code and ≤ 0.3% at R_count.
- **P4 (the naive kill, negative control):** the same L-sort WITHOUT the eccentric widening
  (2.2e_hi per e-bucket) misses hits (I expect >5% of truth hits missed — the equation of
  center genuinely carries bodies ±2e rad off their mean longitude).
- **P5 (maintenance):** the index shears by n_max·Δt = 1.1e-3 rad over the whole 16,000 s
  flight — under one re-epoch per flight; per-kick re-slot is one binary search + splice at
  the kick rate 3.55e-5/body/game-s (stated, not float-measured).
- **P6 (composition):** 193 held mints × standing bytes (224 B/candidate, c481) ≤ 250 MB at
  10⁵ with R_code — under the box ceiling, where the shipped shape's 193 × 29.4 MB = 5.7 GB
  is the measured ruin.

Kill criterion for the tier: any truth hit outside the candidate set (the bound is wrong),
or candidates > 10% of N at R_code (the cut is not load-bearing).
