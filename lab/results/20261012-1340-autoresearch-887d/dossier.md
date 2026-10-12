# Dossier — autoresearch 20261012-1340

**Claim.** The plane's kick event costs 16–24% less wall time (interleaved A/B: 38.8 → ~28.8 µs/kick, −26%) with byte-identical canonical outcomes (`Universe::digest()` unchanged on every configuration), by deleting three redundant decodes and one redundant residual per kick — no law, cadence or precision change.

**Bottleneck.** Board #1/#3: kicks dominate the engine's cost; "cheaper events". The artifact is the shipped plane (`crates/universe`, `behave --law plane` path): `kick_clock` → `rebind` → `bind_in` → `Rebinding::from_state`. Scalar: ns per kick (`crates/universe/examples/bench_kick`, public API only, threads=1).

**Evidence** (Linux x86, shared window — interleaved binaries for every A/B; orders of magnitude only, M1 re-measures):

| round | change | ns/kick (interleaved) | verdict |
|---|---|---|---|
| 0 | baseline, 64 ships / 2 planet periods / step 7 | 38,837 | — |
| 1 | `from_state_fit`: the bind path no longer computes the residual `bind_in` discards (the handoff path keeps it) | 35,771 (−7.8%) | keep |
| 2 | `Binding.orbit` caches the orbit state at the binding event (was re-decoded every rebind) | 33,300 (−7.0%) | keep |
| 3 | `readout_with_orbit` returns state + orbit; `rebind` takes the kick-time orbit instead of re-decoding `t` | 30,400 (−8.7%) | keep |
| 4 | `boundary_clock` decides the crash/leave certificates from the tube's own periapsis/apoapsis (no decode unless the tube can cross) | 28,800 (−8.6%) | keep |

Held-out (predictions.md, run once, never tuned): digests identical on all four configurations (tuned 64/2/7; 16/3/7; 128/2/9; 64/1/6) and event counts unchanged; gains 16.4–23.7% at load (baseline absolute µs inflated by sibling runs — the interleaved deltas are the measurement). Tests: `cargo test --release -p emergent-space -p emergent-universe` — 66 passed, 0 failed. `cargo test --release -p xtask plane` — 12 passed, 1 failed (`across_a_kick_the_register_and_the_angular_momentum_agree_to_the_post_newtonian_gap`), **the same single test fails on pristine main on this machine** (verified by stash/rebuild/re-run), so it is pre-existing, not caused by the patch. Reproduce: `cargo build --release -p emergent-universe --example bench_kick && ../../../../home/glmlab/lab-target-2/release/examples/bench_kick 64 2 7` (digest + ns/kick printed; any config). Patch: `work/opt.patch` (+45/−27 over 5 files; bench example included, scaffolding stripped).

**Predictions** (predictions.md): held — four rounds landed at 7.0–8.7% each (predicted ~3 µs each), total −26% vs predicted −20–25%; digests identical everywhere; gains N-independent (128-ship case −16.4%, at the low end under load); the witnessed `fit_key(state, true)` was left alone as predicted. Miss: prediction 4's absolute 29–31 µs assumed a quiet machine; load spikes reached 51–70 µs/kick mid-run, so absolute numbers are orders-of-magnitude only.

**What would make it wrong.** A digest difference on any untested scene (only circular-ship scenes were run; the `needs` fallback path in `boundary_clock` triggers on surface-crossing tubes — it reproduces the old exact check, and the universe suite's crash tests pass, but an eccentric-crash scene digest would strengthen it). Adoption cost: one new `Binding` field (`orbit`, an `OrbitState` copy), `bind_exact` now returns `Res<Binding>`; no API break beyond that.

**Fit with PRINCIPLES.** #1 "The cheapest compute is compute not done. Delete before optimizing" — all four rounds delete recomputation of already-known values, no new state machines; #14 "we only care about changes"; #2 exactness kept by construction: the deleted computations were pure re-derivations, and the digest (canonical, schedule-independent) is the control on both sides (identical before/after = the change is observation-only in the outcome sense).

**The lens (autoresearch) and its blind spot.** A local search finds local optima: the remaining per-kick floor is `fit_key` (~4 µs) + `Orbit::compile` (~3.6 µs) + `at_radius` (~1.1 µs) — the tube is **recompiled from scratch on every kick** (99% of kicks, per the board). The structural change that would beat this best: an incremental rebind (the new state differs from the old by one velocity quantum; the key, shape tables and orientation shift by one quantum too), or caching the compiled shape across kicks keyed on the quantized key — that is a law-adjacent design move (the memo artifact, 5 October: the exact memo hits 0% on distinct kicks; the quantized memo hits 94.5% but changes orbits), not autoresearch. Also untouched: ~4.8 µs/event in the queue/apply machinery outside `step.rs` (Calendar, Vec churn) — a second lens could take it.
