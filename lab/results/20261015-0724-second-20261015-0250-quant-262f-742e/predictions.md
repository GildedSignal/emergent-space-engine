# Predictions (written before the decisive timing run)

Question: the checker's one experiment to gold — one Rust arm, one box, three
timings at true belt keys: (a) the shipped compile per promotion, (b) a native
scalar closed-readout loop, (c) the native batched loop including per-body
coefficient setup. This turns 262f's ≈4 µs projection into a measurement,
evaluates prediction #4's kill rule (batched/scalar ≥ 2×), and prices the win
against the shipped compile on the same instrument.

Belt keys are generated the shipped way (scenario.rs ladder_ship belt lane):
a uniform in [2,3) AU at 2⁻⁸ root units, e Rayleigh(0.07) in Q48 re-drawn at
0.4, p = a(1−e) at 2⁻⁸, AU = 101,300,000 root units. The same bodies feed all
three arms (the closed arms take the f64 copy of each key).

Cases I have NOT tuned on (predictions written before any timing):

1. **Kernels on this box** (i7-4790, AVX2/FMA, paper-verbatim Carlson with
   tail): rf 40–80 ns, rj 120–220 ns per scalar call (de99 measured 50/152 on
   comparable x86).
2. **Shipped compile (a)** — `Orbit::compile` at belt keys (weak branch: the
   shape key carries compactness ZERO, so panels take `weak_quad`): **8–30 µs
   per promotion**. Belt e ≤ 0.4 sits at the bottom of cd6e's 5.2–255.8 µs
   compile range; a669's ~30 µs/kick compile anchor is the upper edge.
3. **Native scalar promotion (b)** (lean 1-t-eval/iter Newton, per-body GE
   coefficient solves + cold start + final adv/τ read): **2.5–5.5 µs**.
   Composition: ~8 t-reads × (1 rf + 3 rj) ≈ 8 × 510 ns ≈ 4 µs.
4. **Batched (c)**: ufunc-style SoA pass **2.5–4.5 µs** (kernels stay
   data-dependent; the gain is layout/streaming only); 4-wide AVX2 masked
   Carlson **0.9–2.0 µs**. **Kill rule (262f's #4):** if the best batched arm
   is < 2× the native scalar arm, the vectorization does not survive the
   duplication loops' divergence and the batched route is dead — report that,
   do not tune the width to rescue it. I predict the AVX2 arm clears 2×
   (belt lanes have nearly identical Carlson arguments; convergence is
   uniform).
5. **Value**: every closed channel — scalar, SoA batch, AVX2 batch — agrees
   with adaptive Simpson of the shipped `node()` integrands to ≤ 1e-15
   relative on t and τ at belt keys; the three closed arms agree with each
   other to ≤ 2e-16 (this is the value-check that would have caught 262f's
   factor-2 slip; it runs before any timing is trusted). Advance stays
   floored near ~1e-8 at belt q — 1/q-amplified f64 cancellation in both
   instruments (checker-established, 40-dps mpmath proof; not re-litigated).
6. **Newton at belt**: 6 iterations, median = worst (as 262f's numpy). Slope
   verified against finite differences at every verification point.
7. **Wider grid** (the promise 262f dropped): e ∈ {0.001..0.999}, p ∈ {7..1e8},
   u → π/2−1e-3: closed vs Simpson ≤ 1e-6 on t/τ at every corner (the checker
   already saw ≤ 4.4e-13); Newton iteration count at e = 0.999 degrades
   (≥ 12, possibly hitting a 60 cap) — belt-scoped as 262f claimed.
8. **Size**: the open direction asked 10⁷ promotions; I run 10⁷ (ten 10⁶
   chunks, < 2 GB peak). Timing spread over 3 repeats, median reported, all
   repeats printed.

Gold criterion (the checker's): if the best native batched arm holds ≤ ~5 µs
at belt keys AND ≥ 2× scalar AND ≥ 6× the shipped compile measured on this
same arm, the f64-layer adoption case is complete. If the shipped compile at
belt keys comes in under ~6× the batched read (i.e. the compile is cheaper
here than the record's anchors), the honest result is a refutation of the
adoption case's magnitude — that is the other decisive outcome. Not
predicted, decided by the run.
