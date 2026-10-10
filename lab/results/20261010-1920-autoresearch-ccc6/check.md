Grade: silver

**Abstract.** Claim: four changes to `crates/encounters` cut candidate-pair setup 1.4–2.1×, and a dual-guard slack skin cuts kick re-certification ~5× at ε1e-9 with zero violations. All reproduced in a clean tree from `work/patch.diff`: setup σ1e-3 34427→16855 ns/pair (2.04×, evals 120.73→59.29 exact), σ0.01 1.69×, held-out σ3e-3 1.81×, n30000 1.43×; kick 7377→851 µs/kick at ε1e-9 (8.7×; 9.08→1.05 µs/pair-equivalent, the board's ~1.1 target), skip 94.5%, skin_violations 0 on the ladder, changed/flipped fractions byte-identical. My adversarial cases hold: k=12 zero-miss on hot belts e≤0.5 (author stopped at 0.2); fresh seed + ε up to 1e-1 zero violations. Not gold: the headline R5 prediction (10–15×) delivered 5×, and 8.7× < 10×; the guard is measured, not derived. Cost to adopt: one research-crate patch; budgets need +16 B/pair and an anchor rule.

## Reproduction (clean tree, `git apply work/patch.diff`, medians of 3, load 2.4–2.9)

| spec | baseline | patched | author |
|---|---|---|---|
| setup σ1e-3 ns/pair | 34426.6 | 16855.3 (2.04×) | 35592.9→16701 (2.13×) |
| setup σ0.01 n10⁴ | 8400.9 | 4972.3 (1.69×) | 9165.8→4987 (1.84×) |
| held-out σ3e-3 | 13065.3 | 7209.2 (1.81×) | 1.79× |
| held-out n3·10⁴ | 5582.5 | 3897.7 (1.43×) | 1.40× |
| kick ε1e-9 µs/kick | 7377.1 | 850.6 (8.67×) | 7188.6→914.8 (7.86×) |

Evals/pair exact (120.73→59.29, 20.26→9.59, 39.57→19.15, 9.69→4.63). Skin-off path (skin inert at ε1e-3, skip 0.0000): 4648.7 µs vs author's 4527.2 — the same-binary skin A/B (5.01×) reproduces as 5.47×. All 14 verify belts `missed:0 false:0 dup:0` before and after; `changed_fraction`/`flipped_fraction` identical to baseline at every ε; `crossover_orbits` 43.7 unchanged. Baseline kick reproduces the 5 violations of the 1.5-factor phase rule at ε1e-3 exactly as pre-registered.

## Predictions

`predictions.md` (10 min before log.md and author-final; order consistent). Held: R1 −14% (author's isolated A/B), R2 5–15%→8%, R3 1.5–2.2× on Wide-heavy (evals halve exactly), R5 ~2× at 1e-7 (got 1.9×), ~1× at ≥1e-5 (got 1.01–1.09×), phase-only rule violations >0 at 1e-3 (got 5). Missed: R5 at 1e-9 predicted 10–15×, delivered 5.0× same-binary — disclosed as a miss. By the letter ("reproduced, and the held-out predictions held") that headline miss blocks gold.

## Attacks (mine)

1. **Hot belts beyond the author's e ≤ 0.2** (verify set x: σ_e 0.3–0.5, e at the 0.5 cap, incl. narrow a∈[1,1.0025] and ρ3e-5 combos; 6646 truth encounters): all zero-miss with k=12. The author's own risk on R3 was conservative.
2. **Extended kick ladder, fresh seed 20269999, ε up to 1e-1**: skip fractions match (94.7% at 1e-9, 50.9% at 1e-7), skin_violations 0 everywhere; the Binet guard refuses to skip at ε ≥ 1e-3.
3. **Kick sequences** (the dossier's unmeasured case). Conservative variant — guard sees cumulative drift from the certificate's anchor: 0 violations, skip fraction decays 0.51→0.08 by q=6. Naive variant — guard sees only each single kick's drift, budget never repaid: **522 violations by 3 kicks of ε1e-7, 374 by 12 kicks of ε1e-9**. The skin is sound only with drift measured against the anchor state; adoption must repay or re-anchor budgets per skip. This is a contract, not a flaw of the measured per-kick claim, but it is absent from the dossier's adoption cost.

## Novelty

The encounters crate is untouched since c7b225d (r8 v2/v3); R1–R3 are new. The skin is the designed follow-up to the 6 Oct gold `components-4643` ("the slack skin (12.6×) stays the lever; nothing to build") and to H0211's queue; this run builds it, corrects the 12.6× forecast to a measured 5× (the residual range scan is not skippable), and kills the phase-only rule. Not a redo.

## Goal fit

Board focus line 3 (encounters without work per orbit) and the top scaling risk: candidate work must track real encounters. Fits PRINCIPLES 1 ("The cheapest compute is compute not done" — whole re-certifications deleted) and 3 ("Compute only surprises" — the budget is the certificate that a kick is not a surprise). Setup gain is uniform across held-out specs (no overfit signature: gains track the eval ratio everywhere).

## The one experiment for gold

Derive the guard — drift of the integer circle rotation under ε plus section shift vs cone margin — and validate the anchor/repay rule on kick sequences; then the skin is law rather than a measurement, adoptable in one step into law.md's encounters design (with the +16 B/pair store and the M1 re-measure deciding the final number).

## What the author missed

- The anchor contract (attack 3): unrepaid budgets violate immediately under kick sequences; the dossier calls sequences "unmeasured" when one run would have shown the contract.
- At ε1e-9 the skin deletes the setups but the kick keeps a ~280 ns/entry range scan (3122 scanned/kick ≈ 1/3 of the remaining 851 µs); the next lever after the skin is the scan itself, not cheaper setups.
- `us_per_pair` in the skin runs divides by the 45 non-skipped pairs and is not comparable to the baseline's 9.08; the honest 1.05 µs/pair-equivalent should have been printed.
- R4 (arc-local Lipschitz) was predicted but skipped; my hot-belt result suggests it is where the remaining e ≥ 0.1 setup waste lives.
