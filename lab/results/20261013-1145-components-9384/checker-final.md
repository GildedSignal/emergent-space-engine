Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-1145-components-9384/check.md`.

**What I verified (my own runs, clean tree with `work/patch.diff` applied):**
- **Exactness:** 21M independent fuzz cases (splitmix64 RNG, std `u128::isqrt` as a reference independent of both implementations), targeting what the author's uniform fuzz statistically misses — the top band [(2^64−1)², 2¹²⁸), squares±1 at power-of-two roots, both call-site shapes, perturbed seeds ±2¹²/2²⁰/2³⁰. 0 mismatches; the "degrades only speed" robustness claim holds.
- **Numbers:** primitive 99–101 → 53–54 ns (1.85–1.9×); compile A/B/A −10.5–12% on the author's grid (author claimed −9.5%), digests equal in every arm; 70/70 oracle tests; plane digest identical (regen).
- **Instrument sensitivity:** a deliberately off-by-one isqrt flips the sweep digest — the identity check is not vacuous.
- **Two adversarial cases outside the author's domain:** a wider grid (p ≤ 2²⁰, e ≤ 0.999) holds at −8%; and the Kerr A/B the author left unmeasured — Kerr improves **−11%**, contradicting prediction 2's direction ("less than Schwarzschild").
- **Novelty:** 7d2b named the lever unmeasured; c914 measured divisions only. First build and measurement.

**Why silver:** same class as a48d/2833 on this topic — real, digest-identical, one-step adoptable, but ~10× below the gold bar (≈3–5% at kick level, deletes no component). Small dossier errors found: the "~17% share" inference doesn't follow from its own numbers (~22% implied; corrected on the page), the "~2^10 seed error" understates the worst case (~2¹³), and prediction 6's instrumented fix-up census was never run. The proposed wiki page also left open direction 1a dangling mid-sentence — corrected in place with the folded result and my Kerr/wide-grid numbers marked as checker-measured. Tree restored to its found state; nothing committed.
