# Dossier — the kick's rebind+compile cost, attributed and shaved

## Claim

The engine's per-kick "rebinding fit and compile" (the 15 µs of the measured
29 µs kick, board bottleneck "kicks dominate the engine's cost") is dominated
by `Orbit::compile`'s quadrature nodes, whose cost order is **cos (≈32% of
compile) > panel glue (≈24%) > square roots (≈10%) > 128-bit divisions
(≈8%)**, and one exact change (f64-seeded floor sqrt) cuts compile by **6.2%
on the tuning corpus and 4.8% held-out, with every output bit identical**.

## Bottleneck

Board focus line 1/3 ("fewer kicks per orbit… kicks dominate"; "cheaper
events"). The gain is a fraction, not an order of magnitude — the value here is
the attribution: it kills the folk belief that the integer divisions are the
cost, and it sizes the three real levers for whoever attacks this next. It
deletes nothing yet; it redirects.

## Evidence

Cloud box (Linux, 2 vCPU EPYC 7763, shared — timings are order-of-magnitude;
integrator re-measures on the M1). Reproduce (each ≤ 60 s; min of ≥3
back-to-back runs; `HELDOUT=1` swaps in the never-tuned corpus p ∈
{6,7,12,700,9000,262144,1048576}, e ∈ {0.05,0.2,0.8,0.95}):

```
cargo build --release -p emergent-space --example rebind_bench
target/release/examples/rebind_bench        # tuning corpus: hashes + ns
HELDOUT=1 target/release/examples/rebind_bench
cargo test --release -p emergent-space      # ~65 s: 50 tests, all pass
```

Interleaved A/B, stock vs changed (min of 5–6 runs):

| corpus | metric | stock | changed | Δ |
|---|---|---|---|---|
| tuning (66 keys) | compile | 19546 ns | 18333 ns | **−6.2%** |
| tuning (132 states) | from_state | 28228 ns | ≈26800 ns | −4.5% |
| held-out (22 keys) | compile | 22781 ns | 21692 ns | **−4.8%** |
| held-out (44 states) | from_state | 31739 ns | 30557 ns | −3.7% |

Bit identity (behaviour gate): FNV-1a hashes over every output bit — tuning
`39bc6467da11a6c3`/`07d70774d7390e51`, held-out `93ace10682a4dc06`/
`98c5868f71207f1e` — identical stock vs changed; same 22/28 held-out refusals;
the crate's 50 tests pass. Attribution numbers and the kept/reverted table are
in `log.md`; the kept change is 18 lines (`num::isqrt_word` + one call site in
`fast_quad`).

## Predictions

Written before the decisive run in `predictions.md`. All five held: held-out
hashes identical, latency −4.8% (predicted band 2–8%), refusals unchanged,
test suite green, and the risk clause (any bit mismatch kills the change) was
never triggered.

## What would make it wrong, adoption cost, fit

Wrong if: a denominator ≥ 2^62 ever reaches `isqrt_word`'s call site (it cannot
today: `denominator < ONE` and `word_root` bounds it below by 2^60 — the guard
is structural, not numeric luck), or if the M1's f64 sqrt were not correctly
rounded (it is, IEEE). Adoption cost: 18 lines, no API change, no memory
change, zero behavioural surface. Fit: "The cheapest compute is compute not
done. Delete before optimizing" (§1) and "Floats may explore; only integers
decide canonical outcomes" (lab rules) — the f64 only proposes; integer
corrections decide, and the hashes prove it.

## The lens (what autoresearch may have missed)

Greedy micro-search stops at local optima; three of my four rounds gained
<10% and stopped honestly. What would beat this best by 10×, in order:
(1) **stop recompiling per kick** — `from_state` compiles a fresh `OrbitShape`
for every kick although shapes depend only on (k, q); routing kicks through the
crate's own `QuantizedMemo` (12-bit shapes) turns most rebinds into scale-only
rebinds (compile is 65% of from_state; small kicks keep the quantized shape).
That is an engine-side change (`crates/universe` calls `Rebinding::from_state`
directly), not a space-crate one — the integrator owns that door.
(2) **cos is 32% of compile and latency-chained** — the 13-level nested product
is the bit-exact spec; beating it needs either a table with exact correction
or a pair-SIMD formulation, i.e. new proofs, not micro-edits.
(3) the fit's 63-iteration bisection pays full `Scalar` polynomial evaluations
for every q > 2^-18 because `root_witness` refuses strong fields; extending its
concavity certificate (P'' = −2 + 6qz < 0 fails only for q·z > 1/3) would cut
the fit half. None of these were attempted: one change at a time, and my 60
minutes were spent proving where the cost actually lives.
