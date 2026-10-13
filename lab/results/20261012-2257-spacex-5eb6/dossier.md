# Dossier — 20261012-2257-spacex-5eb6 (Spacex lens)

## Claim

The zero-event frame tier is deleted: a tick-keyed due-ness calendar plus a player-motion-gated
rekey makes the quiet frame **O(1) instead of Θ(N)** — median **1.35 µs at 200,000 bodies against
14.7 ms shipped (10,900×)** — with **digests bit-identical** across both arms on 15 schedules
(3 seeds × rtf {1, 100, 1000} × threads {1, 4} × engine budget {5 ms, 0.05 ms}) and the quiet
populations at every size.

## Bottleneck

`frame-cost`, open direction 1 ("delete the fixed tier — the determinism-safe construction is the
missing experiment"). The shipped `Universe::advance` pays three Calendar touches per body per
frame whether or not anything is due: the `rekey()` sweep (`universe.rs`) plus the drain that sets
aside every entity past the target to find due ones hiding behind them. Measured wall: the 16.7 ms
frame breaks at ≈1.5–6×10⁴ entities (wiki). This run removes both passes; the expected gain is the
whole tier (unbounded at scale: the frame no longer cares how many bodies are quiet), and it
deletes the "hidden tick" as a concept — the frame now costs O(events + 1).

## Evidence

All numbers from `regen.sh` (Linux/x86 runner, i7-4790-class, orders of magnitude only). Probe:
`crates/universe/examples/lazy_probe.rs`; the construction: `work/patch.diff` on
`crates/universe/src/universe.rs`.

**Quiet frames** (a player circling at 1 AU, n bare hyperbolic tubes — nothing pulls them, nothing
is due; 200 frames at rtf 100, `Budget::unlimited`):

| n | legacy median µs | lazy median µs | speedup | lazy p99 µs | lazy rekeys |
|---|---|---|---|---|---|
| 428 | 16.45 | 1.49 | 11× | 6.8 | 2 |
| 10,000 | 359.19 | 1.34 | 268× | 126 | 2 |
| 40,000 | 3,483.68 | 1.35 | 2,580× | 674 | 2 |
| 100,000 | 8,119.98 | 1.34 | 6,060× | 2,137 | 2 |
| 200,000 | 14,675.96 | 1.35 | 10,872× | 5,089 | 2 |

Legacy is linear at ~73 ns/body (the three touches); lazy is flat in n. The p99 is the amortized
full sweep (the player moves ~10⁻⁴ c ≈ 34 root units per rtf-100 frame against a quantum of
`want/64` ≈ 5,285 ticks: one sweep per ~155 frames — rekeys counted 2 in 200 including `start`).

**Digests** (`fly`): the plane (star, planets, moon, ships, a 16-member fleet battle, the player
with a 24-decision input log at absolute ticks) run to the canonical cut 2.9×10⁸, settled, digested.
All 15 schedules print one digest per seed in each arm, and the arms agree:

| seed | digest (both arms, all 15 schedules) |
|---|---|
| 1 | a8496bfff17a43dd… |
| 3 | c48002602519bf1f… |
| 7 | 4dc0556c8cd27c72… |

The quiet populations also agree per n across arms. Full rekeys on the same flights: legacy
1,719–80,005 (one per frame, worse at small rtf), lazy 1–219.

**Suite**: `cargo test --release -p emergent-universe` — 10/10 unit tests, clock c1 level 8 ok;
the full file-by-file run (motion, plane, ties, lifecycle, replay, throttle, origin, view, memo)
regenerates in `regen.sh` with the two multi-minute clock tests skipped (`c1_level_8`, skipped at
~90 s, passed standalone before the skip; `c1_level_15` and `c1_to_the_leave` are 500+ s clock-law
flights, not scheduler tests).

## Predictions

Written before the decisive runs (`predictions.md`). Held: the flat lazy median (1), the < 5 sweeps
in 200 quiet frames (1), digest identity across schedules and arms (2, 3). Failed once, then fixed
and re-run: my own red-team case (5c) — the fleet stalled the presented time at tick 2,096,683 —
but by a different mechanism than predicted: not the horizon leaking into canon, see below.

## What would make it wrong

- **The resolution order is now tick order, not deadline order.** This is the load-bearing claim:
  the engine core must be schedule-independent (H: taleb-40c0, gold) — then a different due-order is
  just another schedule. Every digest here and in the suite tests that. A same-tick tie that is not
  pinned by (tick, id) would move digests; none moved on the schedules tried. A wider schedule
  sweep (checkpoints, starvation) is the checker's to run.
- **The stale-deadline slack.** Between sweeps every stored deadline is within `wander` (the
  player's displacement since the last sweep, in light ticks) of its truth; the overflow horizon
  subtracts it, so a budget-cut frame can only under-present, never over-present. If some consumer
  reads a deadline as exact (the view does not; it re-derives crossings from state), it would see
  ≤ `want/64` of staleness.
- **The fleet cap floor** (`cap.max(tick + 1)`): a stale-low cap could let a fleet commit up to the
  stale amount past the second-in-line's true deadline — mid-session freshness only; `frame_to`
  clamps the target to the cut, so nothing canonical passes a cut (digests confirm).

## The trap found (for the next builder)

The fleet entity is due **every tick** (`next_time = tick + 1`); shipped's deadline order is the
regulator that lets the second-in-line resolve, move its deadline, and raise the fleet's cap. My
first slack-subtracted cap deadlocked exactly there: `to == tick`, `run_to` no-ops, the plan item
never fires, ~700 no-op resolutions burn the 5 ms budget every frame and the presented time froze
at 2,096,695 (diagnosed with `Universe::debug_queues`, kept in the patch). The fix is the one-tick
progress floor; the slack subtraction on the cap was deleted — it guarded freshness, not canon.

## Cost of adopting

~120 lines in `crates/universe/src/universe.rs` (one extra `Calendar`, the lazy gate, the loop
split with the verbatim legacy arm behind `ES_EAGER=1` for A/B). Memory: one more calendar
(12 B/slot). Risk: the order change rides on schedule-independence, which is a frozen, gate-tested
property. The `legacy` flag and `debug_queues` should be deleted on merge.

## Fit with PRINCIPLES

- "No work for no reason, so no ticks" (CL 09-29): the quiet frame no longer touches every body —
  the hidden tick is gone, not tuned.
- "Compute only surprises" (§3): the frame now costs O(events); everything quiet costs one peek.
- "The simulation tells us what's next not us" (OC#36): due-ness is read from the tick calendar,
  not re-derived per frame.
- "Light cones partition compute" (§5): the deadline survives only where light actually decides
  (the fleet cap, the overflow horizon), and its staleness is bounded by the player's own motion.

## The lens

The SpaceX lens pushed delete-first (both passes, not a faster rekey) and the A/B arm; it may have
underweighted the tie-order risk (the blind spot it names: a deleted certificate may have been
catching a rare divergence). The suite's cross-schedule digest tests are the certificate that
stayed in place.
