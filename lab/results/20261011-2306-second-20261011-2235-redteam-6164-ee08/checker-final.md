Working...
Check complete. `check.md` written to the run folder, grade **gold**.

**Reproduction (clean tree; `work/patch.diff` is empty):**
- `probe.py` → `probe_out.json` **byte-identical** (8.9 s)
- All six `probe2.py` parts + `merge` → **identical to the author's records** modulo the unavoidable `machine` block
- `equality` 10/10 (184 s), `identity` 9/9 (468 s) — including the 1-chronon-epoch storm and the planted-late-kick negative control
- Pre-registration holds: `predictions.md` (23:15) predates every probe2 output (23:36+); P5–P9 all held

**My adversarial cases (three, plus one extension):**
1. **P8 decomposition on unseen grid points** (p=50/e=0.9, p=200/e=0.7, p=30/e=0.99): T-channel/((15/8)(δE/(1−E))²) = 0.994–0.998, T dominating the precession channel by 3–4 orders — the parent's decomposition inversion is real and independent.
2. **Oracle-noise attack on the decisive row** (a=0.9, ε=10⁻⁶): |∂T/∂E| stable to 9 digits under h-refinement — the logarithmic divergence is physical, not quadrature noise.
3. **Retrograde Kerr** (a=−0.9, r_c=6.0), the author's named-open case: same failure structure (1.9·10⁷ divergence, 43% quantum-kick error, plunge at 3·10⁻³) — the finding extends beyond the prograde scope.
4. Doc-level findings re-verified by direct grep: 21 gates, zero mentioning jet/recompile/separatrix/root-distance; r5/r6 absent from `lab/rungs/`; B19 gates Kerr behaviours only; Metal leg macOS-gated.

**Discrepancies found (minor, all noted in check.md):** "2–80×" L-vs-E range is wrong at one point (136×, in the claim's favour); the stale `predictions.md` paragraph claiming no dense/sparse evaluator exists (falsified by the author's own later probe); χ=0.998 deep-ε rows committed but not run.

Left behind: only `check.md` added to the run folder; scratch dirs removed; no commits, no pushes.
