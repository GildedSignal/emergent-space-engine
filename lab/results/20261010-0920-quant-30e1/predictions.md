# predictions.md — run 20261010-0920-quant-30e1

Written BEFORE the decisive instrumented runs. Baselines already measured (unmodified
build, seeds 1/2/7, `--rtf 100 --members 400 --seconds 10`): per-kick median 77–86 µs,
p99 ~370 µs, exact memo hit rate 0% (every fired kick rebinds a fresh exact cycle
shape), quantized 12+12-bit key would hit ~95.5–96.4%.

## What I will measure

Per-kick budget of `step::process` on a Kick item (the engine's dominant event), by
instrumenting `crates/space`'s `Scalar` ops (add/mul/div/sqrt), `isqrt` Newton
iterations, `cbrt` iterations and `next_periapsis`/`next_exit` bisection iterations,
plus wall time, split across the kick's five stages (readout, forces, sigma-delta,
fit=`rebind`, plan). Determinism: the replay digest must equal the baseline digest per
seed, proving the counters watched identical work.

## Predictions (cases not tuned on)

- **P1 attribution:** the fit (`rebind`) is the over-share stage: > 50% of per-kick
  Scalar ops and > 40% of per-kick time. Rationale: exact_hit_rate 0% ⇒ every fired
  kick refits a trajectory; lab components-4643 measured "92% of per-kick evals are
  window setup".
- **P2 mix:** mul is the top Scalar class, > 45% of ops; div+sqrt combined < 20%.
- **P3 iteration tail:** isqrt + cbrt + bisection iterations are < 15% of ops but have
  data-dependent trip counts ⇒ a within-kick tail contributor, not the median driver.
- **P4 no microarchitectural 10×:** the per-kick working set is L1-resident (records +
  one trajectory); no layout or branch fix alone buys 10×. The only ≥10× door on the
  median kick is paying fewer fits — the re-anchored quantized jet already priced in
  law.md at ~0.05 compiles/kick — on top of (multiplying with) the slack skin.
- **P5 held-out stability:** on seeds 11 and 23 (not used for any tuning here), the
  stage shares stay within ±5 percentage points of seed 1's.

## Kill criteria

- If no stage holds > 30% of time and ops, the "one stage over its share" premise is
  dead: the budget is flat and the kick is not compile-dominated. Report that.
- If instrumented wall time diverges from baseline by > 1.5×, the instrumentation
  perturbs the measurement: attribution stands (counts), timing is discarded.
- If digests differ between baseline and instrumented builds on the same seed, the
  instrumentation changed the work: VOID, fix before reading anything into counts.

## Controls

- Positive: a known-op unit path (hand-counted Scalar ops in a test) must match the
  counters exactly.
- Negative: a `--seconds 1 --rtf 1 --members 4` run (near-idle scene) must report
  near-zero ops per frame outside kicks.
