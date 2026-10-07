# Predictions (written before the decisive experiment)

Tuned on: seed 1, rtf 100, 20 s (949 samples, kick_us_leavers median 91.45 µs, kick_us made 35.15 µs, replay_digest eaef383e…).

Change under test (round 1): carry the decoded `OrbitState` from the kick's own readout into the rebind's proper-time bookkeeping, and cache the binding's proper time at its event (`proper0`, taken from the `Bound.orbit` the fit already produced). Bit-identical by construction: the same `decode` Scalars, no new arithmetic paths.

Tuned on: seed 1, members 48, rtf 100 (the leaver kick median).

Held-out cases (not tuned on): seeds turned out not to change the scene (identical digests at seeds 1–3), so the held-out axes are the population and the cadence: `--members 24`, `--members 96` and `--rtf 60`, plus the p99 tail and the whole test suite.
1. **`--members 24`, `--members 96`, `--rtf 60`** (20 s each): I expect the leaver kick median to drop 8–15 % and the made-kick median to drop 5–12 %, with `refused` staying 0.
4. **Share**: a re-profile should show `u_tau2` collapse from ~2 % of total to ~0, with `compile`'s share rising correspondingly (its absolute cost unchanged).

Kill criterion for the round: median gain < 10 % on the tuned case, or any digest difference, or any test failure.

If round 1 holds, round 2 (a per-(source, tick) decode memo inside one frame's force reads) I predict to be worth < 10 % (u_secs+u_tide ≈ 7 % of a leaver kick) and expect to revert it on cost/complexity grounds; I will measure one variant before deciding.
