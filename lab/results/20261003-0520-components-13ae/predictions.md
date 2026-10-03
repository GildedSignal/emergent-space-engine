# Predictions (written before the decisive grid; smoke-tuned only at a=0.12 R_H)

Smoke tuning used only: a/R_H = 0.12, e₀ ∈ {0, 0.3}, both directions, fixed
phases (ω₀=0.7, M₀=1.1), T = 30 planet orbits. Nothing at a ≥ 0.14 was looked
at before this file. Conventions: `avg2Q` = double-averaged quadrupole flow
(r9 `kick-avg`'s law), `avg1Q` = single-averaged quadrupole slow flow (keeps the
evection harmonic cos 2(ω−λ_star), zero moon-orbit-resolution events),
`kickN` = exact Kepler drift + tidal kick at fixed phase step (N per moon orbit,
the current design shape, H0190's layer).

- **P1 (avg2Q is truncation-limited, not strength-limited).** Its relative
  precession error scales ≈ e₀² and only weakly with a: it already exceeds 10%
  at 0.10–0.12 R_H for e₀ = 0.3 (smoke: 18.5% pro, 22.6% retro), and stays
  below 10% for e₀ = 0 circular births (error → multipole floor). So r9's
  τ₀ = 0.0036 (0.17 R_H) was mostly the e₀-distribution crossing the evection
  term, not a tidal-strength boundary of the method.
- **P2 (avg1Q holds the whole hierarchical domain).** For e₀ ≤ 0.3 and
  0.10 ≤ a/R_H ≤ 0.30, both directions, relative precession error ≤ ~3%
  (smoke: 1.6% / 2.2% at 0.12 R_H). It first exceeds 10% only where the true
  dynamics approaches the prograde instability (a ≳ 0.35–0.45 R_H), which is the
  doll/dense-order territory, not the kick layer's.
- **P3 (kick floor of the current shape).** kickN needs N ≈ 8–16 per moon orbit
  for ≤ 10% precession error at e₀ = 0.3 boundary seeds, and N ≈ 64+ for ≤ 1%;
  error falls ≈ N⁻². So the layer's own floor is ~10× below H0190's 32.
- **P4 (held-out cases).** At e₀ = 0.6: avg1Q error grows (5–15%) but stays
  several × below avg2Q's; evection truncation in e is the cause. At a = 0.35 R_H
  prograde: strong modulation or escape; avg1Q's class or precession may break
  there — the honest boundary. Random starting phases shift rates by ≲ the
  quoted errors (quasi-periodic, non-chaotic regime).
- **P5 (multipoles were never the missing term).** The double-averaged
  octupole+hexadecapole residual over the quadrupole is ≤ 3×10⁻³ at 0.3 R_H,
  e = 0.3 (≈ (a/D)² scaling), i.e. three orders below the observed 20% gap.
- **P6 (the floor and the idiot index).** The only frequency the generator must
  resolve is the slow one: events per moon orbit ~ m = n_p/n_moon =
  (a/R_H)^{3/2}/√3 × (slow steps per planet orbit, ~100) ≈ 0.02–0.6 events per
  moon orbit across 0.1–0.5 R_H, vs the design's 32 kicks: idiot index
  ≈ 32·√3/(a/R_H)^{3/2} ≈ 300–1300 over the Hill regime.
