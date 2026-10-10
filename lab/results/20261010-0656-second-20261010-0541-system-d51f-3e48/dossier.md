# Dossier — run 20261010-0656-second-20261010-0541-system-d51f-3e48 (second author on 20261010-0541-system-d51f)

## Claim

The named experiment is done: the incremental deadline (the last doll-chain readout carried
forward by its velocity — the arrival rate `1 + n·β` in position form, re-anchored by a real walk
only when the carried displacement could pass 1/8 of the light distance) deletes the scheduler's
per-event walk (1123 → 42 walks at seed 7 rtf 100; 4224 → 42 at rtf 1000) with the universe
digest and the gathered view **bit-identical at settle cuts in all eight flight configurations**
— but the saving lands in the **mean** engine frame (−26.6 µs, exactly the walk tax), not the
median: the median frame carries ~2 events, so the original's "46% of the median engine frame"
was a mean-per-frame number read against a median frame, and the checker's expected "~26 µs off
the median" is falsified in that form (the median drops only where its frame carries the events:
−86 µs at rtf 1000).

## Bottleneck

Board #1 (kicks dominate) at the scheduling layer: the same finding as the silver run — the
retarded readout is the cost atom — with the deletion now **built and measured** instead of
designed. What it deletes: `Universe::apply`'s per-event `root_state_raw` walk (the queue's lack
of the arrival rate, repaired per event), amortized 26.7× at rtf 100 and 100× at rtf 1000; the
per-kick read cost of the coming news gravity keeps its full per-(source, kick-epoch) budget.

## Evidence (Linux x86, shared runner, 8 vCPU, orders of magnitude only)

`cargo test --release -p emergent-universe --test lab_arrival -- --nocapture --test-threads=1`
(≤ 10 s; full log in `run-log.txt`; the original record regenerates in the same command):

- **Digests and views at settle cuts** (`frame_to` with `limit`, `settle`, `digest`, then one
  gather): equal, asserted, in all eight configurations — plane seeds 7/3/99 at rtf 100, seed 7
  at rtf 10 and 1000, stream at 0.99c toward/away/toward with the observer at 0.9c — and at all
  three staleness floors. The design's own claim (the digest is "independent of schedule") holds
  under a real scheduling perturbation for the first time on this record.
- **Walk amortization**: seed 7 rtf 100: 1123 → 42 walks (0.397 → 0.015 per event); rtf 1000:
  4224 → 42; rtf 10: 94 → 38. The 42 are ~one anchor per body over the whole flight.
- **Where the saving lands**: seed 7 rtf 100 engine **mean** 399.0 → 372.4 µs (−26.6; the walk
  tax is 1123 × 7.18 µs / 300 = 26.9 µs), seeds 3/99 −18/−21 µs, rtf 1000 −93 µs (mean) and
  −86.7 µs (**median** 1094 → 1008, where the median frame carries 38 events); the **median** at
  rtf 100 is flat within noise (54.8 → 57.8 µs; the median frame carries 2 events ≈ 14 µs of
  walk). Presented time before the settle identical to 4 digits in every configuration.
- **Deadline error at the cut** (the records are identical there): median 2.1e3 ticks = 0.6% of
  one rtf-100 frame; max 2.07e6 ticks on a body 5.72e8 ticks away = 0.36% of its light distance
  (inside the 12.5% bound; near-doll bodies err in hundreds of ticks). The floor knob trades
  walks for near-body accuracy (42/147/438 walks at floors 1e6/1e4/1e3) without moving the max
  (far bodies anchor once by construction of the flight).
- **β→1**: the stream flights have **0 events** (no shipped scene has relativistic events — a
  stated limit, so the deadline carry under β→1 *kicks* is not exercised); digest and view equal
  there anyway, and the carry itself against the walked readout along inertial 0.99c worldlines
  is 5.5e-8 relative over 5e7 ticks — f64 noise, flat in t: the position form does not degrade
  where the rate form (`1 + n·β` → 0.01 closing, 1.99 receding) is at its worst.
