Working...
Second check complete: **`Grade: silver`** — written to `lab/results/20261012-1019-quant-b29b/check2.md`, `check.md` untouched, tree left exactly at the patch-applied reproduction state (my experiment reverted, no commits).

**What I did**
- **Reproduced all four rows** from the dossier's commands on a quieter box: empty frame 0.002 / 0.26 / 5.1 / 66 ms at 12 / 1.2k / 12k / 120k entities with zero events (author: 0.004 / 0.245 / 2.9 / 133.6 under load 7.4), RSS 484 MB identical, digest Θ(N) confirmed, ceiling ≈ 15–30k entities either way.
- **Verified the mechanism in source**, not just timing: `universe.rs:792` rekeys unconditionally, `:805–831` drains and requeues every non-due entity, and `Budget` counts only resolved events — the tier is genuinely unbudgeted, contradicting plane.md foundation 7 verbatim.
- **Adversarial cases:** threads=8 (fixed tier serial ✓), rtf=10000 — 100× the author's highest cadence, still 0 events (ticks are ~5 µs of light; sparsity is real). Novelty checked against HISTORY (ends at H0215; prior frame-cost work is the retired engine crate).
- **The decisive probe:** gated `rekey` out of `advance` (the dossier's fix (a), listed first in leverage order). Empty frame fell only 5.09→4.64 ms at 12k and 66.3→62.5 ms at 120k — **the drain owns ~90% of the tier, rekey ~10%**. The finding stands; the adoption plan's ranking is measured wrong. Reverted.

**Why silver, not gold:** the claim, predictions, novelty and premise-correction all hold, but the gold-making artifact (the non-draining fix collapsing the frame to O(events), digest-invariant) doesn't exist in the run, and the dossier's stated first step buys ~1.1×. One named experiment closes it; my gated-rekey build + suite is the template (suite was still compiling at my 30-minute cutoff and was cancelled, so safety is marked as asserted-by-design, not verified).
