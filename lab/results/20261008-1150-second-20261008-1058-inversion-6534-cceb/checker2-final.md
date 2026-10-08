Working...
`check2.md` written. Final state of the check:

**Grade: silver.**

**Reproduced** — full `run.sh` ladder from a clean tree: every deterministic number matches `work/second-outputs.jsonl` bit-exact (anchors, xcorr quantiles, all seven xcert rows; missed=false=dup=0 everywhere; 3.8/3.9/3.8 pairs per encounter flat in m). Predictions predate the decisive runs, with the m=25 smoke disclosed and misses honestly reported.

**My three attacks:**
1. **Fresh seeds** (the author's flagged weakness): 3 new seed pairs — zero-miss, selectivity unchanged. Holds.
2. **Incoherent ϖ** (crossings spread over the full circle): **rank misses 2–4 truth pairs (~0.1%)** — the break the author didn't measure. Localized to the lane-mean-rate shift over π-sized arcs (π-spread → 0 misses, TAU-spread → 2–4); `mean` survives only by degenerating to the full product. The fix is a closed-form window term, so the representation likely stands — but it's unbuilt and unmeasured, which is exactly one named experiment short of gold.
3. **Near-apsis** (apoapsis on the annulus, sin γ ≈ 0.001): zero-miss on both e_b — confirms the author's "in principle" claim empirically; inherited check-cost blowup as disclosed.

One incident during the check: an edit tool path-resolution error briefly touched `work/crossing/src/main.rs`; I restored it byte-identical from the pristine copy and verified with `diff -r` — the run folder is pristine apart from the new `check2.md`.
