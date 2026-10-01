# Rung r10: the compiled drift plus kicks, with a smooth changeover

Frozen by the integrator on 1 October 2026, before any run. This is the cheapest falsifier of the plane's motion law (`docs/law.md`, "Perturbed motion"; `docs/plane.md`) before the plane commits to it. events3 (a state-selected switch at the sphere of influence: Jacobi growth 0.83) and events4 (a free Cartesian drift: Jacobi −28 in 8 orbits) were killed. r9 and r4 v3 killed averaged tides beyond τ₀ and compiled normal forms.

**Question.** In the circular restricted three-body problem (star mass 1 − μ, planet μ on a circle), the motion is a symmetric, symplectic split. The drift is an exact Kepler drift about the dominant body. Kicks carry the rest at a fixed step in the drift's phase. Near the planet, a smooth changeover function of the separation splits the interaction across recursive sub-steps (Duncan, Levison and Lee 1998, SyMBA). Does this keep the Jacobi constant bounded, get the Hill moons' apsidal precession right, and keep resonances librating, at a cost far below dense stepping?

**Configurations.**
- `symba`: Kepler drift about the star, planet kicks, and the changeover with recursive sub-steps near the planet. Moons in the planet's region drift about the planet; the dominant body follows the changeover, never a hard switch.
- `wh-fixed`: Wisdom–Holman with no changeover (a fixed step everywhere; close passes unresolved).
- `truth` (positive): DOP853 at relative tolerance 10⁻¹² in barycentric inertial coordinates, converged against 10⁻¹³ (B12's and B14's reference).
- `soi-switch` (negative): the drift switches dominant body at the sphere of influence (events3's configuration, state-selected). It must fail `jacobi`.

**Cases** (sampler: Python `random.Random(20261011)`):
- B12's 16 ships (μ = 10⁻³; ≥ 20 sphere-of-influence crossings in 200 planet periods; the frozen seed rule from `xtask/src/behave/sample.rs`, ported);
- B14's 256 moons (0.2–0.9 Hill radii, prograde and retrograde, e₀ up to 0.3, 50 planet periods);
- r4 v3's resonant cases (2:1 and 3:2, μ from 3×10⁻⁵ to 3×10⁻³, detuned).

**Metrics,** one set per configuration:
- `jacobi_exponent`: the median over B12's ships of the growth exponent of |ΔC_J/C_J|, judged only above a 10⁻¹² floor (B12's rule).
- `class_match`: the fraction of non-chaotic moons whose bound or escaped class matches the truth.
- `precession_match`: the fraction of bound moons with a defined apse whose apsidal rate is within 10% of the truth's.
- `libration_ratio`: over librating resonant cases, the worst of min(r, 1/r) for the libration amplitude.
- `force_evals_per_orbit`: the median number of force evaluations per orbit of the body's dominant period (the truth reports its own).

**Output.** `metrics.json`, plus one picture: |ΔC_J| against time for each configuration on three ships.

```configs
symba candidate
wh-fixed candidate
truth positive
soi-switch negative
```

```criteria
jacobi type jacobi_exponent <= 0.2
class behaviour class_match >= 0.99
prec behaviour precession_match >= 0.99
lib behaviour libration_ratio >= 0.8
cheap cost force_evals_per_orbit <= 200
```
