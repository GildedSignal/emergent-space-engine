# log.md — 20261010-2220-autoresearch-2fe1

Artifact: `crates/space` (the motion law's orbit compiler + per-kick inverse).
Metrics: ns/compile (`lab_bench compile-main`), ns/rebind (`lab_bench rebind`).
Machine: shared 8-vCPU Linux runner (i7-4790 class), release profile. Medians of 7 rounds.
Behaviour guard: output checksums in all four bench modes + `cargo test -p emergent-space`.

Baselines (before any change):
- compile-main 31,185 ns/event (ck 0x2b346ac433041c73, 27.8 knots/orbit)
- compile-deep 81,608 ns/event (ck 0xfbbe78bcc0532588, 60.8 knots/orbit) [held out]
- compile-circ  5,741 ns/event (ck 0x40d632244d5a003e, 6.0 knots/orbit) [held out]
- rebind       59,962 ns/event (ck 0x855ba4e402a6c53c, 195/512 ok) [held out]
- component microbench: u64::isqrt 22.3 ns; crate u128 isqrt 86.8 ns; u128/u128 div 22 ns;
  i128/i128 div 26 ns; div_word 20 ns; u64/u64 div 6.7 ns.

| # | Hypothesis | Change | compile-main | rebind | Verdict |
|---|---|---|---|---|---|
| R1 | std `u64::isqrt` (software Newton, 22.3 ns) dominates the per-node cost of `fast_quad`'s word root and seeds the u128 isqrt | f64-seeded exact-fixup `isqrt64` (identical bits by construction) in `num.rs`; used at `orbit.rs` word-root and as the u128 seed | 27,251 (−12.6%) | 52,693 (−12.1%) | **kept** |
| R2 | `append()` pays 3 i128 divisions per panel even when n==1 | n==1 fast path + span hoist (bit-identical: n=1 ⇒ a=lo, b=hi) | 26,742 (−1.9%) | — | kept |
| R3 | `fit_key`'s bisection `poly` recomputes z² and 2q per iteration (~63 iters) | hoist `twoq`, reuse `z2` | — | 51,651 (−2.0%) | kept |
| R4 | loop-invariant hoist in `fast_quad` + u64-divisor division in `ratio_sqrt` | hoist + rewritten division | 27,530 (+2.6%, 3× re-measured) | — | **reverted** |

Stop: R2, R3, R4 all < 10% ⇒ three consecutive rounds under threshold. Stopped.

Final (tuned set): compile-main 26,742–26,898 ns (−14% vs baseline); rebind 51,651–53,277 (−11…−14%).
Held-out (run once, after the loop): deep 71,687 (−12.2%), circ 5,305 (−7.6%), rebind 53,277 (−11.1%).
All checksums identical to baseline; `cargo test -p emergent-space` 50/50 green.

The one idea that carried most of the gain: exact integer sqrt does not need an integer
division chain — an IEEE-exact f64 sqrt seed plus monotone integer fixup returns the same
floor(sqrt) bits for a fraction of the cost. Everything else was <2%.
