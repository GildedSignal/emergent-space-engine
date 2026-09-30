# Scaled cycle compiler: verified envelope, events integration still open

Base: `40f0209`, branch `wt/envelope`. Follow-up changes are in this worktree; git staging is denied by the sandbox (`index.lock`). The integrator must commit them. No gates or judge implementations changed.

## Verification

- `cargo test --release -p emergent-space -- --nocapture`: **53 PASS**, 27.40 s including build; test executables and doctest each below 1 s. See `crate-tests-final.log/json`.
- `cargo run --release -p xtask -- behave --law space`: **G1–G6, B7, B9, B10, B11 PASS; B12–B14 FAIL**, exit 1. Complete output: `behave.log`. G1 worst 6.59e-4, G2 5.54e-4; G5 zero shape/invariant growth over 10,000 cycles.
- B10: 1k/10k/100k/1M initialization 11.1 ms / 114.1 ms / 1.23 s / 19.06 s; fitted exponent 1.073. Its zero-event extrapolation is not a billion-body game qualification.
- `coarsest-gates.log`: all six unchanged G gates also pass with 11+12-bit significands.
- `history-check.log`: PASS; no journal entry added. `clippy-final.log`: library warnings denied, with only the existing doc-overindented-list-items exemption.

## Envelope and exactness

- 627 bound sweep points, p/M=1e4..1e12, e=0..0.9: positive advance; worst relative advance error 4.702e-4 against 6π/p, coordinate/proper period errors 1.080e-5 against Kepler+1PN. Chosen memo widths also pass the period tolerance.
- Strong-field and near-separatrix checks pass. Stable periodic radial orbits require p>6+2e: periapsis tends to 4M, not 3M. Plunges, L=0 and unstable circular generators remain outside this compiler.
- Scale ladder p=2^40..2^20000: one shared weak shape, positive advance/period, exact phase repetition after a million cycles. No absolute L/r/period cap; checked signed-i16 exponent exhaustion returns an error.
- Unbound parabolic/hyperbolic readouts, finite passage times and asymptotic bend pass weak-field checks and an independent Binet-ODE check down to periapsis 3.3M. Infinite arrival time is not encoded; finite endpoints must resolve the phase word.
- **Remainder proof at an event:** C=X−F(QX), so F(QX)+C=X bit-for-bit. Reconstruct before each integer translation/boost/kick; induction proves no conversion walk. Tests exercise 40 alternating transforms/kicks per seed, both directions and scales through p=1e12, and bound the fit residual so a bad fit cannot hide behind the identity.
- This is **not a proof for moving handoffs**: transport of C through subsequent motion is absent. B12's Jacobi test still fails. A constant Cartesian offset is not a proved transport law.
- Tube is 16 bytes; scale/chirality belong to its 32-bit catalogue index. Additional storage: Orbit binding 128 B, shape header 208 B, knot 88 B, residual 64 B, plus containers/units/event references. Nearly unique bindings preclude claiming 16 B total per body.

## Key width and reuse

`MemoCode`: 44 live bits in u64 = 11+11 stored fraction bits, 6 shape-exponent bits, 16 signed radius-exponent bits; leading significand bits implicit. Boundary tests cover every shape exponent and both i16 scale extremes. Coarsest measured in the 7..15 rectangular search: **11 shape +12 scale significant bits**; chosen **12+12** to pass the wider weak sweep. This is not a global optimality proof.

Chosen-width lookup occupancy, 1,000,000 seeded orbits per row; e uniform [0,.9], p log-uniform, seed `0x454e56454c4f5045` (`key-width-populations.log/json`):

| p range | Shared-shape hit rate | Complete-binding hit rate |
|---|---:|---:|
| 10..1e3 | 0.5361% | 0.5361% |
| 10..1e12 | 57.5320% | 0.1014% |
| 1e6..1e12 | 99.1161% | 0.1797% |

## Timing and machine

| Population / 1,048,576 samples each | Compile p99 | Crossing p99 | Interior p99 |
|---|---:|---:|---:|
| Frozen bound sampler | 26.417 µs | 0.584 µs | 2.875 µs |
| Weak p=1e4..1e12 | 30.417 µs | 0.583 µs | 2.666 µs |

`timing-*-sustained.log/json`: sequential mixed compile/crossing/interior loops, 14.73 and 15.26 s; construction/drop included, no memo for compile, 256 shapes repeated 4096 times, interior at 13/31 period. Compile maxima 143.959/440.667 µs are retained. Earlier failed timing configurations and short passing samples are retained too. These are component costs, not a rendered-view or steady-thermal certification.

MacBook Air M1, 8 GB, 4 performance +4 efficiency cores, AC/100% charged; strong-run load averages 3.41/2.92/2.92 → 3.17/2.89/2.91. No quieting/cooling/pinning. `vm_stat` records compressed memory and swap activity (36 swap-in pages during the strong loop). Thermal readings and swap occupancy were unavailable under sandbox restrictions; their errors remain in the records.

## Handoff

`crates/space/ENVELOPE.md` contains the exact module-by-module migration: records/catalogue, scaled clocks with outward rounding, edge certificates, authoritative rebinding with remainder transport, kicks, and the tide/Hill selector. B11/photon adapters still use v2. B12–B14 return unsupported results until events integration exists. Readout still uses i128 products, beyond the draft law's compilation-only wide-integer rule. No global v3 quadrature bound, GPU/hardware determinism qualification or high-c event boost integration is claimed.

Reproduce timing: build `cargo build --release -p emergent-space --example envelope`, then `python3 artifacts/evidence/space-envelope-20261001/run-measured.py NEW_STEM target/release/examples/envelope --rounds 4096` (add `--weak`). `--keys` reproduces widths/occupancy. Use fresh stems; retain existing evidence. `source-sha256.json` records the tested source and unchanged judge hashes.
