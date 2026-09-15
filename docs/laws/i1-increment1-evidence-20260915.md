# I1 increment 1 diagnostic evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, base `254ba1f`. Target dir `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-law-lab --lib -- --test-threads=1 coupled_` | PASS (54) |
| `cargo test -p emergent-engine --lib -- --test-threads=1` | PASS (29) |
| `cargo test -p emergent-engine --test causal_contract -- --test-threads=1` | PASS (18) |
| `cargo test -p emergent-engine --test i1_connected_scene -- --test-threads=1` | PASS (2) |
| `cargo test -p emergent-observatory -- --test-threads=1` | PASS (10) |

## Tests that pin increment 1

- `crates/engine/tests/i1_connected_scene.rs::i1_increment1_connected_diagnostic_scene`
- `crates/engine/src/coupled_adapter.rs::tests::euler_and_pair_inverse_jobs_yield`
- `crates/engine/src/coupled_adapter.rs::tests::adapter_does_not_report_canonical_gravity`
- `crates/law-lab/src/coupled_source_response.rs::tests::compile_job_suspends_inside_collocation_not_after`

## Remaining I1 holes (not increment 1 diagnostic wiring)

- Historical `compile_source_response` compact fit remains atomic (`seal_compiled`); diagnostic seal skips that sidecar.
- Increment 2: finite-semantic GEM reference, independent branch validation on moving cases, contact/light-cone near-ties and full interval bounds, slow vs compiled canonical GEM facts, separately versioned physical resolution, shifted units, moving near-tangent between sample times, input-epoch changes. Sampled `certified: true` still must not authorize events (`i1_increment2_sampled_certified_does_not_authorize_events` pins the refuse only).
