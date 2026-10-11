Grade: gold

**Abstract (for the integrator).** The kick jet's premise ("a kick updates the cycle by a multiply-add", representation.md §3) is measured false outside a corner, and nothing guards the border. Reproduced bit-identically (`python3 probe.py`, 4 s). One-kick jet error = C·(r_apo·α)², C ∈ [1.9, 6.1] (my extrapolation to r_apo = 10⁵: C → 1.8): law.md's "about 0.05 compiles per kick" holds only near r_apo = 40, α = 10⁻⁶; at p = 100, e ≥ 0.9 one 10⁻⁶ quantum kick breaches the 10⁻⁶ floor (to 190×), at r_apo = 2000 every kick recompiles (N_floor = 1, measured), near the plunge separatrix encounter kicks (α ≥ 10⁻³) err 43–79% or exit the bound family, and r1's ISCO seed sits 0.19% in E from that separatrix. Also verified: representation.md still teaches the dead Minsky mechanism as primary and names rungs r5/r6 that were never frozen. Adopt in one step: root-distance recompile trigger (roots darwin16 already factors), one kick-rung criterion, two doc fixes.

**Reasons.**

1. **Reproduction.** Clean tree, `patch.diff` empty (self-contained probe). `python3 probe.py` in a fresh directory: `probe_out.json` byte-identical to the author's, 4.0 s, well under budget and 2 GB. Every number the dossier cites against `probe_out.json` matches (P1 grid, C ∈ [1.89, 6.14] recomputed by me; N_floor 178/18/2; exponents 1.9962; separatrix |∂T/∂E| 2.8e4 → 2.6e7, Δφ 15.5 → 30.6; seed gap 1.9297e-3; whirl 14.18 rad = 2.26 rev). I re-derived the seed's (E, L, r_c, E_sep) by hand from the double-root conditions (L_circ² = r²/(r−3), r_c² − L²r_c + 3L² = 0): all agree.

2. **Pre-registration.** File times: run start 22:35:48, `predictions.md` 22:42:15, decisive `probe_out.json` 22:52:31 — predictions precede the run. The scorecard is honest: P1 and P4 failed in the direction of the finding and are reported as failures, not held; P2 held with a disclosed reconciliation (730/18 = 40.6 ⇒ df81's quantum ≈ 2.5e-8, flagged as a guess).

3. **My attacks (all consistent with the claim).**
   - h-refinement (h = 2e-3/1e-3/5e-4): headline 1.886974e-4 at p = 100, e = 0.99 stable to 8 digits — not quadrature noise; the 5.18e-9 case likewise.
   - Mixed-sign kicks (E±, L± at p = 100, e = 0.99): all within 1.9e-4 ± 0.7%; the E-only channel is the envelope, L-only 7.5e-12. The dossier's "wrong if L-dominant" branch is closed.
   - Extrapolation one decade past the grid (p = 100, e = 0.999 and p = 1000, e = 0.99, both r_apo = 10⁵): C = 1.81/1.83, error 1.8e-2 per quantum kick — the validity condition r_apo·α < 4e-4 extrapolates.
   - Escape side: at p = 100, e = 0.99 (1 − E = 9.95e-5), α ≥ 1e-4 on E exits the bound family — the categorical failure the dossier showed for plunge also holds for unbinding.
   - Recompile saturation at r_apo = 2000, α = 1e-6: measured N_floor = 1 (first kick already 7.57e-6 > floor) — "every kick recompiles" confirmed directly.
   - Separatrix robustness: the 0.466 error at ε = 1e-6 is stable across derivative steps 1e-8 → 3e-7 — not a finite-difference artifact.
   - The p = 500/1000 precession ratios (1.0092/1.0046), which the shipped code does not regenerate: I regenerated them (1.00922/1.00459) — correct, but see misses.

4. **Novelty.** The only prior on this premise is df81 (law.md line 35: 730 correlated quantum kicks, C·drift², "about 0.05 compiles per kick" — one orbit family). New here: the domain map (C vs r_apo), the correction that the adopted 0.05 figure is a corner, the encounter/separatrix categorical failures, the ISCO-seed proximity, and the unguarded-domain audit. Nothing in HISTORY.md or the docs covers the jet's validity domain; the HISTORY "jet" hits are unrelated linearized-GEM Delay/Bend jets.

5. **Doc claims verified.** representation.md line 67 quotes §3 exactly; line 32 still names Minsky's two-addition map as "the primary in-cell solution" while law.md line 20 records its replacement by `space-darwin16-v1`; §7 (lines 129–130) names r5/r6 and `lab/rungs/` contains only r1–r4, r7–r10; the gate table (law.md B5–B19) has no recompile-rate or jet-domain criterion; B17/r4 v3 cases are e₀ = 0.02 (near-circular); r1 line 25 is the quoted ISCO seed; §6's kick row "<1% of a core" and the mass-moments/spokes tension (lines 36 vs 31) are both real text.

6. **Goal fit.** Board focus items "fewer kicks per orbit" and the smoothness p99 both route through the jet; the finding converts a hidden surprise into a schedulable certificate. PRINCIPLES 13 ("errors never compound… basically we don't want errors that can compound that's the goal"), 21 ("rough first, refine when a certificate could break… simple and powerful"), 19 (wrong-representation signal; the dead Minsky text is exactly the drift it warns of).

**What the author missed.**
- Two oracle-validation numbers (precession ratios at p = 500/1000) are in the dossier but not regenerable by the shipped `probe.py` — the exact failure mode the taste log flags. I regenerated them and they are correct; the record should carry them in `probe_out.json`.
- The Kepler T-channel remainder is 15/8·α² (measured 1.8751e-12 at α = 1e-6), not the stated 15/4·α². Immaterial (both ≪ the precession-phase term at all measured r_apo) but it is a derivation slip.
- "2.8 compiles/kick at r_apo = 2000" is an unsaturated formula extrapolation: compiles/kick caps at 1, and the measurement (N_floor = 1) says every kick recompiles. The physical conclusion is stronger than the number, but the number as printed cannot occur.
- The L-channel errors (≤ 7.5e-12) sit at the oracle's own h-refinement noise (~1e-11): the honest statement is "harmless, at the noise floor".
- B13's flybys change heliocentric E by more than 10⁻³ at the close end (that is what an assist is); α = 1e-3 is the mild end of the encounter band, so the separatrix finding is conservative — worth saying, since it strengthens the claim.
- Kerr (χ ≠ 0) and the integer-law rerun are named by the author and remain open; premise 4 got a doc-level finding where a probe was owed (admitted).
