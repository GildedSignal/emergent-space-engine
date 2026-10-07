Working...
Check complete — `check.md` written, nothing else in the run folder touched.

**Grade: silver.**

**Reproduction:** All 9 decisive runs bit-for-bit identical to the author's artifacts (every per-particle field), `summarize.py` → `verdict.json` identical, and the port reproduces the parent's `decisive.json` with zero diffs (physics functions byte-identical; edits additive only). Every dossier number regenerates from shipped artifacts, including the 4·C₀ row, the flank set, and the parent's previously-unsaved 0.106 no-memo control. Predictions timestamped between last edit and first decisive run.

**Attack results (3 out-of-sample scenes):**
- **Low-e extreme (e₀ 0.002–0.02):** B catastrophic (median 11.8, 24/30 wrong-sign), B2 accurate (0.065, zero wrong-sign) — the O(μ/e) window-residual mechanism independently confirmed; but the worst B2 particle (2:1 flank, e₀ 0.005) over-rates 9×.
- **High-e (0.2–0.35):** both laws excellent on rate — failure is a low-e singularity as claimed; guard excludes 17/30 (greedy at high e, unpriced).
- **Double horizon (H=48000):** B2's median holds but the away-set p90 **inverts vs A** (0.877 vs 0.674) and the flank envelope compounds (pump 2.8–3.1×) — "fixes the rate completely" is horizon-local.

**Why not gold:** the pre-registered rescue criterion fails on its own env clause (honestly disclosed and coded to fail in the shipped script), and my attacks show the rate rescue is horizon- and e-local on the flank — the away-layer replacement isn't one-step adoptable. The named gold experiment: B2 + guard (or law.md's rotating doll on the flank) on a flank-heavy, low-e belt at 2× horizon, judged on rate and envelope tails vs A.
