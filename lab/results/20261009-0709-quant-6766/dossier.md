# Dossier — 20261009-0709-quant-6766 (Quant lens)

**Claim.** The plane's frame has an O(N)-per-frame fixed cost (a calendar drain plus a deadline
rekey that touch every entity whether or not anything is due) that breaks a 60 Hz presentation
near 5×10⁴ bodies on this class of core; one line — `break` at the first too-late heap head
instead of draining — cuts that fixed cost 5.4× with every behavioural guard green (digest
invariance included), and the residue, the rekey, is the next lever.

**Bottleneck.** Board item 4 (smoothness and the allocator) and the Quant lens's #1/#6 (latency
budget; a frame's cost when nothing happens). Not the event path: per-event cost measured flat at
≈ 21 µs from 10³ to 10⁵ bodies (arithmetic-bound; the memory-wall prediction for events is
refuted). The wall is the *schedule's* overhead, which grows with N and is paid 60× per second.

**Evidence** (Haswell i7-4790, 8 vCPU shared, loadavg 1.1/2.4, 15 GB, ~5 GB free; Linux/x86 —
orders of magnitude only, integrator re-measures on the M1):

The harness is `crates/universe/examples/quant_events.rs` (saved in the patch): the repo's own
`restricted` scenario — star, one planet at 5.2 AU, N test ships over ±6 Hill radii at seeded
angles, no player, one thread, unlimited budget — so nothing here is encounter or view cost.
Stage attribution comes from six `Instant` buckets added to `Universe::advance`/`apply` (also in
the patch; experiments only).

Per-event (kicks and boundaries fire ≈ 1:1 at the default 128 kicks/orbit):

| n | ns/event p50 | empty frame p50 | ns/entity |
|---|---|---|---|
| 1 000 | 21 555 | 0.25 ms | 250 |
| 10 000 | 21 730 | 2.63 ms | 263 |
| 100 000 | 21 418 | 60.6 ms | 606 |
| 1 000 000 | (fixed cost dominates) | 695–835 ms | 695–835 |

- Empty-frame split (profiler, stable across n): main-loop calendar drain ≈ 50–58%, deadline
  rekey ≈ 18–20%, deferred requeue ≈ 24–31%. Three O(N) passes per `advance`, resolved events
  or not. At 10⁵ a frame that resolves *nothing* costs 3.6 presentation frames (16.7 ms each).
- Eventful rounds are 99% `resolve`; within it, the per-event position readback
  (`root_state_raw` into `self.pos`, which only feeds the light-distance deadline heuristic)
  costs 3.1 µs = **14% of every event** — scheduler bookkeeping priced as physics.
- The one-line change (`break` at the first `t > target` head; the heap is deadline-ordered so
  that head carries the minimum remaining deadline — the horizon arithmetic is unchanged):
  empty frame 2.63 → 0.49 ms at 10⁴, 60.6 → 11.2 ms at 10⁵ (**5.4×**), ns/event unchanged.
  Guards: `cargo test --release -p emergent-universe` motion (8), plane (6, including
  `the_same_digest_at_every_budget_and_thread_count`), replay (6), origin (4), ties (8),
  throttle (3) — all pass, 0 failed.
- Memory: `bytes_per_body` = 1 039 on the live store; HWM ≈ 2× that with allocator growth; the
  no-player history retains ≈ 0.9 KB per event between prunes. 10⁹ bodies ≈ 1–2 TB against the
  8 GB target.

Reproduce (each ≤ 60 s):

```
cargo build --release -p emergent-universe --example quant_events
B=target/release/examples/quant_events   # here /home/glmlab/lab-target-3/release/examples
$B 100000 16 20000        # events + 20 empty frames, with the profiler's JSON lines
$B 1000000 8 10000        # the 10^6 point, memory-safe settings (HWM ≈ 2 GB)
```

Guards: `cargo test --release -p emergent-universe` motion (8), plane (4, including
`the_same_digest_at_every_budget_and_thread_count`), replay (6), origin (3), ties (8),
throttle (3) — all pass, 0 failed.

**Predictions** (`predictions.md`, written before the n ≥ 10⁴ runs): P2 confirmed and stronger
than guessed (per-entity cost *grows* with n: 263 → 606 ns, DRAM streaming, not the flat 200–300
I predicted; the break near 5×10⁴ stands). P3 confirmed (≥ 1 KB/body). P1 half-refuted — per-event
cost is flat in n (the event path is cache-friendly); the memory wall lives in the fixed passes,
exactly where P2 said. P4 answered by stage buckets rather than perf (`perf_event_paranoid=4`,
no sudo): calendar work is < 2% of an eventful round; the events themselves are the cost. One
honest miss: my first attempt at the one-line change swallowed the `budget.spent` block and
*failed* the motion test; I initially blamed the break, concluded the drain was load-bearing, and
only the stash-and-rerun control exposed my own edit error. The clean variant passes everything.

**What would make it wrong.** The digest guards cover budget, thread and frame-shape invariance,
not every scenario; a case where an entity with `t ≤ target` but a later deadline must resolve
*within* the same frame (not merely before the frame's presented time) would show it — the
horizon rule should then present earlier, not lose work, but that is an argument, not a
measurement. On the M1 the constants shift (~2×, 128 B lines, 12 MB L2); the O(N) shape and the
5.4× ratio are the claims, not the nanoseconds. The 14% position-readback figure is measured on
bodies in one doll; a doll tree deepens the readback.

**Cost of adopting, and fit.** The break is one line plus two comments in
`crates/universe/src/universe.rs` (`advance`); the stage profiler should be dropped or kept
behind a feature flag. It deletes work, adds none (PRINCIPLES #1: "the cheapest compute is
compute not done"), touches only the schedule — "the queue's own order … is only a schedule"
(universe.rs, line 16) — and pays toward #12 ("p95/99", "the algorithm that allocates the work").
The next levers it exposes, in measured order: amortize the rekey (still O(N), ≈ 112 ns/entity
at 10⁵ — the 60 Hz wall moves to ≈ 1.5×10⁵ bodies, not away), then the 3.1 µs/event position
readback, then cadence (21 µs/event here; a ship-orbit at 128 kicks costs ≈ 5 ms of one core).

**The lens.** Quant prices tails and capacity; it can over-value shaving a constant that a
representation change would delete. The rekey's O(N) is exactly that shape: the fix is not a
faster sqrt but deadlines re-derived only when the observer crosses a cell — the slack skin the
board already queues. I measured the wall and deleted the worst pass; I did not design the skin.
