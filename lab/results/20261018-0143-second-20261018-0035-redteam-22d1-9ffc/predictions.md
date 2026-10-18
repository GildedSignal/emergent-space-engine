# Predictions — second-author fix run (...-9ffc)

Written BEFORE the decisive run. Target: the checker's named experiment — fix the W2/W2p
onset instrument in 22d1's `eclipse_parity.py` (retarded-time quadratic on the
perpendicular offset d_perp, not the current distance |occ(t)|; W2p offset at constant
letter distance), rerun, and restate the W2 leg. Everything below is pre-registered from
closed-form algebra derived independently of the script's code path (centre row, ψ = 0,
transverse occluder at perpendicular distance d, disk R, speed β, c = 1):

- t_on(W1) = −R/β
- t_on(W3) = d − R·√(1+β²)/β
- t_on(W2) = √(d²+R²) − R/β   [sprite: the anchor's y-offset crosses β|t_ret| = R with
  t_ret tied to t_O through the exact quadratic]
- t_on(W2p) = d − R/β          [letter offset, constant d]

Arcs (t_O = 0, transverse; exact per-row predicates):
- W3: sinψ ∈ ( [−β(d²−R²) − R√(d²−β²(d²−R²))]/d² , same with + )
- W2: |sin(ψ + asin β)| < R/(γd) — sprite distance exactly γd at t_O = 0
- W1: |sin ψ| < R/d

## Pre-registered expectations

- **PA (W2 onset, the corrected headline).** Refined W2−W3 onset error =
  √(d²+R²) − d + (R/β)(√(1+β²)−1): **+0.472/+0.286/+0.241 s** at 2/10/100R, β 0.5 and
  **+0.620/+0.434/+0.389 s** at β 0.9 — the checker's corrected values; grid-quantized
  table within one grid step (≤ 5 ms), sub-grid bisection within 1e-3 s of the closed
  form. Bounded in d; the d→∞ limit (R/β)(√(1+β²)−1) = 0.236 s (β0.5) / 0.384 s (β0.9).
- **PB (the artifact).** The original buggy W2 column (recomputed as C4) exceeds the
  fixed value and grows with β²·d·(scan asymmetry): of order +1 to +9 s at 10R and
  +15/+125 s at 100R (β 0.5/0.9) — converging with the buggy W2p value at 100R β 0.9
  (the tell the checker named). At planet β (1e-4) the bug is invisible (< 1e-3 s).
- **PC (rim).** Fixed W2 rim onset error (β 0.5) bounded ≤ ~0.5 s and shrinking with d
  (≈ 0.44 s at 2R → ≈ 0.28 s at 10R; checker's numbers), NOT growing — the original
  +0.75/+1.82 s were artifacts.
- **PD (arcs, the restated mechanism).** Per-row closed-form agreement EXACT: 0
  mismatched rows of 10⁴ for W1, W2, W3, transverse (2/10/100R × β 0.1/0.5/0.9) and
  oblique 45° (d 10R, β 0.1/0.5). W2 arc centre at −asin β (deg) within one grid row
  (0.036°); W3 centre → −asin β as d grows (exact −asin β only at d→∞: at 2R β0.5 it
  sits at ≈ −22°, the edge-asymmetry case). Half-angle ratio W2/W3 → 1/γ within grid
  resolution (≥ 30 rows): ≈ 0.995/0.866/0.436 at β 0.1/0.5/0.9 (10R, 100R). Jaccard
  (W2,W3) → √(1−β²): 0.995/0.866/0.436, measured within ~0.01 (grid + curvature).
- **PE (W2p onset).** W2p−W3 refined = +(R/β)(√(1+β²)−1) at every d (constant
  +0.236/+0.384 s at β 0.5/0.9): the naive wiring's *timing* is fine — its arc is what
  breaks (Jaccard 0.000 at 100R).
- **PF (independence of the solve).** Max |t_quad − t_bisection| over every onset grid
  < 1e-9 s (100 bisection steps); bracket signs valid everywhere.
- **PG (what must NOT move).** The t_O = 0 Jaccard table (jac_W1/W2/W2p), n_occ_W3, W1
  and W3 onset columns, arm_observer, arm_b: all identical to the original run's JSON
  (the bug only touched the W2/W2p onset path and oblique W2, which was unpublished).
  Price re-measured, order of magnitude only.

Kill criterion for this fix: any of PA/PC/PD failing ⇒ the corrected story does not
regenerate and the silver stands with an unresolved instrument.

Controls: positive — closed forms reduce to e59e's static arcs at β→0 (|sinψ| < R/d);
negative — buggy column C4 must disagree with the fix at 100R β 0.9 (else C4 is not the
artifact the checker described).
