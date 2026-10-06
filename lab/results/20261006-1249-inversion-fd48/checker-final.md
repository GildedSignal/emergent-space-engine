Working...
Check complete. **Grade: gold** — written to `lab/results/20261006-1249-inversion-fd48/check.md`.

**What I did:**
- **Reproduced everything bit-for-bit** in a clean tree with `work/patch.diff` applied: echelon (trigger 0.5999, 15/15 encounters, pair [0,5] at distance-rank 5/5), all 7 trigger-table rows, all six jams (misses 35.33/37.09/36.03/10.55/7.47/14.55%, m̂ 11.06/11.31/11.07/4.44/0.21/5.64), and the xcheck (664 boundary disputes, 0 interior, 0 spurious). Only `truth_s` timing differed.
- **Verified predictions pre-registration** by file order: `predictions.md` predates all experiment JSONLs; the pre-registered kill criterion is met; the two magnitude misses are disclosed honestly.
- **Built an independent instrument** (Python re-implementation: exact RNG, integer-period Kepler, own brute-force contact set, own rank code — no shared path): 5927 contacts at n=800/σ_λ=0.004, k=4 miss 27.2% by sort rank (21.2% interior-only), 44.7% by distance rank, max_rl 16 — bracketing the author's 35.3% and proving the interior-minimum convention doesn't manufacture the finding. I caught and fixed a bug in my own first pass (unfiltered argmin arrays) before grounding these numbers; the earlier tighter-jam percentages I discarded as ungrounded, keeping only the valid contact growth (3481→11916 at σ_λ=0.002).
- **Novelty**: the adoption is live in the board's taste log and `lab/refs/opus-motion/memo.md` §6 line 275, which assigns the rank-≤4 certificate to exactly the dense-formation regime the author kills; the memo's known-holes list (line 277) does not include rank multiplicity.

**One residual, flagged in check.md:** the gold's own branch is unreachable from this checkout (no credentials), so the trigger formula rests on the author's quotation — but the in-domain kill doesn't depend on it, and the author's table shows e=1e-4 already reads 4.8, so the motivating fleet (e~1e-3) is outside the domain under any reasonable variant.

The core result stands: partner rank is a density number (m̂ ∝ n/σ_λ), not a regime constant; k=4 silently drops 21–45% of true sub-ρ contacts inside the certificate's own firing domain. Premise-wrong, reproduced, independently confirmed — gold.
