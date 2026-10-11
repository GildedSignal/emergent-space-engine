Working...
Check complete. `lab/results/20261011-1332-fermi-e3bc/check.md` written; tree restored clean (patch applied to reproduce, then reverted; my temporary adversarial bench deleted); nothing else in the run folder touched; no git commit/push.

**Grade: silver.**

**Reproduction** — clean tree + `git apply work/patch.diff` + the dossier's one command: deterministic outputs (sinks, collapse counts, cycle bytes) reproduce **bit-for-bit**; timings within load noise (compile 10.3/26.9 µs vs 8.5/25.3; all other tiers ≤6%). `predictions.md` (13:40:47) precedes the bench (13:45:08Z header) — held-out discipline held. All journal inputs verified at source: H0190 K1/K2 + economics row, H0210's rtf 100 / 29 µs kicks, law.md's 0.05 compiles/kick and 16 B tube. The identity's arithmetic checks throughout (rtf 3/17/63/190/27,000; ceilings 3×10⁷ and 6×10⁸; 0.8 µs/kick budget), and `state()` is confirmed unmemoized.

**Adversarial cases** (all run, none flip a conclusion, all worsen margins):
1. **High-e tail:** compile at e 0.6–0.9 / 0.9–0.99 costs **53 / 98 µs** (0 errors) — 2–4× the ladder's top rung; the jet there is ~6× short, not 1.6×.
2. **`crossing_state` exists:** 429 ns direct table read (vs 4.6 µs `state`) — refutes the letter of "no cheap readout tier" for crossing-indexed reads; the jet's ε was assumed ≈0, so the honest shortfall band is **1.6–7×**.
3. **Populated memo:** hits cost **782 ns** at 10⁵ entries, not 422 — memo-hit rtf halves to ~100.

**Why not gold:** held-out P2 failed (readout 4.6 µs vs predicted 0.03–0.3) — disclosed informatively, but lab precedent (1 October red-team) bars gold on a failed prediction; and every tier number is the optimistic edge. **The gold experiment:** the author's own proposed probe — measure bodies kicked per parent orbit, cycle-cache miss rate, the real per-kick readout tier and re-anchor rate in the plane's bench, anchoring the identity on the shipped kick path instead of an assumed ε. Also flagged: a factor-2 ambiguity in H0190's averaged rate silently resolved to the optimistic end, and the L2-resident integer floor.

The run's real value stands: the belt memo-amortization plan is killed by measurement (1.0× collapse, a fortiori for the finer exact `ShapeKey`), compile-per-kick at 10⁹ is confirmed dead, and the per-active-body cycle-memory cap (~10⁶–10⁷ sparse-active across 8 GB) is new information the jet/b-h-live/b-encounter-skin builders must fit under.
