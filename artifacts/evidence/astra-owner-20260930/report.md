# Cycle owner handback — 30 September 2026

**Correctness/API PASS; compile p99 target FAIL. Keep Darwin.** The old map's recorded turning-cell errors (0.8% advance, 1.4e-3 period, 1–4% below p=7) are worse; see [owner review](review.md). No silent revert. This is one static-mass cycle compiler, not integrated galaxy qualification.

Base `9b23fb1`, branch `wt/cycle`, worktree `/private/tmp/emergent-wt-cycle`. **No new commits:** both staging attempts failed to create `.git/worktrees/emergent-wt-cycle/index.lock` (`Operation not permitted`). The integrator must commit. The final working tree contains all changes; numbered patches under `artifacts/runs/astra-cycle/` are cumulative snapshots, not sequential patches.

`space-darwin16-v2` fixes the quantized near-ISCO input, globalizes separatrix panel refinement, retains enough clock precision for responses, and exposes bounded 64-bit operands in the node kernel. Zero/crossing reads use cached endpoints. The 64-bit phase-mirror overflow is fixed. The old three failing tests pass without relaxing their behavior gates; the oracle now compares its actual quantized inputs and computes GL8 nodes once.

**Checks:** `cargo test --release -p emergent-space`: 26/26, **18.391 s including build**. `cargo test --release -p xtask behave::`: 13/13 (planted wrong laws included), 11.183 s. History check PASS (206 entries); `git diff --check` clean. Logs and source hashes: [status.json](status.json).

`cargo run --release -p xtask -- behave --law space` (21.862 s including build):

```text
G1 PASS advance per cycle: 256/256 within 1e-2, worst 1.14e-6 [0.04 s]
G2 PASS radial periods: 256/256 within 1e-3, worst 7.18e-7 [0.04 s]
G3 PASS deflection: 64/64 within 1e-2, worst 3.44e-7 [0.00 s]
G4 PASS capture: 0 of 10 misclassified [] [0.00 s]
G5 PASS long run: 32/32 seeds over 10000 cycles (0 short), worst growth E 0.000 L 0.000 (limit 0.2), worst shape drift 0.00e0 (limit 1e-2) [0.01 s]
G6 PASS prograde: 256/256 advances positive [0.00 s]
behave space: PASS
```

**Timings:** `examples/measure.rs`, 256 behave keys × 16 rounds, no memo; compilation includes allocation/drop. Apple M1 MacBook Air, 8 GB; 2026-09-30 12:51:53 UTC, load **4.37 / 5.38 / 5.35**, AC reported with battery **47%, discharging**. Thermal and current swap usage queries denied; raw VM/compression/swap-activity counters retained in [measurement](owner-optimized-measure.log).

| Operation | Median | p99 |
|---|---:|---:|
| Compile | 18.667 µs | **54.750 µs (FAIL ≤50)** |
| Crossing position | 125 ns | 417 ns |
| Crossing position + velocity | 333 ns | **625 ns (PASS ≤1000)** |
| Interior position | 5.291 µs | 11.667 µs |
| Interior position + velocity | 5.417 µs | 12.208 µs |
| Compile / full-cycle band crossing, 4,048 nonzero-crossing cases | 550 ns | **2,812 ns** |

Compilation divided by crossing count is not cached crossing latency; if the 1 µs target includes amortized compilation, its p99 also fails. Before arithmetic narrowing, compile was 21.458/53.500 µs at load 6.84/6.52/5.68; both runs are retained. The narrowed kernel produces bit-identical full Cycle records for all 256 keys: SHA-256 `fd06a9795157daa56c0920763c7e4584795d6950e26ecb738f37f0107767752f`. No quiet-machine rerun replaced a miss.

**Bound:** [QUADRATURE.md](../../../crates/space/QUADRATURE.md) proves `|I−GL4| ≤ h^9 B8/44100` for full panel width h, with B8 from a positive derivative-majorant recurrence, plus a conditional fixed-shape node/sum rounding bound. Checked against independent refined GL8 on 323 bound shapes and unbound geometry: **8,338 panels**, maximum measured error/bound 0.682, maximum relative panel error 9.22e-7. The conservative maximum relative bound is 0.556; it is not a uniform 1e-6 certificate. Global refinement reduced the old worst measured panel error from 6.76e-5. The original ellipse, one-unit continuum-root, and uniform rounding claims were withdrawn.

**API:** documented executable example in `crates/space/src/lib.rs`. `Cycle::compile(Key)`; **16-byte `Tube`** (four u32 words, shared cycle owned by the population); `Tube::state` returns polar position, Q30 signed coordinate velocities `(dr/dt, r*dphi/dt)` and proper time. Key quanta: E Q48, L Q32; Darwin input p Q16, e Q30. `Tangent::centered`, `d_energy`, `d_angular`, `Derivative::apply`, and `predict` expose all six signed responses with explicit steps, units and 16 guard bits. Independent analytic GR derivative checks retain the 0.2% criterion at ΔE=2^-23, ΔL=L/2048; smaller/larger failed probes are retained.

**Open:** compile tail target; authoritative kick remainder/Hessian and a full root/key-to-continuum certificate. Derivatives are finite-difference predictors: recompile before canonical decisions. Topology changes and inadmissible probes refuse explicitly. The f64 bound checker is diagnostic, not a runtime interval certificate. The integrator must reconcile `docs/law.md` motion steps 2–3 with Darwin v2 (that file is absent here), independently review, commit and merge; no freeze or integration claim is made.
