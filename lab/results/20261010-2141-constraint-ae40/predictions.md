# Predictions (written after the rtf-100 baseline, before the sweeps)

Baseline (tuned on): rtf 100, 30 s, 76 bodies + 48 fleet members. Frame p50 4.4 ms;
view_gather share 0.697, engine 0.172, json 0.092, wire 0.039; engine p99 5.17 ms
(budget 5 ms), 42/1800 overflow frames; us_per_item: player 1315, ship 268, fleet 60.

Held-out cases (not yet measured) and what I expect there:

1. **rtf 1000, same scene**: engine p50 grows ~10x to 2–3 ms; the 5 ms budget binds at
   p90+ (overflow frames > 10%); view_gather ms/frame stays ~constant (per-frame, emitter-
   driven, not game-time-driven) so the frame stays view-bound at the median.
2. **rtf 10000**: the engine budget is the binding constraint outright — rtf.median falls
   below target (engine cannot advance 167 game-ms per 5 wall-ms), overflow frames > 50%,
   and hitches above 16.7 ms appear (engine + view together exceed 16.7 ms in some frames).
3. **members 400 at rtf 100**: fleet items scale ~8x; engine p50 grows to ~1.5–2.5 ms
   (fleet-dominated, still under budget); view_gather unchanged or slightly up; the frame
   stays view-bound; player remains the max us_per_item by >= 4x.
4. **threads 4 at rtf 10000**: if the fleet/lattice work parallelises, engine per-frame
   time falls ~2–3x and rtf.median recovers toward target; if threads touch only the
   lattice clock, the change is small (< 1.5x). I expect the latter-ish (modest), because
   the player and ship events resolve on the one frame thread.
5. **The p99 engine spike is cadence-shaped, not load-shaped**: at members 400 the engine
   p99 stays within ~2x of its rtf-100 value per item class; the spike comes from kick
   boundaries landing in the same frame (aligned block steps), so it should persist as a
   multiple of the per-item cost, not grow with member count per event.

Kill criterion for the lens's claim: if the engine (not the view) already dominates the
median frame at rtf 100 with 76 bodies, or if the player's per-event cost is not the max
by >= 4x across all sweeps, the "view-bound frame / player-bound engine" reading is wrong.
