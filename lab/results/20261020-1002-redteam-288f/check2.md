Grade: gold


**Abstract.** The fleet doll's interior law — the Newtonian tidal tensor in the Fermi
frame (frame.rs L14–19, representation.md L23, law.md L50's phase 1) — is refuted at
the game's own speeds. Against exact Schwarzschild geodesic truth the radial tide is
γ²(2+β²)/2 × Newtonian: measured 1.0988 (closed 1.1000) at the shipped c/4 legality
cap, where the letter's own budget line claims O(β²) = 6.25% and its per-orbit member
error is 30%/115%; ×1.5052 at β 0.5; along-motion exactly 1× at any β (the
cancellation; radial-infall arm 0.9995). Reproduced bit-for-bit (`bash regen.sh`,
7.6 s); closed form verified analytically and on four fresh adversarial cases
(oblique 45°, β 0.95, r = 20 M, mirrored member). B15's 0.9c fleet stream collides
with `ORBIT_SPEED_DIV = 4`. Cure: same integer kick, contracted coefficients; a
hyperbolic E9 arm is freeze-ready. Adopt in one step.

## Reasons

**1. Reproduction (exact).** `bash regen.sh` in a clean invocation: ALL PASS, 7.6 s,
and every number in results.json matches dossier.md and run_output.txt to the digit
(coefficients, exit errors, controls). `work/patch.diff` is empty — a pure probe, no
engine edits to apply; the falsifier is self-contained float64. Machine: Linux x86
cloud, 8 vCPU, load light; orders of magnitude only per the lab rules (the
integrator re-measures on the M1 — but this run's evidence is physics ratios, not
timings).

**2. The instrument is sound and the physics is exact.** I re-derived the closed
forms from scratch off the Schwarzschild static-orthonormal Riemann
(R_{rtrt}=−2w, R_{tθtθ}=+w, R_{rθrθ}=−w, R_{θφθφ}=+2w, w=M/r³ — exactly the "Newtonian"
pattern; no higher-order corrections): radial (⊥ motion) γ²(2+β²)/2, along-motion
γ⁴(1−β²)² = 1 exactly (the tθ cross-term is load-bearing, as the author says),
out-of-plane γ²(1+2β²), radial-infall channels exactly Newtonian. Trace-free in
vacuum at every β — all four formulae mutually consistent. The circular
specialization (2r−3M)/2(r−3M) equals E9's frozen w(3γ²−1) identically (engine-judge
L75). The script's `Est` matrix (falsifier.py L193–196) matches this component-by-
component; the Fermi axes, Christoffels, geodesic RHS and born-rigid member launch
are all correct GR. The measured rows agree with the closed form where the author
claims them clean (1.0988/1.1000; 1.5052/1.4963; 0.9995/1.000).

