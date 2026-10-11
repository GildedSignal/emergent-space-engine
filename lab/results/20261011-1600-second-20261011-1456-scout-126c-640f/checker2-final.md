Working...
`check2.md` is written: **Grade: gold**. The run folder is otherwise untouched (original file timestamps intact, no commits, all probe work in `/tmp`).

**What the check established:**

**Reproduction — perfect.** Two fresh `python3 falsifier.py` runs (26.7 s / 28.8 s) are bit-identical to each other and to the stored `metrics.json` on every key except `machine`/`wall_seconds`; E1–E6 are bit-identical to the prior silver's git record; both formerly-orphaned keys regenerate from `main()` (adaptive counts 43/83/133/205/3765 exact; bound control live on all three seeds). The named silver-killer — the record — is dead.

**Predictions.** P-D and P-C held; P-A/P-B cost, panel and kill lines held, but the ≤1e-9 accuracy predictions failed by ~2.5 decades — reported as failures with magnitudes, no pre-registered kill criterion tripped, claim restated at the measured level. Predictions predate the run by 30 min (mtime evidence).

**My held-out attacks all landed inside the shipped claim:** intermediate δ (no cherry-picked grid), L̃² ∈ {12.05, 12.5, 14} (the σ-rule generalizes), kick fracs 0.1/0.5/0.9 and other L̃² (uniform fails up to 0.32; ladder m=1 ≤ 4.2e-7 at ≤ 53 panels, m=2 ≤ 9.7e-8 at ≤ 71), deeper terminal, safety/base/m=4 invariance.

**Two independent contributions beyond the run:** at δ=1e-10 three mutually independent quadratures (candidate ladder, my θ-substitution, scipy adaptive) cluster within 4.5e-7 while DOP853 sits 2.4–6.6e-6 away with a 4.1e-6 internal shift — the oracle, not the candidate, degrades (the run's inference is now measured; the run actually understated itself there). And my exact factored rquad proves the bound-control flat residual was the reference's Rfun floor (candidate is at 1e-12–1e-13), confirming the author's diagnosis digit-for-digit.

**Reported misses for the builder:** the valley's bound-side twin (uniform cos panels hit 7.5e-5@8p just below Vmax — the ladder is cosh-only), the non-monotone 9.1e-7 at δ=1e-9 (m=2 re-derivation is load-bearing), the trap being a hard `None` crash on the cosh branch only, and one loose budget sentence.
