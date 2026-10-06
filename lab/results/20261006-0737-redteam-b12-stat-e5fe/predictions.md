# Predictions (written before the decisive statistics run)

The trajectory data (16 frozen ships, three tolerances, four one-ulp nudges) is already generated;
nothing below has been measured on it yet. The decisive experiment is the evaluation of B12's
statistic (median growth exponent) and the recurrence ratio on the planted and reference series.

Held-out cases (not tuned on): the reference itself at rtol 1e-11 and 1e-13; a time-periodic
bounded error; a saturating random walk; the plane-like encounter-jump law; plant shapes in e and
1/r2 (only the a-shape is tuned to, as in laws.rs); one-ulp nudges of every plant.

1. **Today's statistic on the reference itself.** The raw (non-conserving) reference at rtol 1e-12
   has a Jacobi error of order 1e-10, above the 1e-12 floor, and I predict its median growth
   exponent is 0.2–0.6, i.e. **the gate fails its own reference at its working tolerance**. At
   1e-11 the error is larger (1e-9–1e-8) with a similar exponent; at 1e-13 the error is near or
   below the floor and the ship drops out of the judging (borderline). If all three tolerances
   fail, the premise is dead on arrival: no float64 law can pass except one that projects onto the
   invariant.
2. **Planted bounded vs compound (P2 replication, independent harness).** Median exponent:
   bounded-a ≈ 0.45–0.55 (fails), compound ≈ 0.25–0.35 (fails): the inversion the integrator
   measured (0.49/0.31) reproduces in my port. The e-shape and 1/r2-shape read 0.2–0.4 and
   0.2–0.3 respectively (synth.py read 0.255/0.218): both fail or are borderline.
3. **Recurrence ratio (the draft in handoff.rs).** State-only errors (bounded-a/e/1r2, scaled
   1e-11, noise 1e-11, echo-level): ratio 0.8–1.1. Memory errors (compound, leak, drift, the
   plane-like encounter-jump law, saturating walk): ratio ≥ 1.25. I predict the gap is real but
   the margin is thin for the compound walk (1.25–2), because its far/near spread ratio is the
   ratio of random-walk increments over ~26x spanned time, about sqrt(26) ≈ 5 at p90 at best but
   dragged down by pair-count imbalance.
4. **Time-periodic bounded error (the adversarial case I built against the recurrence ratio).**
   err = 1e-7·sin(2πt/100P): no memory of the error, never compounds, but the recurrence ratio
   reads ≥ 2 (far pairs span different phases than near pairs): **the recurrence ratio fails it,
   a false positive by the state-only criterion**. If this holds, the recurrence ratio measures
   time-correlation of the error, not compounding, and its disposition must say so.
5. **Saturating walk** (compounds for the first ~50 encounters, then stops): exponent 0.1–0.3
   (passes today's gate — bounded, correctly), recurrence ratio 1.5–4 (fails): the two statistics
   disagree on a law whose error is bounded-after-saturation. Disposition question for the
   integrator, predicted to surface here.
6. **One-ulp chaos.** At least 5 of 16 ships change their closest approach by more than a Hill
   radius under a one-ulp nudge (the memo's §1.8, 9/16); the per-ship exponents of every plant
   scatter by more than the 0.2 limit width, so **no per-ship decision is stable; only medians
   over the 16 are**, and thresholds need margin against this scatter.
7. **The floor is below the reference's own noise.** The two-tolerance C agreement of the frozen
   ships is ~1e-11 relative (they were selected at 1e-9), so the 1e-12 floor sits below the
   reference's own reproducibility: a perfect law judged against a rerun of itself at rtol 1e-12
   reads err ~1e-10, above the floor. Prediction: confirmed by probe r12-vs-r12 rerun (nudges).

Kill criteria for the recurrence ratio as drafted: any compounding law that fails today (compound,
leak, drift, encounter-jump) reads a ratio below any state-only law's ratio; or the ratio's value
for one law moves by more than ~2x across one-ulp nudges (then it measures the path, not the law).
