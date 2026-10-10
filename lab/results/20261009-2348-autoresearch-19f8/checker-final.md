Working...
Check complete. **Grade: silver** — written to `lab/results/20261009-2348-autoresearch-19f8/check.md`.

**Reproduced (clean tree, patches applied by me):**
- Digests exact on both corpora: tune `fd33f759b10e569f`, held-out `c45b567dfc5b395c`; KEPT patch bit-identical to BASE, p50 gain 0.8% (claimed ~0.7%).
- Attribution: fit/compile/orient/residual = 26.3/46.5/8.5/18.6% (quoted 25/47/9/19 ✓).
- Space 50/50, universe 0 failures.

**Adversarial findings:**
1. **E4 re-implemented from scratch** — tune digest changes and `witnessed_fit_keeps_the_full_search_key…` fails: the kill is real. Nuance found: held-out digest is *unchanged* under E4 (the kill bites on tune only), and E4 bought just ~6%, so killing it cost nothing.
2. **Extreme corpus of my own** (8× kick quantum, near-max e, radius exps outside both sets): bit-identity holds (`57a2c0d885335b22` both sides), KEPT ~1.6% faster interleaved.
3. **Regeneration gap:** the shipped instrumented build does not regenerate the quoted op counts (measured 61 div/35 isqrt/354 mul/450 add/84 iter vs quoted 54/31/317/404/76) — same order, no conclusion changed, but it's the exact "numbers the shipped code cannot regenerate" defect the taste log flags.

**Why not gold:** everything reproduced and all four predictions held, but the run confirms the board's standing cadence-first conclusion (already measured by components-4643 on the sibling artifact) rather than killing a live premise or moving anything 10×. The gold-making experiment is named: bit-identical warm start of the compile phase (47% of the call, ~99% recompile rate) — either branch (reuse proven, or sequence semantics proven to forbid it) upgrades to gold. Tree left as the author had it (KEPT patch applied); only `check.md` added.
