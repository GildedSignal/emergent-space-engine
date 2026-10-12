# dossier — run 20261012-0036-autoresearch-e3ca (lens: autoresearch)

**Claim.** The orbit compiler's hot kernel `num::isqrt` was replaced by a provably
bit-identical f64-seeded version (−28% on the kernel, −4–6% per compile) plus one
pure CSE in `node()`, and the loop's attribution shows the remaining compile cost
is division-bound (3 `__udivti3` per quadrature node ≈ 24 ns each), with
`div_word` measured *slower* than the compiler's software 128/128 division on
x86-64 — so no ≥10× exists inside the bit-identity constraint at this node cost.

**Bottleneck.** Board #1/#3 ("kicks dominate the engine's cost"; "cheaper
events"): the plane recompiles an orbit on ~99% of kicks (taste log, 5 October),
so ns per compile is paid per kick. Expected gain: the honest ceiling found is
single-digit × , not 10× — reported as such.

**Evidence** (Linux/x86-64, Haswell i7-4790, shared runner; orders of magnitude only).
Commands, each ≤ 60 s:
```
cargo build --release -p emergent-space --example bench_compile
/home/glmlab/lab-target-2/release/examples/bench_compile 30 main     # 300 belt-like keys
/home/glmlab/lab-target-2/release/examples/bench_compile 30 heldout  # near-separatrix + far field
cargo build --release -p emergent-space --example bench_kernels
/home/glmlab/lab-target-2/release/examples/bench_kernels             # isqrt agreement + timing
cargo test --release -p emergent-space                               # 5/5 behaviour tests pass
```
Interleaved A/B of two saved binaries (`ab-numbers.txt`; the box drifts ±10%, so
cross-time comparisons are void):
- main: mean 40.1 → 38.5 µs/compile (−4.2%), p99 −6.1%;
- heldout: mean 62.0 → 58.7 µs/compile (−5.7%), p99 −5.1%;
- output hash identical on both corpora (main `7932a7d0…780f2`, heldout `1d3ac911…17e2`),
  computed over the full Debug dump of every compiled orbit (knots, crossings, increments);
- `isqrt` kernel: 97.5 → 65.3 ns, agreement on 2.2×10⁶ adversarial inputs of all widths;
- `cargo test -p emergent-space`: 5/5, including `every_cycle_is_the_compiled_one`.

Attribution (temporary stage counters, removed): quadrature ≈ 70% of compile
(≈225 ns per GL node in `fast_quad`), band cuts ≈ 15% (≈190 ns), bookkeeping ≈ 15%.

**Predictions** (`predictions.md`, written before the decisive run): bit-identity
HELD exactly; the speed predictions FAILED in magnitude (predicted 10–20% heldout
mean and 15–25% p99, measured 5.7% and 5.1%; predicted cut −20%, measured −11%).
Reason: most nodes take the `word_root` u64 sqrt path (delta ≥ 2⁻²), so the 126-bit
isqrt is rarer than estimated. The stop rule fired after three sub-10% rounds.

**What would make it wrong.** The margin proof (`est + (est>>40) + 16 ≥ r` for
x ≥ 2⁴⁰, then the unchanged Newton-from-above descent) fails on some untested
input width; the 2.2×10⁶-sample agreement and the crate's tests are evidence, not
proof of the f64 bound. Timing conclusions are this box only (cloud timings are
orders of magnitude; the integrator re-measures on the M1, where `__udivti3` is
also software but `div_word`'s two hardware `div`s may win — re-measure before
trusting the div_word rejection there).

**Cost of adoption.** One 18-line change in `num.rs` (seed only; descent, rounding
and every output bit unchanged) and a 4-line CSE in `orbit.rs::node` (the duplicate
`cos` evaluation). Patch = `git diff` of those two files; benches are
`crates/space/examples/bench_{compile,kernels}.rs` (copies in this folder). No API,
law id, or stored-value change — `LAW_ID` need not move because outputs are
bit-identical (the memo-safety rule "never reuse a memo across law versions" is
respected: same bits, same law).

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" (P1): the seed
was compute not needed. "an error type over error size" / integers decide: the f64
value only *chooses the starting point* of an integer descent that provably returns
the same floor — floats explore, integers decide, and the 2.2×10⁶-case agreement
plus test suite check it. "Measure before claiming": every keep/revert above is an
interleaved A/B, and the failed magnitude predictions are reported as failed.

**The lens (what it may have made me miss).** A local search inside bit-identity
cannot touch panel count, `CAP`, or the `word_root` threshold — all law. The
structural change that would beat my best: (a) prove the Q31 `word_root` floor
exact enough at delta ≥ 2³⁰ (kills the 126-bit isqrt entirely for all fast shapes),
or (b) batch the four independent GL nodes of a panel onto SIMD/NEON lanes doing
the identical integer ops (bits preserved per lane), or (c) attack cadence instead
of node cost — the board already says the lever is cadence, and this run's
attribution agrees: per-node cost is three divisions, and divisions do not shrink
without changing the law.

**Grade asked for:** lead/silver at best — real, reproduced, bit-identical, but a
5% move on a board bottleneck, not a 10×. The reusable products are the attribution
(dead generic path: bound keys cannot reach delta < 2³⁰ ≈ within 2⁻³² of the
separatrix), the div_word-on-x86 measurement, and the two benches.
