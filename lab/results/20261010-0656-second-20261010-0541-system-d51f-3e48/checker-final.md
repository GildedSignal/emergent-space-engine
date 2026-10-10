Working...
Check complete. `check.md` written to the run folder; tree restored; nothing else in the run folder touched.

**Grade: gold.**

**Reproduced** (patch applied clean, decisive test 13 s): every deterministic number regenerates exactly — walks 1123→42 (rtf 1000: 4224→42), all eight configs' digest/view equality asserts pass, deadline err med 2.061e3/max 2.070e6 ticks, carry error 5.49e-8, control 7680/0/0.0%. Timings ~1.7× the author's (my load 2.9 vs their ~1.0), inside their noise band, and the walk-tax arithmetic closes on my rerun too. Full crate suite 57/0 — default path untouched.

**My five adversarial cases all held:** seed 13 (the first checker's wall-divergent seed) and seed 42 equal at settle cuts with the same amortization; a 0.5 ms wall budget (heavy bites, forced different resolution order) still settles to identical digests with no rtf collapse (ratios 1.03–1.04); 600 frames pins incremental walks at exactly 42 while the walked mode grows to 1712 — anchors are O(bodies), not O(events).

**Why gold despite two falsified predictions:** both failures (median drop, relative error form) are instrument errors, honestly reported with closing arithmetic — the mean drops by exactly the walk tax, and the falsification corrects both the parent silver's "46% of the median" and the first checker's gold criterion, which inherited the same mean/median conflation. The mechanism's core predictions (amortization, digest/view equality, presented time, rtf dilution) all held. Novelty is clean: the parent designed the deletion, this run built and measured it; the prior readout-cost build died VOID on a different mechanism.

**Flagged for the integrator:** the dossier quotes an earlier execution's timings than the run-log it cites; the near-body floor needs re-derivation before the flag flips; and the β→1 gap is deeper than "no shipped scene" — the carry's error grows with worldline *curvature*, and no fast curved worldline exists in this record.
