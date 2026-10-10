Working...
Check complete. **`Grade: silver`** written to `lab/results/20261010-1920-autoresearch-ccc6/check.md`; tree restored to clean.

**Reproduction (clean tree, `git apply work/patch.diff`)** — every number within 3–8% on a shared box:
- Setup: σ1e-3 34427→16855 ns/pair (2.04×), σ0.01 1.69×, held-out σ3e-3 **1.81×**, n30000 **1.43×**; evals/pair match the author exactly (120.73→59.29 etc. — gains track the eval ratio, no overfit signature).
- Kick: 7377→851 µs/kick at ε1e-9 (**8.67×**; 9.08→1.05 µs/pair-equivalent — the board's ~1.1 target), skip 94.5%, **skin_violations 0 across the ladder**, changed/flipped fractions byte-identical to baseline. The baseline's 5 phase-rule violations at ε1e-3 reproduce exactly as pre-registered.
- All 14 verify belts zero-miss before and after.

**My attacks:**
1. Hot belts σ_e 0.3–0.5 (author stopped at 0.2): k=12 stays zero-miss on 6646 truth encounters — the author's own risk on R3 was conservative.
2. Extended ladder ε→1e-1, fresh seed: zero violations; the Binet guard correctly refuses to skip at large kicks.
3. Kick sequences (the dossier's unmeasured case): drift measured from the certificate anchor → 0 violations; **naive unrepaid budgets → 522 violations by 3 kicks of ε1e-7**. The skin is sound only with an explicit anchor/repay rule — absent from the adoption cost.

**Why silver, not gold:** the headline R5 prediction (10–15× at 1e-9) delivered 5× same-binary — a disclosed miss, and the gold bar demands held-out predictions held plus 10×; measured is 8.7× cumulative, and the guard is measured, not derived. The one experiment for gold: derive the drift/section-shift bound and validate the anchor rule, making the skin law.
