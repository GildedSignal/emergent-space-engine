Working...
Check complete. Summary of the verdict:

**Grade: silver** (`check.md` written; author's wiki page corrected in place).

**Reproduced** — applied `work/patch.diff` to a clean tree, rebuilt, and verified: digests bit-identical across arms on all three scenes, transition counts exactly 27/30/233, suites 0 failed. My regen's bind cuts (−19.8/−19.7/−13.2%) match the author's claimed order (−15.0/−17.5/−12.9); recorded every differing number (incl. suite wall ~2.5 min vs "17.9 s", two ignored tests vs one).

**Mechanism proven beyond digests** — `Orbit`/`Passage` store the compile key verbatim and `Passage::outer_radius` is the compile argument, so `word_of_key` is structurally the same computation as `word_for`. I added a per-bind differential (`ES_CHECK_WORD`): **0 word disagreements in 130,803 binds**.

**Adversarial** — (a) outside range: 800 members / 1200 s / seed 7 → digest identical, bind −11.6% corrected, settle −7%; (b) new regime: planet-doll `restricted` scene → digest identical, but transitions **0.066%** (vs 5–6% on planes), cut ≈ 0 — the gain is plane-regime-specific, confirming the author's no-op caveat (the raw −15.3% there was my own instrumentation, corrected in the check); (c) the differential above.

**Why silver** — real, adoptable (60 lines, never slower, digest-identical on 5 scenes), novel (f797 priced headroom only; no HISTORY entry), but a 13–20% slice rather than a 10× lever, and held-out P1 missed (≥10% transitions predicted, 5–6% measured, disclosed). The named gold experiment: measure the cut on the leaver/handoff tail's p95/99 — transitions concentrate on 278–310 µs leaver binds, which is where PRINCIPLES #12 says smoothness is decided.

Tree restored to clean (only `lab/results/` untracked); no commits made.
