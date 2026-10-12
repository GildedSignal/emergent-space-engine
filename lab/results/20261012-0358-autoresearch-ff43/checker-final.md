Working...
Check complete. `check.md` written: **Grade: silver**.

**What I did (30 min, tree left pristine):**

1. **Baseline reproduced** with the shipped binary: digests bit-identical (`eccc7f5a…` / `0e02bf0f…`), refused 0, n 1158, median 78.0 vs author's 77.0 µs.
2. **All six held-out cases** (seeds 2–5 rtf 100, seeds 1/3 rtf 1): digests and sample counts bit-identical, medians within noise.
3. **Independent re-instrumentation** — the author's `instrumentation.patch` doesn't ship the two `prof.rs` modules it references, so I wrote my own from the call sites: op counts reproduce exactly (595.0 div_word, 437.6 cos, 112.9 isqrt per kick), 68 panels/build, rebind = 84–90% of kick time, digests unchanged under instrumentation.
4. **Microbenches reproduce**: div 26.5→21.7 ns (3.6% max, bit-equal on 200k operands), isqrt 0%, `OrbitShape::new` 528 ns vs `bound` 19.3 µs.
5. **Blocker verified in source**: `orbit.rs:630-639` — `state()` derives `cycles` from the full table's last-knot period, so lazy tables change bits, as claimed.
6. **Novelty checked**: the exact-memo negative is already pinned in main (`dbd4add0`), and the structural conclusion re-confirms the 6 Oct gold's "slack skin is the lever".

**Silver, not gold:** everything regenerable reproduces, but the headline "fit = 63.9 µs = 82%" is not derivable from the saved record (empty `phases`, overlapping counters whose 117 ms sum exceeds the 93 ms total kick time — `state_reads` nests inside `shape_bound`), the patch can't rebuild the profile as shipped, and the strategic conclusion is confirmatory. The gold experiment is named: bind-maintained cycle counts (or a period certificate) that keep digests bit-identical and delete the per-kick quadrature walk.
