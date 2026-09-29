# Check — rung r4 (20260929-1940, bed9)

## Abstract

Reproduced **bit-identically**: every metric, the five truth files, the machinery checks, the picture. But the candidates' tidal field is **sign-inverted**: `tidal_acc` returns −m₂[3(R̂·r)R̂ − r]/R³ (verified against the exact Newtonian perturbation at five geometries; the layer's C1 apsidal precession is retrograde −1.7×10⁻⁴ where truth is +1.09×10⁻⁴ and the author's own `averaged` config gives +9.0×10⁻⁵). The reported PASS is an artifact of m₂ → −m₂ physics. With the one-line sign corrected, both candidates are killed: conj-quad pump 1.32/1.56, conj-oct 1.41/1.51 (> 1.25), controls 2/3 (C3 envelope 0.45×) — `verdict.py` outputs DISPUTED. The frozen metrics are provably sign-blind (ψ → ψ+π leaves conc; pumping scales with |m₂|). Spec-correct conclusion: this kick layer does **not** carry the 2:1 resonance within the frozen gates.

## Reasons

### 1. Reproduction — exact
Clean copy of `rung_r4.py`, `truth.c`, `picture_util.py` in /tmp; `gcc -O2`; `truth`, `check`, `metrics`, `picture` re-run.
- All 24 metrics values identical to `metrics.json` (worst relative difference 0.0); `data/truth_*_2400.txt` byte-identical (`cmp`).
- Machinery checks identical: GL24 = 4×GL48 |dv| = 1.40657742e-2; `averaged` C1 precession 9.002783e-5 vs classical 9.000000e-5 vs truth 1.094788e-4.
- Truth convergence extended one point to 4800 steps/orbit: R1 0.15698162, R2 0.17349883, C3 0.044137387 (≤ 1e-5 relative drift from 2400). Truth is converged; dE ≤ 8.6e-12.
- Prediction ordering consistent: `predictions.md` 19:58:20 precedes every metric output (metrics-log 20:21:47; metrics.json 20:24:00 is a deterministic re-run identical to the logged values). `rung_r4.py` (20:21:17) postdates predictions, matching the disclosed discarded wrap-bug fix. No silent fixes found elsewhere.

### 2. Implementation vs specification — the candidates run inverted physics
`rung_r4.py:116` `ax = c*(x - 3.0*dot*hx)` with c = M₂/R³ gives the **negative** of the star-frame tidal acceleration (direct + indirect). Evidence:
- Numeric: at (x,y)=(0.9,0), R=(1.587,0) the exact m₂[(R−r)/|R−r|³ − R/R³] is +5.158e-3; the true quadrupole term +1.350e-3; the author's field −1.350e-3. Same inversion at four other geometries, quadrupole and octupole alike.
- Observable: the layer's C1 apsidal precession is −1.676e-4 (quad) / −1.264e-4 (oct) — retrograde — where truth is +1.0948e-4 and the author's own `averaged` config (classical formula, correct sign) gives +9.003e-5. The author's two configs disagree on the sign of the same physics.
The specified configurations ("one analytic quadrupole tidal kick") were therefore not run; conj-quad/conj-oct as executed kick with m₂ = −3×10⁻³.

### 3. Consequence — corrected sign kills both candidates
Patching only the sign and re-running `metrics`:
- conj-quad: pump_min 1.316, pump_max **1.557** (fails pumphi ≤ 1.25), ctrl 2/3 (C3 0.0199 vs 0.0441 = 0.45×, fails), lib 0.850, kicks/orbit 0.575.
- conj-oct: pump_min **1.411**, pump_max 1.508 (fails), ctrl 2/3 (fails), lib 1.468.
`verdict.py <rung> corrected author` → **DISPUTED** (4 outcome flips). The author's `predictions.md` item 1 — conj-quad over-pumps 1.4–2.2× — was physically correct; the sign error inverted the outcome, and the gates could not see it: |mean e^{iψ}| is invariant under ψ → ψ+π and pumping amplitude scales with |m₂|.

### 4. Oracle values
- R2's frozen oracle (truth conc 0.867) is unreachable under any reading of "w2 = 4.0" I tested: e₂ ∈ {0.03,0.05,0.1,0.2} with ϖ₂ = 4.0 gives conc 0.452–0.514; λ₂(0) = 4.0 readings give 0.311–0.402. The red-team ICs are genuinely absent; the author's e₂ = 0.05 choice is a fair mid-range reconstruction, consistently ratioed against its own truth, and honestly flagged. The frozen case as written was not (and cannot be) run exactly.
- Truth values for R1, C1–C3 and the convergence claim: verified (above).

### 5. Adversarial cases
- **Ratio 2.02** (μ frozen): truth maxe1 0.133; author-sign layer over-pumps 1.29 (quad) / 1.32 (oct) — already past the 1.25 gate; corrected-sign 1.58/1.86. The frozen-case PASS has thin margin and does not extend off-nominal, under either sign.
- **μ = 0.03, ratio 2.0**: the truth itself disrupts (maxe1 ≈ 3274, scattering regime) — outside the rung's domain; both layers stay bounded and the comparison is meaningless there. The rung's domain is μ ≈ 3×10⁻³.
- **μ = 0.03, ratio 2.15**: corrected-sign layer crashes (e ≥ 1 inside one kick → `sqrt(1-e)` domain error in `el_from_rv` before the `0 < e < 0.95` guard). Robustness hole below the frozen cases.
- Machinery spot-checks all clean: `state_at` matches independent Kepler propagation to 5e-16 with exact energy; `el_from_rv` round-trips to 9e-14; conjunction residuals ≤ 8e-14 × 2π over 50 events; GL24 correct on test integrals.

### 6. dense_steps and cost
Zero ODE steps in a candidate: conjunction finding is a Newton root on an analytic function, and the kick is a 24-node Gauss–Legendre quadrature of the analytic field — consistent with the metric's intent, though it charges 24 field evaluations per conjunction (~12 per inner orbit vs the truth's 2400 steps; ~200× cheaper, not the design's closed-form kick). `none` reports 0.53 kicks/orbit for conjunctions where nothing is applied — cosmetic, gate-irrelevant.

### 7. Novelty
First execution of frozen rung r4 (source: commit 61d5b73, red-team silver). H0190 K1/K2 measured kick rates and averaging cuts, not resonance reproduction on the cheap path. No prior H-entry claims this; nothing to cite as duplicate.

## What the author missed
- **The sign of `tidal_acc`.** Their machinery checks validated the quadrature and the `averaged` formula but never the tidal field itself against the exact perturbation — the one function only the candidates use. One exact-field comparison at one geometry would have caught it.
- Consequently missed that the gates are sign-blind, which strengthens their own "what would make it wrong" note: the concentration metric is weak not just to frozen-vs-librating but to a perturbation with the wrong sign; a phase observable (precession sign, ψ histogram center) belongs in the next rung alongside their proposed upper bound.
- The `none` config counts conjunctions as kicks; the layer's unguarded e ≥ 1 path; the thin gate margin at 2.02; the μ-domain boundary.
- Everything else was done well: deterministic byte-reproducible artifacts, converged truth, honest caveats written before checker contact, and a predictions file whose physics was right even though its implementation was not.

## Bottom line for the integrator
`verdict.py` on these two files prints PASS, but that verdict measures an anti-Newtonian tidal field. On the specification-correct field the frozen criteria kill both candidates (pumphi and ctrl, DISPUTED against the author's file). Treat the rung outcome as not supporting adoption until re-run with the sign fixed; the one-line fix and the corrected-sign table in §3 are the re-run.
