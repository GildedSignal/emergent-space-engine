# Rung r4 v2: arc-integrated kicks keep resonances that averaging erases

Frozen by the integrator on 29 September 2026. r4 v1 (claude/lab-20260929-1940-rung-r4-resonance-3530) killed instantaneous per-conjunction kicks: the checker corrected the author's sign error in the osculating elements, and the kill still stood, with over-pumping of 2–9× and failed controls. That kills the configuration, not the method. v2 tests kicks integrated along the arc. Source: the premise red-team (claude/lab-20260929-1835-redteam-2ef5), whose checker named this as the experiment that would make it gold. Its truth integrator, `e1_resonance.py`, may be reused as the reference.

**Question.** Does the design's event layer reproduce mean-motion-resonance behaviour when each kick is the first-order integral of the perturbing acceleration along the unperturbed Kepler arc between conjunctions? Resonance behaviour means eccentricity pumping and a librating resonant angle. The arc is never integrated: the orbit is held fixed within each window, and the change of the invariants is applied at the window's end (Gauss–Picard, first order). Osculating elements must round-trip position and velocity to 10⁻¹².

**Configurations.**
- `arc-g8`: windows between conjunctions, with the kick computed as Gauss quadrature at 8 nodes along the unperturbed arc, using the full direct and indirect perturbing acceleration.
- `arc-g16`: the same, with 16 nodes.
- `arc-g8-half`: the same as arc-g8, with two windows per synodic period.
- `truth-1200` (positive): the dense truth at 1200 steps per orbit, judged against truth at 2400. It must pass, or the criteria are unpassable.
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
- `dense_steps`: the number of dense integration steps inside the configuration. It must be 0 for candidates; quadrature nodes along a fixed arc are not dynamics steps. The positive control reports 0 by convention.
- `kicks_per_orbit`: the median number of kicks, i.e. window ends, per inner orbit. Quadrature nodes are reported separately in the dossier.

**Output.** `metrics.json`, plus one picture: e₁ against time, with the law and the truth overlaid for each case, and the histogram of the resonant angle.

```configs
arc-g8 candidate
arc-g16 candidate
arc-g8-half candidate
truth-1200 positive
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
