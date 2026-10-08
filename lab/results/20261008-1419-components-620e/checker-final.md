Working...
Check complete. `check.md` written; tree restored to pre-patch state.

**Grade: gold.**

**What I did:**
1. **Reproduced** from `work/patch.diff` in a clean tree — every timing part byte-close to the stored output (bind 28,417 ns vs author's 28,452–28,649; secondaries 10,633; Scalar force 2,267; integer body-only 218.5; idiot index 25×), deterministic exactness numbers identical.
2. **Found the residual's cause.** The shipped comparator in `accel_floor` computes `ox` but never runs `fx += ox` — the integer path silently drops the x origin fall that `force::acceleration` subtracts (force.rs:118–119). One-line fix: max dv deviation **1.573 → 6.254e-4 of a 2^-30 quantum** (160× inside the author's pre-registered 0.1), max relative 1.845 → 8.702e-3. The author's "unexplained 3e-3 residual" was the second half of their first bookkeeping bug; the evaluator itself is exact.
3. **Verified metric consistency** with an instrumented sweep: the remaining 0.87% relative sits on a near-cancelling component (~78 quanta of the 2^-80 band, deviation 5.7 quanta) — designed truncation, not a Newton-chain error.
4. **Checked for strawmen:** `secondaries_like` matches the real uncached `Ctx::secondaries`, called per body per kick (step.rs:358–360); the 0.05 compiles/kick is adopted law (law.md:35); predictions.md predates the decisive run by 8.5 minutes; H0210's independent "kicks cost 29 µs" agrees with the composition.
5. **Novelty:** the total was known; the decomposition (68/27/6), the jet confirmation, the epoch-shareable 27%, and the verified integer-band evaluator are new — and the premise "integer arithmetic is where the money is" is corrected (it's 6% of the kick).

The gold gates on one named, author-flagged adoption measurement: the shared-epoch hit rate at real belt step spreads.
