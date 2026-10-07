# Predictions (written before the decisive runs)

Baseline measured first (not tuned on): `universe --bench --seconds 30 --rtf 100` on this machine,
76 bodies, frame p50 1.54 / p99 9.94 ms, engine share 18.9% (p99 5.06 ms, at the 5 ms budget cap),
view_gather share 67.5%, RTF median 100, lowest 1% 39.6, 27 overflow frames.

## P1 — the engine budget is not the throughput constraint at this scale
Run `--rtf 100 --engine-ms 12 --seconds 30` (paced):
- overflow_frames drops (fewer than 27) but I do NOT expect 0: the overflows are burst work
  (settle, handouts, the player's O(doll) checks), some of it beyond any budget that fits a frame.
- lowest-1% RTF rises above 39.6.
- frame p99 stays under 16.7 ms (engine and view still fit together).
- **digest identical** to the baseline (the budget changes when work is done, never what).

## P2 — the engine's true demand is modest; the view is the frame's constraint
Run `--rtf 100 --engine-ms 1000 --unpaced --seconds 30`:
- engine p99 demand < 8 ms (bursts included), i.e. the 5 ms cap clips only a few frames;
- view_gather share of frame CPU ≥ 60% again (it scales with bodies, not with the budget);
- digest identical again.

## P3 — view cost scales with member count through serialisation, not through Newton
Run `--rtf 100 --members 400 --seconds 30` (≈ 8x the fleet members, bodies ≈ unchanged):
- view_gather p50 grows by less than 2x if members stay in frames (they are extrapolated, no
  per-member Newton); the bodies that leavers become do cost a readout each;
- view_json grows near-linearly with members (every member pushed and serialised every frame);
- total frame p99 stays under 16.7 ms (this is still a small scene).

## P4 — the player's per-event cost is O(doll bodies), not O(1)
From the baseline's engine_cost_by_kind (no new run): player 907 µs/item vs ship 220 µs vs the
pure kick resolver's 64 µs (kick-bench). I predict the gap is the player's neighbourhood check
reading every body of its doll: measured cost per player event should grow ~linearly with the
bodies in the player's doll. I verify this by reading the code path (no time for a scaling run):
if `encounters_for_player` iterates all bodies, the prediction stands as a code-confirmed lead.

## Kill criterion
If the digest changes across budgets, or engine p99 (unpaced, uncapped) exceeds ~12 ms, the
constraint story is wrong: the engine, not the view, is the frame's constraint, and I say so.

## Outcomes (added after the runs)
- P1 HELD: budget 5→12 ms: overflow 27→1, lowest-1% RTF 39.6→99.99, frame p99 11.1 ms, digest identical (41343a14…).
- P2 HELD: uncapped unpaced: engine p99 1.24 ms, max 12.7 ms; gather share 69.8%; digest identical.
- P3 HELD with a correction: members stay in frames and are cheap; the cost driver is *bodies*
  (leavers become bodies): gather p50 1.11→3.85→6.47 ms at 76/221/428 bodies = 14.6/17.4/15.1 µs
  per body per frame, linear. Frame p99 hit 14.5 ms at 428 bodies, 403 overflow frames,
  lowest-1% RTF 0.0 — the "stays under 16.7 ms" clause failed at 221 bodies' p99.9 (16.86 ms).
- P4 PARTLY: `encounters_for_player` calls `self.encounters.find(&ctx, p, t, interval)`
  (crates/universe/src/universe.rs:944), the exact per-doll check of plane.md foundation 6;
  player cost 907→2459→3424 µs/item at 76/221/428 bodies (grows with doll population,
  sub-linear in these runs). Code-confirmed, not isolated by a run.
- Kill criterion did not trigger: digests matched across all budgets; uncapped engine p99 1.24 ms.
