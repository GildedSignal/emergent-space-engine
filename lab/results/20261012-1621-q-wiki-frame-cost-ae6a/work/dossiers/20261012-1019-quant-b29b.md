# Dossier — 20261012-1019-quant-b29b (quant lens)

**Claim.** The plane's presented frame carries an unbudgeted Θ(N) fixed tier — `rekey` plus the
defer/requeue drain in `Universe::advance` — that already eats 38 % of a 16.7 ms frame at 12,000
root entities and 133 ms (8× the whole frame) at 120,000, **with zero events resolved**; the event
budget bounds the wrong tier, so the frame's ceiling is N ≈ 1.5–6×10⁴ entities, five orders below
10⁹, unless deadlines become lazy or bodies collapse into fewer entities.

**Bottleneck.** Board #4 (smoothness and the allocator) and the top scaling risk. plane.md
foundation 7 says "nothing takes an unbounded synchronous claim on the frame": the frame's own
scheduler is exactly such a claim, and it is the first component to cross the budget. Fixing it
deletes the per-frame recompute of every deadline (PRINCIPLES 3: nothing derived is evolved) and
unblocks any doll that would hold ≥ 10⁴ independent ships — the belt (`b-belt-wire`, in flight)
must not enter the root queue as entities.

**Evidence** (i7-4790, 8 vCPU, shared, load 7.4 — orders of magnitude only; the M1 re-measures).
Ships on circular orbits ±(1.5–3) Hill radii of a μ = 2⁻¹⁰ planet at 5.2 AU, deterministic LCG
layout; `restricted_with`, threads = 1, rtf = 1 (events rare on purpose: the frame is then pure
fixed tier). Medians of 9 samples for rekey/empty-frame; 240 frames for p50/p99.

| N | rekey ms | empty frame ms | frame p50/p99 ms | events/frame | settle µs/item | digest ms | RSS MB |
|---|---|---|---|---|---|---|---|
| 12 | 0.001 | 0.004 | 0.004 / 0.004 | 0 | 44 | 0.02 | 102 |
| 1,200 | 0.045 | 0.245 | 0.245 / 0.443 | 0 | 20 | 1.5 | 81 |
| 12,000 | 0.47 | 2.9 | 6.3 / 11.9 | 0 | 35 | 33 | 99 |
| 120,000 | 14.0 | 133.6 | 132 / 143 | 0 | 50 | 341 | 484 |

- Threads = 8 leaves the empty frame unchanged (6.33 ms at 12k) and does not help per-item
  (53 vs 35 µs on this loaded box): the fixed tier is serial.
- rtf = 100 at 12k: p50 6.5 ms, still 0 events/frame — at real cadences the fixed tier, not
  events, owns the frame.
- The event tier itself stays affordable and near-flat (20→35→50 µs/item, 2.5× over 100× N;
  matches `cost_split`'s 52 µs whole-universe per item at the plane): the budget can bound it.
- Per-entity fixed cost: ~0.25 µs at N ≤ 12k (cache-resident), ~1.1 µs at 120k, where the pass
  streams the 448-byte `BodyRec`s (54 MB) three times — rekey reads `next_time`, the drain pops,
  the requeue re-inserts. Memory-bound, which is why it is 5× worse per entity at 120k.
- `digest` is Θ(N) (341 ms at 120k): fine per settle, impossible per frame — keep it per settle.

**Mechanism** (crates/universe/src/universe.rs). `advance` calls `rekey()` unconditionally: one
deadline recompute + heap `set` per entity per frame, even when the player has not moved (the only
input that changes a deadline besides the entity's own item, which `requeue` already handles).
When the heap minimum's *tick* is beyond the frame target — the common case — the loop pops every
entity into `deferred` and requeues each, two more full passes, because the single deadline-keyed
heap must also answer tick-due-ness, a different order. So ~3 Θ(N log N) passes plus Θ(N·448 B)
traffic per frame, all outside `Budget`.

**Predictions** (predictions.md, written before the run): P1 held (rekey ≥ 1 ms by 10⁵; empty
frame ≈ 6× rekey), P2 held (≥ 10 % of the frame at 12k; wall-dominated at 120k), P4 held (digest
Θ(N), 341 ms ≥ 10 ms), P5 held (threads do not shrink the fixed tier). P3 held to 12k and broke
mildly at 120k: per-event cost grew 2.5× (cache footprint), so the event tier drifts too — but 30–
60× more slowly per entity than the fixed tier does per frame.

**Commands** (from the repo root; `run.sh` saves the added example as the run's patch).
```
cargo build --release -p emergent-universe --example lab_frame_audit   # ~2 min cold
for n in 12 1200 12000 120000; do cargo run --release -p emergent-universe --example lab_frame_audit -- $n 1 1; done
cargo run --release -p emergent-universe --example lab_frame_audit -- 12000 8 100   # threads/rtf controls
```
Each command ≤ 60 s except the 120k row (~75 s wall: 2.5 s build of 120k tubes + 240 frames × 0.13 s).

**What would make it wrong.** If bodies at scale never sit in the root queue as entities — every
population collapsed into one fleet/frame entity whose internal events are scheduled elsewhere —
then N_entities stays ≤ 10³ and the fixed tier never bites; but then the *fleet* entity must be
audited for hidden per-member per-frame work (the same probe applies to it). M1 absolute numbers
may shift ×2–3; the unconditional Θ(N) structure and the exponent are portable. x86-only timing is
a stated lab caveat.

**Cost of adopting.** The schedule is not an outcome (B8: one digest across budgets and orders), so
the fixes preserve bits and are testable by digest at a canonical cut. One step each, in leverage
order: (a) `rekey` only when the player moved more than the deadline quantum (docked or slow
player: rekey amortizes to zero); (b) serve tick-due-ness without draining — a min-peek on the
deadline heap plus the per-lane tick minimum `lane()` already implements for planets, so nothing
is popped that is not resolved; (c) the full fix: lazy deadline keys as slack lower bounds, valid
across frames, rechecked on pop — per-frame fixed cost falls from Θ(N log N) to O(events).
Also worth pricing: `apply`'s per-event `root_state_raw` (7 µs ≈ 20 % of an item, `cost_split`)
maintains the same deadline cache eagerly.

**Fit with PRINCIPLES.** "Compute only surprises… Nothing is evolved that can be derived when
looked at" (#3): a deadline for an unmoved player and unresolved item is the same value N times
over. "the algorithm that allocates the work to prevent those heavy tails, it's the most important
one" (#12) and "minimize spike compute and average compute usage" — the allocator's own queue is
the spike. plane.md foundation 7's "nothing takes an unbounded synchronous claim on the frame" is
the premise this run corrects, with the budget unspent while the frame is 8× over.

**The lens.** A quant lens prices schedules but does not ask whether per-entity deadlines are the
right representation at all: a light-cone partition of *cells* (bottleneck 0) might delete the
per-entity deadline entirely, which is cheaper than making it lazy. Timing ran on a shared loaded
x86 box; percentiles are indicative, exponents are the result.
