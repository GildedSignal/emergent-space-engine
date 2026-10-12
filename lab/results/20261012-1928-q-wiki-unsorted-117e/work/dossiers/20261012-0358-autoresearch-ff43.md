# dossier — 20261012-0358-autoresearch-ff43

**Claim:** the plane's kick cost (median 50–84 µs) is 82% exact orbit recompilation whose
quadrature arithmetic already sits at the x86 floor — every bit-exact speedup I measured
is under 10% — so the next 10× must change what is compiled, not how; and the one exact
structural lever (lazy shape tables) is blocked precisely by `Orbit::state()`'s
cycle-count division, which needs the full table's exact period. Nothing adopted.

**Bottleneck:** board #1, "fewer kicks per orbit … kicks dominate the engine's cost" —
the ns-per-event half. Measured on the plane's own deterministic kick replay.

**Evidence** (commands, each < 60 s; seeds 1–2 tuned, 3–5 and rtf 1 held out):

```
cargo build --release -p xtask
/home/glmlab/lab-target-3/release/xtask universe --kick-bench --seed 1 --rtf 100 --seconds 30   # med 77–84 µs, p99 ≈ 410, n 1158
#   seeds 2–5, rtf 100: med 56.5 / 51.4 / 63.5 / 49.7 µs; rtf 1, 55 s: 49.5 / 43.5 µs; refused 0 everywhere
# phase/op profile (apply instrumentation.patch first): fit = 63.9 µs/kick = 82%;
#   Orbit::compile 48.8 µs (≈66 panels × 4 nodes of cos+products+div_word), passages 3% × 332 µs;
#   ops per kick: 595 div_word, 437 cos, 113 isqrt; 1125 shape builds, 1125 distinct ShapeKeys
cargo build --release -p emergent-space --example bench_div && target…/examples/bench_div
#   div_word shipped 26.0 ns | one-divq 21.9 | u128/u64 22.6 (all bit-equal, 200k cases)
#   isqrt shipped 89.2 ns | word-div variant 90.4 (bit-equal, 100k cases)
cargo build --release -p emergent-space --example bench_new && target…/examples/bench_new
#   OrbitShape::new 545 ns vs full bound 19.1 µs per build (weak keys, e ≈ 0.33–1)
```

Digests are bit-identical across runs, rebuilds and the instrumented binary (seed 1 rtf
100: replay `0e02bf0f3448…`, universe `eccc7f5a3d78…`), so the instrumentation itself
changed no outcome.

**Predictions:** `predictions.md` predicted 8–15% from H1 and 5–10% from H2; both
**failed** — measured 3% and 0%. This is the run's most useful surprise: the intuition
"595 divisions per kick must be optimizable" is wrong on this hardware; the shipped
base-2³² Knuth division and `__udivti3` are within 15% of a hardware `divq`. The
held-out digests/no-regression predictions held (nothing was adopted, digests stable,
no seed regressed).

**What would make it wrong:** the same phase profile measured on the M1 with its fast
`udiv` and different `mulhi` latency could re-rank the op mix; and a workload of many
co-orbital ships sharing one doll could show a different panel-count distribution than
the plane's single fleet. If 66 panels/kick were dominated by near-apoapsis refinement,
a shape representation whose panel count does not grow with eccentricity would break the
"arithmetic floor" conclusion entirely.

**Cost of adopting / not adopting:** nothing to adopt — tree restored pristine; the
deliverable is the map (which 82% to attack), the negative results (arithmetic is
closed; exact shape memo can never hit — 1125/1125 distinct), and the named blocker.
**Fit with PRINCIPLES:** "Compute only surprises" — today every kick pays the whole
orbit's table, and 90% of it is never read before the next kick discards it; the exact
blocker is the period in `state()`, so the cheap-kick road runs through restructuring
that readout (incremental cycles in the binding, or a period certificate independent of
the panel walk), not through faster arithmetic. "A failed experiment kills that
configuration, never the method": killed — div/isqrt micro-optimization, exact-shape
memoization, lazy tables under bit-exactness.

**The lens's blind spot:** a local search over the current representation can only find
floor-level wins; the 10× here requires deciding that the compiled-table-per-kick
representation itself is the cost, and re-deriving the readout contract — a design
change (one law at every scale), not an autoresearch step.
