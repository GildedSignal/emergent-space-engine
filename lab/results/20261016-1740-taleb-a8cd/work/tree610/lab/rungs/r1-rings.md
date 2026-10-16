# Rung r1: orbits in rings around one mass

Frozen by the integrator on 29 September 2026, before any run. Design: [docs/representation.md](../../docs/representation.md). If every candidate is killed, only those configurations die, never the method.

**Question.** Around one static Schwarzschild mass (G = c = M = 1, equatorial plane, float64), are orbits and light correct in a cell model where motion inside a cell is that cell's exact local solution, the cells follow the rotational symmetry, and one radial cycle repeats exactly?

**Configurations.**
- `binet-m8`, `binet-m16`, `binet-m32`: Binet cells.
  - With u = 1/r, bands are rings r_k = 2^(k/m) (m bands per octave, k an integer), and u_k is the value at the band's geometric centre.
  - Inside band k the orbit obeys u″ + (1 − 6u_k)·u = 1/L² − 3u_k², where ″ is d²/dφ². Its exact solution is a rotation when 1 − 6u_k > 0 and a hyperbolic motion otherwise.
  - u and u′ are continuous across bands.
  - Coordinate time per band is a fixed rule of the band and of (E, L): dt/dφ = E/(L·u²·(1 − 2u)), integrated over the band's φ-interval. The author states the rule, and it may not depend on the body's step.
  - Light is the same model with the 1/L² term dropped (u″ + (1 − 6u_k)u = −3u_k²), parameterized by b = L/E.
- `river-m16`, `river-m32`: river refraction at the same rings.
  - Inside ring k the flow is the constant-magnitude radial flow β_k = −√(2/r_k)·r̂, with Hamiltonian H = √(1 + |p|²) + β·p (light: |p| + β·p).
  - At a ring boundary, H and L are conserved exactly and the radial momentum is solved; no real root means reflection, a turning point.
- `square` (negative): a dyadic square grid, cell side = r/16 at the cell's centre, with a constant flow per cell and H conserved at edges. It must fail.
- `tiltonly` (negative): a kick that rotates the velocity toward the mass and keeps its magnitude. It must fail.

**Cases** (sampler: Python `random.Random(20260930)`, drawn in this order).
- **Bound seeds:** 256, with p log-uniform in [10, 1000] and e uniform in [0, 0.7]. Reject and redraw unless p ≥ 6.5 + 2e.
- **Light seeds:** 64, with b log-uniform in [10, 1000], launched from r = 10⁴ toward the mass. Deflection is measured with the exact outgoing tail correction beyond r = 10⁴.
- **Capture:** E = 1, inward from r = 100, with L/4 ∈ {0.5, 0.9, 0.97, 1.03, 1.1, 1.5}.
- **Photon capture:** b/(3√3) ∈ {0.9, 0.97, 1.03, 1.1}.
- **Innermost stable orbit:** L 1% above the circular value at r = 7 must stay bound for 100 orbits; L 1% below the circular value at r = 5.5 must plunge within 50 orbits.
- **Long runs:** 32 of the bound seeds (the first 32 drawn) run for 10⁴ radial cycles.

**Oracle** (float64, independent of the configurations): port `periapsis_elliptic` (`xtask/src/gr_oracle.rs`), `bound_period_quad` (`xtask/src/gr_oracle_extended.rs`) and `deflection_quadrature` (`xtask/src/gr_oracle.rs`). The checker verifies each ported value.

**Metrics,** one set per configuration:
- `precession_pass_fraction`: the fraction of bound seeds with |Δφ − Δφ_GR| ≤ 0.01·Δφ_GR, where Δφ is the advance per radial cycle.
- `prograde_fraction`: the fraction of bound seeds whose advance is > 0.
- `period_pass_fraction`: the fraction of bound seeds whose radial period in coordinate time is within 0.1% of the oracle's.
- `deflection_pass_fraction`: the fraction of light seeds within 1% of the oracle.
- `capture_misclassified`: the count of wrong outcomes over the capture and photon-capture cases (absorbed means r ≤ 2 was reached).
- `isco_correct`: 1 if both innermost-stable-orbit cases behave, else 0.
- `shape_kept_fraction`: over the long runs, the fraction whose periapsis and apoapsis stay within 1% of their first-cycle values.
- `cycle_repeat_fraction`: over the long runs, the fraction where the band-crossing sequence of cycle 2 equals cycle 1's, and every later cycle's Δφ and Δt equal cycle 1's to 1e-12 relative.
- `crossings_per_cycle`: the median, over bound seeds, of band or ring crossings per radial cycle.

**Output.** `metrics.json`, plus one picture: the orbit trace for p = 20, e = 0.5 over 5 cycles per configuration, and five light paths.

```configs
binet-m8 candidate
binet-m16 candidate
binet-m32 candidate
river-m16 candidate
river-m32 candidate
square negative
tiltonly negative
```

```criteria
prec behaviour precession_pass_fraction >= 0.99
prog type prograde_fraction >= 1.0
period behaviour period_pass_fraction >= 0.99
defl behaviour deflection_pass_fraction >= 0.99
capture behaviour capture_misclassified <= 0
isco behaviour isco_correct >= 1
shape type shape_kept_fraction >= 0.99
repeat type cycle_repeat_fraction >= 0.99
cost cost crossings_per_cycle <= 512
```
