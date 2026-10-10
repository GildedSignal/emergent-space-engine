# Predictions (written before the decisive run)

Run: 20261010-0306-spacex-acb2. Reference belt (my spec): planar, a ∈ [1, 1.02] (W=0.02),
e ~ Rayleigh(σ_e), N=1e4, star M*=1, units a=1, v_K=1. Belt mass M_belt ∈ {1e-7, 1e-5} M*.
Cases not tuned on: everything below comes from the analytic kinetic/shear model; the
Monte Carlo has only been smoke-tested for invariants (circular min distance = Δa, shear
speed 0.5·Δa), never for rates.

- **P1 (cold rate).** σ_e=0.01: Λ(ρ=1e-3) ∈ [1, 15] encounters per body per orbit, point
  estimate 5 (kinetic 2·n₂D·⟨v⟩·2ρ with n₂D=7.9e4, ⟨v⟩≈0.015). Λ(1e-4) ∈ [0.1, 1.5].
- **P2 (ρ exponent).** d ln Λ / d ln ρ ∈ [0.85, 1.2] for both σ_e = 0.01 and 0.1
  (kinematic regime: ρ ≪ σ_e·a; the ρ² planar-shear regime needs σ_e·a ≪ ρ and should
  NOT appear here — if it does, my epicyclic picture of conjunction distances is wrong).
- **P3 (hot rate).** σ_e=0.1: Λ(1e-3) ∈ [10, 150], point 47 (scales with v_rel ~ σ_e).
- **P4 (impact-parameter uniformity).** Among encounters with b_min < ρ, b_min is uniform:
  P(b < ρ/2 | b < ρ) ∈ [0.4, 0.6].
- **P5 (kick tail).** Per-body kick δv = 2m/(b_min·v_rel) (equal masses, negligible
  focusing at these masses): P(δv > x) ∝ 1/x above the typical value; the crossing rate at
  quantum q_v equals Λ·min(1, δv_typ/q_v) within 30% (the 30% is the b–v_rel independence
  assumption inside the integral).
- **P6 (design numbers, held out).** With the law's finest quantum q_v = 2⁻³² ≈ 2.33e-10·v_K
  (32-bit E/L key), M_belt = 1e-7, W=0.02, N = 2²⁰ (B18b's belt): scar bits per body per
  hour of play at rtf 100 < 6 bits (budget 64 bits/body for 10⁹ in 8 GB). At M_belt = 1e-5
  it breaks: > 200 bits/body/hour.
- **P7 (mass, not count).** In the sub-quantum regime the per-body crossing rate at fixed
  (W, M_belt, σ_e) is independent of N (Λ ∝ N, δv_typ ∝ 1/N): the composed product
  Λ·δv_typ/q_v is constant in N to within the P5 agreement. A billion real bodies cost the
  same live memory as ten thousand, at the same belt mass.
- **Controls.** Blunt (uniform-in-time) sampler undercounts P(b<1e-4) by > 10× on the
  tightest bin; widest Δa bins return P ≈ 0 (the instrument can say zero).

Kill criterion for the run: if the Monte Carlo contradicts P1–P3 by more than the stated
bands, the kinetic model of conjunction distances is wrong and the design table is not
earned; the dossier then reports the measured rates and kills the analytic model instead.
