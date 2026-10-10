# Predictions (written before the decisive runs)

Held-out cases: I derived, before running anything, that for two same-a, anti-aligned
ellipses the crossing happens at true anomaly ±90° from the apsides, where the two
ships' mean longitudes differ by λ₂ − λ₁ = π − 2m(e) ≈ 4e (m(e) = M(ν=90°), and
M(ν=90°) ≈ π/2 − 2e for small e). Generalisation: two ships can only meet when their
mean-longitude offset is O(e) (the M–ν distortion is 2e sin ν), so the along-orbit
rank distance of *encounter partners* under a frozen mean-longitude sort is
O(e / spacing), where spacing = Δφ/n is the fleet's phase spacing.

Scenes (all coplanar, a = 1, GM = 1, encounter radius ρ = 1e-4, one orbit, brute-force
truth with fine refinement — no conjunction logic, independent of any tier):

- **A control (the gold's premise):** n = 800, circular, zero element spread, uniform
  mean longitude over Δφ = 0.2 (spacing 2.5e-4 ≥ 2ρ). Prediction: encounters exist
  (pairs with Δλ·r < ρ), and **all** are within partner rank 4. If this fails my
  pipeline is wrong, not the gold.
- **B post-burn fleet:** scene A plus a burn footprint: σ_a/a = 1e-4 (r8 v4's kick
  scale), σ_e ∈ {1e-3, 1e-2} (r8 v4's steady σ_e), random ϖ for each body's e-vector.
  Still one tight spatial clump. Predictions:
  - σ_e = 1e-3: encounters appear at mean-longitude rank up to ~4e/spacing ≈ 16;
    miss fraction at k = 4 roughly half of encounters.
  - σ_e = 1e-2: max rank ~160; miss fraction at k = 4 ≈ 90%+.
  - Under a sort by *instantaneous true azimuth* at the encounter time, miss ≈ 0 in
    all scenes (partners are at the same point by definition) — the break is specific
    to the frozen along-orbit order, and the fix costs churn.
- **C intercept (two co-orbital groups, anti-aligned apsides):** 400 + 400 ships,
  e = 0.05, ϖ₂ = ϖ₁ + π, tight λ-clumps timed to co-arrive at a crossing (this is a
  designed intercept; spatially it is *more* concentrated than scene A). Predictions:
  - within-group encounters (the formation contacts) stay rank ≤ ~10;
  - **cross-group encounters — the war events — sit at rank ≈ (π−2m)/spacing ≈
    0.2/spacing, i.e. a large fraction of the whole list**; miss at k = 4 ≈ 100%;
  - the fleet is spatially concentrated by any density measure, so a spatial
    concentration trigger fires and the miss is silent.

What would make me wrong: if encounter partners in B/C still cluster at rank ≤ 4
(e.g. because my O(e) offset bound is too loose and simultaneous arrival needs
λ-offset ≈ 0 in practice), the gold's claim survives contact with burn spread, and I
will say so. That is the control on the other side.
