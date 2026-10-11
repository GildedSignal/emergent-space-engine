Working...
Check complete. Final state of the run folder verified: `check.md` written; `view_images.json` restored byte-identical to shipped (md5 `ed44871a…`); `bands.json`/`bands_jet.json` regenerated bit-for-bit identical; nothing else touched.

**Grade: silver** — `lab/results/20261011-1234-redteam-6eae/check.md`

**What held (reproduced exactly + independently verified):**
- The headline multiplicity table: ≥2 and ≥3 images for 100% of emitter azimuths at every r_o (100M→3.2M), 4 images for 99% at 3.2M, deepest resolved bends 9.4→18.0 rad — the full 165 s rerun differs from the shipped JSON in **one field only** (see below).
- My own integrator + crossing finder (independent of the author's counter) confirms the image directions to 1e-8, the winding indices (k=0 at b=7.02M, k=1 at b=5.199M≈b_c), and ≥3 images at the weakest point probed (100M).
- The design quotes are verbatim-accurate: view.rs "Each tube crosses the cone once", law.md:53 single-sheet `deflection(b)` memo, the lifecycle never-shown-twice assertion, r6 unfrozen, B16 one-deflection-per-seed, H0210's 83% gather. Novel for the project; the GR itself is textbook (Darwin/Virbhadra–Ellis).
- `bands.py` reproduces bit-for-bit; the r1 sampler gap is confirmed verbatim from the frozen rung file.

**What broke the gold:**
1. **Non-regenerable number:** `control_weak_field` — shipped JSON says bend 0.018 (10% off); the shipped code regenerates **0.0** (the control ray is born below its own escape cut — the exact defect class the dossier claims v3 fixed); the correct arc value is ≈0.0195 (2.1% tail), so the recorded number and its "analytic tail" explanation match neither code nor physics, and the pre-registered 1% bar fails while the dossier reports the control as passing.
2. Held-out record mixed: case D failed (honestly reported as a premise surviving), case A magnitudes split.
3. Adoption is one experiment away: the magnification cutoff was unmeasured — my probe supplies the first number (first winding image ~740× demagnified vs the aligned pair at 10M, ≈e^{−2π}; effectively invisible at 100M where it sits 0.1% from b_c).

Also found: the withdrawn jet probe's "separatrix crossing" diagnosis is actually a coding slip (x = 1/L instead of 1/L², plus the wrong quadratic root) — VOID either way, but the stated cause and proposed fix are wrong.

The gold-making experiment is named in check.md: the per-winding visibility ladder plus a regenerated weak-field control — it turns "wrong by an integer" into the cutoff number the multi-sheet memo needs before r6 freezes.
