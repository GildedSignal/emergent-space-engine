Working...
Check complete. `lab/results/20261009-1754-quant-f2f7/check.md` written; nothing else in the run folder touched; tree restored to clean.

**Grade: silver.**

What I did and found:

- **Reproduced** from `work/patch.diff` on a clean tree: deterministic event counts bit-identical at every N (293 / 18 814 / 150 040 / 1 207 775, same kick/open/boundary splits); per-event 17.7–19.4 µs (author 16.8–19.4, shared box); allocs 5.94/event; cold/hot = 1.07 on a quiet run (my first run's 33 µs hot was load noise — pool-cold and clflush bracketed the author both runs); stages and `cost` all match; budget arithmetic verified by hand.
- **Verified the central claim independently**: `from_state` = 12.4 µs on the scene's *own* 512 readout states (not just `cost.rs`'s orbit), called exactly once per kick (`step.rs:381` → `bind_in:226`) → the ~60 %-of-kick share stands for near-circular orbits.
- **Two corrections to the headline**: `plan_interval` emits one kick *and* one boundary per interval (`step.rs:502-503`, 46 % of measured events at ~equal cost), and the default cadence is `step_log2 = 7` ≈ 557 events/orbit — so "the engine sits on the budget line today (19.7 µs)" is ~2× over at the 64-kick target and ~8× over at today's cadence; and the incremental-rebind lever is 1.4–1.5× whole-engine by mix arithmetic, not 1.7–2.5×. Both corrections *sharpen* the author's own conclusion (cadence, not per-event polish).
- **Adversarial cases**: `from_state` at e = 0.5 costs 43 µs, at e = 0.9 costs 101 µs — the flat ~20 µs event is a near-circular fact; a passage state is refused outright; per-event cost grows with settle depth (12 µs at h = 4e11 vs 18.5 at 2.5e12), so the p99 claim doesn't extrapolate to an hours-long game.
- **Novelty**: H0210 recorded "kicks cost 29 µs" and `cost_split.rs` pre-existed (author disclosed in P2); the rebind share, N-flatness, allocator counts, cold/hot kill, and budget derivation are new. Predictions provably preceded the decisive run (18:00:52 < 18:04:13); the author's honest miss list matches mine.

Gold path named in the check: the delta-rebind probe, measured whole-engine on near-circular *and* eccentric populations, with the budget recomputed on all events.
