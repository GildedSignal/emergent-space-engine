Grade: silver

**Abstract.** Claim: B12's attractor class is readable from increments (VR(τ*) with no amplitude floor) plus OLS/HAC trend, where the frozen growth exponent fails every bounded chaotic law. Reproduced bit-identically twice: warm rerun (88 s) and cold regeneration from seed in a fresh tree (4m58 s); every number, ship and flip in metrics.json matches; the EXP port is faithful to `fit.rs`. VR+trend passes all positives and fails all negatives (7.0σ separation); leak sweep shows VR exactly drift-blind (0.0049 for every leak). Predictions P2/P3/P6/P7 held; P1 failed (no inversion on the author's ships), honestly reported. Gain: unblocks the frozen gate for ~40 lines. Cost: my attacks show VR at the registered τ*=200 leaves amplitude-matched walks INDETERMINATE (FAIL rests on marginal trend t=3.3–4.1, partly the admitted |·|-folding artifact), a reversing leak passes both tests, and the demo is not on the gate's frozen harness. One experiment away.

## Reproduction

- `python3 b12attractor.py metrics.json` (author's command, output redirected): 88 s warm, **bit-identical** to the author's metrics.json — all 21 rows, se_null, flips, ships.
- Cold: fresh `/tmp` copy, no npz cache: 4m58 s, regenerated scene **bit-identical** again (matches "5–6 min cold").
- `growth_exponent` verified a faithful port of `xtask/src/behave/fit.rs:17-48` (same window edges, window maxima, geometric-mean x, NaN rules).
- `work/patch.diff` empty: self-contained script, no tree edits.
- Leak sweep is paired (same seeded noise across rates): all 10 leak rows read VR(200) = 0.00493 — VR drift-blind by construction, as claimed; VR = 1/τ for a pure ramp confirmed (0.00456).

## Predictions

Timing consistent with holding-out: predictions.md (24 min old at check start) precedes shipsbase.npz (6 m), shipsnudged.npz (3 m), metrics.json/run.log (1 m). Held: P2 (reference compounds at every tolerance: EXP 1.29/2.07/2.09), P3 (7.0σ ≥ 3σ), P6 (ulp-nudge flips only planted-compound INDETERMINATE→FAIL), P7 (kick VR 1.58). Failed, all honestly reported and mechanistically explained: P1 (exponent ranks correctly on these ships — the inversion is scene-dependent, itself the finding), P4 (VR is exactly, not marginally, drift-blind), P5 (OLS floor ~2 orders below the endpoint estimator; amplitude-linear half held). P8 marginal (se 0.064 vs [0.08, 0.25] — disclosed).

## My attacks (5)

1. **Amplitude-matched walk under the real chaotic background** (σ_w = 0.3/0.7/1.4×σ_Δe; end amplitude 1.0/1.6/2.6×A): VR at the registered τ*=200 reads 0.245/0.446/0.708 → PASS/INDETERMINATE/INDETERMINATE. VR **alone does not FAIL a walk even at 2.6× the bounded amplitude**; the pair's FAIL rests on trend t = 3.7–4.1 (threshold 3), which the author himself shows is inflated by the folded |·| series. At the derived τ* (τ=100: 0.355/0.529/0.792) it separates. The "no amplitude floor" paragraph overstates VR's own reach; the demonstrated advantage over the exponent is calibration, not floor.
2. **Long-memory bounded law** (AR(1), A=1e-11): φ=0.995 (decorrelation ≈ T/8) passes (VR 0.274); φ=0.998 (κ ≈ T/3) falsely fails (t=3.5, VR 0.47). The dossier's caveat ("decorrelating at 10⁴ periods") understates the boundary: it is ≈ T/3 — 30× the scene's measured κ=17, a thinner margin than implied.
3. **Reversing leak** (triangle peaking at 2e-10 = 20× the 1e-11 background): VR 0.045, trend t = 0.0 — **passes both**. A drift that reverses at mid-horizon is invisible to the pair; undisclosed. Partially mitigated by B12's max-err ≤ 1e-4 clause.
4. **Leak on a chaotic background scaled to A=1e-11**: 1e-13/period caught at t=30.4 — the claimed chaotic floor (~6e-13/period) is conservative. On the native background (A≈2e-6), 1e-12/period is invisible (t=2.0): floor linear in amplitude, as claimed.
5. Bounded AR(1) at φ≤0.99, plus noise plants: no other false verdicts found.

## Novelty

No variance-ratio/HAC work in docs/HISTORY.md or docs. The killed predecessor is the recurrence ratio (taste log 6 Oct; `handoff.rs` probe, ignored test) — rejected because it could not separate a slow leak from bounded error; this run's leak sweep answers exactly that. The exponent's miscalibration was known (handoff.rs ignored probe, 0.49; H0215); new here is the calibrated replacement statistic, controls on both sides, and floor analysis.

## Goal fit

HANDOFF's named instrument risk ("B12 cannot yet tell bounded from compounding error on chaotic ships") and "Headed next" item 2. Principle 13 ("errors never compound"), principle 2 ("error type over error size"), principle 26 (unit-root/HAC tests from practitioners who paid for being wrong), principle 18 (the level was the wrong observable). Fits.

## The one experiment for gold

Repeat on the frozen harness — `handoff.rs`'s kept 16 ships and real laws (echo, scaled-echo, the motion law v2, planted faults) — with τ* pre-registered by the event-cadence rule, the trend test on the signed Jacobi error (or the folding artifact quantified on walks), and the adversarial families above (amplitude-matched walk, long-memory bounded, reversing leak) as controls.

## What the author missed

- The reversing drift blind spot (both statistics pass a leak that grows to 20× the background and returns).
- VR's own floor at the registered τ*=200: walks INDETERMINATE to 2.6×A; the headline FAIL leans on a marginal, partially-artifactual trend t.
- The derived τ* rule is post hoc on this scene (gap 61 measured from the same data); it must be pre-registered.
- The long-memory false-fail boundary is T/3 decorrelation, not 10⁴ periods.
- Cosmetic: dossier says "16–35 three-Hill entries each"; the recorded per-ship table counts R_SOI hits (9–31). The 3-R_H entry counts are never recorded.
