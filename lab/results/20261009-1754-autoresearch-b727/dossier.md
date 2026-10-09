# Dossier — run 20261009-1754-autoresearch-b727 (lens: autoresearch)

**Claim:** the law pipeline's kick-rebuild cost (`crates/space`) is not division-,
allocation- or normalization-bound on x86-64 — five bit-identical kernel changes buy
only 2–13% (shape-dependent), so the lever for the engine's per-kick cost stays cadence
or a representation change, not micro-optimization of the exact paths.

**Bottleneck:** board item 1, "fewer kicks per orbit / kicks dominate the engine's cost";
the plane recompiles an orbit on ~99% of kicks (taste log, 5 Oct). Metric: ns per kick
rebuild (`Rebinding::from_state` + `Orbit::compile` + readout) on an 8-shape bank
(circular/weak/moderate/eccentric/near-separatrix/strong-field/far), behaviour held
bit-identical by full-output digests plus the crates' own test suites. Expected gain when
I started: 1.5–3× (four `__udivti3`-class divisions per node measured at 22.5 ns vs
`div_word`'s 1.6 ns). Real gain: ≤2% on the bank. The premise was wrong at the
representation level: weak-field shapes quantize compactness to zero and take
`weak_quad`, which already uses `div_word`; the multiword divisions I replaced live on
the strong-field path only.

**Evidence** (shared Linux x86-64 i7-4790, ±5–8% noise between batches; commands ≤ 60 s):

```
cargo build --release -p emergent-universe --example autoresearch
/home/glmlab/lab-target-1/release/examples/autoresearch 400 all      # stages + digest
/home/glmlab/lab-target-1/release/examples/autoresearch 200 heldout  # held-out bank
cargo test --release -p emergent-space -p emergent-universe          # all green
```

- Bank (min over repeated runs): `from_state` 18.2→17.7 µs (−3%), `compile` 31.4→30.9 µs
  (−2%), state-stage 34.5→34.0 µs (−1.5%). At or below noise.
- Held-out (single runs, `heldout_before.txt` vs after): circular compile −13%
  (3813→3325 ns, confirmed min-of-N), weak-e −8..−10%, strong-field flat
  (17.7–18.0 vs 18.7 µs min-of-N), near-separatrix flat (panel-count-bound: e 0.9 costs
  47 µs over 68 panels).
- Cycle profile (instrumented, `#[cfg(feature="profile")]`, now stripped): quad ≈ node ≈
  read ≈ 1500 cycles/call uniformly; per-op microbench: `Scalar::add` 14.2 ns,
  `sqrt` 107 ns, `div` 29 ns chained, native u128/u128 division 22.5 ns vs `div_word`
  1.6 ns. Diffuse cost spread over ~100 normalized-dyadic ops per rebuild, no single
  hotspot above ~15%.

**Predictions** (`predictions.md`, written before the loop): digest invariance held
(after two caught breaks, below); H1's 15–35% on weak cases did NOT hold (wrong path —
weak shapes never reach `fast_quad`); strong-field gain from H1 flat; near-separatrix
panel-bound as predicted; stop rule fired after three rounds < 10%.

**What would make it wrong:** timings on the actual M1 (different division costs, this is
Haswell x86-64); a workload dominated by strong-field shapes (there `fast_quad`'s
`div_exact` replacement should matter most, but I could not resolve it above noise here);
the bank's shapes may not represent the plane's live kick distribution.

**Cost of adopting:** trivial — 223-line patch, all bit-identical, whole test suite
green (`lattice-metal`'s fuzz failure is pre-existing on this host: "no Metal device",
reproduced on the clean tree). No gate touches, no API change.

**Fit with PRINCIPLES:** "The cheapest compute is compute not done" — the honest reading
of this run is via negativa: stop polishing the exact kernel (already near its floor),
the 10× lives in cadence (fewer rebuilds) or in the representation (panel count is the
accuracy contract; a cheaper per-panel law changes bits and needs re-gating). Also
"measure before claiming": two of my three rounds would have claimed gains a noisy
single run cannot support.

**Disclosed breaks (both caught, both fixed, final state bit-identical):**
1. My H1 edit accidentally deleted `sum[0] += w·g1` (the advance integral) from
   `fast_quad`. The tuning digest (period only) still matched; the held-out digest
   (hashes advance) caught it. Lesson: a digest must hash every observable, not a sink.
2. My H2 same-sign fast `add` missed the `h + (l>>gap) ≥ 2^63` carry (caught by
   `scaled`'s tests) and then the `gap == 64` masked-shift case (`l >> 64u32` = `l >> 0`
   in release; caught by universe's lorentz test, which my 20M random differential
   missed because an LCG's low bits made its exponent stream periodic). Final `add`
   verified by a splitmix-based 30M-case differential (0 mismatches) and all tests.
   Lesson: an LCG is not a test generator; and the crate's cross-crate tests are the
   real behaviour net.

**The lens (what it may have made me miss):** autoresearch optimizes what exists. The
structural change that would beat my best: cache the readout's Newton solve as a
panel-local inverse-time table built during `append` (the derivative is already computed
at knot edges), or merge `from_state`'s `at_radius` + `decoded_event` double readout —
both change bits, i.e. they are law changes to propose to the integrator, not
optimizations. Also missed: I did not measure the plane end-to-end (`xtask universe`)
— the bank is a proxy; the checker should run one plane scenario for sanity.

**Grade suggestion:** lead. Real, bit-identical, no regression, but the bank metric moved
≤3% — three consecutive rounds under 10% stopped the loop, and nothing here deletes a
component or kills a premise except the negative one stated in the claim, which is worth
exactly one board line: "kernel micro-optimization exhausted; per-kick cost is
representation-bound."

Files: `patch.diff` (the five changes), `autoresearch.rs` (harness, also left in
`crates/universe/examples/`), `log.md` (loop log), `predictions.md`,
`heldout_before.txt`, `ho5check.rs` (strong-field/circular min-of-N check).
