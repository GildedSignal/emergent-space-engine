topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261015-0128-dynamics-b9be

# Chaos, the shadowing clause, and trapping statistics under quantization

## Current best

**The dwell arm now runs on the shipped law, and there the toy's distortion is absent:
trapping statistics are preserved at the engine's Q, while a different statistic — survival
— is not (20261015-0128-dynamics-b9be).** Scene: the judge's own CRTBP (`JUPITER`, μ = 1e-3),
144 ICs across the 1:1 co-orbital (Trojan) band edge, horizon 512 P, in-band = |a/sep−1| ≤
√(8μ/3) sampled P/8. Classes (captured/escaped/dead): float oracle 1e-12 and 1e-10 both
54/90/0; shipped plane (step_log2 = 7) **54/42/48**; plane at 32× coarser cadence 50/62/32.
Captured counts identical to the oracle (54 = 54), dwell p90 equal (13.0 vs 13.6 P), and the
statistic survives even a 32× coarser cadence — so at engine Q, in this scene, the shadowing
clause's invariant statistics hold and need no certificate. Checker-verified stronger: on the same
96 surviving ICs the max-dwell quantiles are identical to the oracle (p50 13.00 vs 13.00 P, p90
512.12 vs 512.12). **The separating statistic is survival: the plane loses 48/144 of the ensemble
(41 of the 48 outer chaotic-layer ICs; 7 at |du| ≤ 0.6) while the oracle keeps them — false
deaths, a behaviour class the truth never has** (two more ships refused at birth; the conjunction
epoch reading rests on the 16 P trace's two deaths). Checker, outside the author's range: a
periapsis-resolved oracle pass (P/256, both surfaces) puts the ensemble minimum at 2.89 Rp (the
P/8 sampling missed 10×) yet **zero** oracle trajectories enter the planet or approach the star
(min 300 star radii), so no plane death stands for a real surface hit; all 48 deaths are
`fault=None, refusals=0, handoffs=0`, far from both surfaces at every sample. Rung warning:
dwell cannot separate even a coarse law (the pre-registered negative control failed to fail);
deaths can (48/32/0). First run on shipped code; one ensemble, one μ; the plane-side death
branch (real star-crossing periapsis of a diverged trajectory vs spurious planned terminal) is
still open.

The toy result stands for what it measured (20261014-2248-redteam-5cad): the standard map's
quantized law distorts trapping tails by Q, non-monotonically, and deterministic rounding is
not interchangeable with same-magnitude noise. The shipped law's error model (error-feedback
carries, bounded handoffs, engine Q ~2e-9 relative here) is not the toy's per-event state
rounding, which is the read of why the distortion vanished.

## Refuted

- "A deterministic law with the right statistics is a true orbit of nearby initial
  conditions" (representation.md thesis 2) in mixed phase space: the quantized law's
  trapping statistics are not the true ones at any Q tested (toy, 20261014-2248-redteam-5cad).
  Not refuted on the shipped law: preserved there, this scene, engine Q
  (20261015-0128-dynamics-b9be).
- "Deterministic rounding per event ≈ noise of the same magnitude" (the doc's error
  model implicit equation): 14.1% vs 1.2% permanent traps at Q = 10⁻³ (same toy run).
- "The toy's distortion transfers to the shipped law at engine Q": not in this scene —
  captured 54 vs 54, p90 13.6 vs 13.0 P, unchanged at 32× coarser cadence
  (20261015-0128-dynamics-b9be).

## Open directions

1. **The survival certificate** (the new separating statistic): the oracle-side pass is done
   (checker, P/256, both surfaces: zero contacts — no plane death stands for a real hit); what
   remains is the plane-side branch — sample the plane's own state at kick resolution through
   each death (or read the binding's terminal/periapsis) to decide real star-crossing periapsis
   of a diverged trajectory vs spurious planned terminal, at μ = 1e-2 too; then a false-death
   bar in B12's family for the co-orbital layer. This is what the integrator would gate.
2. **Stress the regime before trusting the preservation**: μ = 1e-2 (thicker layer), longer
   horizon, eccentric births; the toy's distortion peaked near critical K.
3. **Freeze the trapping-statistics rung** (criteria above) once B12's statistic is
   rebuilt — with the measured warning that dwell alone cannot fail a coarse law: the rung
   must include the survival class or it is a control.

## Contradictions

None open. The toy (rounding distorts) and the shipped law (preserved) measure different
error models at different Q; both stand, and the pair now names the boundary of the claim.

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
  quantization inflates or crushes trapping tails by Q; rounding ≠ noise.
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped law — trapping preserved
  at engine Q (54 = 54 captured, robust to 32× cadence, identical quantiles on the surviving
  96); survival is the separating statistic (48 vs 0 dead, zero oracle surface contacts).
