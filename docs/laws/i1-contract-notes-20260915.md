# I1 contract notes (I0 freeze sketch)

Not an I1 completion. Sampled `certified: true` is not a canonical event.

## Model and authority

Diagnostic enclosure (`enclose_compiled_interval`, 16 sample times, f64, `q = τ L` or `H L`) is a **distinct type** from an authoritative certificate. I1 must not commit gravity from leftover-zero at samples. Authority path needs interval-wide coverage, retarded-root bounds and arithmetic error, or the result stays labeled diagnostic.

## ResponseDomain / Response

Keep `SourceResponse` identities, committed incoming cut, horizon, interval functions and worldtubes. Bind I1 consumers (ship, ray, clock, contact) to selected geometry, not gallery labels.

## Validation

`Enclosure.certified` remains diagnostic. Runtime certificate (I1 increment 2) must be cheaper than replaying full history; offline audit stays on `ChargeRole::OfflineAudit` and is never subtracted from a performance claim.

## Resumable work

Current interval compile/repair/factorization/enclosure are atomic. I1 must split them into continuation jobs. `advance(…, WorkBudget)` suspends those operations; it must not charge after they finish.

## Commit and dependency

Repair may insert an earlier intervention only in an uncommitted suffix or a new history branch. It does not rewrite the committed past. I0 `repair_from_committed` now continues with the complete ordered input history.

## Cost and lifetime

`Charge::total` is the historical flat sum (H0124 scope). `ledger_total` includes nested children. `runtime_request_total` excludes offline audit. Source ops, `wall_ns` and pair-inverse bytes are distinct baselines. No new speedup is claimed.

## Dense `store_pair_inverse`

Quiet two-body compile eagerly factorizes a dense `(I-K)^{-1}` whose dimension is `2 * interval_functions`. Setup bytes grow with horizon. I1 should keep this lazy unless a consumer actually uses the stored inverse. A dense boundary replacing a small source system can erase reuse.

## I1 increment 1 started (not complete)

`CoupledCompileJob::poll` charges one collocation block then yields when `op_budget` is 0. Atomic `interval_continue` polls with `u64::MAX`. Tests: `compile_job_suspends_inside_collocation_not_after`, `diagnostic_scene_is_not_canonical_gravity`, `adapter_does_not_report_canonical_gravity`. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`.

Still remaining for increment 1: `Engine::advance` does not yet suspend these jobs; seal/pair-inverse/enclosure are still atomic; received-message course change and in-flight signal save/restore are not connected through the engine; consumers are bound in the law-lab diagnostic scene, not a headless engine loop. Increment 2 (authority-backed commit) has not started.

## I1 increment 1 diagnostic exit (2026-09-15 follow-on)

`Engine::advance(..., WorkBudget)` now polls the diagnostic pipeline before inertial work: collocation (per block), residual seal (per sample; compact sidecar skipped), pair-inverse (per FD column and LU step), enclosure (per Euler/Picard dt), repair collocation. Headless scene `crates/engine/tests/i1_connected_scene.rs` binds ship/ray/clock/contact to interval functions, applies received-knowledge course change, retains an in-flight signal across checkpoint restore, pauses at budget=1, varies query order, clears consumer cache, replays inertial facts, and keeps beyond-horizon required queries visible.

Historical `compile_source_response` still runs compact fit atomically so H0124 counts stay. Diagnostic path does not use that compact decode. `Enclosure.certified` remains diagnostic. Increment 2 authority is recorded below. `production_law` null.

## I1 increment 2 authority (2026-09-15)

Canonical facts are exact inertial contact and light-cone on `es-inertial-causal-v1`. Independent geometry predicates on committed worldlines match compiled events on the connected scene (`Engine::canonical_facts_agree`). GEM stays `es-linearized-retarded-gem-response-v0`: 16-sample enclosure is labeled `sampled-16-not-interval-wide`; sampled `certified: true` does not authorize events; historical compact seal stays `atomic-h0124-not-authority`. Shifted units, input epoch and `Domain.dt` are separately versioned. Tests: `crates/engine/tests/i1_increment2_authority.rs`. Gravity acceptance remains `diagnostic-only`.
