Working...
Check complete. Verdict: **silver** — written to `lab/results/20261011-0006-constraint-48cf/check.md`, nothing else touched.

**What I did:**
- **Timeline:** `predictions.md` (00:13:27) precedes all three decisive runs (00:13:53–00:14:29); exploratory benches earlier; empty `patch.diff` — a pure measurement run on main (a838a28, binary built from HEAD, tree clean).
- **Reproduction:** all dossier commands rerun. P1: far 36.3 ms at 10× less motion (author 37.1 vs 32.3 baseline — flat as predicted). Sample counts (680220/600277) and B13 (60/64, worst 2.12e-2) bit-identical; frame shares match (gather 63%/66%, engine 21%/21%). Absolute ms noisier on my loaded box — orders of magnitude only.
- **Adversarial:** rtf-10 (100× less change) → 47.0 ms, cost flat; 1080p → 110.7 ms (worse than the author's ~60+ extrapolation); source read of `xtask/src/galaxy/draw.rs` confirms the tick structurally — `accumulate()` clears all planes and re-splats every tube per frame, rtf enters only via `plan.t`.
- **Novelty:** the queue already held `b-readout-cost` and the lens brief quoted gather costs at 12 ships; new on the record is the whole-frame accounting (view 55–95% vs engine 21–25%), the goal-scale over-budget measurement, and the proven tick structure.

**Why silver, not gold:** nothing moved 10× — the fix (deposit-delta re-splat, digest as kill criterion) is the queued build itself, a build away from adoption; one of three predictions held cleanly; and the headline contradicts its own table twice ("55–79% of every frame" vs the 95% row; "engine fits its budgets" vs its own "p99 5.91 ms, budget 5"). Gold experiment: deliver the measured ≤1/5-median same-digest re-splat on these baselines.
