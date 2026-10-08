Working...
Check complete. `lab/results/20261008-1719-constraint-1fe2/check.md` written; tree restored to clean (patch reverted, only untracked `lab/results/` remains).

**Grade: silver.**

What I did:
- **Reproduced** from a clean tree at main's tip (a838a28) with `work/patch.diff` applied: all four sweep corners, both identity runs, and `--kick-bench`. Deterministic counters exact (seen_max 76/428, readouts/frame 44.1/44.1/68.0/280.8); pipeline share 69–94% vs engine 5–31% (author: 71–95% vs 5–32%); identity 12.6/13.8% quantized-identical vs author 12.6/14.1.
- **Attacked** with seed 2, seed 3, and rtf 300 (3× event density, the author's own stated break point) — the share claim holds everywhere reachable (`--members` clamps at 400).
- **Verified the mechanism in source**: plain loop over all bodies (view.rs:300), fleet members extrapolated without readouts, and `Seen.age = t_now − t_e` advancing every frame — the delta-Seen kill is structural, not float luck.
- **Predictions conduct**: `predictions.md` (17:24:53) predates the sweep (17:32:01) and identity (17:40:12) by mtime; one prediction failed and is honestly disclosed.

Why silver, not gold: the headline was already in the journal — H0210 records "the view gather is 83% of a light frame" and the readout's cost is already a queued build (b-readout-cost). The genuinely new content (four-corner split, the measured delta-Seen kill, the ~2–6k-body ceiling) is real and adoptable as a redirect, but moves no bottleneck 10× and deletes nothing. Also flagged: the "369 µs for leavers" is the p99 (median is 79 µs), and at the top corner the worst frame is already engine-owned (max 6.5 ms > gather 6.0 ms), so the claim is a p50/share claim. The named gold experiment: build the display-quantum visibility gate and show the m400-r100 frame p50 drop by the pipeline's share.
