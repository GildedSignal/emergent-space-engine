# Dossier — run 20261018-0143-second-20261018-0035-redteam-22d1-9ffc (second author)

## Claim

The checker's named experiment is done: with the W2/W2p onset instrument fixed
(retarded-time quadratic on the worldline's own geometry, W2p at the letter's constant
d), **every corrected number the checker derived now regenerates from the run's own
script and is certified by exact closed forms** — the sprite wiring's eclipse timing
error is bounded, exactly `(√(d²+R²) − d) + (R/β)(√(1+β²) − 1)` (≤ 0.62 s here,
→ (R/β)(√(1+β²)−1) ≈ Rβ/2 as d→∞, shrinking with β), and its parity break is the arc:
the exact law's occluded arc is the static arc translated to −asin β (edge roots
sinψ = [−β(d²−R²) ± R√(d²−β²(d²−R²))]/d², half-angle → R/d) while the sprite's is the
same-centre arc shrunk by exactly 1/γ (|sin(ψ+asinβ)| < R/(γd), half-angle R/(γd)) — so
Jaccard(W2,W3) → √(1−β²), measured 0.8652/0.4357 against 0.8660/0.4359 at 10R — and
the run's +125.13 s "unbounded" headline is confirmed dead as an instrument artifact
(the two originally-convergent wirings now disagree: +0.3855 vs +0.3809 s), so 22d1's
kill of both cheap occlusion wirings stands **on the corrected mechanism, with the
sprite-negative rung bars now exact and freezable**.

## Bottleneck

The view's correctness half (`view`, `representation-premises` direction 2/5): the
wiring decision for the occluder test that must be frozen before the lensing memo
lands. This run removes the record defect that held 22d1 at silver — the numbers were
checker-supplied, not regenerable — and upgrades the corrected physics from
asymptotic argument to per-row exact certificate.

## Evidence

