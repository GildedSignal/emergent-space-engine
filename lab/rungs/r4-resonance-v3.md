# Rung r4 v3: the resonant normal form

Frozen by the integrator on 30 September 2026. r4 v1 and v2 killed first-order kicks along the unperturbed orbit, whether per conjunction or integrated over arcs, at every window size (the v2 checker's refinement study: the limit over-pumps e about 2×, because first order in μ lacks the phase feedback that limits a resonance). The law now names the next configuration (`docs/law.md`, kicks): average over the fast, non-resonant angles only and keep the resonant angle. Julien, 30 September, allows this: averaging is fine for predictable behaviour ("an orbit is stable an predictable"), and a libration is one.

**Question.** Near a first-order mean-motion resonance (j+1):j, the averaged Hamiltonian keeping only the resonant angle φ = (j+1)λ₂ − jλ₁ − ϖ₁ is one degree of freedom (the "second fundamental model of resonance"), so it is integrable and compiles like a cycle. Does that compiled generator reproduce the resonance's behaviours: libration or circulation, the eccentricity pumping, and the resonance width? What does it cost per orbit?

**Configurations.**
- `nf1`: the first-order-in-e normal form with the perturber's disturbing function to first order in μ, averaged over the fast angles; its trajectories are the level curves of the 1-DOF Hamiltonian, followed exactly (a compiled cycle in (φ, Φ)).
- `nf2`: the same, with the second-order-in-e resonant and secular terms included.
- `truth-1200` (positive): r4 v2's dense truth, judged against 2400. It must pass.
- `averaged` (negative): the full orbit average (the resonant angle averaged away). It must fail.
- `arc-g8` (negative): r4 v2's killed configuration. It must fail.

**Cases.** r4 v2's, with two fixes that its checker asked for:
- **Resonant:** 2:1 and 3:2 at perturber mass ratios 3×10⁻⁵, 3×10⁻⁴ and 3×10⁻³, each at three detunings (exact, and ±1/3 of the resonance half-width), so that the metric never sits on exact commensurability alone. Initial phases: the red-team's, with w₂ read in **degrees** where the v2 checker found the rung meant that (λ₂₀ = 4°).
- **Controls, far from resonance:** period ratios 5.0, 2.55 and 2.15.
- The truth integrator and its convergence ladder are r4 v2's. Each case runs for at least 200 synodic periods.

**Metrics,** one set per configuration:
- `e_pump_ratio_min`, `e_pump_ratio_max`: as in v2.
- `libration_amplitude_ratio`: over the resonant cases that librate in the truth, the worst ratio of the law's libration amplitude to the truth's, symmetrized (min(r, 1/r)), where 1 is perfect. This replaces v2's concentration, which degenerates at exact commensurability.
- `regime_match_fraction`: over resonant cases, the fraction whose regime (libration or circulation) matches the truth.
- `control_pass_fraction`: as in v2.
- `dense_steps`: as in v2 (0 for candidates).
- `evaluations_per_orbit`: the median number of generator evaluations (event updates) per inner orbit.

**Output.** `metrics.json`, plus one picture: the (φ, Φ) phase portrait of the normal form with the truth's trajectory overlaid, for one librating and one circulating case.

```configs
nf1 candidate
nf2 candidate
truth-1200 positive
averaged negative
arc-g8 negative
```

```criteria
pump behaviour e_pump_ratio_min >= 0.8
pumphi behaviour e_pump_ratio_max <= 1.25
amp behaviour libration_amplitude_ratio >= 0.8
regime behaviour regime_match_fraction >= 1.0
ctrl behaviour control_pass_fraction >= 1.0
cheap type dense_steps <= 0
cost cost evaluations_per_orbit <= 8
```
