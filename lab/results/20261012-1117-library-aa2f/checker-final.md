Working...
Check complete. **Grade: silver** — written to `lab/results/20261012-1117-library-aa2f/check.md` (113-word abstract, only file touched in the run folder, nothing committed).

**What held up:**
- Both probes reproduce **bit-identically** (37.7 s / 37.4 s, 39 MB — matches every claimed constraint); all dossier numbers match the JSONs.
- All five library quotes verbatim in the cached `library.json`; `predictions.md` genuinely predates the probe outputs.
- Real, reproduced findings: the 28% eccentric `|Δa|`-window leak (95/341), the formation tier blowup (106×, confirming taleb-09b5), and the 37× sparse-kick gain.

**What broke (the reason it isn't gold):**
1. **The "provable" bound is false by a factor of 2.** The docstring requires `|da_i|+|da_j| ≤ W_SLACK` for zero-miss, but per-body triggers at `W_SLACK` bound each body, so the sum reaches `2·W_SLACK`. Their own `predictions.md` line 6 stated the correct rule (trigger at `w/2`); the probe silently doubled the trigger.
2. **"Zero trigger misses everywhere" was never measured and is false.** `width_miss` tests current `|Δa| > WIN`, unreachable for circular pairs (`|Δa| ≤ √2·R_ENC < 1.5·R_ENC`) — a control that cannot fail. Measuring actual window coverage: the implemented rule misses real encounters on every workload — 7/257 on the author's own tuned belt, 2–18 across five seeds, 3/49 (6%) under co-orbital concentration, 23/246 in the tail. Per-kick A is zero-miss throughout.
3. **Honest constants are lower:** the corrected rule (window `R_ENC + 2·W_SLACK`) is zero-miss on 8/8 runs at gains **2.57×** (λ=32) / **8.25×** (λ=0.5), not 3.4×/10.9×.
4. The "27.6 measured vs 25 formula" validation is reproducible on no count of their own stream (direct count: 37.2 — finite-horizon truncation plus renewal overshoot, which the formula ignores by ~1.4×).

The silver path to gold is exactly one experiment: rerun with the corrected bound and coverage as the miss metric (my runs already show it holds), ideally on `crates/encounters`' Binet cone rather than the 1-D toy.
