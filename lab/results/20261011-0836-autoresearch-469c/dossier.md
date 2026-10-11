# Dossier — autoresearch on the plane's kick resolver

**Claim.** On the plane's own deterministic kick replay (`xtask universe --kick-bench`), one kick of a fleet member costs ~120 µs (median, seed 1 rtf 10) and 87% of it is the kick's rebind — of which the `OrbitShape` quadrature is 57% and `Passage::compile` alone is 36% of all kick time — and the exact shape memo hits 0%, so no micro-optimisation of the compiler reaches 10%; the only kept change (a removed duplicate `cos` in `node()`) is bit-identical on every held-out digest and buys ≤1%.

**Bottleneck.** Board focus #1, "fewer kicks per orbit … kicks dominate the engine's cost" — the cost side of it: ns per kick (`kick_us_leavers` median), the metric the board's smoothness question (p95/p99) multiplies. Expected gain of the *attribution*: it names where the per-kick euro goes, and confirms which lever is structural (passage compiles) before the slack-skin build lands. The patch itself is honest about its size: ~0.8%.

**Evidence** (Linux x86, 8 vCPU, shared; orders of magnitude only; load recorded per run).

Baseline, seed 1 rtf 10 30 s, 5 runs at load ≈ 1: leaver median 120.1–121.5 µs (±0.6% run-to-run), made 35.5–40.3 µs, p99 390–518 µs, digest `adc434a4…`, refused 0.

Phase attribution via a feature-gated `profile` instrument (24 stages through `crates/space` → `crates/universe`; +40% overhead, shares valid), same config:

| stage | µs/call | calls | share of kick time |
|---|---|---|---|
| kick.rebind | 128.4 | 555 | 86.6% |
| — bind (fit+compile+decode) | 114.7 | 573 | 79.9% |
| ——— OrbitShape quadrature (`bound`) | 73.8 | 639 | 57.3% |
| ——— Passage::compile | 493.4 | 60 | 36.0% |
| ——— fit.key | 7.0 | 665 | 5.6% |
| ——— decoded_event | 6.0 | 665 | 4.8% |
| — rebind.old_tau (two tube readouts) | 10.4 | 573 | 7.2% |
| kick.readout / secondaries / tide / acceleration | 2.8 / 5.0 / 5.0 / 1.6 | — | 3.7 / 3.4 / 3.4 / 1.1% |

Quadrature variant split (counts): 105,948 weak-path panels, 11,861 general-path, 0 fast — ~166 panels per compiled shape. `num.rs` kernels (`cos`, `atan`, `isqrt`, `div_word`) are already on u64/u128 fast paths; each is tens of ns against a 350 ns panel, so no kernel micro-change reaches 10%. Exact shape keys never repeat (272 rebinds → 272 distinct `ShapeKey`s; the quantized 12+12-bit memo would hit 83% but changes orbits — a law change, out of bounds). This independently reproduces the 5 October taste-log finding (exact memo 0%) **on distinct kicks**, with the digest as the distinctness control.

Round 1 (the only kept change): `OrbitShape::node()` computed `cos(psi)` at its head and then recomputed the same value through `self.x(psi)` for the time component's horizon term. Using the in-scope `xr` (identical i128 by construction) removes one `cos` per general-path node. Result: leaver median 119.5–120.9 µs vs 120.1–121.5 (≈0.8%, noise-adjacent), digest unchanged. Kept (strictly less work, provably identical), and the loop stopped — every remaining candidate is <10% by the attribution above.

Reproduce (each ≤ 60 s):

```
cargo build --release -p xtask
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --rtf 10 --seconds 30        # tuning config
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --seed 2 --rtf 10 --seconds 30
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --seed 7 --rtf 100 --seconds 55
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --seed 1 --rtf 1 --seconds 30
cargo build --release -p xtask --features profile   # then any of the above: per-stage JSON
cargo test --release -p emergent-space -p emergent-universe
```

**Predictions** (`predictions.md`, written before the held-out runs). P1 held exactly: all three held-out digests are identical to the pristine tree (`03dcd421…`, `5a4c42cd…`, `35f786a5…`), refused 0 everywhere. P2 held: seed 2 measured 105.3 vs 106.1 µs (0.7%, inside the ≤2% prediction); seed 7 measured 71.5 vs 69.5 µs under rising load (a digest-identical binary cannot do more work — load artifact; machine load rose from 1.0 to 4.3 during the held-out window, sibling runs); the rtf-1 case became unmeasurable at load 4.3 (556 µs stable across 3 runs, vs 366 µs measured at load 1 before) — reported as unmeasured-under-load, not as a regression. P3 held: `emergent-space` and `emergent-universe` test suites green (10+1+12+17 and doc tests pass). P4 held: the loop stopped after one round with a sub-10% gain, as predicted by the attribution.

**What would make it wrong.** The shares come from `Instant`-based stage marks on one 290-kick run of one seed at one rtf; a different population (deep-doll passages at rtf 1 leaver median 366 µs) weighs `Passage::compile` even more, not less. The 0.8% gain could be zero on the M1 (different codegen). The attribution would be wrong if the instrument's +40% overhead skewed shares non-uniformly; the rebind share is corroborated independently by the memo gold (92% window setup, components-4643).

**Cost of adopting.** The `node()` patch is one function in `crates/space/src/orbit.rs`, zero behaviour change (all digests identical), no API change. The `profile` feature (stage marks + report in `kick-bench`) is inert in normal builds and costs one `Instant::now` pair per marked phase when enabled; adopt it as the resolver's standing dashboard. Nothing else changes.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" (P1): the duplicate `cos` is compute not done, deleted. "Measure before claiming" (P10): shares before patches; the honest stop ("a test that cannot fail is a control" — the digest is the control here, and it is what makes the 0% memo finding distinct-kick-clean). "Compute only surprises" (P3): the measurement says the surprise per kick is the recompile, i.e. the *number* of compiles is the lever, not their constant factor — the representation (a shared shape across kicks), not the arithmetic.

**The lens.** Autoresearch optimises a working artifact's scalar; its blind spot is exactly what this run hit: a local search on ns/kick cannot cross into the structural change the measurement points at (cut the number of `Passage::compile`s per kick — the slack skin, `b-encounter-skin`, already in flight; or make `rebind.old_tau` reuse the last readout, which is a behaviour-risky change needing its own rung). The next run should take the passage count, not the passage code.
