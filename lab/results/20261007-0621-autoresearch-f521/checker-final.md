Working...
Check complete: **Grade: silver** (`lab/results/20261007-0621-autoresearch-f521/check.md`; tree restored, nothing else touched).

**Reproduced from a clean tree with the patch applied:**
- Setup 8 328 → 5 983 ns/pair (1.39×, min of 3 alternated, load ~5; author's 1.43× under load 7.6), run 9 057 → 6 604 (1.37×). Saved raws match the dossier digit for digit.
- Correctness: all 14 verify belts missed=0/false=0, and full JSON outputs byte-identical to the baseline binary modulo timing and the `evals` counter — the bit-identical-certificate claim holds at every observable (sections/checks/hits/queries/qsteps, slack fractions, changed/flipped, skip violations 0/0/0/5).
- Adversarial: `verify long10k` (in the binary, author never ran it) — 10 000 orbits, 1 897/1 897, identical to baseline. Code-level check of the caching premise confirms j's grid is s-invariant and computed with the identical float expression.

**Discrepancies found (all reported in check.md):**
1. Kick "unchanged at eps=1e-9" does not reproduce on clean load — I measure 1.35× there, roughly flat across eps; the author's 1.66–1.77× and eps-dependence are load-7.6 artifacts (same order of magnitude, so the claim survives at the lab's granularity).
2. The `evals` metric changed units between binaries (baseline scan eval = 2 Kepler solves, candidate = 1), so "40.5 → ~21 solves" mixes units.
3. predictions.md promised two changes; the local-Lipschitz change never ran — disclosed in log.md but not in the dossier's Predictions section, and the setup ≤ 5 500 miss is partly that, not only "closed-form dilution".

**Why silver, not gold:** real, reproduced, adoptable in one step, but ~1.4× — far from the 10× bar; novelty is loop-invariant hoisting correctly aimed by instrumentation, distinct from components-4643's killed deferral lever. Gold experiment is named: kill the geometric tail (54% of advancement calls below 16ρ) or store the arc grid per pair so a kick re-pays no setup (the board's 12.6× slack-skin lever), verified with bit-identical certificates.
