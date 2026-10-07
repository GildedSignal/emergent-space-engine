# Predictions — inversion of gold 20261006-0346-taleb-09b5 (the k=4 train certificate)

Written before any run of the decisive experiment.

**The premise under attack.** The gold's train certificate: "every real encounter sits within distance-rank 4 of its partner → a phase-neighbour watch at k≈4 replaces the quadratic tier in the co-orbital regime." Measured on scenes whose tightest local packing was ~0.8 ships per ρ of arc (σ_λ=0.01, N=200 gaussian). The certificate's hidden invariant is a *packing* bound: the number of ships inside one encounter tube (ρ of along-track arc) must stay below k. Nothing in the gold scales k with packing, and the board's target scene (a concentrated 10⁶-ship fleet; a 10⁶ fleet in a 1° arc has packing Π = ρ/s ≈ 6·10³) sits far outside the measured regime.

**Definitions.** ρ = 1e-4, a ≈ 1, μ = 1 (their units). Packing Π = mean ships per ρ of along-track arc. Rank r = number of ships strictly closer than the partner at closest approach (their convention, min over both directions); their certificate passes iff r ≤ 4. Scenes: uniform co-orbital arcs, a-spread ±0.3ρ (every overtake is a sub-ρ conjunction), e = 0 unless said. Brute-force dense sampling, dt = 0.02 (per-step relative motion ≤ 0.02ρ).

**Pre-registered expectations on cases I have not tuned on:**

- P1 (instrument calibration, their scene family): N=200, σ_λ=0.01, a_hw=1e-5, e~Rayleigh(1e-3), ϖ ±0.1 → r_max ≤ 4 (reproduces the gold's held result).
- P2 (uniform packing at their boundary): Π=0.8 → r_max ≤ 5, no material r>4 fraction.
- P3 (first break): Π=2 → r_max ≥ 5; fraction of encounters with r>4 between 0.1% and 5%.
- P4: Π=4 → fraction r>4 ≥ 10%; r_max ≥ 8; simultaneous-ρ multiplicity (ships within ρ of a target at its closest approach) reaches ≥ 4.
- P5: Π=8 → fraction r>4 ≥ 40%; r_max ≥ 12; median multiplicity ≥ 2.
- P6 (the gold's own flagged worry is NOT the breaker): Π=0.5 with e~Rayleigh(0.01) (radial breathing 100ρ ≫ ρ) → r_max ≤ 4. e-spread alone does not inflate rank; packing does.
- P7 (the corrective law): the watch size that restores zero miss grows with packing, k* ≈ 2Π·c with c ∈ [1, 2], so the certificate is sound only with k set by the cell's local packing number (dimensionless, cheap), and at Π ≳ O(1) the "encounter = isolated pair event" premise itself dissolves (multiplicity > 1 for most encounters) — the concentrated fleet must route to contact compute, not to any pairwise train.

**Kill criterion for my own claim:** if r_max ≤ 4 holds at Π=4 and Π=8 (P4/P5 fail), the packing inversion is wrong and the gold's k=4 stands broader than its evidence; that too is a result (the certificate is packing-robust), and I will report it as such.
