# Dossier — 20261009-0401-autoresearch-e044

**Claim:** the geodesic compiler (`Orbit::compile`, the plane's per-kick rebind path) is
within ~3–4% of its bit-identical floor on x86-64 — the exact nested-product `cos` is a
serial-latency chain worth ~33% of per-knot cost and cannot be made cheaper without
changing the law's declared arithmetic; the only free exact win left is ~3% from native-digit
divisions, delivered as a patch, plus a measured warning: near-separatrix rebinds cost ~1 ms.

**Bottleneck:** board focus line 1, "fewer kicks per orbit ... kicks dominate the engine's
cost", sharpened on the cost side: each kick rebinds, the plane recompiles on ~99% of kicks
(board, 5 October) and the exact-key memo hits 0% on distinct kicks, so ns/compile multiplies
the engine's dominant cost. Expected gain from a successful micro-loop: 2–10x. Measured
gain: none of that size exists without changing bits. This is a negative result with a
small exact patch and one cost-concentration measurement the board lacks.

**Evidence** (all commands <= 60 s, Linux/x86 shared runner, taskset -c 2; orders of
magnitude only):

    cd lab/results/20261009-0401-autoresearch-e044/bench
    cargo build --release                       # depends on emergent-space by path
    /home/glmlab/lab-target-1/release/bench-compile tune 200 5    # bank stats + digest
    /home/glmlab/lab-target-1/release/bench-compile heldout 200 5 # corners + digest

- Baseline (main + read-only `Knot::sums` accessor for hashing): tune median 17.6 us,
  p99 94 us; held-out median 9.8 us.
- R1 (patch): four software 128-bit divisions per node in `fast_quad` replaced by guarded
  `div_word` — exact by construction (guard `n>>64 < d` implies word-sized quotient; the
  software path remains as fallback): tune median 17.1 us (−3.0%), held-out 9.4 us (−3.6%).
- Digests (FNV-1a over knot psis, all knot sums, crossings, increments, crossing times):
  tune 11806c4030d5dd5f and held-out f8c456a28a52db9a, identical baseline vs patch.
  `cargo test --release -p emergent-space`: 50/50 pass on the patched tree.
- Attribution by ablation (timing-only build): stubbing `cos`'s thirteen nested products
  cuts per-knot cost 842 -> 567 ns (cos ~33% of per-knot cost). The chain
  `s <- 1 - ((x2*s)>>62 * r)>>62` is serial per factor; the four nodes of a panel are
  independent but the chain is latency-bound, so scalar rewrite gains nothing.
- R2 (raw i128 sums) killed before landing: `Scalar::add` renormalizes through `raw()` on
  every add, so fixed-exponent accumulation is not bit-identical.
- R3 (hoist per-panel `weak_tau_term.fixed(62)`): −0.7% in interleaved A/B on min-totals,
  inside the shared machine's noise band; reverted to keep the patch minimal.
- **Cost concentration found:** the held-out corner k = HALF+1 (one quantum above the
  separatrix, periapsis 2^3..2^38 M) compiles 756 knots in ~1.0–1.24 ms — the dyadic
  ladder doing its exactness job near a near-parabolic orbit. A kick that leaves a body
  near-parabolic pays a millisecond-class rebind on a plane that rebinds ~99% of kicks.

**Predictions:** see `predictions.md` (written before the loop). What happened: P1 falsified
(gain 3%, not >= 25% — the division hypothesis was wrong; the software divisions are a
minority of node cost). P2 falsified in its favoring direction (p99 gained nothing
measurable). P3 killed on semantics before measurement (renormalizing adds). P4 held
(held-out gain 3.6% ~ tune gain 3%, digests identical). P5 held (cos untouched; ablation
confirms it is big but latency-bound, not a lever).

**What would make it wrong:** an M1 (ARM64) run where `__udivti3` costs relatively more
than on x86-64 would raise R1's gain; a harness bug in the digest (fields missed) would
invalidate the exactness claim — the digest covers every field reachable through the public
surface including the new `sums()` accessor, and the crate's own 50 tests pass. The ~1 ms
corner could be a bank artifact if real planes never rebind near-parabolic — the board's
B13 flyby work says they do (deep flybys fail there today).

**Cost of adopting:** 10 lines in `fast_quad` plus a read-only `Knot::sums()` accessor
(52-line diff, `patch.diff`); zero behaviour change by construction and by digest; no new
dependencies. Fit with PRINCIPLES: "The cheapest compute is compute not done" (the patch
deletes software-division work); "Measure before claiming" (the loop measured and reports
that no big exact lever exists); "A failed expectation is not automatically a failed
method" (R1's hypothesis was wrong; the artifact stands).

**The lens (what it may have made me miss):** autoresearch tunes one artifact with
behaviours held fixed, so it cannot see the two structural levers outside its frame:
(1) compiling less often (the quantized memo is a law change — 5 October measured it
shifting orbits — and the exact memo misses; a *certified-cheap* memo family is the real
10x question); (2) a SIMD (2–4 lane) evaluation of the four independent nodes' cos chains
via 32-bit-limb exact products could beat the latency wall bit-identically — a build-worthy
follow-up, not a tuning step. Also: single-thread bench, one CPU vendor; the M1 re-measures.
