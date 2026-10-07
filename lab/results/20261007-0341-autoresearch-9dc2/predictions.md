# Predictions (written before the decisive experiment)

Artifact: `xtask universe --kick-bench` (the plane's own kick resolver, pure, digest-locked).
Metric: median µs per kick; `replay_digest` + `digest` must stay bit-identical (behaviour fixed).

Tuned-on configuration: `--rtf 100 --members 400 --seconds 8` (4918 distinct kicks).

Held-out cases (not tuned on):
- H1: `--rtf 1000 --members 400 --seconds 8` (more game time, passage-heavier, fatter p99).
- H2: `--seed 7 --rtf 100 --members 200 --seconds 10` (different population).
- H3: `cargo test -p emergent-space -p emergent-universe` (behaviour gates).

Measured baseline (probe-included build): kick median ≈ 85–91 µs, p99 ≈ 377–402 µs.
Attribution: rebind 97% of kick time; `compile` 79%; inside compile, quadrature panels 75%
(0.589 µs/panel, ~70 panels per bound-orbit compile), `cut` 25%. Each quadrature node does
four `u128/u128` software divisions (`__udivti3`); the divisors provably fit `u64` on the
hot weak-field regime.

## Change under test

`fast_quad`: replace the four `u128/u128` divisions with `div_word` (128÷64, hardware),
each guarded by an exact `n < (d as u128) << 64` precondition check that falls back to the
original expression. Bit-identical by `div_word`'s tested contract (quotient equal to
`u128` division whenever the quotient fits `u64`).

## Predictions

- P1 (tuned config): kick median drops 20–35% (to ≈ 55–67 µs); p99 drops similarly.
- P2 (H1, passage-heavy): median and p99 drop by a LARGER fraction than on the tuned
  config (passages have more panels per compile, all through `fast_quad`); p99 < 320 µs.
- P3 (H2): the drop is within ±5 percentage points of the tuned config (same arithmetic mix).
- P4: `replay_digest` and `digest` are unchanged on every case; tests pass.
- P5: the p99/median ratio stays within ±15% of baseline (no tail-specific mechanism).
