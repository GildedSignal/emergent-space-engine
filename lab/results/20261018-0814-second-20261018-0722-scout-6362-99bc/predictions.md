# predictions.md — 20261018-0814-second-…-99bc (written before the decisive run)

Setup: closed form re-derived on the shipped v1 Householder operator
(N = (d·p, E·d), f50d's 4-normal). The reflection is scale-invariant in d, and the
root direction n' = P_num − √D·w is integer + one irrational, so N' = U − √D·V with U, V
INTEGER: the whole reflection closes in Z[√D], and the velocity targets' floor/ceil —
all the lattice machinery consumes — is exact via integer square roots. Predictions:

- **P1 (the skip, negative control on the shipped stepper).** The shipped `Chronon`
  (Law::RelativisticV1, Q = 2²⁰, reach 2048) on the crossed-in-bin head-on pair
  (closing 0.9c) logs exactly ONE Contact event, both velocities stay
  ±471859 forever after (no exchange, no re-fire in 300 chronons), and body a ends
  beyond body b (they passed through each other).
- **P2 (the criterion, exact rule).** With the root branch on, the equal-mass pair
  exchanges EXACTLY: a.k → −471859, b.k → +471859 (hand derivation: p_total_spatial = 0
  makes N purely spatial, pa' = (E, −p) exactly, target = −k an exact integer, single
  candidate per body, zero residual and zero carry). Root fires exactly once; ledger
  identity holds bit-exactly (ΣE(end) − ΣE(0) = Σresidual = 0).
- **P3 (exactness across geometry, speed, contrast).** On every arm (b/R to R−1
  grazing, closing 0.5–0.99c, mass to 10⁴:1) the exact Z[√D] rule's final lattice
  velocities equal the independent f64-oracle's (reflection of the float root normal),
  and equal the integrated fixed stepper's outcome. Disagreement count 0; the smallest
  floor/ceil margin over all arms exceeds 10⁻⁶ lattice units (f64 oracle decisive at
  that margin, exact rule right regardless).
- **P4 (the cheap variant).** The one-isqrt quantized direction (j = 31) reproduces the
  exact rule's final velocities on ≥ 99.9% of the random sweep; every disagreement has
  margin < 10⁻⁴ (a genuine floor/ceil boundary pair), and the worst angular error of
  the quantized direction stays ≤ 10⁻⁵ rad at R = 2048 (it degrades toward grazing ×
  max speed, ~2⁻ʲ·|w|/b).
- **P5 (τ-window classification).** The integer firing test agrees with the float
  τ− ∈ [0,1] classification on every pair (0 disagreements in the sweep); it never
  fires on misses (D < 0), past/future roots (τ− outside the bin) or already-inside
  starts (|d0| ≤ R).
- **P6 (digest controls).** (a) The copied stepper with the fix OFF digests bit-identical
  to the shipped Chronon over 2000 chronons of a 256-body v1 gas (the copy is faithful).
  (b) On a slow gas (|w| ≪ reach per chronon, no pair can cross in-bin) the fix is
  dormant: fix ON digest == shipped digest, root fires 0 times. (c) On a fast gas
  (vmax 2¹⁸, ρ to 0.35) the fix fires on a 0.1–3%-of-contacts class (1648's regime),
  the digest then differs from shipped (it must — those pairs now exchange), and the
  ledger identity plus subluminality hold end to end on the fixed run.
- **P7 (algebra identities).** w·P_num = 0 exactly in i128 and |P_num|² = ww·(ww·R² − D)
  exactly in BigInt on every pair of the sweep, including misses and degenerate
  (tangent, D = 0) cases.

Kill criteria: P1 failing (skip not reproduced on shipped code) voids the premise; P2
not an exact swap kills the Z[√D] derivation; any P3 disagreement with margin > 10⁻⁶
kills the exact rule; P5 misclassification kills the firing test; P6a digest mismatch
kills the copy (VOID, not kill); ledger breaking anywhere kills the fix as specified.

Non-goals (named by the checker, not retried): multi-pair-bin ordering (1648 measured
≤ 1.6% contamination; the fix inherits the shipped batch convention), the already-inside
class (needs its own design decision), root-tick position application (P4 of the parent
run: the schedule owns the ≤ R·ρ offset; the impulse is identical).
