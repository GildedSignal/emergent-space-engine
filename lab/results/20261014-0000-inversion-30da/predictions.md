# Predictions — written before the decisive runs (14 October 2026, inversion lens)

Question: does `universe --replay-all` (the pre-merge regression gate, merged 13 October)
keep checking the flights as Julien flies more? Mechanism in shipped code
(`xtask/src/universe/replay.rs`): a 55 s budget shared over all flights, at most 27.5 s
per flight, and a flight the time does not reach is **skipped with exit code 0**.

Held-out cases: the two largest coordinate sizes below are not tuned on; the cliff
arithmetic is fixed by the code before any measurement.

- **P1 (throughput/linearity).** Unpaced replay advances the plane at a roughly constant
  coordinate rate R (cost is event-driven), so `replay_s ≈ a + C/R` in covered coordinate
  time C, with scenario-build overhead a ≈ 0.2–0.8 s (isolated by a near-empty flight) and
  R ≈ 2–5×10³ coordinate-s/s (scaled up from the three committed flights: ~2,900
  coordinate-s ≈ 1 s each). If events per coordinate-second grow along a flight, the
  largest point sits above the fit and the cliff arrives *sooner* than the fit says.
- **P2 (the per-flight cliff).** At that R, one flight becomes unreplayable-by-the-gate
  (needs > 27.5 s) once it covers ≈ 27.5·R ≈ 5.5×10⁴–1.4×10⁵ coordinate-s ≈ **9–23
  minutes of play at rtf 100**. I predict the measured 6×10⁴-coordinate-s flight lands
  within a factor 2 of the cap (5–40 s of replay).
- **P3 (the corpus cap).** The whole 55 s covers ≈ 55·R ≈ 1.1–2.8×10⁵ coordinate-s ≈
  **18–46 min of rtf-100 play in all flights combined**; past that the gate silently
  skips (exit 0) on every merge.
- **P4 (control, today).** The three committed flights (measured 2.3 s in all, all
  reached) leave the gate at full coverage today — the decay is ahead of us, not present.
  A control that cannot fail would be broken: the skip path must be demonstrated
  directly, not inferred — I will place the longest generated flight in a flight
  directory copy and require `replay-all` to print `skipped` and still exit 0.
- **P5 (the budgeted session).** The approved budgets name one-hour flights. One hour of
  play at rtf 100 is 3.6×10⁵ coordinate-s; I predict it needs ≥ 70 s of replay (≥ 2.5×
  the per-flight cap), i.e. **a budgeted session can never be checked by the gate as
  shipped**, whatever the corpus size.

Kill criterion for the worry: if R ≥ 1.3×10⁴ coordinate-s/s (the 6×10⁴ flight replays in
≤ 5 s), a one-hour rtf-100 session still needs ~28 s — the cliff question stays alive
only as corpus growth; if additionally R ≥ 4×10⁵, the gate holds a month of daily
one-hour sessions and the finding is "headroom, no action".
