# Patch note (the tree is restored by run.sh; this is what was changed)

Diagnostics (no behaviour change):
- `crates/space/src/binding.rs`: `RebindDiag` atomics + `rebind_diag_report()`; timing of `fit_key` and the compile inside `Rebinding::from_state`; thread-local consecutive-key comparison (contaminated across bodies — superseded by the per-body counters below).
- `crates/universe/src/step.rs`: `KICKS`/`KICKS_FIRED` around `quantize`; per-body old-vs-new `Entry.trajectory.key()` comparison in `Work::rebind` (`REBINDS`, `REBIND_SAME_EXACT`, `REBIND_SAME_CELL`, `REBIND_DK_*`); `REBIND_WALL_NS` around the rebind call in `kick`; `kick_report()`.
- `crates/universe/examples/cost_split.rs`: prints both reports.

Prototype (bit-identical by construction — a memo of a pure compile):
- `crates/space/src/binding.rs`: `SHAPE_MEMO` (a global `ShapeMemo`, the crate's own type) wired into `from_state`'s `Trajectory::Cycle` branch; `MEMO_HITS` counter; `LAB_NO_MEMO` env var bypasses it (the A/B control). Eviction policy deliberately left open (owner's call); unbounded growth is fine for the bench only.

## Raw evidence

Baseline (unmodified tree, quiet container):
```
pure kick (resolve) 29.3 us (3000 kicks of 3000)
own readout 3.12 us | secondaries (moon) 3.04 us | tide 3.01 us
root_state 6.12 us | rec() clone 0.04 us
whole universe over 3e10 ticks: 47.8 us per kick/open/boundary (49596 items)
```

Instrumented (quiet container):
```
pure kick (resolve) 29.4 us | readout 3.02 | secondaries 3.01 | tide 2.99
rebinds 27721 | fit 3.8 us avg | compile 6.7 us avg
kicks 27814 | fired 27694
per-body rebinds 27698 same-exact 0 same-cell 27346 | dk max 114859694013884 avg 16744983761
```

Prototype, memo on / off (3 interleaved rounds; counts deterministic, µs load-noisy):
```
memo on : shape-memo hits 24443/27721 (88%)   — every round
memo off: hits 0                              — every round
```

Tests with the prototype wired:
```
cargo test --release -p emergent-universe
1 + 5 + 3 + 6 + 4 passed, 0 failed, 1 ignored (pre-existing)
```

Key facts derived: firing rate 99.6%; same 44-bit memo cell 98.7%; same exact key 0;
avg shape-key movement 2^34 of the Q48 word → ~2^14 rebinds per cell crossing;
fit+compile = 10.5 of 29.4 µs (36%), whole rebind path ≈ 16–19 µs (55–65%), quiet container.
