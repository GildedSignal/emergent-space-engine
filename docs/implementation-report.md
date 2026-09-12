# Implementation evidence — 12 September 2026

The deliverable is a working native observatory and an exact causal laboratory with indexed populations. **The full physical engine remains unqualified.** G2 produced no passing gravity law; its failed experiments are retained. This follows the plan's explicit causal-kernel-plus-research-failure path, not completion of G3–G8.

Implementation revision: `1dac6586e3cb30592abb775ba2a844d7d0e2d189`, clean working tree during qualification. Hardware: Apple M1, 8,589,934,592 bytes RAM. Rust 1.90.0. Frozen manifests and source hashes are recorded in [the evidence directory](../artifacts/evidence/1dac658/).

## What works

- Arbitrary-precision rational planar worldlines, subluminal controlled motion, dyadic proper clocks, exact continuous contact predicates and finite-speed signals.
- Simultaneous event batches, selective identity extraction, causal invalidation, limited cooperative advancement and external actuator accounting.
- Spatially distinct indexed families, shared motion, exact splitting and random member access. Individual interventions retain their own history.
- Atomic checksummed checkpoints, reconstruction, and complete replay from initial generators plus recorded external commands.
- Exact occlusion by individual and generated ships. Historical sensor queries leave canonical history unchanged; diagnostic geometry is separate.
- A native wgpu/Metal observatory with pan/zoom, clocks, ship lookup, course changes, signals, event chronicle and archive controls.

**53 tests pass.** Workspace Clippy passes with warnings denied. The causal relay independently fixes reception at tick 14, contact at 43 and return notification at 71. Differential cases include between-sample contacts, tangency, integer extrema, simultaneous impulses, compressed/individual collision and sensor parity, checkpoint restarts, resource rejection and full replay. Native worker tests exercise course changes, sensing, lookup, signal dispatch, advance, save and restore.

## Measured compression mechanisms

These are single-run measurements of frozen inertial fixtures. They demonstrate reusable structure, not integrated gravitational evolution. Serialized bytes are not RAM. Cold cases create fresh engine state; the population sweep shares a process and warmed code/allocator, so it is not a per-case cold-process study.

| Workload | Measured result |
|---|---|
| One billion distinct addressable ships, 16 affine families, ten-billion-year horizon | 5,463 serialized bytes; initialization 53 µs; certified inertial advance 209 µs |
| Same case, including initialization and 1,024 requested identity positions | 4.313 ms |
| One billion ships with 1,000 individually changed velocities, 32-tick horizon | Setup 7.740 ms; advance 18.478 ms; 923,734 serialized bytes including intervention history |
| Entire mechanism sweep, including checkpoint round trip | 0.217 s; 8,372,224-byte cumulative CPU process peak RSS |
| Billion ships in 256 families, checkpoint | 91,214 bytes; write 9.987 ms; restore plus integrity check 1.677 ms |

The early 1,000-exception probe spent about one second advancing. Excluding already-extracted identities before family refinement brought this mechanism to about 19 ms. This is a scoped engineering observation, not a whole-engine speedup claim. Source/history accounting changed during the implementation, and the early probe was not a controlled release baseline.

Fermi estimates identified assumptions to test: independent descriptions rather than headcount, common versus relative drift, and exception/refinement cost. The results update those assumptions. No estimate was used as a feasibility oracle. [The worksheet](fermi.md) records the reasoning.

## Physical-law result and remaining gates

The stationary quantized Verlet experiment passes several orbital and source-accounting diagnostics, but fails stationary clocks, causal dynamic sources, exterior treatment, compact-field certification and exact branch qualification. The stationary shell-lapse experiment also fails orbital stability, rotation and quantum-refinement gates. These failures concern the implemented stationary experiments; they do not disprove all variational or piecewise-metric constructions.

Both experiments respond to a changed source before its light cone arrives. Neither defines a qualified causal exterior or terminating authoritative exact evaluator. Their complete measurements and failed gates appear in [law-qualification.json](../artifacts/evidence/1dac658/law-qualification.json).

Production causal gravity/FMM, general interacting route families, source evolution, reusable nonlinear block responses, chunked long history, moving-target propulsion navigation, fully resumable query/preparation work, parallel commits and GPU physics remain incomplete. The integrated billion-ship/ten-billion-year workload, 30 FPS operating envelope and GPU-inclusive memory budget have **not passed**. See [architecture boundaries](architecture.md) and [machine-readable gates](../artifacts/evidence/1dac658/qualification.json).

## Run and reproduce

```sh
cargo observatory
./scripts/package-macos.sh
cargo test --workspace --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo run --release -p xtask -- qualify artifacts/runs/reproduced
```

Qualification exits **2**, preserving G2 failure. Full qualification took 2.812 seconds including test execution in this run; build time is separate. The local development app is `artifacts/Emergent Space.app`. A packaged native smoke run rendered 120 frames and wrote `artifacts/screenshots/observatory.png`, exiting successfully. It took 4.39 seconds including startup, capture and shutdown, with 172,441,600-byte maximum RSS and a macOS-reported 234,572,416-byte peak footprint. These are not interactive FPS or GPU-inclusive memory certifications.

The source repository remains in Documents. Build artifacts on this machine are linked to a local cache outside iCloud because offloaded files stalled Cargo. This is a local build arrangement, not a repository requirement. No release publication or notarization is claimed.
