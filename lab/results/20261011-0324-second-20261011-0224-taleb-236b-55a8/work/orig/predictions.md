# Predictions — 20261011-0224-taleb-236b

Written before the decisive full-size run. Tuning history disclosed: four smoke
runs at reduced n (S0 300, S1 800, S2 2x200, S4 200) fixed scenario parameters
(spacing > R so no birth adjacency) and exposed one bug (rank baseline). The
numbers below are for the full sizes (S0 500, S1 1600, S2 2x400, S4 300), not
tuned on.

- **P1 (control, S0 shear, pure a-dispersion):** >= 99% of contacts at rank <= 4.
  The certificate's premise must hold where its premise (shear) holds; if this
  fails the instrument is broken, not the certificate.
- **P2 (S1 collision family, e-vector dispersed):** <= 1% of contacts at rank <= 4;
  median rank > 0.3 n. Held-out scaling: median rank at n=1600 in [610, 830]
  (smoke at n=800 gave 356 = 0.45 n).
- **P3 (S2 interception, two clumps on crossing ellipses):** >= 95% of cross-group
  contacts at rank > 4, median cross rank within 10% of n * |dM*|/2pi ~ 555
  (n=800, dM* = 249.7 deg); within-fleet events are birth-stacked pairs,
  <= 60, all rank <= 4.
- **P4 (S4 realistic formation, sigma_omega = 0.1 rad, sigma_e = 2e-3):**
  <= 10% of contacts at rank <= 4; median rank > 0.2 n (conjunction branch is
  absent: with omega dispersion, dM=0 is not a close approach; contacts live at
  crossing offsets).
- **P5 (R sensitivity, held out):** at R = 3e-5 and 3e-4 the mechanism, not the
  threshold, decides: frac(rank <= 4) stays <= 2% in S1/S2(cross)/S4 and >= 99%
  in S0.
- **P6 (trigger):** the family's intra-family Binet cone fraction separates the
  regimes: S0 ~ 0 (shear, certificate valid) vs S1/S2/S4 ~ 1 (crossing offsets
  required). It is computable in the representation the design already uses.

Kill criterion for my own probe: if S0 does not pass P1, the run is VOID
(instrument). If S1/S2/S4 come back rank-local, the certificate's premise is
stronger than I argued and the probe reports the certificate as robust.
