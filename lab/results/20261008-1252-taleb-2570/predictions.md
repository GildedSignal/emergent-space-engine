# Predictions — the plane's cliff under load (written before the decisive runs)

Instrument: the shipped bench (`cargo run --release -p xtask -- universe --bench`), the same
dashboard that produced H0210/H0211 ("frame p99 2.45–2.72 ms, no hitch"). All prior numbers were
taken at the default load: 48 fleet members, rtf 100, engine budget 5 ms. Nothing has been measured
above that. These predictions are for cases I have not tuned on; Linux/x86 shared runner, so I
predict orders and shapes, not M1 values.

Baseline Fermi: at 48 members the engine fits its 5 ms budget on typical frames (p99 ≈ 2.7 ms).
Fleet events scale ∝ members, so the engine budget first bites somewhere near 4–16× members.
The view gather was already 83% of a light frame at 48 members (H0210 limitation), and I believe
the gather is synchronous and NOT budget-clamped (only `advance` takes the budget), so the frame
wall should grow with members even after the engine clamps.

## Held-out predictions

P1 (tail shape, the load ladder at rtf 100, 30 s): frame p50 grows roughly linearly with members
past the engine clamp; frame p99 and worst-hitch grow superlinearly (convex) once the gather
dominates. Specifically at 768 members (16×) I predict wall p99 ≥ 8 ms and at least a few
hitches > 16.7 ms — i.e. the "no hitch" claim does NOT survive a 16× load by clamping alone.
If instead p99 stays < 4 ms flat in members, the budget clamps everything and my gather model
is wrong.

P2 (the cliff is silent): there is a member count between 4× and 16× where `overflow_frames`
turns positive and `rtf.lowest_1pct` falls below 50% of target, with NO refusal, NO lost
bodies, no panic: the failure mode is silent lag (the horizon falls behind), exactly as
universe.rs §"The budget" promises. Predicted first overflow at 192 or 768 members.

P3 (digest invariance at the cliff): at the most overloaded config that still completes, the
digest at the canonical cut is identical across engine budgets 0.5 / 5 / 50 ms, across
paced/unpaced, and across threads 1/4. This is the load-bearing claim "a budget moves work,
never decisions"; a mismatch is silent nondeterminism (ruin), and I expect it to HOLD.

P4 (loud-vs-silent accounting): lost_bodies stays empty and stats.refused/lost/dissolved stay 0
on the whole ladder; any nonzero value at overload is silent degradation and a finding.

P5 (memory): bytes/body stays roughly flat (order 1 KB) and the resident size stays far below
the 2 GB machine cap up to 1536 members; at plane scale the ruin is time (lag), not memory.

Controls: positive — members 48 at rtf 100 reproduces H0211's order (p99 a few ms, ~0 hitches).
Negative — members 1536 (and rtf 1000 at 48 members) MUST show overflow/RTF dip; if nothing
overflows even there, the instrument is not measuring overload and the run is void.

Kill criteria: if P3 fails (digest differs across budgets/threads at overload), that alone is
the result: a reachable silent-nondeterminism ruin on the flying plane, to be reported with the
exact two commands that differ.
