Working...
Check complete. **Grade: silver** — written to `lab/results/20261008-1859-scout-141c/check.md`, nothing else in the folder touched.

**What I did:**

1. **Reproduction** — `python3 news_scaling.py` in a clean /tmp copy: 0.61 s, `news_scaling.json` byte-identical, every dossier number regenerates. `patch.diff` is empty (0 B); work is self-contained. File times confirm pre-registration: `predictions.md` 19:04 precedes the outputs 19:09.

2. **Attacks (4)** —
   - Extended the sweep with the author's own code to R=8192: quantum +44.8/+45.3/+46.1 per octave, naive exactly ×4/octave — log law holds over 4.6 decades.
   - Non-central observer (the author's admitted gap): still log (+91/+88/+88 per octave); only c₀ moves, as predicted.
   - Falloff a⁻¹: ×3.66/octave ≈ R² — the kill-condition caveat is honest and load-bearing.
   - Closed-form audit: **found a real defect** — `run_event_case` never multiplies by ρ, so the simulated disk has π× the stated sources; the dossier's "λN(R)" (1.05e4 vs actual 3.29e4 at R=1024) and analytic constant "47" (their formula gives 15 with ρ=1/π) are both wrong. The correct closed form 2πλδln2/Q = 43.6 matches measured 44, so the "~6% r_cut deficit" story is miscalculation. Exponents, crossovers and the 130× head-to-head are unaffected.

3. **Novelty** — no prior entry; the prior silver `b-news-gravity-e300` built the cursor mechanism, not the scaling law, and the dossier frames this correctly. The quoted risk is HANDOFF:74 (verbatim), though the dossier misattributes it to "the board".

**Why silver, not gold:** the quantum channel counts floor(Σs/Q) — a one-line integral the predictions themselves derive, so the "measurement" cannot fail by construction; P5/P6/bursty are closed forms. One experiment to gold: run both channels on the plane's real event stream through the engine's own news cursor, per the design's-cheap-path lesson.
