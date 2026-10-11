# Predictions (written before the decisive runs)

Inverted claim: lab gold `20261006-0346-taleb-09b5` — "every real encounter lies within partner
rank 4 along the orbit, so a phase-neighbour certificate at O(n·k) replaces the quadratic tier,
triggered by a dimensionless number."

The claim silently assumes the λ (mean-longitude) rank order is **stable over the certificate's
horizon**. It is not: λ_i − λ_j advances at δn = n_i − n_j, so rank adjacency churns at the synodic
rate. All predictions below use closed-form λ dynamics (λ = M + ϖ, M from the crate's integer
period), encounters from the shipped method (`pair_events` over all cone candidates), scenes at
n = 300, ρ = 1e-3, random ϖ, λ.

Notation: rank₀(i,j) = number of bodies strictly between i and j in the circular λ(0) order
(short arc). k_needed(T) = max rank₀ over encounters in [0, T]. "Lazy pairs" = distinct pairs with
≥ 1 conjunction in [0, T] (the re-certification volume a swap-triggered certificate must pay).

## P1 — the gold's own scene, longer horizons (a ∈ [1, 1.0001], σ_e = 3e-4)
- k_needed grows ≈ linearly in T: about 1.1 per 50 orbits (from 1.5·(Δa/a)·(n/2)·T_orbits).
- k = 4 holds (100% coverage) at T = 50 orbits; breaks (coverage < 50%) by T ≈ 200–400 orbits;
  at T = 5000 orbits coverage of k = 4 is < 10% and k_needed ≳ 100.
- Encounters remain λ-adjacent **at the moment of encounter** (rank_at_encounter ≤ ~4 at all T):
  the gold measured adjacency at the wrong time if it equated this with setup-time coverage.

## P2 — spread sweep at fixed T = 200 orbits (σ_e = 3e-4, Δa ∈ {1e-4 … 1e-2})
- k_needed ∝ Δa·T: coverage of k = 4 collapses from ≳ 90% at Δa = 1e-4 to < 10% at Δa ≥ 1e-3.
- The deferral saving (eager cone pairs / lazy conjuncting pairs) falls from ≳ 30× at Δa = 1e-4
  to ≈ 1× at Δa = 1e-2: the "replaces" is a deferral whose benefit is exactly T_mix/T
  (T_mix = synodic mixing time), not a deletion.

## P3 — hot formation (Δa = 1e-4, σ_e = 3e-2, T = 200)
- Conjunctions outnumber encounters by ≈ σ_e·a/ρ (order 10–60×): a swap-triggered certificate
  that pays per adjacency event pays the temperature ratio per real encounter.
- But sections() rejects most hot pairs outright (arc radial separation > ρ → None), so the eager
  tier's per-pair setup is cheap there; temperature is NOT the phase certificate's problem.

## P4 — cross-group (A: 150 on a ∈ [1, 1.0001]; B: 150 on a = 1.3, e = 0.25; T = 200)
- A↔B encounters have rank₀ ~ uniform in [0, n/2] in any global λ order: k = 4 covers < 5% of
  them; within-A encounters keep small rank₀.
- So the certificate must be scoped per group, and the "dimensionless number" must be a per-group,
  per-horizon churn number Θ = n·⟨|δn|⟩·T/(2πk), not a static concentration measure.

## Kill criterion for my own run
If k_needed at T = 50 on the gold's scene already exceeds 4, or coverage of k = 4 does NOT fall
with T and Δa, my churn model is wrong and the gold's claim is stronger than I think.