All numbers: `python3 eclipse_parity.py` (~40 s, deterministic) then
`python3 analyze.py` (~0.1 s) in this folder; `bash regen.sh` runs both. Instrument:
22d1's script with exactly two fixes — W2's retarded-time quadratic anchored on the
worldline (general lookback solve `τ = (P·v − √((P·v)² + (1−β²)|P|²))/(1−β²)`, P the
occluder's position at arrival time) instead of the current distance |occ(t)|, and
W2p's row offset at the constant letter distance. Everything else byte-identical.

- **Corrected W2 onsets (the checker's six values, now regenerating):** +0.4729 /
  +0.2862 / +0.2423 s at 2/10/100R (β 0.5) and +0.6194 / +0.4341 / +0.3855 s (β 0.9);
  closed form above, sub-grid-bisection residual ≤ 3.6e-12 s over all cells and all
  four wirings (W1 = −R/β, W3 = d − R√(1+β²)/β, W2 = √(d²+R²) − R/β, W2p = d − R/β
  all to machine precision). Bounded in d; the d→∞ limit 0.236/0.384 s at β 0.5/0.9.
- **The artifact, reproduced as a column (C4):** the original instrument reads
  +1.2514 / +15.0547 / +125.1389 s where the fix reads +0.2862 / +0.2423 / +0.3855 s
  (10R β0.5, 100R β0.5, 100R β0.9) — the run's published +1.25/+15.05/+125.13 s.
  The tell resolves: original W2/W2p converged (+125.1344/+125.1206) because the
  buggy W2 degenerates to the naive current-distance offset at large scan times; the
  fixed pair is distinct (+0.3855/+0.3809). Honest miss against my own prediction:
  the bug is NOT invisible at planet β — it shifts onsets +0.37…+1.16 s even at
  β = 10⁻⁴ (at eclipse the occluder sits ~R off the axis, so |occ(t)|² ≠ d² at the
  R²/d level).
- **The 1/γ arc mechanism, now per-row exact (C3):** in all 11 cells (transverse
  2/10/100R × β 0.1/0.5/0.9, oblique 45° d=10R × β 0.1/0.5) the segment-test
  classification of every one of the 10⁴ rows equals the closed-form predicate —
  **0 mismatched rows anywhere**. W2's arc centre sits at −asin β (−30.006° vs
  −30.000° at 10R β0.5); W3's centre → −asin β from −25.67° (2R) through −29.84° (10R)
  to −30.01° (100R), the close-approach offset being the exact (1−R²/d²) factor in
  the root formula. Half-angle ratio W2/W3: 0.9969/0.8648/0.4340 at 10R against
  1/γ = 0.9950/0.8660/0.4359 (grid-limited at 100R: 28 vs 14 rows). Jaccard(W2,W3):
  0.9969/0.8652/0.4357 at 10R, 0.8750/0.4516 at 100R, against √(1−β²).
- **Rim (β0.5):** fixed W2 rim error +0.4363 s (2R) → +0.2751 s (10R) — bounded and
  shrinking with d, exactly as the checker said (their 0.44 → 0.28); the run's
  +0.75/+1.82 s were artifacts. P2 re-graded: **held in form** (bounded rim-class
  error), refuting the run's "P2 refuted".
- **W2p is killed under either reading of its letter:** constant-d offset gives
  bounded timing (+0.2368/+0.2364/+0.2377 s at β0.5 — constant, = (R/β)(√(1+β²)−1))
  but the arc breaks (Jaccard 0.3065 at 10R β0.5, 0.0000 at 100R β≥0.5); the
  per-frame-current-distance reading gives onsets +15.05/+125.12 s at 100R
  (β0.5/0.9). Either way it is not the law.
- **Oblique (held out, now with a correct W2):** Jaccard(W2,W3) = 0.9971 (β0.1) /
  0.9341 (β0.5) at d=10R — the sprite survives oblique motion better than transverse
  at the same β (its light-time/distance identity holds exactly: sprite distance
  9.3615 = light time 9.3615). W3's oblique predicate anchors at the frame-time
  distance d, not the perpendicular foot: d²(sinψ+v_y)² < R²(1+β²+2v·Ê̂) — a
  representation detail this run pinned down.
- **Independence of the solve (C1):** quadratic vs 100-step bisection over every
  onset grid: ≤ 1.1e-11 s, brackets valid everywhere.
- **What did not move (PG):** the t_O = 0 Jaccard table, n_occ, all W1/W3 onset
  columns, the observer arm and Arm B are byte-identical to 22d1's JSON (verified
  field-by-field, violations []). Price re-measured 109–138 ns/row on this box
  (three executions; order of magnitude, consistent with 22d1's 69–79 and the
  checker's 81).

## Predictions

`predictions.md` was written before the decisive run. **PA held** (all six corrected
onsets to the grid step, closed forms to 3.6e-12 s); **PB held** on the artifact
column and the tell, **refuted on one sub-clause** (planet-β invisibility — the bug
is +0.4…+1.2 s there, reported above); **PC held** (rim bounded, shrinking);
**PD held** — but only after the first execution exposed two defects in *my own*
certificate, not in the instrument: the bare sin-intervals are two-sided (the segment
test is one-sided, cosψ ≥ 0) and my centre/half-width extraction was wrap-unsafe;
the oblique arm also caught a parametrization error in my first fix (anchoring the
retarded solve at the perpendicular foot shifts the worldline's time origin — the
general lookback quadratic above is the correct form, and it leaves every transverse
number unchanged). **PE held** (constant +0.236/+0.384 s; reading (a) documented as
worse). **PF held** (≤ 1.1e-11 s). **PG held** (zero violations).

## What would make it wrong

The corrected numbers are exact closed-form algebra certified per row; what would
undo the claim: (a) the worldtube test itself mis-models the renderer's row semantics
(it is the game's own "null segment vs worldtube" letter, Julien's conversation
L984); (b) the game never places fast occluders in view (false — the ladder's 0.9c
stream, and a planet at 2R passed at β0.5 sits at β·d/R = 1); (c) aggregate emitters
make row-level eclipse the wrong observable (each rung row would then be a partial
dimming — the arc certificates still bound the geometry).

Cost of adopting: none beyond 22d1's — the occluder test is one exact quadratic per
row per occluder (~20 flops, 69–138 ns/row measured across machines). What this run
adds is the frozen rung at corrected rates, now with **exact bars**: arc Jaccard
(W2 vs W3) = √(1−β²) at d ≥ 10R; W2 onset error = the closed form above (≤ 0.62 s
at R = 1, β ≤ 0.9); W2p arc Jaccard ≤ 0.31 at 10R β0.5 → 0 at 100R (kill robust to
the letter reading); W1 disjoint beyond β·d/R ≳ 2 with onset error −d/c +
(R/β)(√(1+β²)−1); judged in the observer's frame at player β (17.6°/49.8°, not 30°),
plus Arm B's duration bar (0.782 s = 19.6% at β0.5, invisible at planet β).

Fit with PRINCIPLES: principle 19 — "bandaids are basically fixes resulting due to a
poor representation… the right representation always just feels right": the corrected
story is *stronger* for the thesis — every cheap occlusion wiring breaks parity by
geometry (arc placement/width), which no cadence or budget fixes, and the exact test
is the same quadratic the contact resolver already is. Principle 2 — "error type
over error size": the sprite's error type is a 1/γ-narrowed blackout (stars that
should be hidden stay visible along a thinned arc), not a timing lag. Principle 26 —
"agreement is not independence": the tell (two wirings converging to +125.13) was the
signature of the shared broken instrument; this run's certificates are three
independent methods (closed form, bisection, per-row predicates) agreeing.

## The lens

Second-author lens: it fixes and certifies, and its blind spot is faith in the
checker's frame. Verified independently here (closed forms derived before the run,
pre-registered), but: the strong-field composition (Arm B) is still first-order; the
arcs are 2-D (a real 3-D sky wraps the same algebra around a great circle — the 1/γ
shrink should survive as the cone's transverse scale, unmeasured); extended
occluders and aggregate emitters remain unmeasured; and the oblique arm covers one
angle (45°) — the general oblique sprite distance (9.36 ≠ γd⊥ = 7.11 at β0.1) shows
the oblique regime has its own algebra worth one dedicated cell before the rung
freezes.
