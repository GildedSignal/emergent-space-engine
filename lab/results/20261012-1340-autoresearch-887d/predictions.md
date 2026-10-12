# Predictions — autoresearch 20261012-1340 (held out; written before the decisive runs)

Artifact: the plane's kick path (`crates/universe` settle loop, `kick_clock` → `rebind` → `bind_in` → `Rebinding::from_state`).
Scalar: ns per kick (bench_kick, threads=1, Linux x86 — orders of magnitude only). Baseline: 38.8 µs/kick (64 ships, 2 planet periods, step_log2 7), digest 82d40ca8…f324.

Tuned on: 64 ships / 2 periods / step 7 only.

Held out (run once at the end, no tuning against them):
- H-A: 16 ships / 3 periods / step 7.
- H-B: 128 ships / 2 periods / step 9.
- H-C: 64 ships / 1 period / step 6.
- H-D: `cargo test --release -p emergent-space -p emergent-universe` and `cargo test --release -p xtask plane` all green.
- H-E: digest identical to baseline on A, B, C.

Hypotheses (each: one change, measure, keep or revert):
1. H1 `from_state` computes a residual that `bind_in` throws away (it recomputes its own): removing it from the bind path saves ~3 µs/kick (−8%). The handoff caller (`events/handoff.rs` → `TubeEvent::bind`) keeps the residual via a wrapper.
2. H2 `rebind` calls `old.orbit_state(old.event_time)` — the exact `OrbitState` the previous `bind` already produced (`Bound.orbit`): caching it on `Binding` saves one decode (~3 µs/kick).
3. H3 `kick_clock` decodes at `t` (`readout`) and `rebind` decodes the same `t` again (`orbit_state(t)`): threading it through saves ~3 µs/kick.
4. Prediction: H1–H3 together land at 29–31 µs/kick (−20 to −25%), event counts unchanged, digests identical.
5. Prediction: the remaining floor is `fit_key` (~4 µs) + `Orbit::compile` (~4 µs); I will NOT touch the witnessed fit (`fit_key(state, true)`) — dropping certification is a law change, not a cost change.
6. Prediction: per-kick gains are N-independent, so H-B shows the same fraction saved as the tuned config.
7. Stop rule: three consecutive rounds < 10% each → stop (lens rule).
