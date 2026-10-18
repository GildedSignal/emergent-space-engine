Working...
Check complete. Summary of what was done and found:

**Grade: gold** — written to `lab/results/20261018-1530-components-e87d/check.md`, with the author's proposed page corrected in place.

**Reproduction** — applied `work/patch.diff` in a clean tree, rebuilt, reran all eight modes. Every integer measurement is **bit-identical** across two independent regens (runner's and mine); only ns timings wobble on the shared box (arm_pair 1,365/1,409 vs dossier's 1,394). Verified the replica mirrors shipped `tier::arm_pair`'s integer setup line by line.

**Adversarials (5, one outside the author's range):**
- **Kind::Full formations** (their named unmeasured corner): kill *extends*, stronger — pre-kick due is "never" for all 240k pairs (d=0); one quantum kick flips 22.7% on at KH=10⁶. But the **3.4× cache lever does not extend**: δw p50 0.32·w per kick, 26% shape changes at 2⁻¹⁷.
- **ρ=10B** (their own named-but-never-run held-out arm): kill holds (flips 1.1×10⁻² ≫ 10⁻⁶) but decorrelation is partial (ratio 0.56–0.63) — the law is ρ-dependent toward the known ρ* regime.
- **σ_e=0.3**, **N=6000/new seed**, **keys fleet**: law holds tight (0.84–0.98), dv-flat. No Wide sections appear anywhere.

**Page corrections** — "δw < 1 tick" qualified as Cross-class p50 (my tail: 0.14·w belt, 0.32·w Full); both "could still live there" Full-corner clauses closed with my measurement; cache lever marked Cross-only.

**Noted misses** — one non-regenerable supporting number ("slack ≈ pi/5 at L≤10⁴"; the criterion is actually carried by stale.txt at L=10³), the cache store's unpriced ~32 KB/body memory cost at 10⁹, "1a29 reproduced" being law-consistency rather than their number, and the thin-w class still killed only by inference.

Tree left clean (variant example removed, patch reversed, run folder's regen outputs verified byte-intact).
