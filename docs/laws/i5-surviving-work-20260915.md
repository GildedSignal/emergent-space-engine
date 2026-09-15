# I5 surviving-work CPU-only — 15 September 2026

Not `production_law`. `CANONICAL_GRAVITY_ACCEPTANCE` remains `diagnostic-only`.
Does not start I6. GPU unused (no measured crossover). Combined simulation+rendering not run.
Kernel KEEP stays in the published quiet/weak-kick domain only.

## Cuts

| Cut | What changed |
|---|---|
| Full-history knowledge scan | `received_knowledge` uses per-observer `signal_arrivals` plus `broadcast_receptions`; no walk of `events.values()` |
| Redundant policy walk | `apply_received_policy` uses `policy_fired` only |
| Eager dense pair inverse | Solar/family GEM compile keeps `store_pair_inverse: false` |
| Family GEM | Moment source KEEP ([family GEM](i4-family-gem-20260915.md)); extract every member is the fallback |

Hardware cannot replace an unbounded extract of every member. Moment KEEP is a representation cut, not a GPU story.

## CPU-only measurements (M1, debug test, `CARGO_BUILD_JOBS=1`)

Composed scene: laboratory two-body GEM + family moment (3 GEM bodies), I2-like ship/signal/policy/family, `es-inertial-causal-v1`.

| Quantity | Value | Meaning |
|---|---|---|
| cold_ns | 4_190_541 | Wall to attach+compile GEM genesis and reach ready |
| warm_ns | 568_500 | `Engine::from_state` + `received_knowledge` + `history_digest` |
| rss_kb | 5216 | `ps -o rss=` of the **test process**, not an isolated engine heap |
| owned_bytes | 4566 | `serde_json` of `CanonicalState` (owned checkpoint bytes) |
| gpu | none | No upload/residency/dispatch/sync/readback/verify |
| full_events | 4 | Former knowledge scan width |
| indexed_arrivals | 1 | Observer arrivals in the derived index |
| history_digest | equal on `replay()` | Canonical outcomes unchanged |
| received_signals | equal on replay and `from_state` | Knowledge answers unchanged |
| gem_bodies | 3 | Pair + family COM; mass not dropped |
| pair_inverse | skipped | Lazy; no eager dense LU |
| kernel_ledger | 1137 | Quiet H=8 memory-kernel KEEP (domain only) |
| family extract vs moment | 127395 vs 1906 | Nested Charge `ledger_total` |

No worse unbounded tail: knowledge query is O(arrivals) not O(events). Index is derived, not a canonical fact, rebuilt from events on `from_state`.

## I5 CPU-only exit

End-to-end improvement at equal outcomes on the surviving I2/I3/I4 path. Combined rendering unpublished because GPU was not used. Remaining named physics gaps (moving multi-mass compact fields, galaxy direct sums, accel PN jump 0.10) are not I5 work.

I6 not started.
