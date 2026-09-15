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

## Packet 6 policy/storage

`policy.rs` and `archive.rs` compile as isolated modules. I1 increment 1: connect Broadcast delivery, received-message course change, in-flight signal across save/restore. I1 increment 2: authority-backed commit. Do not report canonical-gravity acceptance from increment 1.
