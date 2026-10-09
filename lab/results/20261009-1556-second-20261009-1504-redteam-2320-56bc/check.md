# Check — 20261009-1556-second-20261009-1504-redteam-2320-56bc

Grade: gold

## Abstract (for the integrator)

Claim: representation.md §2's continuation-only view gather cannot enumerate images; for compact lenses (r\* < b_E ≈ 80), including the r\*=3M black hole, the second image exists from doll entry at every alignment, is missed in 100% of frames at 3.5–77.6% brightness, and even a handed branch dies at the gather's budget; for normal stars the source never reappears after occultation (36/36). All six records regenerate bit-identically from shipped code; predictions were fixed 11 min before every decisive output (6/7 held; P2 honestly refuted, strengthening). Independent DOP853 tracing confirms the roots, slopes and the thin-lens magnification ratio (0.036 vs 0.038). Adoption: one design sentence (±b branch enumeration per lensing doll) plus r6 criteria on two transits — one step.

## Reproduction

Clean tree, scripts copied out, all six commands run: `falsifier.py` (15 s), `bh.py` (22 s), `diag.py` (0.1 s), `wraps.py` (11 s), `star-extra.py` (25 s), `envelope.py` (17 s). Every output JSON is **bit-identical** to the stored record (wall times excepted), including all 59×2 BH frames and the census. `falsifier-out.json` also matches the parent author's stored `falsifier-out-author.json` frame-for-frame, so the parent record regenerates through the same shipped instrument. `work/patch.diff` is empty — nothing outside the run folder was touched. Patch applied: n/a.

## Predictions

`predictions.md` mtime 1791561867; the earliest decisive output (`bh-out.json`) is 1791562533 — fixed **11+ minutes before any BH/envelope/occultation number existed** (the earlier `falsifier-out.json` is the parent record's reproduction, allowed). Outcome as the dossier states: P1 held, P3's band missed low but its pre-registered decision rule held, P4 (control) passed, P5/P6/P7 held; **P2 refuted** — reported as refuted, with the mechanism measured. A refuted prediction blocks gold when it undermines the claim or is hidden; here the author predicted the design would *hold* a handed branch and it *died* — the failure is the finding, in the claim's favour, and honestly reported.

## My attacks (independent tracer: scipy DOP853, rtol 1e-10, same Binet law, own code path)

1. **The missed image is real and bright (independent confirmation).** η=400: strong root 0.2064809 (grid 0.2064814), slope 2.857×10⁵ (grid 2.944×10⁵), missed/held brightness 3.63% (grid 3.53%). η=20: root 0.0461574, ratio 0.776. Thin-lens 2D analytic: image positions 0.20519/−0.00780 (η=400) and magnification ratio 0.038 vs measured 0.036 — the instrument's 1/|ds/dθ| measure is sound. Note the game is 2D and the Binet photon law is the design's own (representation.md §1), so these ratios are native, not a toy.
2. **Wrap family confirmed, not a grid artifact.** Fine log-spaced sweep (90 pts, offsets 5×10⁻⁷–1.5×10⁻⁴ from the capture edge, η=400): s oscillates ±8×10³ with sign changes at offsets 2.5×10⁻⁶ and 5.7×10⁻⁵; bracket slopes ≈3.2×10⁹ and ≈1.4×10⁸ vs the grid's 3.21×10⁹ and 1.22×10⁸. Brightness vs primary: 3.2×10⁻⁶ and 7.2×10⁻⁵ — invisible, as claimed.
3. **Cadence escape closed.** BH cold-start transit at 10× finer cadence (589 frames, Δη≈1.28): truth ≥2 images at 589/589 frames, continuation holds 1 at 589/589, max n_cont = 1. The miss is not a frame-step artifact.
4. **"Never recovered" is fallback-specific; the fragility is not.** With a proper local-slope Newton (fresh two-point slope at the new geometry, same 6-iteration budget) the handed strong branch still dies at frame 1 — but by slow convergence, not divergence: |s| walks 939.7 → 2628.8 → 634.5 → 401.0 → 219.3 → 44.3 and converges at **iteration 7** (s = 0.088 at the truth root 0.2004134). So the shipped fallback's death (basin capture, per diag) is permanent, but a design-faithful Newton holds the handed branch given ~8 iterations. The dossier's clause "lost after one frame step and never recovered" should read "lost at the gather's 6-iteration budget" — the entry-like-landscape curvature is the honest, still-true statement.
5. **The occultation emptiness is conditional on an unnamed policy.** Re-seeding the empty tracker from the unlensed direction (θ=0) recovers 25/36 post-occultation frames (11 still fail to converge). The author's hatch (3) anticipated this; by their own principle-19 test such a rescue is a bandaid — it still enumerates nothing and fails where the fallback walk stalls.

## Novelty and fit

No HISTORY entry or doc treats image enumeration; the live texts carry the premise verbatim (representation.md:57 "Lensing adds crossings, from each doll's memoized deflection(b)" with no finder; law.md:53; H0211 ships the per-tube Newton gather in the plane). r6 as written freezes cost only ("Newton iterations and samples per frame") — the cost of not fixing is exactly as the dossier says. This completes the parent run's checker-named experiment; the scope correction (r\* < b_E) is measured (envelope: 6/5/4/0/0/0 two-image alignments for r\* = 50…100) and matches the b_E geometry. Fit: principle 30, "what really matters is navigation, knowledge and dynamics those need to be perfect" — a permanently missed companion at 3.5–77.6% is wrong knowledge; principle 19 — branch enumeration is the representation, empty-tracker rescues the bandaid. Not a board row, but the author argued it as premise 5 + r6, and the parent run was already accepted in scope.

## What the author missed

- The P2 clause overstates: "never recovered" holds for the shipped fallback only; a proper-slope Newton recovers at iteration 7 (my #4). One sentence fixes the dossier.
- Internal inconsistency: claim line says wrap brightness 3×10⁻⁶–2×10⁻⁴, evidence line 3.2×10⁻⁶–1.0×10⁻³, and bh.py's own classifier labels the η=1600 outer member (2.3×10⁻³) a wrap. All ≥9× under the 2% bar — no verdict impact, but the numbers should agree.
- The 2D/3D caveat is raised for wraps only. In 3D the secondary's |μ⁻| at η=400 is 0.14% (below the bar; ≥2% only for η ≲ 290), so "≥2% at every transit frame" is the 2D measure. Since the game's law is the 2D Binet photon this is mostly moot, but the dossier should say so.
- Fine cadence (my #3) was the untested escape hatch closest to saving the design; it closes.
- My own b=100 deflection control in attack.py was mis-posed (finite-radius sweep against the asymptotic 4M/b) and is superseded by the thin-lens cross-check in #1; no author number rests on it.
