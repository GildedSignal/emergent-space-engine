Grade: gold

**Abstract (for the integrator).** The jet (kick → compiled cycle via stored ∂/∂E, ∂/∂L; law.md line 35, adopted from df81, which had only one checker) is invalid near the Schwarzschild separatrix — the regime it is named for ("strong-field reuse"). Reproduced bit-identically; instrument independently verified (RK pericenters = quadrature to 7 digits at δ = 10⁻³). One 10⁻³-of-L kick errs 10³–10⁹× the 10⁻⁶ floor (up to 110× the cycle itself); energy kicks too (10⁷× at δ = 10⁻³); even a second-order jet fails 3×10⁴×; the re-anchor certificate's "constant C" is 2.7×10⁵ larger than weak field, so its threshold is 50–2500× too lax. A kick across the separatrix is mispredicted as a bound cycle (type error). No frozen gate measures any of it. Adoption: per-kick Darwin root-count regime test + forced recompile in a declared band; small, local, one step.

## Reproduction

- `python3 sep_jet.py` in the run folder: output identical to `sep_jet.out`, every number in the dossier's tables matches. 2.9 s, 79 MB. `work/patch.diff` is empty (no repo edits to apply).
- Prediction timing: `predictions.md` mtime 13:02 precedes `sep_jet.out` 13:08 and `dossier.md` 13:10. `run.log` is empty, so ordering rests on mtimes; consistent.
- Premises verified in the docs: law.md line 35 (the jet, re-anchored, "about 0.05 compiles per kick", C·drift² with C constant, "Graded gold by one checker; the second never ran"); the gate table (B12 weak-field handoffs; B5/B9 unperturbed cycles; B19 classification at unperturbed compilation — nothing kicks then classifies); representation.md §6 cost table; HANDOFF "In flight" line 25 (`NoBoundOrbit` freeze on near-radial fall — the dossier's player-visibility claim is grounded, and honestly phrased as "near-plunge states").

## Adversarial checks (my own, independent implementation)

1. **Instrument at the deepest point**: direct RK integration of the Binet equation at family A δ = 10⁻³ gives pericenter spacings 14.472651 vs quadrature 14.472651. The zoom-whirl quadrature is right where it matters.
2. **Energy kicks** (fixed L, E toward E_sep, ε_E = 10⁻³): err 8.3×10³× floor at δ = 0.01, 1.0×10⁷× at δ = 10⁻³. The kill is not an artifact of torque kicks; encounters move both E and L.
3. **Mechanism**: second-order Taylor (stored ∂²) at δ = 10⁻³, ε = 10⁻³ reduces the error only 3.8× (2.96×10⁻² = 3×10⁴× floor). d²Δφ/dL² = 2.1×10⁴ vs 7.5×10⁻² weak field (2.7×10⁵×). The re-anchor threshold √(floor/C) computed with weak-field C is 50×–2500× too lax across δ = 10⁻²→10⁻⁴ — the certificate's "C constant" premise is directly measured false.
4. **Realistic kick sizes**: err = floor at ε* ≈ 3×10⁻³·δ. At the plane's own kick quanta (10⁻⁴–10⁻⁵ of L, HANDOFF's P3' fit): 14× floor at δ = 0.01 for ε = 10⁻⁴; the kill band narrows to δ ≲ 0.03 (ε = 10⁻⁴) / δ ≲ 3×10⁻³ (ε = 10⁻⁵) but persists, and the regime-flip test binds at every ε.
5. **ε-scaling** with a tight stencil: 81/98/100 per decade — clean quadratic Taylor remainder, not quadrature noise. Corollary: a practical stencil derivative (h = 10⁻⁴) is itself worse than the exact derivative near the separatrix (2.3×10⁻¹ vs 1.12×10⁻¹), so the author's exact-derivative numbers are a *lower bound* on any implementable jet.

## Defect found (non-load-bearing)

`plunge_phi`'s prefactor is √(2s); the substitution u = ua + s·sin²θ gives 2√s. Corrected: horizon at **12.51 rad**, not 8.85 (quadrature ratio exactly √2 = 1.414215; direct RK confirms 12.51, u passes 0.5 and blows up). P4's conclusion is unchanged — the kicked orbit plunges (single real root; RK through the horizon) while the jet predicts a pericenter at 13.8 rad, now 1.3 rad *past* the horizon crossing instead of 4.95. Still an error of type; the dossier's number and the "100×" phrasing margin are wrong there. This is the only defect; `cycle()`'s prefactor is correct (verified twice above).

## Predictions

P2 held (family B even exceeded the predicted range: 2.8×10⁹× at δ = 0.001). P3/P5 controls pass. P4 held in substance (number defective as above). P1 half-wrong — Δφ amplitude ~4× smaller than guessed (2.30 orbits at δ = 10⁻³, not ≥ 10) — reported as a miss, structure (log divergence) as predicted. Honest reporting throughout; no post-hoc edits detected (reproduction is bit-identical).

## Novelty

docs/HISTORY.md has no separatrix/jet run: the G2 judge work (whirl windows, H-entry of 28 September) is oracle-side. df81 — the run whose gold anchored the jet — tested correlated quantum kicks (weak-field statistics: "730 kicks") and its second check never ran. This run is that missing check, and it finds the hole in the strong-field band the jet was adopted for. Distinct, not a redo.

## Goal fit

Shows an adopted premise is wrong in its named regime and converts a silent wrong-type error into a bounded one — principles 13 ("errors never compound": the phase error sits in the description and reaches encounter timing) and 2 ("error type over error size": the flip). The fix is via the regime test, not a bandaid (principle 19). Player-visible today (`NoBoundOrbit` freeze, HANDOFF). Cost of adoption is small and local; it deletes nothing else.

## Why gold, not silver

Reproduced bit-identically; the kill survives every adversarial strengthening (energy kicks, second order, realistic kick quanta — the one experiment I would have demanded, I ran it, and it holds); it falsifies a singly-checked adopted premise at the exact bottleneck the board's focus list names ("the changeover near a secondary" / strong-field cycles); adoption is one step. The two blemishes — P1's amplitude miss (disclosed) and the √2 slip in a decorative number of P4 (found here, conclusion unaffected) — do not touch the load-bearing claim.

## What the author missed

1. The kill band's width scales with kick size (ε* ≈ 3×10⁻³·δ): the forced-recompile band should be sized to the measured kick quantum (10⁻⁴–10⁻⁵ of L), not to ε = 10⁻³; the band is ~30× narrower than the dossier's headline case.
2. The √2 prefactor in `plunge_phi` (above).
3. The exact-derivative jet is the best case; any finite-stencil derivative accumulates extra error near the separatrix — the case against the jet is stronger than reported.
4. The claimed (ε/δ)² scaling is loose: measured 82× and 37× per decade (the logarithmic Δφ divergence adds a slow factor); direction unambiguous.
5. Kerr untested (disclosed by the author); attacks 2–3 argued, not measured (disclosed).
