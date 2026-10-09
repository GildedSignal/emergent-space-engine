# Loop log (autoresearch b727): artifact `crates/space` law pipeline, metric = ns per kick
rebuild (`from_state`/`compile`/readout) on an 8-shape tuning bank, behaviour constraint =
bit-identical digests + full crate test suite.

Machine: shared Linux x86-64 (i7-4790 Haswell), noise ±5-8% across batches; min-of-N used
where noted. Baseline (single run, 400 iters): from_state 18.2 µs, compile 31.4 µs,
state-stage 34.5 µs (includes a compile per read: harness artifact, see R0).

| # | Hypothesis | Change | Metric (bank) | Kept? |
|---|---|---|---|---|
| R0 | profile: where does time go | cycle counters (profile feature) | quad≈node≈read≈1500 cyc/call uniform; Scalar add 14.2 ns, sqrt 107 ns, div 29 ns chained; native u128/u128 div 22.5 ns vs div_word 1.6 ns | instrumented, then stripped |
| H1 | fast_quad's 4 multiword u128/u128 divisions per node dominate | `div_exact` wrapper → div_word with legality guards, fallback = original | flat (≤2%, noise). Diagnosis: weak-field shapes quantize compactness to 0 → take weak_quad, not fast_quad. Only strong-field shapes (1/8 bank) reach it | KEPT (bit-identical, strong-field only; no regression) |
| — | digest check caught a real break | my H1 edit accidentally deleted `sum[0] += w*g1` (advance integral). Tuning digest (period only) still matched; HELD-OUT digest (hashes advance) caught it. Restored; both digests match | lesson recorded in dossier | fixed |
| H2 | Scalar::add (i128 variable shifts → libcalls + re-normalize, ~50 cy) dominates the ~1500 cyc/call uniformity | same-sign fast path with u64 arithmetic (proved: normalized operands, no cancellation, ≤1 carry bit), opposite signs keep original path. First version WRONG (missed the h+l>>gap ≥ 2^63 carry; 2 unit tests caught it), fixed with carry branch + exponent-overflow guard | flat (≤3%, noise). LLVM already pipelines the i128 shifts in-context; the 14 ns microbench was a latency chain, not throughput | KEPT (bit-identical, all 10+ tests pass) |
| H3 | sqrt (107 ns) + per-call recomputed half/period Scalars + Vec realloc churn | (a) isqrt Newton division → div_word (divisor always ≤ u64 after first step); (b) half_time/full_time cached in Orbit (from_shape/newtonian), used by at_phase/state; (c) knots/crossings capacity estimate 16·log2(u_p/u_a) | bank flat (2-3%); held-out single runs: circular compile −13% (3813→3325 min-of-N), weak-e −8-10%, strong field flat (17.7-18.0 vs 18.7 µs min-of-N) | KEPT (bit-identical, no regression) |

Stop rule: three consecutive rounds < 10% on the bank metric → STOPPED after H3.

Final min-of-N (300 iters ×3): from_state 17.7 µs (−3%), compile 30.9 µs (−2%),
state-stage 34.0 µs (−1.5%). All within or barely above noise on this shared machine;
shape-specific gains are real but small (circular −13%, weak-e −8-10%).

Digests: tuning `1f057b8337399608ffa4224da12d3c95`, held-out `854b4b514191ee6db8ad74db1e6056e3`
— both identical before and after every kept change.

## Post-stop corrections (disclosed in dossier)

- H2 final: two bugs found and fixed after the loop's stop point —
  (1) same-sign carry `h + (l>>gap) >= 2^63` (scaled's unit tests), (2) `gap == 64`
  masked-shift release semantics `l >> 64u32 == l >> 0` (universe's lorentz test; my
  20M LCG-random differential was blind because LCG low bits made its exponents
  periodic). Fixed; splitmix differential 30M cases: 0 mismatches; all space+universe
  tests green; both digests unchanged from baseline.
- The `lattice-metal` fuzz failure on this host is pre-existing (no Metal device;
  reproduced on the clean tree).
