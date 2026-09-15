# I0 full-cost report — 15 September 2026

Not a speedup claim. Source operations, wall-time and memory are distinct. Historical `1188 vs 1675` and `1126 vs 1722` remain scoped compile/repair counts.

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, base `254ba1f`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`.

## Repair completeness

`repair_from_committed` previously stored `compiled.incoming + extra` in metadata while `interval_continue` received only `extra`. Fixture `extra_only_repair_inputs_drop_later_recorded_cause` retains that extra-only omission. Continuation now uses the merged ordered history. `repair_keeps_later_recorded_cause_after_earlier_extra` matches a genesis reference with both kicks, including repeated repair. The earlier extra is in an uncommitted suffix / new history branch; it does not rewrite a committed past.

## Nested ledger

`Charge::total` stays the historical flat sum. `ledger_total` adds nested children once. `runtime_request_total` excludes `OfflineAudit` / `Certificate`. `reuse_certified_interval_functions` nests the full `enclose_compiled_interval` charge (two genesis evolutions + Picard) instead of copying only validation/verification. Quiet compile baseline (H=4, dt=1/32, two-body): source ops **803**, wall_ns **46250** (warm; cold runs differ), pair-inverse n **28** / **6272** bytes, `charge_total` **1531** = `ledger_total` (no enclosure child on compile).

## Dense pair inverse (I1 note)

Quiet pair `store_pair_inverse` at H=3: n=20, 3360 bytes, source ops 704. At H=6: n=44, 15840 bytes, source ops 1262. Setup is dense in interval-function count. Wall-time is not those source ops (cold H=3 was sometimes slower than warm H=6).

## H0124 historical scope (still passing)

Recoupled reuse/repair: leftover 0 at 16/128/tail/lookback; reuse_ops **1188** vs full **1675**; repair_ops **1126** vs mid **1722**; suffix se 11 / 24; copies 81 / 70. Encounter share refuse **1.5193527764310737**. `production_law` null.

## Commands

```
CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-law-lab --lib coupled_ --offline --locked -- --test-threads=1
CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo test -p emergent-observatory --no-default-features --lib --offline --locked -- --test-threads=1
cargo test -p emergent-engine --lib --offline --locked -- --test-threads=1 policy archive
cargo xtask history check
```
