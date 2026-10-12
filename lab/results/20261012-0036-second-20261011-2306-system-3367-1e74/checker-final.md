Working...
Check complete. `check.md` written: **Grade: gold**.

**What I verified:**

- **Reproduction (bit-exact).** Patch base confirmed against the committed file hash (self-contained, subsumes the prior run's patch); built with the fixed feature-flag command. Bench digest `41343a143a92f956…` at cut 609076340, all four replay digests, memo integers (1125/0.0%/51/95.47% etc.), key matches (1284–3306, all 100%), anchor counts (14/14/10/7 and at threshold/100), and `dv_frac_median` to the last digit. Timing ratios reproduce within noise on my box: made share 33.3%, leaver 72.1%, jet drops 1.49×/3.65×; live-loop player 548 µs/item vs 35 µs pure resolver.
- **Predictions.** mtime order consistent (predictions 00:42:08 before every saved JSON); the 00:47 fix and 00:49 re-run disclosed. P3/P4 held (P4 exactly), P1 half, P2/P5 missed — and the misses are the pre-registered refutation itself, honestly headlined.
- **Adversarial (four fresh configs).** seed 42, fleet 400, rtf 10000, 55 s horizon — drops stay 2.5–3.4×, key fidelity 100%, anchors ≤ 0.017/kick at the law's threshold. Found two scope limits worth recording: the ~26 µs floor is cadence-scoped (leaver jet median ~109 µs at rtf 10⁴), and quantized key count grows with fleet size (51→126→246) while the hit fraction stays ~95.5%.
- **Novelty/goal fit.** The time-domain attribution is new (shape counts were known from H0211/the prior silver); the ~10× was the adopted expectation, and its measured ceiling (≤ 3.8×) redirects the queue per board focus line 1 — the lab's "shows that a premise is wrong" gold disjunct, same precedent as the components-4643 gold.

Tree restored to clean; nothing committed or pushed; nothing else in the run folder touched.
