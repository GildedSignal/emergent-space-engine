Grade: gold

**Abstract.** Claim: the jet (law.md line 35's strong-field reuse, re-anchored with a constant C at "0.05 compiles per kick") is invalid near the Schwarzschild separatrix, and no gate measures it. Reproduced bit-identically (3 s, < 50 MB); instrument cross-checked (RK vs quadrature to 7 digits; weak-field 1PN confirmed). Adversarial cases (mine): error ∝ ε², so even a 10⁻⁵-of-L kick fails the floor 14–132× at δ = 10⁻³ (not cherry-picked); two new L families (3.9, 3.55) blow up identically; the plunge flip verified by root count and RK, and it is bidirectional. One number corrected: the horizon sweep is 12.51 rad, not 8.85 (a √2 slip in `plunge_phi`); P4's verdict is insensitive. Adoption is small: post-kick root-count regime test plus a recompile band plus one gate criterion.

## Reproduction

- `python3 sep_jet.py` in a clean tree: output byte-identical to `sep_jet.out`, 3.0 s, well under budget. `work/patch.diff` is empty (no tree edits to apply).
- Provenance: `predictions.md` 13:02:19 < `sep_jet.py` 13:08:39 < `sep_jet.out` 13:08:44 < `dossier.md` 13:10:24; `run.log` is empty, so file times are the only order evidence — they support held-out-before-run.
- Instrument independently checked: I re-derived the Darwin θ-substitution algebra (the `cycle()` integrand is correct; C1's RK agreement at 7 digits confirms it in execution), and at p = 225 the quadrature's Δφ−2π sits 2.08 % off 6π/p, consistent with the 2PN term — the author's C2 gap at p = 75 is physics, not instrument error.

## Held-out predictions

P2 held and exceeded range (2.8×10⁹× floor at δ = 0.001, family B); P3/P5 controls pass (P3a is 2.0× floor, "≈ floor" as stated); P4 held in verdict; P1's amplitude (~4× high) is honestly reported as a miss. The declared held-out families are exactly the ones run.

## My adversarial cases

1. **ε-scaling** (is 10⁻³ cherry-picked?): at δ = 10⁻³, error falls as ε² (step ratios 37→82→98→100× per decade) and even ε = 10⁻⁵ leaves Δφ 14× and Δt 132× floor; ε = 10⁻⁶ is the first under the Δφ floor. The band fails for any realistic kick.
2. **New families** (held out from the author too): L = 3.9 and L = 3.55 give the same blow-up (1.3×10⁵× floor at δ = 10⁻³; 4.4×10⁶× at δ = 10⁻⁴). Generic, not an artifact of L = 3.7/4.
3. **P4 plunge, independent methods**: the kicked orbit's cubic has one real root (plunge); RK on the Binet ODE from the true turning point is monotone in u and reaches u = ½ at φ = 12.5119 rad; the corrected θ-substitution gives 12.5118. The bound side has three roots. The flip is an error of type, as claimed.
4. **The reverse flip**: L kicked up across L_sep turns a plunging orbit into a bound one (cycle Δφ = 15.05 rad exists) — a jet anchored on the plunge side predicts absorption. The type error is bidirectional, strengthening the claim.
5. **Weak-field control at another point**: p = 225 matches 1PN to 2 %, the expected 2PN offset.

## Novelty

The adjacent prior work is `20261006-0346-redteam-df81` (cited in law.md line 35), which *calibrated* a global C from correlated quantum kicks; this run shows C is not a constant (it varies by ≥ 6 orders across the bound band and diverges at the separatrix) and that the bound↔plunge flip is unrepresentable by any derivative update — distinct, and the two compose. The old G2.2 judge explicitly excluded separatrix anchors (HISTORY, the gravity-law red-team entry): the territory was known dangerous and never measured for the jet. No gate covers it: B12 is Jupiter-like handoffs, B19 classifies plunge only at unperturbed compilation, B5/B9 measure the unperturbed cycle (all verified against law.md's gate table). The HANDOFF's live `NoBoundOrbit` freeze is real, and representation.md:32 still carries the killed Binet-map text while law.md:20 replaced it — attack 6 is accurate.

## Goal fit

Shows a premise of the adopted law text is wrong in its own designated domain ("strong-field reuse is the jet", law.md line 35), violating PRINCIPLES 13 ("basically we don't want errors that can compound") and the design's own one-floor-per-event budget, as an error of type (principle 2: "error type over error size"). Adoption is one step: the Darwin cubic's root count is already computed at compile; the band is small; recompile-per-kick there is honest. The board's focus list names the changeover problem and the Schwarzschild tide; the marquee strong-field content (§1 of representation.md) is exactly where this bites.

## What the author missed

- **`plunge_phi` has a √2 algebra slip** (`sqrt(2·D)·cosθ` where `2·sqrt(D)·cosθ` belongs): the true horizon sweep is 12.51 rad, not the reported 8.85. Verified three ways (RK from the true turning point, corrected quadrature, ratio exactly 1.414214). The dossier sentence must be corrected on adoption; the phantom pericenter (13.8 rad) still falls after the horizon crossing, so P4's verdict stands.
- P4's clocks are loosely framed: the jet's 13.8 rad counts from a pericenter, the truth's sweep from the plunging orbit's only turning point (an apocenter). The comparison should be restated phase-explicitly; the type error survives any phase.
- The band's *measure* is unquantified (what fraction of BH-adjacent orbits sit within δ of the separatrix, and how they get there) — the cost line of the recompile-band fix rests on "the band is small", asserted, not measured.
- Attacks 2 and 3 are argued, not measured (flagged by the author; lens-limited). Kerr is untested, and the same failure is a fortiori there.
- The dossier says the error "scales ≈ (ε/δ)²": confirmed in ε; in δ it carries the logarithmic zoom-whirl correction (measured step-down 82→37× per decade), which the author's own Δφ column implies but the text oversimplifies.
