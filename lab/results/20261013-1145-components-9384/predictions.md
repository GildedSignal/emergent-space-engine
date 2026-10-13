# Predictions (written before the decisive in-tree run)

Decisive experiment: replace `num::isqrt`'s body (f64 seed + one soft-division Newton +
exact square fix-ups; 24M-case fuzz-clean against shipped) in the shipped tree and measure
(a) a deterministic Orbit::compile sweep over a fixed key grid, (b) the space crate's test
suite (frozen oracle values), (c) a universe plane digest.

Held-out cases I have NOT tuned on:

1. **The in-crate compile sweep** (grid of p × e keys, both bound and passage-leaning shapes):
   I predict the compile wall drops by 4–9% of total compile time, per c914's isqrt share
   (6–14%) times the measured primitive ratio (~1.8×), not per 7d2b's 30%-of-node (which
   would predict ~15–20%). If the drop is >15%, 7d2b's node decomposition beats c914's
   compile-level split on the real path.
2. **Kerr compiles** (`kerr.rs` uses `ratio_sqrt` at the equatorial cut, and `word_root`
   is false there? — I have not checked): prediction — Kerr compiles also improve, by
   less than Schwarzschild ones (fewer isqrt calls per compile).
3. **Digests and oracle tests**: bit-identical / all pass. isqrt is a unique integer
   function and the fuzz found 0 mismatches in 24M cases incl. perfect squares ±1 and the
   u128 top corner. If ANY test fails, the wiring is wrong (not the math) and the run
   reports it without a fix if not obvious.
4. **The plane digest** (universe, 48 members, short settle): bit-identical.
5. The `x >= 2^126` region (never reached by any call site, covered by the fuzz edges
   anyway): unchanged behaviour by construction (no guard branch in C; the Newton+fixup
   path is domain-general).
6. **Cross-check on the seed**: the f64 seed lands ~2^10 away from the root at full width
   (histogram in the harness); the single division must pull it to ±1 in one step. The
   fix-up loop census inside the real compile (instrumented sweep) should show ≤ 3
   iterations per call. If it shows more, the seed analysis is wrong somewhere and I
   report the histogram.

Kill criterion for the configuration (not the method): if the compile sweep improves
< 2%, the primitive win does not reach the compile on the real path and the lever is dead
as a kick lever (it may still matter for kerr/plunge paths).
