# Predictions (written before the decisive sweep, 12:24 UTC)

The decisive experiment: `PROBE_HAULERS` sweep (12 default, 60, 240) on
`universe --bench --rtf 100 --seconds 10`, plus `--members` 4 vs 400. Sections timed by the
probe patch (body crossings vs fleet members vs player readout).

Cases not tuned on, and what I expect:

1. **Body crossings dominate the gather and scale linearly with visible bodies.**
   Expect body_crossings/frame ≈ (8–20 µs) × n_bodies at rtf 100; fleet_members/frame flat
   in haulers. If body_crossings/frame is flat in haulers, my constraint claim is wrong.
2. **Fleet members are ~40× cheaper per emitter than bodies** (measured 0.39 µs vs ~15 µs
   on the 30 s run). Expect the members sweep (4 vs 400) to move fleet_members/frame
   linearly at ≤ 1 µs/member and body_crossings/frame not at all (members live in the
   frame, not the doll). If members move the body section, the split is misread.
3. **Warm-cache crossings cost about 1–2 readouts per body per frame.** Expect
   gather_last_readouts ≈ (1–2) × n_alive_bodies, independent of rtf. If it is ≥ 4, the
   cache is cold and the per-readout story (b-readout-cost) is not the whole cost.
4. **Readouts concentrate on ships, not planets/moon.** The engine_cost_by_kind shows
   planets/moons at 0 ns (compiled drift). If the view's per-body cost were dominated by
   planets instead of ships, the readout lens (b-readout-cost) targets the wrong bodies.
5. **Frame ceiling**: extrapolating the measured slope, the view alone eats a 16.7 ms
   frame at ~10³ visible bodies (order of magnitude). If the sweep shows a sublinear
   slope (log or saturating), the ceiling recedes and the engine (kicks, 50 µs each,
   growing with N and rtf) is the true scale constraint instead.

Also recorded: run-to-run p50 on this shared cloud box swings ~4× (3.5 → 0.85 ms) with
identical digests, so all claims below use within-run shares and orders of magnitude,
never absolute p50s across runs.
