Working...
Check complete. **Grade: gold** — `lab/results/20261018-0543-taleb-6de0/check.md` written, author's wiki page corrected in place, tree restored to clean at `55972278`.

**What I did and found:**

- **Reproduction (bit-for-bit).** Applied `work/patch.diff` to a clean tree, rebuilt, reran both ensembles and deep traces: all 288 ICs match the author's saved data exactly (events/kicks/capped/alive; only wall-clock differs); ka2 and kb traces end at the identical tick (t = 7.331 P / 14.982 P, v = 0.1991 / 0.7133, intervals 132 / 10). Determinism and chunk-invariance (20k vs 100k) verified. The runner's `regen.sh` exit 124 was its own timeout, not a reproducibility failure.
- **Predictions.** `predictions.md` (05:51:43) predates every run (first screen 05:51:56, decisive 16 P ensemble 05:52:40, traces 06:02+). The decisive P2 storm clause held exactly; P1 (the wiki's own capture hypothesis) honestly refuted.
- **Attack, one beyond the domain.** μ=1e-2 at 32 P: **31/144 capped, 70% of events** — the ruin grows with horizon. μ=3e-2 at 8 P: 19/144, 80%. μ=1e-3 at 128 P: 0 capped. I also traced the two capped ICs the author skipped — both ejected, making "every capped IC ends ejected" 10/10; one is a register-mint variant that verifies the full two-term drift identity dt·y = Δs·(1/y + 1/b) to 0.02%.
- **Two author errors closed, both in the claim's favor:** the "30% A-gap" dissolves once Δs's round-down to 2⁻²⁶ is applied (2.6176 shipped vs 2.618 measured); and the kick weight pins at the guard c/8 via the origin-fall term in U_P (not "y → c") — which is what produces the measured 6.52e-7/kick.
- **Page correction.** "interval 10–22 ticks at the cap" was true only of the 1.5M traces; fixed, plus [Checker] notes carrying the held-out extensions.
