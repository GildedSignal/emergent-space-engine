Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-1237-dynamics-9dbb/check.md`, with the author's page corrected in place.

**Reproduction (perfect):** applied `work/patch.diff` myself; all 57 series TSVs byte-identical, `analyze.py` output identical, cost 20.5 µs. The b9c8 control re-run independently: 864 chains / 0 nonzero dr_rel / 92 key-cyclic. Verified every headline number from raw TSVs with my own script — exact {−13} translations, circle ratchets (−7571 median, 99.7% negative, decelerating −10365→−2656), twins (k identical, w gap exactly 1 ulp, psig 505), fixed corner (k,w constant after 1/4/16/19), radius law exactly linear (ecc) and √n (circles), zero refusals.

**Adversarial (9 chains, all outside the author's range — all confirm):** depth 65536 keeps −13 exact with w frozen; circle at 32768 stays 99% one-signed (√n radius, sub-floor); w₀ = 1/3 turn and 1 ulp walk the same −13; new e = 0.25/0.7 are exact −28/−5; φ7/8 is exact −169; the fixed corner absorbs under w₀+1 ulp.

**Why silver, not gold — three sentences contradicted by the run's own log:**
1. "at φ 5/8 … k exactly −13 while w jumps >1/256 on 1023/1023" — the −13 arm has **0/1023** such jumps (max 1.4×10⁻⁶ turns); the 1023/1023 jumpers are the p=8M arms walking −1. Two true facts composed into one false sentence (Claim, Evidence, and page).
2. "every walker ≥ 98% one-signed in k" — the census's own 3 mixed arms are 68/83/88%.
3. "P1 fails only its ±10% clause on circles" — P1's own ≥90% kill criterion also fires on those mixed arms, unreported; and "−1 exactly at 8 M" holds only on the μ doll.

All three corrected on the page; the underlying conclusions (translation family, k-independence of the w lottery, neutral response) survive and are strengthened by the adversarial runs. Gold path: corrected record plus the circle ratchet's k-vs-rate rung the author names — my 32768 run shows the rate falling ~n⁻⁰·², so whether the circle leak's total walk is bounded is still extrapolated, not measured.
