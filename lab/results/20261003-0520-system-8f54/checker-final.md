Working...
Check complete. **Grade: silver** — written to `lab/results/20261003-0520-system-8f54/check.md`; tree restored (only untracked `lab/results/`).

**Reproduced exactly** on a clean tree with `work/patch.diff`: rebinds 27721, kicks 27814 / fired 27694 (99.6%), same-cell 27346 (98.7%), dk avg 16744983761, memo hits 24443 on / 0 off, and 49596 items identical with memo on and off over 3×10¹⁰ ticks — a strong bit-identity proxy. An independent seed (2, sparse, full horizon) replicates every rate (98.6% same-cell, 87.9% hits, fit+compile 11.1 of 25 µs). Timings ran ~3× the author's under container load, as they pre-flagged; counts decided, and the author's own tests pass (18+1 ignored, 0 failed).

**Adversarial findings that kept it from gold:**
1. **Bit-identity hole:** `ShapeMemo::get` returns `NoBoundOrbit` on `compile`'s symbolic-circle branch (k = UNIT, q ∈ [1/6, 1/3)) — verified for p ∈ {3.5, 4, 5, 5.9} — and `fit_key`'s `circular(state)` path produces exactly that key, so the prototype breaks reachable states. Generic branch matches exactly.
2. **The memo is not the win:** compile-avg 10.5 µs on vs 10.8 off — `from_shape`, not the quadrature, dominates; the 88% hit rate buys ~1% of the kick here. The dossier's real claim (delete `from_state` per kick) survives; the wall-time gain itself remains unmeasured anywhere.
3. **Arithmetic slip:** "~2^14× over-paid" should be ~4× at the memo's actual 12-significand-bit resolution; the measured 98.7% is unaffected.

Named gold experiment: land kicks on (E, L) with rebind at cell overflow (circle branch fixed), priced on a quiet machine/M1 against the 29 µs baseline under B5/B12.
