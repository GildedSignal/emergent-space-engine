# I2 composition evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3–I6. One composed scene, not several fixtures.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, base `254ba1f`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-engine --lib -- --test-threads=1` | PASS (31) |
| `cargo test -p emergent-engine --test causal_contract -- --test-threads=1` | PASS (18) |
| `cargo test -p emergent-engine --test i1_connected_scene -- --test-threads=1` | PASS (2) |
| `cargo test -p emergent-engine --test i1_increment2_authority -- --test-threads=1` | PASS (6) |
| `cargo test -p emergent-engine --test i2_composed_scene -- --test-threads=1` | PASS (1) |
| `cargo test -p emergent-law-lab --lib -- --test-threads=1 coupled_` | PASS (54) |

## Scene

`crates/engine/tests/i2_composed_scene.rs` `i2_composed_scene_crosses_extraction_remerge_history_and_cuts`

Hierarchy (emitter/ship/beacon) plus a massive affine family (8 × mass 10) and the I1 coupled diagnostic. A signal is in flight. The scene then crosses:

- family-level common transform and extraction of one identity
- restricted exact re-merge of affine-adjacent partitions (permutation of extracted slots refused)
- range broadcast with per-receiver reception times and logical vs stored counts
- unequal certified cuts, arriving influence, then reconcile to a global cut
- incremental archive seal, resident-tail eviction, cold observation without loading every chunk
- second seal into the same directory; restore; replay; collective mass unchanged
- burst recovery Instant; resident history bytes before/after eviction
- policy fires once (I1 re-fire hole closed)

## Honest leftovers

- Certified cuts overlay a single physics clock; they are not two independent `advance` loops.
- Broadcast indexing still walks the small materialized range; it is not a billion-member closed-form schedule.
- Cold observation still uses remainder worldtubes plus selected chunks, not a one-identity-only decode from disk.
- GEM remains diagnostic. The family does not gravitationally perturb the coupled two-mass compiler.
- I3 not started. Measured bottleneck from this scene: history reconstruction (seal/evict/restore) plus the single-clock scheduler overlay.
