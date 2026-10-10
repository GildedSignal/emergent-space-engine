Working...
Check complete. `check.md` written to the run folder — nothing else touched, no git operations.

**Grade: gold.**

**What I did (45-min window):**

1. **Reproduced exactly.** Ran the dossier's commands in a clean tree (`/tmp/check-repro`): the 38-run grid (1005 s wall, < 300 MB), the 13-run B re-run, and `analyze.py`. Result: `analysis.txt` byte-identical, both JSONs identical on every shared field, pair counts identical, total miss(W) = 15 exactly as reported (8 A/0.99-30k + 5 B/0.99 + 2 B30). My copy of the final script also recomputes `misses_c = 0` directly for family A, upgrading the author's `dtau_max ≤ W′` inference (max ratio 0.9973) to direct measurement.

2. **Verified prediction timing.** mtime/log chain: prompt 14:07 → pilot 14:18–14:22 (reproduces bb88's 18850 pairs) → grid 14:37 → addendum 14:47 → B re-run 14:52 → analysis 14:56. All failures disclosed, none reported as held; Z1′, CA, TA/TA′, CB′, MB′, the 8 Poisson-max range letters, KCTRL and held-out B30 all held.

3. **Attacked with 5 adversarial cases.** Correlated element spreads (the author's admitted untested orientation, both corners + drift regime), 1000×-wider e/w spreads, bimodal max-drift a, and e=0.995 — zero W′-misses everywhere. The e=0.995 "failure" (3106 misses) I diagnosed as the probe's Kepler solver diverging at e≥0.995 (residual 8e15; machine-exact at e≤0.99); a robust Danby-start solver rerun gives zero misses, tightness 0.9965, cost/enc 1.007 — W′ extends one corner past what was measured.

4. **Novelty & fit.** No HISTORY/docs entry on apsis-time keying or W′/X; base is gold 20261006-0346, W was bb88's unmeasured proposal. Satisfies the gold clause "shows that a premise is wrong" on a live build-queue premise, with a one-step adoption rule.

Named in the check as author misses: the undocumented solver domain (e≤0.99), the argued-not-measured drift-regime cost knob, sampled truth, the addendum's false "A had zero misses with W" sentence (conclusion unaffected), the unexplained "1.7e-6 level" in the claim line, and the post-grid script edit left implicit.
