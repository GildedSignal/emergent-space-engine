Check compl**Grade: silver** — `check.md` written, wiki page corrected in place, tree restored.

**Reproduced exactly.** Applied `work/patch.diff` at base e2e4eb1c, ran `regen.sh`: all four configs byte-identical to `metrics.json` (sha a078c9b4…), verdict identical (PASS; killed: poisoned, cold). Freeze hash `88b4dfaa…` matches predictions.md; `--lib` tests 10/10 with the patch; the nladder `proc_pid_rusage` link excuse is real.

**What held.** Warm passes at the frozen scene and beyond it in speed and N (β 0.99999: rows 1.0, 2.0/2.88; N=512: 2.0/2.96), and its ticks are **exact**: my independent bisection oracle agrees on 23,170/23,170 post-light rows at the author's own scale, 35,578/35,578 at 10⁶ units. Predictions 1–4 held.

**What fell.**
- **Prediction 5 wrong:** at rtf 10 cold passes every bar (2.0/3.0, rows 1.0) and the amnesiac *negative* passes (2.0/2.06) — the rung is VOID at that cadence, not "verdict unchanged".
- **Prediction 7 wrong:** at β 0.6 cold (3.69/5.0) and amnesiac (median 2.91) still fail — separation is not confined to β ≳ 0.9.
- **Prediction 6 half-right, with an unpredicted self-failure:** at rtf 1000 warm drops **20.9%** of its own rows.
- **Window-relativity undisclosed:** at the same cadence over 360 frames, warm fails its own presence bar (0.986; drops start at frame 178 — the frozen window ends just before).
- **Mechanism mis-attributed:** the 12 cold drops are emitters 32/33 at frames 118–119; my bisection fails those same rows (root_state read errors at probed ticks; warm resolves them) — read failures, not 64-iteration exhaustion.
- **Instrument claim refuted:** the "±1–2 tick f64 noise, 40% of correct rows fail" story doesn't reproduce — 0.07% bracket violations at eps 1e-3, and 15,230/38,400 = 39.7% is exactly the pre-light tick-0 fallback fraction. Their withdrawn oracle had a pre-light semantics bug; tick exactness is freezable at game scale now.

**Gold-making experiment:** r6 v2 freezing the bisection oracle (already 100% at the frozen scale) over a 360-frame window, with bars the negative fails at every cadence — it closes the "named hole" immediately and re-attributes row loss to the tube-end read artifact.
