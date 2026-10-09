Working...
Check complete. `check.md` written to the run folder — nothing else in `lab/results/20261009-1504-second-…-ca96/` touched, no git operations.

**Grade: gold**

**Reproduced** (all in `/tmp/check-136a`, run folder pristine):
- `exp.py` → bit-identical to `orig/metrics.json` (cmp clean, 7.4 s)
- `exp2` rebuilt and rerun (2:11, 72 MB peak) → every count row identical to `metrics2.json`; only the wall-clock row moved (med 2.27 vs 2.21 µs)
- `exp2b` rerun → `metrics2b.json` bit-identical
- Both controls re-pass: δ=0 gives 10,086 events / 0 missed / 0 extra; brute-force `truth_pair` ↔ exact re-setup 48/48 at all three deltas

**My adversarial cases** (8 full-population sweeps, 90 s, new binary reusing the author's conventions):
- Symmetric drift ±δ/2: 8.5% missed — same order as the author's 9.3%
- Negative δ: 9.0% — direction-symmetric
- **m0-held (tp-kept) bookkeeping: 94.9% missed at the fine band** — the natural alternative bookkeeping is 10× worse, so the author's lam0 choice was the cache-favorable one; no strawman, and the kill strengthens
- Mitigated bracket the author left open: 0 misses at 5e-5, then 4/7/22 at 1e-4/1.5e-4/2e-4 → δ\*_mit ∈ [5e-5, 1e-4), i.e. the design-as-stated's zero-miss amortization is ≈×9 — not the dossier's unmitigated ×1.8, but still 2.4–4.8× below the claimed ×43 and pure loss at the averaged cadence. The certificate refutation stands in every variant.

**Why gold, not silver:** the refutation is bit-reproduced, the pre-registered decision rule was followed exactly with four against-interest prediction failures honestly reported (including the author's own wrong mechanism, corrected by their own safety sweep), it falsifies the prior silver's safety guarantee ("can only cost, never miss") and deletes the band cache from the encounters design at zero adoption cost (never built). Novelty confirmed against HISTORY (ends at H0215; this is the first measurement of what cached `sections()` tolerate).

**Nits recorded:** corner rate 85.7% is Cross-only (86.0% all-kinds); `exp2_fragile.jsonl` was compacted post-run (disclosed in-header, totals match, regenerable); the ×1.8 headline should be read as the unmitigated cache — the mitigated number is ≈×9.
