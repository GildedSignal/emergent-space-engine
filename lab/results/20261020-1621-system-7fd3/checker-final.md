Working...
Check complete. `Grade: silver` written to `lab/results/20261020-1621-system-7fd3/check.md`; the author's page corrected in place; tree restored to shipped (only `lab/results/` untracked).

**What I did**

1. **Reproduced twice.** The runner's regen (exit 0) matched every load-bearing ratio; absolute counts differ 3–15% (frame loop is wall-clock-bound — expected, the claims are ratios). I applied `work/patch.diff` to the clean tree myself (base 83982a7), rebuilt, and flew three arms: the author's 10⁴ coast, **10⁵ coast (a decade beyond his N)**, and **10⁴ burn (a regime he never ran)**. All healthy. Compile share of rebind: 0.265 / 0.276 / 0.265; reads/mint: 18.6 / 28.6 / 19.9; history hit rate: 100% / **99.97% (21 misses)** / 100%.

2. **Adversarial attribution probe** (his named blind spot): instrumented reads inside the kick timer and bisection probes in `next_impact`. The ~20 readers are **not** the crash bisection (probes 0.2–0.4/mint) — they are general event/readout traffic (~5–6 on the kick path, ~13–25 outside it). The many-reader fact survives; the call-site split stays open.

3. **Novelty — the deduction.** The topical page, `mint-knots` (updated 12:10, four hours before this run, conflict-flagged in the index), already holds: the one-object premise (bd4b), a readers census (4ea0: 68–77 reads/generation, never-read 0), panel coverage (1991/624a: 85–98.5% of panels never read), a **flown** store lever (b9ae: knots→0, digests bit-identical; 0757's bounded cache, gold), and compile at **84–87% of the rebind (a765)** against this run's 26% (d4f1's 0.85–0.90 agrees). None cited; the dossier claims the fit was "never named" and the deletion dead — the deletion is dead only *as read-time recompile*, and the 26% vs 85% split is an unresolved contradiction.

**Genuinely new and solid:** the segment-history census (retired segments read 0.4–1.05×/mint at ~100% hit) and the belt's dispatch-level reads/mint. **One experiment to gold:** run the same census on a765's arm — if 26% holds there, the redirect is gold-grade; if 85% holds, 7fd3 is a belt-domain fact.
