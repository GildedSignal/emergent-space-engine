Working...
Check complete. `check2.md` written to the run folder; tree restored to clean; nothing else in `lab/results/20261011-1729-components-b063/` touched; `check.md` never read.

**Grade: gold.**

What I did as the blind second checker:

**Reproduction** (clean tree `a838a284` + `work/patch.diff`): both digests (`eccc7f5a…`, `0e02bf0f…`) identical; timings within 1% — median 75.2 vs 75.6 µs, sub-phases 3.69/4.29/0.265/67.25 vs 3.74/4.32/0.266/67.62 µs; memo block identical (0% exact hit, 95.5% quantized, 1125/1158 cycle rebinds). Floor microbench: 42.0–43.0 ns batched, 2.22 ns streamed, 125.9–127.9 ns causal-random, 13.6 ns/source — all in family with the author's numbers (their 139–161 ns random case regenerates; it isn't saved in `floormatrix.txt`).

**Attribution independently verified beyond the author's evidence**: they only bounded "rest" by subtraction and left open whether it hid Scalar step machinery. I timed `rebind()` directly inside `step::process` (throwaway atomic probe, since `perf` is blocked at paranoid=4): **63.8 µs of the 67.4 µs rest (94.7%), fired on 1158/1158 kicks** — the refit is the lever, their open question resolved in their favour.

**Adversarial**: seeds 2 and 7 keep every structural claim (physics ≈ 8.2 µs, rebind 93–94% of rest, exact memo hit 0% with all shapes distinct); medians range 55–75 µs across seeds, so seed 1 is the high case and the idiot index stays 1,300–1,800×. Shorter windows raise `rest` (79 µs at 10 s), direction unaffected.

**Predictions**: file times prove it preceded both decisive runs. P2–P5 held; P1's two misses (leavers 91.7 > 60, p99/median 4.9 > 4) are disclosed in the dossier and both make the bottleneck worse, not better.

**Novelty**: no prior decomposition or floor in H0210–H0215; the memo part matches the 5 October record and is cited as corroboration, not claimed as new. `representation.md` line 67 quote verified.

Named in the report as adoption risks the author missed or under-measured: the read side at rtf 1, the epoch-batching assumption behind the 2.2 ns floor, the undecomposed p99 tail (5× median), and the seed spread.
