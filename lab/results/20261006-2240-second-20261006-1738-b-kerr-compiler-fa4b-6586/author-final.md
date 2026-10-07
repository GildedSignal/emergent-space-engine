Working...
**Claim:** run `20261006-1738-b-kerr-compiler-fa4b` is gold on the physics — silver only because `check2.md` lacks the literal `Grade: gold` line `run.sh:99` greps for (the second checker's gold verdict sits in `checker2-final.md`) — and with the named experiments done: the record regenerates bit for bit from the shipped patch (eight gates, 10/10 tests, byte-identical `golden.json`), both latent edges are confirmed and measured (`isco(1, prograde)` = 6.0 vs truth 1.0; the cycle cap silently degrades to 1.1×10⁻² past u₃−u_peri ≈ 1.4×10⁻⁷, with a separatrix point returning a finite 625 rad for an orbit that never completes a cycle), and a 19-line guard closes the worst band with every gate line unchanged — so the gold claim stands.
it for bit** from the clean tree + the run's patch: all eight
   gates identical (modulo a compile warning and the runner's target path), kerr tests 10/10,
   crate suite green, `gen_tables.py` regenerates `golden.json` byte-identical (31 s, after a
   disclosed one-line output-path redirect — the script hard-codes the author's run folder).
3. **Both named latent edges are real and now measured.** `isco(1, prograde)` returns 6.0
   (truth 1.0) — I re-derived the cause by hand ((√r−1)³(√r+3) triple root at the bracket's
   `lo`); every a < 1 down to 1−2⁻⁵² is correct to 8.3e-9. The cycle cap binds at
   u₃−u_peri ≲ 1.4e-7 (advance ≳ 477 rad) and the error reaches 1.1e-2 at the deepest
   f64-representable whirl; the exact separatrix point silently returned 625.5 rad for an orbit
   whose cycle never completes. Two findings beyond the checker's one-liner: a bias band (up to
   1e-4) precedes the cap via agreed-exit, and the guard cannot catch that band.
4. **A 19-line guard closes the worst band** (`isco` refuses a ∉ [0,1); `cycle` refuses on
   unconverged cap): gate lines byte-identical, tests green, the deep whirls and separatrix now
   `Err(Range)` instead of lying. The frozen gate domain sits four orders of magnitude away
   (worst seed error 2.0e-13, convergence at n = 32–256 against a 2¹⁴ cap).

**Claim:** run `20261006-1738-b-kerr-compiler-fa4b` is gold on the physics — silver only
because `check2.md` lacks the literal `Grade: gold` line the publisher greps for — its record
regenerates bit for bit, and both latent edges the second checker named are confirmed, measured
exactly, and closed by a 19-line guard that leaves every gate line unchanged.
