# Predictions (written before the decisive experiments)

Baseline measured first (main, Linux x86, 8 vCPU, load ~0.4, release build):

- `universe --bench --seconds 30` (rtf 1, 48 members): frame p50 3.32 ms; view_gather share 73.8% (p50 2.38 ms), view_json 14.8%, wire 6.5%, engine 4.8% (p50 0.145 ms).
- `universe --bench --seconds 30 --rtf 100`: frame p50 4.17 ms, p99 10.07, p99.9 12.59, worst 13.6; view_gather share 68.9% (p50 3.42 ms); engine p50 0.24 ms but p99 5.13 ms > the 5 ms budget → 39 overflow frames, rtf lowest 1% = 39.6 (the sim falls to 40× in the worst 1% of time). bodies 76 (28 born + 48 handed-out members), fleet dissolved.
- `universe --kick-bench --rtf 100 --seconds 20`: 949 distinct kicks, median 76 µs, p99 381 µs; exact memo hit 0%, quantized 94.5%.

The two candidate constraints for the goal (billions of bodies, 60 Hz, 8 GB):

- **C1: the view pipeline** (gather + JSON + wire = 82–89% of the median frame) is the only part that touches **every body every frame** (O(N) at fixed frame rate). The engine is event-driven (cost ∝ events/orbit, which the board drives toward 0).
- **C2: the engine's burst tail** (p99 5.1 ms > the 5 ms budget in ~2% of frames; kicks land in bursts: median kick 76 µs, so ~65 kicks in one frame).

## The decisive experiments (not yet run when this was written)

1. **Members sweep** on the plane bench, rtf 100, 10 s: `--members` ∈ {48, 480, 4800}. Members are lattice bodies of the fleet; handed-out members become universe bodies, so this grows both the gather's fleet loop and its bodies loop, and the battle's contact work.
2. **Pure gather sweep** (`view_rel`-style, bare tubes, no engine, no fleet): n ∈ {24, 240, 2400, 9600} emitters at rtf 1 and rtf 100, warm memo, reporting µs/frame and readouts per emitter. This isolates the per-emitter floor of the gather and the memo's behaviour at high rtf (the retarded tick jumps ~339k ticks per frame at rtf 100).

## Predictions

- **P1 (linearity):** view_gather p50 grows linearly in members between 48 and 4800 (R² > 0.98 on the three points after subtracting the 48-member baseline), because the gather is a per-body loop with no early exit.
- **P2 (where the frame breaks):** the per-emitter warm cost of the pure gather is 0.5–5 µs at rtf 1; at rtf 100 it is ≤ 3× the rtf-1 cost (the memo's slope extrapolation keeps the Newton search at ≤ 3 readouts even though the retarded tick jumps ~339k ticks per frame). If instead it degrades (≥ 10 readouts or a search that walks), C1 is worse than the baseline suggests and the memo is rtf-blind.
- **P3 (view vs engine at scale):** at every members count in the sweep, the view pipeline's per-frame cost exceeds the engine's per-frame cost (engine p50 stays < 1 ms; contacts are local and the battle dissolves). If the engine overtakes the view at 4800 members, C2 is the scale constraint instead.
- **P4 (held-out, not tuned on):** at 4800 members the view_gather p50 alone exceeds 16.7 ms **iff** the per-body cost seen at 76 bodies (~28–45 µs, inferred from 3.42 ms over 76 bodies at rtf 100) is real and not mostly fixed cost; the pure-gather sweep (P2) decides which. My prior: the plane's per-body cost is dominated by the doll-chain readout of *bound* tubes (leavers), not by the crossing search, so the plane's per-body cost is ≥ 10× the bare-tube floor.
- **P5 (the tail):** the engine p99 stays above the 5 ms budget at 480 members (more members → more handed-out bodies → more kicks per burst), i.e. C2 worsens with N too, but as a *rate* it stays below C1's per-frame share.

What would make the constraint story wrong: if the members sweep shows the engine overtaking the view (C2 first), or if view_gather per member is < 0.1 µs (the view never binds before memory does at 8 GB).