**3. Adversarial cases (mine; one outside the author's tested range).**
- *Oblique 45° flyby, β 0.7, r = 100 M* — every author launch is axis-aligned, so the
  tide matrix in Fermi axes is diagonal for them; here br ≠ 0, no probe axis is an
  eigen-direction, and the cure's cross-term structure is what's tested. Scalar
  radial ratio 2.205 vs instantaneous closed 2.261 (2.5%); truth matrix vs letter
  relerr 1.52 (the letter is 152% wrong), vs cure 0.29; integrated exit [r]: letter
  16.3%, cure 1.8%. The kill and the cure both hold off the author's axes.
- *β 0.95 transverse* (above the cure's stated license, below the polluted 0.99): the
  letter is still unambiguously wrong (|A|/|N| 12.7 vs closed 14.8; letter_rel 12.1;
  exit [r] 12.3% vs cure 3.7%), but the cure's integrated [th] error (16.4%) now
  exceeds the letter's (1.5%) — the license boundary at β 0.9 is real, not modest.
- *r = 20 M, β 0.5*: ratio 1.511 vs closed 1.496 — radius-independence confirmed; the
  amplification is purely kinematic (the orthonormal Riemann is exactly ±M/r³).
- *Mirrored member (ξ → −ξ)*: cap 30.0%/0.23%, β 0.9 9.3%/1.0% — matches the +ξ rows;
  no sign asymmetry in the instrument.

**4. The letter, the collision and the citations are real (all checked in the tree).**
frame.rs L14–19 ships exactly `E = (GM/r³)(I − 3r̂r̂ᵀ)` with Schwarzschild deferred to
phase 2; L83–85 the weak-field rule `n·R ≤ c/4` with budget "1PN terms are O((nR/c)²)";
`ORBIT_SPEED_DIV = 4` (L133). law.md L50 promises "the Schwarzschild tidal tensor
projected along the tube" — the letter says Fermi and ships Newton, as claimed.
B15 (law.md L76) flies "the 0.9c stream included … each fleet a free-fall doll" —
refused by the shipped rule; a 0.40 v_c prograde burn already refuses through it
(gravity-news, 20261014-1137). The plane's red-line burn γ ≈ 120 is HANDOFF's
baselined-red row; ×2.2×10⁴ there is the right arithmetic.

**5. Novelty.** The circular GR tide is frozen in E9 (Newtonian 2w must fail; the
author cites it and uses it as a cross-check — honest). The wiki names what remained
"the Schwarzschild-tide/geodetic seam … unprobed" (gravity-news, open directions).
No run, gate or HISTORY entry holds the transverse/hyperbolic closed form, the exact
along-motion cancellation, the cap-scene integrated error, or the B15-vs-legality
collision. fermi2-v2-b7a4 (gold) is the cadence law, not the coefficient. Novel to
the record; the standard boosted-Riemann contraction is, correctly, not claimed as
new physics but as a new measurement against this engine's letter.

**6. Predictions.** predictions.md predates the decisive artefacts (file order:
predictions 46 min, falsifier 14 min, results/dossier 12 min; the not-tuned arms it
pre-registers are exactly the ones the decisive run added). P2 — the central
prediction, the cap at +10.0% — held exactly (1.0988). P1 control held on [r],
marginal on [th]. Four missed, each honestly reported and each sharpening the law
(P3/P7's failure *is* the transverse-only discovery). One bookkeeping overstatement:
P6 is counted "held" but its conservation clause (<10⁻⁹) is violated at β 0.999
(6×10⁻⁸, disclosed in the Evidence section but not in the Predictions summary), and
its linearity clause holds only read as absolute points (0.065 pts; 0.72% relative
against a stated 0.3%). This touches no kill row (β ≤ 0.9 conserves to ≤ 1.7×10⁻¹¹).

**7. Small defects, none load-bearing.** (a) The printed coefficient table's header
is misaligned by one column (`ratio_norm` prints under "cure relerr"); the JSON is
authoritative and the dossier quotes the JSON. (b) The claim sentence lists ×74/×750
at β 0.99/0.999 in the same breath as the measured rows; those two are closed-form
only (the probes there are polluted) — disclosed two paragraphs later, but the claim
sentence should have said so. (c) The cure's β ≥ 0.95 [th]-channel inversion (my
case 3 above) is a stronger boundary than the page's "β ≥ 0.99" phrasing suggests —
corrected in the page.

**8. Goal fit.** It shows a premise of the shipped representation is wrong at its
own legality boundary — the red-team lens's exact job — with the replacement in
hand. Principle 2 ("error type over error size"): a wrong law, not coarse
arithmetic. Principle 30: "what really matters is navigation, knowledge and
dynamics those need to be perfect". Principle 33: the cancellation says the
along-motion channel never needed fixing — half the letter survives untouched. The
cure is the same O(1) kick with corrected coefficients (closed form), so adoption is
one integrator step: swap the coefficients, re-derive the weak-field rule around
compactness, freeze the hyperbolic arm (criterion ready in the dossier).

**9. The page.** Faithful throughout — every number I checked traces to
results.json, the E9 identically-algebra claim is true, and the disclosed instrument
limits are stated, not hidden. I tightened one line (open direction 3: the license
boundary starts at 0.95, with the [th] inversion measured). Three gold runs do not
yet agree on this topic; it stays open.

## What the author missed

- Oblique launches (br ≠ 0 at launch) were never flown; they are the only cases that
  exercise the cure's off-diagonal structure and the strongest single kill scene
  (letter matrix 152% wrong at β 0.7 — a *legal-speed-adjacent* regime, no 0.9c
  needed). Suggest adding one oblique row to the freeze-ready arm.
- The out-of-plane channel γ²(1+2β²) is quoted exact but unmeasured (the instrument
  is equatorial); the game is 2D, so this is a completeness note, not a hole.
- The claim sentence reads the β 0.99/0.999 closed-form rows as if measured.
- Whether the shipped integer law's 2⁻⁸ epoch cadence accidentally masks any of the
  30%/115% per-orbit drift in a digest-visible way is untested (no gate sees the
  interior at player speed — that is the run's own point, and the arm fixes it).
- P6's conservation clause (above).
