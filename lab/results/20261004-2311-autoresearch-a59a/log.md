# Autoresearch log — crates/space kick path (rebind fit + cycle compile)

Artifact: `crates/space` (`Orbit::compile` + `Rebinding::from_state` = the 15 µs
"rebinding fit and compile" of the engine's 29 µs kick, measured by the
integrator on the plane). Metric: ns per compile / per from_state, min of
repeated back-to-back runs, interleaved A/B against a stock binary. Behaviour
gate: FNV-1a golden hashes over every output bit (knots, period, advance,
rebinding fields), identical between builds, plus the crate's test suite.

Machine noise lesson (round 0): timing right after a build is inflated up to
+25% by build/cache effects on this shared 2-vCPU box; every keep/revert
decision below uses min of ≥3 back-to-back binary runs, interleaved A/B.

| # | Hypothesis | Change | Metric (compile, tuning corpus) | Verdict |
|---|---|---|---|---|
| 0 | — | baseline | 19648 ns | — |
| attribution | where does compile go? | stage timers (bias-corrected) | per compile: node math ≈12.5 µs (cos ≈5.9 serial-chained, isqrt ≈1.9, 4×u128 div ≈1.5), panel glue ≈4.5, cut/bands ≈2.7, new/loop ≈1 | reverted (instrumentation) |
| 1 | per-node `u64::isqrt` (Newton, hw divs) is a large node cost | `num::isqrt_word`: f64 sqrt + ≤1-unit correction, exact floor, call site guarded to x < 2^62 | 19648 → 18333 ns (−6.7%), hashes identical | **KEPT** |
| 2 | knots Vec growth ladder (≈5 reallocs/compile) costs | pre-count band edges, `reserve` once | 18333 → ~18300 ns (within noise) | reverted (no gain) |
| 3 | u128 `/` divisions (4/node) dominate | guarded `div_word` swap (div_word vs LLVM's u128/u128 lowering) | micro: div_word 4.8 ns vs `/` 3.6 ns; in situ +18% | reverted (slower) |
| 3b | same, cheaper: attribute first | dummy-out all 4 divisions | 19648 → 18588 (−5% only) | reverted (attribution: divisions are 5%, not 40% — killed hypothesis 3) |
| 4 | 124-bit `num::isqrt` (cut, 2.7 µs) improvable | f64-seeded Newton | wrong under Newton-from-below (off by 147 on 1.37e37); correct fix saves ~15% of isqrt only ≈ 1.5% compile | abandoned (not worth the risk) |
| 5 | cos (5.9 µs, 32%) reducible | none found: 13-level nested product is the bit-exact spec; serial mulx latency chain, no exact algebraic shortcut | — | not attempted further |

Stop: rounds 2, 3, 4 all < 10% (≈0%, negative, abandoned) → stop per lens.

Final, interleaved A/B (min of 5–6 runs each):
- tuning corpus compile: 19546 → 18333 ns (**−6.2%**); rebind 28228 → ~26800 (−4-5%)
- held-out corpus (HELDOUT=1): compile 22781 → 21692 (**−4.8%**); rebind 31739 → 30557 (−3.7%)
- hashes identical on both corpora (tuning 39bc6467da11a6c3 / 07d70774d7390e51; held-out 93ace10682a4dc06 / 98c5868f71207f1e); refusals identical (22/28).

The one idea that carried the gain: **attribute before optimizing — the
obvious suspect (128-bit division) was 5% of the cost; the seeded exact floor
sqrt was the real, safe win.** Expected on the M1: same order (one hw div
sequence per node replaced by an fsqrt + branch).
