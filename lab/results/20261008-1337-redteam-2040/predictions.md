# Predictions (written before the decisive run)

Attack: representation.md §3, "Perturbations … are kicks on E and L. A cycle's derivatives
are stored with it, so a kick updates the cycle by a multiply-add." The claim under test:
first-order response in (E, L) reproduces the recompiled cycle (Δφ, T_t per radial cycle)
within a behaviour band. Oracle: exact Schwarzschild quadrature (the same integral family
as `bound_period_quad`, H0183). M = 1. Derivatives of the exact map by central differences
(h = 1e-8), so the tested error is the premise's nonlinearity, not derivative estimation.

Cases held out (none tuned on; committed before running):

- P1 weak field, p ~ 100 (e ~ 0.6), kick |ΔL|/L = 1e-4, far from the separatrix:
  relative error of the per-cycle Δφ < 1e-5. Premise holds comfortably.
- P2 strong field, p ~ 12 (e ~ 0.6), same kick: error(Δφ) < 1e-3 (still inside a 1% band).
- P3 near separatrix, δL = L − L_sep = 1e-3 · L_sep, kick |ΔL|/L = 1e-4 (10% of the
  distance): error(Δφ) > 1e-2 and error(T_t) > 1e-2 — the 1% behaviour band breaks.
- P4 a kick that crosses the separatrix (δL = +1e-3·L_sep, ΔL = −2e-3·L_sep):
  truth = plunge (no cycle exists); the multiply-add update returns a finite cycle.
  Misclassification, 1/1.
- P5 scale-free form: error > 1% iff the kick exceeds about 1% of the distance to the
  separatrix (ΔL/δL decides; field strength sets only the prefactor). Tested by matching
  δL/L_sep at p ~ 12 and p ~ 100.

What this would mean: every Peters inspiral and every strong-field tide ends inside the
bad window (T_r and its derivatives diverge at the separatrix), so the cheap path fails
exactly at the plunge — the most player-visible GR event — and the compiler must recompile
there (a cost premise consequence, not just an accuracy one).
