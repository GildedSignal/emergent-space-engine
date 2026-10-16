# Rung r8 v3: the Binet cone and exact first hits, verified independently

Frozen by the integrator on 1 October 2026, from the proposal of the Opus research run (`artifacts/runs/opus-encounters/result.md`; the research crate `crates/encounters` on `main`). r8 v2 killed three broad phases and showed that certification follows the candidate set. Its `cheap` criterion was the integrator's error: no algorithm could pass it over 20 orbits. The law's requirement now is no work per orbit in the steady state. This rung verifies the claimed representation with an independent truth and adversarial cases.

**Question.** Each orbit is a point (U, V, W) = (1/p, e·cos ϖ/p, e·sin ϖ/p), and two orbits cross only inside the cone ΔU² ≤ ΔV² + ΔW². At a crossing, the pair's timing is an integer circle rotation whose next close conjunction a continued-fraction recursion finds, and a second-order window with an exact per-pair check decides it. Does this find every encounter exactly, with steady-state work near the encounter rate and kicks that stay local?

**Configurations.**
- `diophantine`: the research crate `crates/encounters`, run as it is on `main` (the code under test). Everything else here is the author's own: the truth, the other configurations and the adversarial cases.
- `element-sort` (negative): r8 v2's configuration. It must fail `steady`.
- `conjunction-sampled` (negative): r8 v2's reference method (a distance check only per synodic conjunction). It must fail `complete`, as the narrow belt shows.
- `oracle` (positive): it reads the truth's encounter list.

**Cases** (sampler: r8 v2's, Python `random.Random(20261008)`, extended):
- (a) 16 belts at N = 10³ over 100 orbits, ρ log-uniform in [10⁻⁴, 10⁻³], plus four adversarial belts: narrow in a (|Δn|·T < 2π for most pairs), co-orbital, equal-period (identical memo keys) and hot (σ_e = 0.1).
  - **The truth:** conservative advancement over every radially overlapping pair, dense in time, independent of any conjunction logic. An encounter is a local minimum of distance below ρ.
- (b) Steady: N = 3000, σ_e = 10⁻², ρ = 10⁻⁴, 10⁵ orbits, no kicks.
- (c) Scaling: N = 10³, 10⁴, 10⁵ with ρ ∝ 1/N.
- (d) Kicks: 100 kicks at N = 10⁴, each changing one body's elements by δa/a ≈ 10⁻³.

**Metrics,** one set per configuration:
- `missed_fraction`: truth encounters not reported, pooled over (a).
- `false_fraction`: reported encounters not in the truth, pooled over (a).
- `steady_ratio`: on (b), events per body per orbit divided by the truth's encounters per body per orbit.
- `checks_per_encounter`: exact distance checks per true encounter, pooled over (a).
- `scale_exponent`: the fitted exponent of check work against N, on (c).
- `kick_setup_ratio`: on (d), the median of pairs set up per kick divided by the kicked body's candidate count.
- `other_certificates_touched`: on (d), certificates of pairs not involving the kicked body that were recomputed, in total.
- Reported, not gated: setup µs per pair, the crossover horizon against element-sort, bytes per body.

**Output.** `metrics.json`, plus one picture: events per body per orbit against the horizon (log-log) for each configuration, with the truth's encounter rate as a line.

```configs
diophantine candidate
element-sort negative
conjunction-sampled negative
oracle positive
```

```criteria
complete behaviour missed_fraction <= 0.0
sound behaviour false_fraction <= 0.0
steady type steady_ratio <= 2.0
checks cost checks_per_encounter <= 1.5
scales type scale_exponent <= 1.1
local cost kick_setup_ratio <= 1.05
isolated type other_certificates_touched <= 0
```
