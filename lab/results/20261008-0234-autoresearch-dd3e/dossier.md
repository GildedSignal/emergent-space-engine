# dossier.md

**Claim.** The plane's kick path decodes the same tube three times per kick where once suffices; caching the binding's proper time at its event and returning the orbit state with the readout makes the pure kick resolve ~20 % cheaper (36.0 → 28.3 µs on the held-out A/B) with bit-identical universes on every tested seed, order and fleet size.

**Bottleneck.** "Fewer kicks per orbit … kicks dominate the engine's cost" (board, live question 1) — attacked from the *ns per event* side (board metric list). Not 10×: this is a constant-factor deletion of two decodes per kick (rebind's `orbit_state(t)` and `orbit_state(event_time)` recomputes), i.e. it deletes compute, not a component. The next lever it exposes is named below.

**Evidence** (all on this shared Linux runner; orders of magnitude only, per the lab rules; the digest is load-independent):

Phase split of one kick before (temporary thread-local instrumentation, `log.md`):
```
rebind 22.2 µs (compile 11.6 + decode/bookkeeping 10.6) | readout 3.3 | secondaries 3.4 | tide 3.4 | force 0.9
```
After the two kept rounds: `orbit_state(t)` 3.5 → 0.00 µs, `tau_event` lookup 3.35 → 0.02 µs; rebind 22.2 → 15.6 µs.

Held-out A/B (base binary vs final binary, interleaved, `heldout.txt`; digests in `baseline.txt`):

| config | pure kick base → final | digest base = final | settle µs/item |
|---|---|---|---|
| seed 1 m8 sparse (tuned) | 36.03 → 28.33 | e317b268… ✓ | 54.6 → 50.0 |
| seed 7 m8 sparse | 35.72 → 28.75 | 74a3a79f… ✓ | 54.0 → 51.4 |
| seed 23 m32 sparse | 36.19 → 28.94 | 366c42e8… ✓ | 107.6 → 101.9 (ships 50.2 → 47.3) |
| seed 3 m16 dense | 35.75 → 31.36 | d9da1adf… ✓ | 1807 → 1816 (ships 43.0 → 41.7) |

Reproduce (each ≤ ~10 s except dense ~95 s):
```
cargo build --release -p emergent-universe --example kick_bench
./target-dir/release/examples/kick_bench 7 8 sparse 30000000000 1 settle   # digest + settle cost
./target-dir/release/examples/kick_bench 5                                  # pure kick, min/median of 5
cargo test --release -p emergent-universe                                    # whole plane suite (see below)
```
(CARGO_TARGET_DIR=/home/glmlab/lab-target-1 on this runner.)

**Predictions** (`predictions.md`, written before the held-out run): (1) digests bit-identical everywhere — held, all four; (2) absolute µs saved seed-independent — held (7.1–7.4 µs on the sparse seeds; 4.4 on dense, whose item cost is dominated by the lockstep chronon, not the kick); (3) rebind loses ~2 decodes — held; (4) settle improves less than the pure kick — held (7–8 % on sparse ships). The universe's own suite passes: `cargo test --release -p emergent-universe` green across all test files (plane, replay, motion, ties, view, throttle, lifecycle, memo, origin).

**What would make it wrong.** The identity claims `tau_event == orbit_state(event_time).proper_time` and `readout_with().1.proper_time == orbit_state(t).proper_time` rest on both coming from the same pure `decode` of the same immutable fields (entry, tube, clock_exp, units). A future change that mutates a Binding's tube/entry in place after construction (none exists; bindings are replaced, never edited) would silently desynchronize the cache. The `None` fallback keeps even the error paths identical. Cost of adopting: ~30 lines in four files, one `Option<Scalar>` (16 bytes) per Binding (the binding is already ~100+ bytes with the Arc and residual), zero new concepts. Fit: "The cheapest compute is compute not done. Delete before optimizing" (P1); "a tube is read, never stepped" (docs/law.md) — this only changes how many times the same read happens. It does not touch the law, the gates or the representation.

**Grain of salt (the lens).** An autoresearch loop with a bit-identity gate can only find *pure recomputation* to delete — it cannot question the representation. The structural change that beats this best configuration: the kick rebinds, and a rebind compiles a whole new trajectory (43 % of the remaining kick, `compile(from_state)` 11.5 µs: `fit_key` + `Orbit::compile`'s quadrature). The exact-key memo is known dead (taste log, 5 October: 0 % hits on distinct kicks), so the gain must come from making the compile itself cheaper (incremental panel reuse from the previous binding's crossing table when the new key is close — same bit-identity gate does not apply there; it is a law-internal precision question and needs its own gate) or from not rebinding at all when the kick is sub-quantum in E/L. Second structural miss the lens hides: the remaining three decodes per kick (own readout, secondaries, tide) re-decode the *same other bodies* at the *same tick* across a fleet — a cross-body (binding, tick) memo in `Ctx` is invisible to a single-ship bench and only pays at fleet scale; measure it with the m32 settle, not the pure bench. Also: the timings are from a shared, contended runner (foreign jobs at 100 % CPU part of the time); the −20 % is an A/B against a base binary run back-to-back, and the M1 re-measure belongs to the integrator.
