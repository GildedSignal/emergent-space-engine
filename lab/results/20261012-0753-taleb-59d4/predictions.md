# Predictions — 20261012-0753-taleb-59d4 (written before any run)

Question: does the adopted train certificate ("partner distance-rank ≤ 4 at closest approach",
gold 20261006-0346-taleb-09b5) survive longitudinal packing tighter than the tightest tested
(σ_λ = 1e-2, spacing ~ρ–3ρ), and does its O(n_c·k) cost claim hold at the fleet scale it was
adopted for?

Independent harness (numpy, my own Kepler propagator, brute all-pairs truth on a common time
grid + per-pair ternary refinement; no code shared with the gold run). ρ = 1e-4, a = 1, fleet
distribution matched to the gold's `fleet()`: a ~ U(1±a_hw), e ~ Rayleigh(σ_e) capped 0.01,
ϖ ~ U(ϖ₀±0.1), λ ~ N(λ₀, σ_λ). Ranks at closest approach, min of both directions, in three
keys: 3D distance (what they measured), true longitude (sound phase key), mean longitude
(the design's likely sort key). Predicted packing number Π = 2ρ·n_c/(σ_λ√(2π)) = expected
ships inside one contact window.

Cases (all held out: none tuned on):

1. **Control** (nc=200, a_hw=1e-5, σ_λ=1e-2, σ_e=1e-3, seeds 31–32): distance-rank max ≤ 4
   (reproduces the gold; if not, my instrument is broken).
2. **Jam ladder** (same, σ_λ ∈ {3e-3, 1e-3, 3e-4}, seeds 31–33): max distance-rank grows ~Π:
   ≈5, ≈16, ≈53. k=4 breaks at σ_λ ≲ 2.5e-3; contacts with distance-rank > 4 are missed by
   any k=4 watch regardless of rebuild policy (structural: >4 ships mutually within ρ).
3. **Scale** (nc=800, σ_λ=1e-3, seeds 41–42): max rank ≈ 4× the nc=200 value (k is linear in
   n_c at fixed tightness, not O(1)).
4. **e-spread at tight jam** (nc=200, σ_λ=1e-3, σ_e=5e-3, seeds 51–52): contact rate drops
   ~ρ/σ_e (radial eligibility thins pile-ups) but distance-rank at contact stays ~Π of the
   e-small case scaled by eligibility; mean-longitude rank inflates by the equation of center
   (~n_local·4σ_e ≫ 4): if the design sorts by mean longitude it misses even where distance
   rank is 1.
5. **Design-scale arithmetic** (computed, not run): n_c=10⁶, σ_λ=1e-2 → k ≈ Π ≈ 8e3;
   n_c·k sections ≈ 8e9 × 72 B ≈ 580 GB and ~10⁹ evals per orbit sweep: the train re-ruins at
   exactly the concentration it was adopted for. The certificate needs a second dimensionless
   trigger (Π > k_budget ⇒ escalate the jam to a pile-up/clump representation), else it is
   convex only while Π ≪ n_c.

What would falsify my mechanism: max rank NOT tracking Π across the ladder (e.g. staying ≤ 4
at σ_λ=3e-4 would mean some unmodelled exclusion keeps pile-ups apart — the gold's invariant
would survive tighter than I claim).

## Addendum (written after the ladder, before the pile-up runs)

The jam ladder FAILED my prediction 2: distance-rank stayed ≤ 3 at Π = 53 (σ_λ = 3e-4).
Mechanism I missed: contacts need |Δr| ≲ ρ as well as |Δλ| ≲ ρ; the fleets' e-spread
(Rayleigh 1e-3 = 10ρ, ϖ spread ±0.1) radially diffuses the jam, so 3D packing ≈ Π·(ρ/σ_e)
stays ~1. Longitudinal packing alone cannot break the distance-rank invariant — the gold's
own fleet family is protected by its radial spread. (Already solid from the ladder: the
MEAN-longitude rank is 182–197 with > 90% of contacts over 4 in every case including the
control — the ϖ spread decouples mean from true longitude at contact.)

Refined decisive cases — a formation tight in all three dimensions (what a flown fleet is):
σ_e = 3e-5 (cap 3σ), ϖ spread ±0.01, a_hw = 1e-5:
- P1: nc=200, σ_λ=1e-3 → Π = 16 → predict rank_d max ≈ 8–20, over4 > 0.
- P2: nc=200, σ_λ=3e-4 → Π = 53 → predict rank_d max ≈ 25–60.
- P3: nc=800, σ_λ=1e-3 → Π = 64 → predict rank_d max ≈ 4× P1 (scale linearly in n_c).
Control side (already run): identical but σ_e = 1e-3 → rank_d ≤ 2.
Falsifier of the refined mechanism: rank_d staying ≤ 4 in P2 would mean some further
exclusion I have not modelled, and the distance-rank invariant survives.
