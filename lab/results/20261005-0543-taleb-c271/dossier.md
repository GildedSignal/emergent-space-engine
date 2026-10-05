# Dossier — 20261005-0543-taleb-c271 (Taleb lens)

**Claim.** The plane's law is schedule-invariant at a fixed canonical cut (confirmed adversarially, the hard way), but the shipped benchmark's digest is not reproducible when run the way the player runs it: player decisions are bound to wall-clock-presented ticks, and the digest's cut is never canonicalized.

## Bottleneck

Not a speed bottleneck: a **ruin-state survey** (bottleneck 0, the representation; and the truth rule "canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware"). Silent nondeterminism is the one unrecoverable state; this run maps which of its doors are open today. Expected gain of adopting the fix: reproducible histories (replays, checkers, and cross-machine comparisons become meaningful), which deletes the need to re-derive "did that really happen?" by hand. No physics changes; cost is two policy-level edits (below).

## Evidence

All on this cloud box (Linux/x86, 2 vCPU), orders of magnitude only. Tool: `crates/universe/examples/ruin_probe.rs` (this run's only repo edit; patch saved by `run.sh`). Every run drives the **same universe to the same asserted canonical tick** (`assert_eq!(u.now, target)` before the digest), varying only how the work is chopped.

**The law holds (controls pass).**

- `restricted` (star, planet, 6 ships, 6,984 kicks, 3 doll hand-offs; no fleet, no player): one digest `c3e90203…` across oneshot / 64-chunked settles / jittered settles / 3-event-budget advance / interleaved `root_state` observation, × threads 1,2 (`restricted_8periods.txt`).
- The full plane, **no player inputs**: one digest per horizon across oneshot / 60 Hz frames / jittered frames / 3-event budget (1 overflow), × threads 1,2,4 — at 20 s (`e1_20s.txt`, 12 runs) and 120 s (`e1_120s.txt`, 12 runs).
- Plane with an **empty fleet**: one digest across all four schedules (`nofleet_20s.txt`).
- **Fixed input log at absolute ticks** (press at t=2 s, release at t=4 s, applied upfront): one digest across all schedules and threads at 20 s and 120 s, with exactly 2 log entries everywhere — the flush-free log design works and is fully invariant **even with the player acting**.
- Cross-process: two separate process invocations of the E1 matrix give identical digests (no hidden per-process randomization).

**The ruin doors that are open.**

1. **The shipped bench is not reproducible under its own pacing.** Two identical paced runs (`xtask universe --bench --seed 1 --seconds 6`) give `321031a4…` ≠ `d816e8e4…` (first pair: `d1cb3057…` ≠ `ef6fe4a2…`; `bench_paced_a/b.json`). Unpaced twice: identical (`a6287cf8…`, `bench_unpaced_1/2.json`). Identical under 4× CPU oversubscription too (engine p99 0.13 ms at the 400-member cap; the 5 ms wall budget never bites on this box — a tail risk on slower/hotter machines, not reachable here).
2. **Mechanism: decisions are bound to presented ticks.** The bench's held-key script through jittered frames (`e3_20s.txt`) moves the input log (107 entries at 60 Hz → 112 / 104 under two jitter patterns) while the fleet's committed state stays identical (`tick/contacts/epochs/anchors = 4060508/77/8/3`) — the canonical history changes **only through when the same decisions landed**.
3. **The digest cut is not canonicalized.** `settle(T)` resolves up to T but never rolls back overshoot: a frame loop that steps past T silently digests a different cut. My own first harness fell into exactly this trap and "found" schedule-dependence that vanished once every schedule landed on the same tick. Any checker comparing bench digests will fall into it too.

Reproduce (each ≤ 60 s): `cargo build --release -p emergent-universe --example ruin_probe`; `./target/release/examples/ruin_probe 20 e1` (and `e2`, `e3`, `restricted`, `nofleet`; `120` for the long horizon); `./target/release/xtask universe --bench --seed 1 --seconds 6` twice for the paced pair.

## Predictions

Written before the decisive runs ([predictions.md](predictions.md)). Held: restricted invariance (1), nofleet invariance (2), threads invariance everywhere (5), flush-free log with exactly 2 entries (6), held-key scripts move the log and the digest (7), cross-process identity (8). Failed, honestly: (3) I predicted the divergence would live in the fleet's counters — wrong, because (4) "schedule-dependence persists at 120 s" was false once the harness landed every schedule on the *same* cut; the fleet's slice *count* is schedule-dependent (17 → 1,205) but its committed state is not. The first "divergence" I observed was my own harness comparing unequal cuts — the trap predictions.md pre-registered.

## What would make it wrong

The invariance results could be weak if 120 s or 48 members is too small a horizon to expose order-sensitivity in the fleet's leaver hand-offs (leavers = 11 here); a much longer run or a denser battle could still diverge at equal cuts. The paced-bench non-reproducibility would vanish if `Session::step` stopped deriving decision ticks from wall dt — that is the fix, not a refutation.

**Cost of adopting:** small and policy-level, no physics: (a) bind player decisions to a canonical clock (e.g. quantize the decision tick, or log decisions in the player's proper time and re-emit at canonical ticks — the E2 result shows absolute-tick logs are already fully invariant); (b) canonicalize the digest cut (settle to a fixed tick, print it beside the digest). **Fit with PRINCIPLES:** "Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware" — the law now passes that sentence adversarially; the bench currently violates it at exactly one point, the decision-to-tick binding. Also #5: "the player is the only wildcard, and their influence travels at c" — the wildcard is allowed to decide whenever it wants, but *when* must be canonical for the history to be replayable.

## The lens

Taleb asked "which ruin states are reachable today" and expected to find the engine fragile; the law turned out sturdier than the lens predicted (via negativa: nothing needs deleting in the law). What the lens may have missed: no speed measurement at all (the 10⁹/8 GB bottleneck is untouched), only one seed (seed 1) and one battle order (Sparse), and the wall-budget tail (overflow → lagged decisions) was probed only synthetically — on the M1, where frame p99 is 2.72 ms and worst 14.5 ms, the 5 ms engine budget may already overflow on worst frames, which would make even unpaced runs non-reproducible there. The integrator should re-run the paced pair on the M1.
