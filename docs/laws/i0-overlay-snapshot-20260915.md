# I0 overlay snapshot — 15 September 2026

Worktree: `/private/tmp/emergent-full-engine-integration`
Branch: `codex/full-engine-integration`
Base: `254ba1f718771ec1d0a25bf59d0d555f7e57993e`
Journal home: `/private/tmp/emergent-g2-law`
`production_law`: null. Default engine law: `es-inertial-causal-v1`.

Original worktrees were not deleted. Cumulative packet branches were not merged wholesale.

## Selected dest hashes (after I0 edits)

See `artifacts/evidence/i0-full-engine-integration-20260915/overlay-hashes.txt` in the integration worktree.

Inertial foundation came from `/private/tmp/emergent-compiler-impl`. Coupled compiler came from `/private/tmp/emergent-coupled-response`. Packet 6 `policy.rs` / `storage.rs` were reviewed and extracted as `crates/engine/src/policy.rs` and `crates/engine/src/archive.rs` without `truncated_admission`.

## Tests in historical H0124 scope

`cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1` — 52 passed (47 historical plus I0 reproductions).
`cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1` — 10 passed.
Pinned H0124 counts still hold: source ops **1188 vs 1675** and **1126 vs 1722**; suffix collocation **11 / 24**; copies **81 / 70**; encounter refuse **1.5193527764310737**.
