Working...
Check complete. `lab/results/20261009-2043-autoresearch-d4f1/check.md` written; nothing else in the run folder touched; tree restored clean (patch reverted, my local mean-probe reverted); no commits.

**Grade: silver.**

What I verified in the 30 minutes:

- **Reproduction, bit-exact.** Clean tree → uninstrumented `--kick-bench` runs on seeds 1/2/3 give replay digests `131a3982…`/`17ba6896…`/`f6541714…`, identical to the author's *instrumented* JSONs — digest-neutrality proven on all three seeds, not just the claimed seed 1. Patched reruns reproduce the phase ratios within noise (compile/bind 0.85/0.60/0.85); baseline medians match.
- **Held-out predictions.** `predictions.md` (20:57:34) predates the seed artifacts (20:58:31); tuning quotes in it come from an earlier repeat, consistent with tune→predict→hold-out. Predictions 2/4/5 held; the strong form of 1 and prediction 3 failed on seed 2 — honestly disclosed, and the pre-registered kill condition (compile < 50% of bind) did not trigger.
- **Adversarial.** Fresh seeds 7/11 (83/70 kicks, leaver-heavy — never touched by the author): compile/bind 0.89/0.90, front 3% — the claim strengthens off-author-turf. Coverage probe: instrumented phases see 75–86% of the true mean kick; compile is 59–65% of it on seeds 1/3/7, 29% on seed 2. `emergent-space` tests: 50/50 pass with the patch (dossier's "40/40" is a miscount).
- **Novelty.** Recompile frequency (~99%, board 5 Oct) and the 29 µs headline (H0210) were known; the ns-resolved phase split, the ≤ 1.2× front-half ceiling, and the tail concentration are new. No H entry measures the split.

**Not gold:** no 10× moved, nothing deleted, no premise killed — a localization; plus the disclosed prediction miss. **Gold experiment:** intervene on the compile (memo/warm start, or split the 440–900 µs tail kicks) and measure the kick-cost drop on held-out seeds.

**Notable author misses:** the dossier table doesn't match its own saved JSONs (medians, p99, seed-2 ratio 0.57 vs 0.62); "leavers empty here" is false (12/8/7 leaver kicks at ~90–400 µs carry the tail — the coverage is *better* than claimed); the "≈97 µs mean" isn't regenerable from the artifacts (bench emits no mean).
