# Predictions (written before the decisive runs B and C)

Rung of reference: `docs/law.md` "Finding encounters" (r8 v3 design: circle rotation +
continued fraction). Belt model: coplanar Kepler pairs about one primary, a2 = 1,
a1 ∈ [1.01, 1.6], e ~ belt-like (Rayleigh σ_e = 0.1), uniform angles/phases.
"Close conjunction" = miss distance at conjunction b_k < R, with R/a ∈ {0.02, 0.05}.

- **P1 (leak scaling).** The fraction of true close approaches (minimum distance over
  the synodic window < R) whose conjunction-sampled miss b_k exceeds R grows with e
  roughly linearly in e and decreases with R: below 1% at e ≤ 0.05, in the 0.5–6%
  band at e ~ 0.1–0.3 (matching the r8 v2 checker's leak), and large (> 10%) at
  e ≥ 0.5 with small R. Cause: the closest approach is displaced from the longitude
  conjunction by the differential epicyclic transverse motion, a b·Δn-scale effect.
- **P2 (gap tail).** For frozen elements (pure rotation), the inter-close-conjunction
  gap T in conjunctions has median ≈ 1/ε (ε = phase fraction with b < R) but a heavy
  power-law tail, CCDF P(T > t) ~ c·t^(-β) with β between 1 and 2 over the measured
  range, so p99/p50 > 10 (pairs sit quiet for very unequal stretches — the payment
  schedule is bursty, not periodic).
- **P3 (clusters).** Consecutive close conjunctions barely cluster at belt e with
  α equidistributed: mean cluster length K̄ < 1.4 and P(K ≥ 4) < 2%. Clustering is
  concentrated in the few pairs whose per-conjunction phase step α/2π is near a
  small-denominator rational p/q, q ≤ 8 (resonant returns).
- **P4 (drift crossover).** With element diffusion turning into a per-conjunction
  phase drift of RMS σ_φ: statistics are unchanged while σ_φ ≪ ε (certificates
  survive drift below the miss quantum), and cross to mixing (exponential CCDF,
  memoryless) by σ_φ ~ ε. A pending certificate with lookahead horizon T is
  invalidated with probability growing as σ_φ · T^(3/2) (random-walk accumulation),
  i.e. exponent 3/2, not 1.

If P2 fails thin (β > 3 or exponential already), the conclusion flips to "benign
schedule, no p99 gate needed" — that would be the useful negative result.
