# Predictions — run 20261012-0358-second-…-0ae6 (written before the decisive run)

The decisive experiment is the checker's named one: steady state with
reabsorption. Programs P1 (checker's λ−λ_J Fourier(8)×Cheb(2,e)×Cheb(2,ω),
true-phase anchor), P1B (same, base-phase anchor), P2 (generator
deformation: Fourier(10) in initial λ × Cheb(2) in initial a,e,ω),
P3 (P1∪P2 joint). Payload = quantized residual vs the frozen program;
refit every k orbits; W = Σ log2(1+2·median|S|) is the verdict metric
(the scout run's own headline instrument); budget 34.4 bits/body.

Instrument checks already run (no belt numbers seen): synthetic fit
recovery relerr 6e-15; shuffled absorption = chance level (153/4096 =
3.3% at the smoke size); perturber-off payload ≡ 0 bit-exact.

- **Q0 reproduction.** `evolve` reproduces the scout's published cold-belt
  numbers exactly: scar_word_bits_median orbits 1–8 = [66.630, 70.236,
  72.168, 73.650, 74.805, 75.785, 76.606, 77.330]; raw per-kick entropy
  median 51.441. Bit-exact (same seed, same operations).

- **Q1 (P1, k=1).** Post-refit W at orbit 8 ≈ 61 ± 4 bits (checker's
  static-fit anchor 61.2). Sawtooth: the phase anchor shears ~0.63·2π per
  orbit while the secular part of the deviation stays anchored at the
  initial phase, so the payload re-grows within each cycle:
  peak/post-refit ≥ 1.2 and peak ≥ 50 bits in every cycle. sup_W > 55.

- **Q2 (k-scan, belt quanta).** No (program, k) keeps sup_W ≤ 34.4 at
  c = 1. k=1 is optimal for every program (sup_W grows with k). If
  falsified, I report the premise-survives branch with the winning config.

- **Q3 (P2).** Plateau plus slow growth, no sawtooth (time-independent
  anchor): peak/post-refit ≤ 1.15; W_post(orbit 1) ∈ [28, 55], point 42;
  growth +0.3…+2 bits per doubling (diffusive secular noise).

- **Q4 (P3 union — the decisive number).** W_post(orbit 1) ∈ [18, 45],
  point 33 ± 8; growth +0.5…+2 bits per doubling. If W_post(1) ≤ 30 the
  budget line may hold to orbit 16; if ≥ 36 it breaches immediately.
  I do not know which — this is the number the experiment exists to
  measure.

- **Q5 (quantum valve).** The smallest uniform coarsening c with
  sup_W(P3, k=1, c) ≤ 34.4 lies in [1, 256]; point estimate c* = 8.
  The angle elements (ω, M) carry ≥ 50% of P3's residual bits.

- **Q6 (controls).** Shuffle absorbed energy at m=8 ≈ chance level
  153/16384 ≈ 0.9% ± 1%. P1 energy absorption at m=8 reproduces the
  checker's 0.87/0.70/0.50/0.50 (per element a,e,ω,M) within ±0.1.

Kill criterion for the headline: sup_W(P3, k=1, c=1) > 34.4 ⇒ no
reabsorption cadence in these program classes holds the live budget at
belt quanta (the kill branch); then c* is the design constant. If
sup_W ≤ 34.4, the premise survives with two-block programs and the
answer is the largest k that holds.
