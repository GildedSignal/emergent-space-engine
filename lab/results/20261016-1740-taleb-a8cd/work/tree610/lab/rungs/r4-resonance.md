# Rung r4: kicks keep resonances that averaging erases

Frozen by the integrator on 29 September 2026, before any run. Source: the premise red-team (claude/lab-20260929-1835-redteam-2ef5), whose checker named this as the experiment that would make it gold. Its truth integrator, `e1_resonance.py`, may be reused as the reference.

**Question.** Does the design's event layer reproduce mean-motion-resonance behaviour? That layer is exact Kepler cycles between conjunctions, plus an analytic kick that depends on phase and is applied at each conjunction. Resonance behaviour means eccentricity pumping and a librating resonant angle, which an orbit-averaged layer erases. No dense integration is allowed anywhere in a candidate.

**Configurations.**
- `conj-quad`: exact Kepler cycles, plus one analytic quadrupole tidal kick at each conjunction, evaluated at the conjunction's true phase.
- `conj-oct`: the same, with the octupole term added.
- `averaged` (negative): orbit-averaged kicks, as in H0190 K2. It must fail.
- `none` (negative): no perturbation. It must fail.

**Cases.**
- **Resonant:**
  - a 2:1 case with perturber mass ratio 3×10⁻³, as the red-team ran it;
  - the red-team checker's phase-shifted 2:1 case (w2 = 4.0), whose truth has libration concentration 0.867.
- **Controls, far from resonance:** period ratios 5.0, 2.55 and 2.15.
- **Truth:** a dense float64 N-body integration, converged over 600, 1200 and 2400 steps per orbit (the red-team's).
- Each case runs for at least 200 synodic periods.

**Metrics,** one set per configuration:
- `e_pump_ratio_min`: over resonant cases, the minimum of (the law's maximum e₁) / (the truth's maximum e₁).
- `e_pump_ratio_max`: the maximum of that ratio.
- `libration_ratio_min`: over resonant cases, the minimum of the law's resonant-angle concentration / the truth's.
- `control_pass_fraction`: the fraction of controls whose secular e₁ envelope is within 20% of the truth's.
- `dense_steps`: the number of dense integration steps inside the configuration. It must be 0, which is what makes this the kick layer.
- `kicks_per_orbit`: the median number of kicks per inner orbit.

**Output.** `metrics.json`, plus one picture: e₁ against time, with the law and the truth overlaid for each case, and the histogram of the resonant angle.

```configs
conj-quad candidate
conj-oct candidate
averaged negative
none negative
```

```criteria
pump behaviour e_pump_ratio_min >= 0.8
pumphi behaviour e_pump_ratio_max <= 1.25
lib behaviour libration_ratio_min >= 0.8
ctrl behaviour control_pass_fraction >= 1.0
cheap type dense_steps <= 0
cost cost kicks_per_orbit <= 8
```
