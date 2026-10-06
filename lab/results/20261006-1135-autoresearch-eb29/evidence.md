# Evidence — 20261006-1135-autoresearch-eb29

All commands on the lab Linux box (8 vCPU i7-4790, shared; timings are cloud/x86 — orders
of magnitude only). Bench: `cargo run --release -p xtask -- universe --kick-bench --rtf 100
--seconds 30 [--seed S]`, pure resolver per distinct pending ship kick at deterministic 60 Hz
snapshots.

## Held-out verification (clean build, R1 only) vs baseline (pristine, same box)

| seed | replay digest (base → R1) | state digest (base → R1) | made med µs | leaver med µs |
|---|---|---|---|---|
| 1 | 27fd0a4427a67d31… → same | a6792eadc5c8b618… → same | 36.6 → 31.5 (−14%) | 103.9 → 88.5 (−15%) |
| 2 | 6ce6c53f3f27703f… → same | b8b4765312e9823e… → same | 36.5 → 31.5 (−14%) | 84.8 → 71.3 (−16%) |
| 3 | 5e121398caba0b5d… → same | cb07680fc167a9c9… → same | 36.7 → 31.5 (−14%) | 100.5 → 85.5 (−15%) |

p99 within its noise band (51–58 µs across identical builds) on all seeds.

## Tests

`cargo test --release -p emergent-space -p emergent-universe`: 67 passed, 0 failed, 1 ignored
(envelope, certified bank, quadrature, tube events included — they exercise `from_state`'s
residual path, which is unchanged for every non-universe caller).

## Behaviour judge control

`cargo run --release -p xtask -- behave --law plane`, baseline (git stash) vs R1: every gate
verdict and number identical; the only diffs are the machine_state timestamp and B13's wall
time (2.73 s vs 2.66 s). The failing gates are main's known state (motion law v2 is the fix,
in flight).

## Anatomy (instrumented build, seed 1, 1158 sampled kicks; per-kick means)

- rebind 82 µs: compile 60 (Orbit::compile; 85% of it in OrbitShape::append/quad) + fit_key
  4.2 + from_state remainder 5.3 + bind decode/residual 4.0
- secondaries+tide 7.2; own readout 3.9; acceleration 1.1
- per compile: 55 EDGE bands (16/octave), 63 knots, 130 quad panels ≈ 520 cos + 520 div_word
- primitives (crates/space/examples/lab_micro, copy in this folder): cos 47.7 ns,
  div_word 18.0 ns → cos+div alone ≈ 34 µs of the 60 µs mean compile
- compile kinds: 1125 full-bound, 33 passages, 0 circle fast paths
- memo: exact hit 0% (1125 distinct ShapeKeys / 1158 kicks), quantized cell 95.5% (51 cells)

## Reproduce

- baseline/R1 timing + digests: the table above; `git stash push crates/` gives the baseline.
- patch: `git diff crates/` = `from_state_lean` (crates/space/src/binding.rs) + the one-line
  call switch in `crates/universe/src/bind.rs::bind_in`.
