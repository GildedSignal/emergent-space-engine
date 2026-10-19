# Predictions — 20261019-0325-second-…-c78d-4ff1 (second author: freeze + execute r11)

The silver's named experiment: freeze the corrected eclipse-parity aggregate arm and
execute it mechanically (13c6's r6 step). Frozen before this run: `r11-eclipse-aggregate.md`,
sha256 de53f4987165a2dbc5227e0a8da1a3a29f591ac34dfcae371cfb069f37705306 (`rung.sha256`).
The original record was verified first: c78d's own script reruns byte-identical in this
tree (13.2 s). Instrument validated before any fleet run: the two retarded solvers
(quadratic root / monotone bisection) agree to 5e-12 and both sit on the light cone to
3e-14; the two predicate forms agree on 100% of a random sample; pixel counts are
113 (disc r3, h0.5; bound π·36 = 113.1), 29 (h1.0; bound 28.3), arc band 3 (h0.5) and
41 (h0.15).

Frozen case: β 0.5, R_f = 3·R_p, impact 0, both orientations, worst one reported;
truth N = 2×10⁴ exact per-ship predicates (β) / 10⁵ (static), seed 20261019.

Pre-registered expectations (blind: no config has been run):

- **pixel-h2 (candidate, 113 samples).** flux_err_p99 ≤ 0.04 (the static peak at this
  pitch was 3.0%; β only multiplies in a k⁴ field smooth on the fleet-depth scale);
  fmin_abs_dev ≤ 0.03; false_blink_frac = 0 exactly; samples = 113;
  samples_over_bound ≈ 1.00. PASSES all five bars.
- **pixel-h1 (candidate, 29 samples).** flux_err_p99 ∈ [0.05, 0.10] → FAILS p99
  (mechanism: the boundary-straddling pixel fraction ≈ perimeter·h/area ≈ 22% at h=1;
  static peak 7.7%). fmin_abs_dev ≤ 0.05 (passes; deep-eclipse quantization is small);
  false_blink 0; passes both cost bars with slack. Killed by behaviour, not cost —
  that is the rung's teeth pointing the right way.
- **one-sample (negative).** flux_err_p99 ≥ 0.5 (c78d peaks 0.592/0.835; error ≈ f_true
  across the 2·R_p blink window inside an 8·R_p seen transit); fmin_abs_dev = 0.815
  (sky orientation: readout min 0 vs exact 0.815); false_blink_frac ≈ 0.06; samples 1.
  FAILS p99, fmin, blink. The letter's first clause dies mechanically.
- **overlap-disc (positive).** flux_err_p99 ≤ 0.005 (c78d's closed-form cross-check dev
  0.003 = MC noise); fmin_abs_dev ≤ 0.005; blink 0; samples 1; ratio 1/π. PASSES —
  controls on both sides, so the verdict cannot be VOID.
- **Verdict: PASS; killed: pixel-h1** (if pixel-h2 also fails any bar, the per-pixel cure
  is NOT licensed at player β and I report the refutation as standing with the cure
  unpriced; if overlap-disc fails, my instrument is broken and nothing is interpreted
  until fixed).

Diagnostics (folded into the same regenerating record):

- **β 0.9, both orientations.** one-sample peaks ≈ 0.70/0.86 with f_true_min ≈ 0.575/0.783
  (both checkers measured this); pixel-h2 p99 ≤ 0.05 both orientations — the cure is
  β-independent to this decade because the error is edge-quantization and the edge stays
  R_p-sized. If it fails, the cure's pitch must shrink with β and I report the scaling.
- **Static cost scaling** (h = R_p/2): R_f = 10 → ~1257 samples, ratio ≈ 1.00, p99 ≤ 0.02;
  R_f = 30 → ~11,310 samples, ratio ≈ 1.00, p99 ≤ 0.015 (error ~ h·perimeter/area ∝ 1/R_f).
  This is the page's corrected cap-as-function, measured.
- **The arc formation (400 ships, the game's own shape).** one-sample peak error = 1.000
  (centroid behind, every ship visible — the checkers' finding, now on a regenerating
  record). Pixels at h = R_p/2 cover the 0.3-wide band with only 3 samples → p99 ≥ 0.2
  (the pitch must resolve the thinnest support dimension, not the fleet's span); at
  h = 0.15 → 41 samples, p99 ≤ 0.05. Readout rule this measures: the readout is one law
  over a representative set — cost = min(N, support pixels at the resolving pitch);
  41 < 400, so pixels win here; below that count, per-ship exact sums are the same thing.

What would make this run wrong: my two paths sharing a bug despite different solvers
(quadratic vs bisection, clip vs case-split) — guarded by the light-cone residual and
predicate-agreement checks above; or the 401/1201-step grids aliasing an error spike
(unlikely: spikes last ≫ one step; the blink window alone is ~2·R_p ≈ 300 steps of the
static path).
