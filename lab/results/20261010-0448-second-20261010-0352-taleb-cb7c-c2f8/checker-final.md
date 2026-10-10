Working...
Check written. Summary of the verification:

**Grade: gold**

**Reproduction (clean tree, no edits — `patch.diff` empty):**
- Every headline number recomputed from the raw JSONs with my own code matches the dossier exactly: ladder cpu_worst medians 13.56/16.59/17.42/15.22/15.62/14.57, CPU-hitch medians 0/0/1/0/0/0, gather share 0.57–0.68, stall guards 6/40 and 0/40, cadence pair 8.06 vs 3.23 ms, spinner tables.
- Digests reproduce bit-for-bit across **three** sessions: my rerun of E0 gives `f8b75cec…`; the second author's `q_M400_s1` equals the original's `mem768` (`3db02d3d…`); my fresh M256-s1 runs match `cd4b2cf5…` under paced, unpaced, and spinner regimes.
- Source check confirms the method: `frame_cpu_ms` is per-frame `CLOCK_THREAD_CPUTIME_ID`, per-term times are wall intervals (so the two stall guards are the correct attribution), `--members` clamps at 400 (mod.rs:32).

**Predictions:** written 04:54:34, before the first bench JSON 04:55:01. P3 failed and is reported as failed — that failure *is* the cliff refutation. P5's −48% cpu_worst miss reported as an unpredicted mechanism. Honest bookkeeping.

**My four adversarial cases (all held out):** seed 11 at M400 → zero CPU hitches, share 0.60 (no-cliff generalizes); `--members 500` clamps; spinner at a second point → cpu_worst drops 12.98→8.48 with digest equal (mechanism generalizes, though the "gather wall max as thermometer" part did not); second identical-frames cadence pair → digest equal, tax ×1.62 (real, seed-dependent magnitude).

**Flagged:** "13/13 reproduced" overstates the cadence tax (2 of 12 points show ~none; identical-frames evidence is 2/2 at ×1.6–2.5); "flat at the deadline" is loose for M320–M400; one scene, N ≤ 428 by the clamp, so fleet-scale sizing is extrapolation.

Gold because it satisfies "shows that a premise is wrong": the ~428-body compute cliff — the number that drove the original silver's smoothness concern — was wall-with-stall, proven from the original's own stored JSON plus causal spinner reproduction, and the replacement evidence (CPU-attributed gather dominance 0.55–0.67, cadence tax) directly grounds the `b-readout-cost` work order the integrator needed.
