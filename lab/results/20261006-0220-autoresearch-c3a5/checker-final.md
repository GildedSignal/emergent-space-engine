Working...
Check complete. `check.md` written with `Grade: silver`; nothing else in the run folder touched, tree restored clean, no git operations.

**Verdict summary:**

- **Reproduced everything.** Both hunks of `work/patch.diff` apply clean. Sentinel digest `c0192de9093e3d5b` identical on baseline (test-only) vs patched builds, ladder 395→237 µs (−40%, matches the claimed −40%). Kick-bench seed 1: `digest 8283cbe3…` / `replay_digest 989892a4…` identical across builds; leaver kicks 405→222 µs on this host (−45%). Suites: 52 + 44 passed, 1 pre-existing ignore.
- **Adversarial cases held.** My own 720-ladder sweep (240 q=0 shapes — extreme k, weak_quad boundary both sides, null flags, 69,528 panels) is bit-identical across builds; two seeds the author never ran (13, 21) have identical digests. I also verified the four shortcut identities structurally in `scaled.rs` (`Scalar::ONE = {1<<62,0}`, exact `isqrt`/power-of-two division), so the bits don't depend on the host.
- **Predictions provenance clean** (02:39 vs patch 02:49, evidence 02:50); the seed-7 miss was disclosed, and my seeds independently confirm the population-specific scoping — 2 of 3 seeds show no leaver gain.
- **Not gold:** 1.4× per affected event against a 10× bar; the author's self-grade is correct.
- **Named misses:** the "test fails if the knots change" claim is false as shipped (the bench prints, never asserts); no direct equivalence sweep was included; the −33% headline is seed-1-specific; one silent assumption (`f(ONE) == Scalar::ONE`) is undocumented in the risk section.
