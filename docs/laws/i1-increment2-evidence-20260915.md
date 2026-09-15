# I1 increment 2 authority evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
`GEM_INTERVAL_COVERAGE = sampled-16-not-interval-wide`.
`HISTORICAL_COMPACT_SEAL = atomic-h0124-not-authority`.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, base `254ba1f`. Target dir `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-engine --lib -- --test-threads=1` | PASS (31) |
| `cargo test -p emergent-engine --test causal_contract -- --test-threads=1` | PASS (18) |
| `cargo test -p emergent-engine --test i1_connected_scene -- --test-threads=1` | PASS (2) |
| `cargo test -p emergent-engine --test i1_increment2_authority -- --test-threads=1` | PASS (6) |
| `cargo test -p emergent-law-lab --lib -- --test-threads=1 coupled_` | PASS (54) |
| `cargo test -p emergent-engine --test i2_composed_scene -- --test-threads=1` | PASS (1) started, not I2 exit |

## Increment 2 pins

- Finite-semantic independent geometry oracle vs compiled inertial events: `i1_increment2_canonical_inertial_facts_agree_on_connected_scene`
- Near-tangent between integer samples: `authority::tests::near_tangent_between_ticks_is_owned_by_the_ending_bin`
- GEM sampled closest-approach is not interval-wide: `i1_increment2_sampled_contact_misses_are_not_interval_wide_bounds`
- Moving kicked pair between enclosure samples: `i1_increment2_kicked_near_tangent_between_enclosure_samples`
- Shifted units / input-epoch / dt separately versioned: `i1_increment2_shifted_units_epoch_and_dt_are_separately_versioned`
- Three-mass GEM compile stays diagnostic: `i1_increment2_three_mass_compile_stays_diagnostic`
- Beyond-horizon pending: `i1_increment2_beyond_horizon_stays_pending`
- Sampled certified does not authorize: `i1_increment2_sampled_certified_does_not_authorize_events` (also in `i1_connected_scene.rs`)

## I1 full-exit reading

The plan I1 exit is the connected diagnostic scene plus exact inertial authority, separately versioned GEM, measured pause/resume duration, and visible pending queries. That milestone is evidenced. It is **not** gravitational qualification. GEM 16-sample enclosure has no interval-wide retarded-root bound; slow Euler vs compiled collocation remain two numerical methods of `es-linearized-retarded-gem-response-v0` and do not mint events.

## I2

`i2_composed_scene.rs` starts a family + in-flight signal on the diagnostic scene and extracts one identity. Re-merge, selective history, indexed range reception and unequal certified cuts are not implemented.
