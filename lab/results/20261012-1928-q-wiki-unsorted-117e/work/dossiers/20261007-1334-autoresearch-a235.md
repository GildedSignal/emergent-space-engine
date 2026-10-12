# Dossier — 20261007-1334-autoresearch-a235

## Claim

The plane's per-kick recompile (`Rebinding::from_state`, 99% of it `Orbit::compile`) gets
12–16% cheaper on a shared Linux box with a 17-line patch to `crates/space/src/orbit.rs`,
bit-identical by construction and by digest, tests green.

## Bottleneck

Board item 1: "kicks dominate the engine's cost", and the plane recompiles an orbit on ~99% of
kicks (5 Oct taste log; the exact-key memo hits 0% on distinct kicks). So ns per compile is the
engine's dominant per-kick cost. Expected gain here is a constant factor, not an order of
magnitude — the panel count (~16·log₂((1+e)/(1−e)) Gauss–Legendre panels per outbound half) is the
law's accuracy contract, and the per-panel rounding sequence is part of the bits. What it deletes:
nothing structural; it widens the per-kick budget by 1.19×.

## Evidence

Harness: `bench/` (this folder) — a stand-alone crate timing `Rebinding::from_state` on integer
states across radii 8..2^30 M and e 0..0.85, both regimes (weak belt `weak_quad`, strong
`fast_quad`; `node()` never runs in these corpora). Digest = FNV-1a over every observable the
plane reads (increments, periods, knots/crossings, states at t/3 and 2t/3, residual, angles).

Quiet-window, same-minute stash A/B (pinned core, min-of-5, ≥2 runs each, spread <1%):

| corpus | baseline median | final median | Δ |
|---|---|---|---|
| tuning (72 states) | 47.1 µs | 39.5–39.9 µs | **−16%** |
| held-out (64 states) | 49.8–50.0 µs | 43.7 µs | **−12.3%** |

Digests unchanged (`b3b2412da6e85f12` tuning, `1c32d7508ad8ef47` held-out).
`cargo test --release -p emergent-space`: 50 passed, 0 failed.

Reproduce: `cd lab/results/20261007-1334-autoresearch-a235/bench && CARGO_TARGET_DIR=/tmp/ar-target
cargo run --release -- tuning 40` (and `heldout 40`); A/B by `git stash`/`git stash pop` of
`patch.diff`, rebuilding between. Each run ≤ 10 s.

Attribution (temporary counters, reverted): ~85% of compile is the quadrature panels, ~17% the
band-cut loop. Micro: cos 41 ns/call (4 per panel), `div_word` 33 ns, u128÷u128 (__udivti3)
~50–60 ns — `fast_quad` had four of those per node; that is what the patch removes (guarded
`wdiv`: exact `div_word` when `n>>64 < d`, wide division otherwise). R1 (dedup of a repeated
`cos` in `node()`) is strictly less work but `node()` is off these paths; part of its measured
−10.7% is code-layout luck and is reported as such.

## Predictions

`predictions.md` was written before the decisive experiments. Held: digests unchanged, tests
green, held-out gain within ±30% of the tuning gain (−12.3% vs −16%). Missed: the cumulative
band (1.25–1.5× predicted, 1.14–1.19× measured) and H2 (Scalar churn was not the cost — R2
neutral, reverted). H1's mechanism was wrong (node() never runs here). One measurement lesson
recorded in the log: under heavy window load the same A/B compresses to −2% — division latency
is what contention hides; the quiet-window number is the one the player sees.

## What would make it wrong

The `wdiv` guard is the only correctness surface: if any fast_quad divisor ever exceeds u64 or
the precondition check were dropped, bits would change silently. It cannot here (root, x,
horizon ≤ 2^62, checked positive before use), and the digest pins it. The gain is
hardware-bound (Haswell x86 shared runner): the integrator re-measures on the M1, where 128-bit
division costs differ. If the plane's kicks ever stop recompiling (the wired memo/jet), this
budget line disappears and the patch is moot.

## Cost of adoption

One file, 17 insertions, 9 deletions (`patch.diff`); no API change, no new invariants, the
exactness argument is one line per division. Review: minutes.

## Fit with PRINCIPLES

- "Floats may explore; only integers decide canonical outcomes" — the patch keeps every integer
  path integer; quotients are identical by construction.
- "Compute only surprises" (§3) / "the cheapest compute is compute not done" (§1): the win is
  deleting redundant 128-bit hardware divisions the representation never needed.
- "Measure before claiming" (§10): stash A/B in the same clock window, both load regimes reported.

## The lens (what it may have missed)

A local search finds local optima. The structural change that beats this best: the panel loop is
serial per shape, but kicks are independent across bodies — the plane already has threads, and
compile is a pure function, so parallelism across kicks (not within) is the 8× this box offers.
Second: cos (41 ns × 4 per panel) is defined as a 13-factor nested integer series; a
representation whose node weights share sub-expressions across panels would cut it, but any
re-expression changes bits, i.e. it is a law change, not an optimization. Third, unexplored:
the band-cut loop recomputes `ratio_sqrt` (94–104 ns) per band from scratch; adjacent bands
share most bits.

## Grade suggestion

Silver: real, reproduced, bit-identical, cheap to adopt — but a constant factor (1.19×) on one
cost line, not a 10× board move; the next run picks up cross-kick parallelism or the cos
representation if the integrator wants either.
