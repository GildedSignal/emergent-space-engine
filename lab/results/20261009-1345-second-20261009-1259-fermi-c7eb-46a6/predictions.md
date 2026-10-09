# Predictions (written before any dump run or RK4 validation)

Run: 20261009-1345-second (second author on 20261009-1259-fermi-c7eb, Fermi lens).
Task: the checker's named gold experiment — per-encounter (d, v_rel) from the shipped truth
encounters, the impulse coefficient validated by integration on real encounters, then m_crit and
the sub-threshold random-walk crossing flux on the measured distribution, over verify belts a, b,
c, d and one game-density 3-D case.

The prior run's checker claims the author's Δa coefficient ((2/3)·2atan(μ/qv²)) is ~13× high and
scales 1/v² where the truth is 1/v_rel (impulse Δa_i = 4 a^2.5 m_j cosψ /(q·v_rel) for equal
geometry), giving m_crit ≈ 1×10⁻¹⁷ M☉ (~1-km rock) at q = 1e-4 AU, σ_e = 0.1, a = 2.7.
I derived the impulse independently (straight-line integral of −μ d/|d|³: Δv_rel = −2μ b/(|b|² v),
Δv_i = +2 m_j b/(|b|² v), Δa_i = 2a²(v_i·Δv_i)) and agree analytically; below are my
pre-registered expectations for the measured runs.

## V — coefficient validation (RK4, Sun + two real belt bodies through real truth encounters)

- V1: across ≥ 90 sampled real encounters (≥ 3 masses spanning 1e-19..1e-13 M☉ each), the
  measured Δa regressed on the impulse prediction has slope in [0.8, 1.25] and no systematic
  residual vs v_rel, d, or cosψ. The prior author's (2/3)θa form will sit ~5–30× above it
  (13× at σ_e·v_k geometry) and regress with the wrong v_rel exponent.
- V2: fitting log Δa ~ α·log v_rel over the natural v_rel spread (1e-4 co-orbital .. 0.3 mixed)
  gives α ∈ [−1.15, −0.85]. The author's form forces α = −2 (rejected at huge significance).
- V3 (control): RK4 with mutual gravity off gives |Δa| < 10⁻³ of the with-mutual signal at the
  validation masses (integrator noise floor well under the signal).

## M — m_crit on the measured distribution

- M1: median m_crit (mass where the median-measured encounter crosses 1 period tick) on the
  game-density case (a ≈ 2.7, σ_e = 0.1, ρ = 1e-4) lands in [1e-18, 5e-17] M☉, i.e. rock radius
  250 m–1.7 km, bracketing the checker's 1e-17 point estimate.
- M2: fraction of measured encounters crossing ≥ 1 tick: < 5% for a 500-m rock, < 50% for a 1-km
  rock, ≈ 100% for 5-km and Ceres. Verify belts at a ∈ [1, 1.5] sit within ~2× of the a = 2.7
  numbers (tick quantum and v_k both scale mildly).
- M3: the co-orbital belt (c) drops m_crit by ≥ 100× vs the hot belt (v_rel ~ 1e-4): fleets and
  co-orbital swarms individualize regardless of mass — the prior author's caveat, now measured.

## F — crossing flux and H_live (3-D game-density: N = 1e9, width 1.5 AU, σ_e = σ_i = 0.1, ρ = 1e-4)

- F1 (a-channel random walk): for a 50-m rock, per-encounter σ_x < 3e-4 ticks → first passage
  > 1e7 orbits; steady crossing flux < 1e-8/body/orbit → < 0.1 distinctions/s at 1e9 bodies —
  negligible vs consumer-scale H_live (≥ 1e5 bits/s), so the ledger's H_live conclusion holds.
- F2 (phase/tp channel — the channel the prior run never checked): a persistent a-offset of S
  ticks drifts phase ≈ S ticks/orbit, so first passage is ~(3/(2σ_x√R))^(2/3) orbits. For a 50-m
  rock at R ≈ 2.8/orbit I expect k* ∈ [100, 3000] orbits — NOT never, but each distinction is
  ≤ 1 tick ≈ 5×10⁻¹¹ rad, ~10⁸ below the player's 10⁻³-rad pixel, so the program belt absorbs
  it; only consumer-resolved bodies need exact tubes. If k* < 20 orbits I will report the
  attractor claim as session-scale-bounded instead.
- F3: the 3-D MC (vertical w, v_z added to measured planar conjunctions) raises m_crit by < 3×
  vs the 2-D transplant (larger d and v_rel weaken the impulse; acceptance prefers small |w|).

## Kill criteria

- V1 slope outside [0.6, 1.6] → the impulse form itself fails on real encounters; I report the
  conflict and nothing else as gold.
- M1 outside [1e-19, 1e-15] M☉ → the threshold claim is not settled by this experiment.
- F2 k* < 20 orbits for 50-m rocks → "the program belt is an attractor between consumer touches"
  fails at session scale and I downgrade the claim explicitly.
