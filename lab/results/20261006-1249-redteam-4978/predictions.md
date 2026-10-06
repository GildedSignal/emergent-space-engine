# Predictions (written before the decisive run)

Attack: the jet (kick updates the cycle from stored ∂/∂E, ∂/∂L; law.md line 35, adopted with
re-anchoring at a cost of "about 0.05 compiles per kick") near the Schwarzschild separatrix.
Held-out cases: zoom-whirl families I have NOT tuned on (fixed L = 3.7 M, E → E_sep(L)⁻; fixed
u_p = 1/4 with L → 4⁻), plus plunge-crossing kicks and weak-field controls.

Instrument: exact equatorial Schwarzschild geodesics in float64. Δφ, Δt, Δτ per radial cycle by
quadrature on the root-factored first integral (Darwin form, no approximation). The jet is given
the *exact* derivative (5-point stencil on the exact map) — the design's best case. Controls on
the instrument: (i) an independent RK integration of u″ + u = 1/L² + 3u² must match the
quadrature Δφ; (ii) weak-field Δφ − 2π must match the 1PN formula 6πM/p.

Numbers I expect (floor = 10⁻⁶, the red-team df81 re-anchor floor):

- P1 (log divergence): Δφ per radial cycle grows ~ A·ln(1/δ) + B as the fractional distance δ
  to the separatrix shrinks. For the L = 3.7 family I expect Δφ of order 2π at δ = 0.3 rising
  to tens of radians (≥ 10 orbits of phase per radial cycle) at δ = 0.001.
- P2 (jet fails near separatrix, one kick): with a single torque kick ε = 10⁻³ in L (best case
  for the design: exact derivative, modest kick), the jet's error in Δφ exceeds the 10⁻⁶ floor
  already at δ ≈ 0.1 (by ~10²×), and reaches ~0.01–1 rad at δ = 0.01–0.001 (10⁴–10⁶× the floor).
  The same holds for Δt (encounter timing) within a factor of a few.
- P3 (control that must pass): a weak-field orbit (r_p = 50 M, e ≈ 0.1) with the same ε = 10⁻³
  kick has jet error ≪ 10⁻⁶ (the method is fine away from the separatrix; the kill is the
  configuration "jet everywhere", not the cycle mechanism). Also: at fixed r_p = 4 M but
  δ = 0.5 (comfortably bound), error stays small.
- P4 (regime flip): a bound orbit within δ = 0.01 of the separatrix, kicked by 1.1% in L
  (constant E) across it, truly plunges: u reaches the horizon 1/(2M) after only a few radians
  of φ, while the jet predicts a full bound cycle with a next pericenter — an error of type
  (regime), not size.
- P5 (weak-field near-parabolic is NOT the failure): at r_p = 50 M with e → 0.99 (E → 1), the
  Δφ jet stays accurate; the weak-field divergence in Δt is a power law and benign for small
  relative kicks. The kill is specific to the relativistic separatrix (r_p ≲ 6 M).

If P2/P4 hold: the jet is invalid in the near-separatrix band (recompile-per-kick there, ~1
compile/kick not 0.05), and no gate measures it (B12 is weak-field handoffs; B19 classifies
plunge only at unperturbed compilation; B5/B9 measure the unperturbed cycle).