- **The original record regenerates** on this machine (2827 events, 36594 levels, 2.9% memo hit
  share, 1123 walks at 7.18 µs/call vs the dossier's 7.13–7.17), and the checker's defects are
  fixed in the shipped test: the stream control now resets before the gather it measures (7680
  levels, 0 hits, 0.0% — their corrected control's numbers exactly), and per-call vs per-level
  costs are no longer conflated (7.18 µs is per call; the plane's average chain depth is 2.04).
- Default path untouched: with both flags off (the default) the engine is the original code path;
  the crate's full test suite passes (`cargo test --release -p emergent-universe`).

## Predictions

`predictions.md`, written before the decisive run. **Held**: amortization ≤ 150 walks (1: 42);
digests equal everywhere (3) — the experiment's core; views equal (4); presented time ≥ 90%
(6: identical to 4 digits); rtf-10 dilution (7). **Falsified and reported**: the engine **median**
drop (2: predicted ≥ 20 µs; measured flat — the median frame has no walk to delete; the mean
drops by exactly the predicted amount); the deadline error's relative form (5: predicted max
< 15% of distance, measured 250× on near bodies in relative terms — but 2.1e3 ticks absolute;
the bound I can actually prove is `|Δd| ≤ ⅛·(dist_anchor + floor)`, and the worst absolute error
is 0.36% of the worst body's distance).

## What would make it wrong

The digest equality is the load-bearing result and it is asserted, not sampled; if a scene exists
where the scheduling order leaks into outcomes (a lane whose `pull` is not a full dependency
closure, or a prune that needs the walked distance), the incremental deadline would surface it —
that would falsify the *engine's* schedule-independence claim, not just this mode, and is worth a
run of its own. The β→1 regime is untested where it bites (relativistic kicks); when the motion
law v2 brings β→1 flights, the carry's re-anchor cadence must be re-measured there. Timings are
one shared Linux runner (medians bounce ±20% run to run; the mean drops match the walk-count
arithmetic in all five plane configs, which is the stable signal); the integrator re-measures on
the M1.

## Cost of adoption, fit with PRINCIPLES

One owner moves `pos`/`pos_v`/`pos_t` from the lab flag into `Universe` (three arrays plus one
branch in `apply` and one extrapolation in `light_distance`), deletes the per-event walk, and
re-derives `REL_DEADLINE`/`FLOOR_DEADLINE` from the scheduler's actual error tolerance before the
news-gravity build amortizes readouts per (source, kick epoch). Fit: "Compute only surprises" (3:
a body whose state has not changed was re-read at full cost per event), "the best part is no
part" (17: the walk is deleted, not optimized), "a fix signals the wrong representation" (19: the
deadline walk repaired the queue's lack of the arrival rate; the carry is the representation that
does not need the repair).

## The lens (what this lens may have made me miss)

The second-author lens took the checker's experiment as specified and confirmed its physics but
corrected its unit: "median frame" was the wrong instrument for a per-event tax that concentrates
in heavy frames — the same mean/median conflation the checker flagged in the original, reborn in
its own gold criterion. What remains unmeasured: whether the 42 anchor walks can be deleted too
(anchor at handouts and rekeys only), and whether the *view* gather — 13–18× the engine — should
take the arrival-rate carry as its Newton guess (the `Crossing.slope` it already stores is that
rate, measured; reusing it across the two mechanisms is the same unification, one step further).

## Artifacts

- `crates/universe/src/observe.rs` (the lab module: counters, memo, incremental flag, floor),
  `crates/universe/src/universe.rs` (`pos_v`/`pos_t`, `body_pos`, the re-anchoring `apply`,
  `light_distance_at`, `next_deadline`), `crates/universe/tests/lab_arrival.rs` (the original
  measurements with the corrected control, and the incremental-deadline experiment).
- Machine state: Linux 6.8.0, 8 vCPU, load 0.9–1.2 during the runs, 12 GB available.
