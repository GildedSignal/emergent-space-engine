# Predictions — the plane's time-zoom envelope (written before the sweep)

Question: where does the shipped plane (`xtask universe --bench`, seed 1, one star system) stop holding its claimed smoothness as game-time-per-real-second (rtf) grows, and which subsystem binds first? Nothing below is tuned on; rtf = 1 and rtf = 100 are the known anchors (HANDOFF: "flying at 100× and more with no hitch in CPU time"), everything above 100 is held out.

Fermi before measuring: the engine resolves surprises (kicks, conjunctions, handoffs) whose rate per game-second is roughly fixed by the scenario (a handful of bodies, 48 fleet members). At rtf R a frame covers R/60 game-seconds, so surprises per frame ∝ R. The engine budget is 5 ms/frame. If the plane's surprise rate near the player is ~10²–10³ events per game-second (a fleet plus a planet and moon), the budget bites around R ≈ 10³–10⁴. The view is bounded by what is on screen (60 presented frames/s regardless of R), so the view share should stay flat while the engine share grows.

1. **Frame CPU p99 vs rtf:** flat (within 2× of the rtf = 1 value) up to some rtf₀, then rising roughly linearly in rtf (work per frame ∝ game time per frame). I expect rtf₀ between 10² and 10³.
2. **Where the budget bites (rtf_median < 90% of target, or overflow_frames > 0):** between 10³ and 10⁵. Below 10³ the plane should be CPU-flat (the claim); above 10⁵ it should be engine-bound, not view-bound.
3. **Share shift:** `where_the_time_goes_ms.engine.share` grows monotonically with rtf once past rtf₀; `view_gather` and `view_json` stay within 2× of their rtf = 1 values at every rtf.
4. **Determinism at the extremes:** at one rtf and seed, paced vs unpaced and engine budget 5 vs 50 ms give the *same* digest at the same canonical cut ("a budget that bites delays work and never moves a decision"). If this fails at high rtf, that is a law break, not a performance number.
5. **The binding subsystem is the engine's event work** (kicks/encounters), visible as `events_per_second` and the engine cost per item growing with rtf — not the view, not the wire.
6. **Losses:** the scripted player's burns are functions of nominal frames; at very high rtf each burn spans much more game time, so I expect `player_alive` to eventually go false (a burn ends in the planet). That is a script artifact, not a plane failure, and I will say which it is by comparing the death tick across rtf.

Kill criterion for the plane's claim ("no hitch in CPU time at 100× and more"): any rtf ≤ 10³ where frame_cpu_ms p99 exceeds 16.7 ms (a full frame) or hitches_per_gameplay_hour above 50 ms is nonzero at paced 60 Hz.
