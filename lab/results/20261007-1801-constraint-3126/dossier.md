# Dossier — 20261007-1801-constraint-3126 (lens: the constraint)

## Claim

The plane's one constraint is the **readout, not the engine**: the view gather is the frame's dominant cost (54–69% of frame CPU at 71–410 bodies, ~7.9 µs per body per frame, one light-cone Newton solve per body per frame), while the engine is already surprise-driven (0.05 events per body per game-second, scale-free) — and 92.9% of the gather's per-body Newton work at rtf 100 (100% at rtf 1, 78.6% at rtf 1000) changes the displayed output by less than one display quantum, so a quantum-driven readout (carry the display state; re-solve on a quantum crossing, an emitter event, or first light) is the Goldratt *exploit*: ~10× off the frame's dominant cost with no new part and no law change.

## Bottleneck

Board item "the readout's cost" (in the queue as a build) and, behind it, "fewer kicks per orbit" (the engine's tail). Measured chain on the whole plane (`xtask universe --bench`, the player's own loop):

- At the player's setting (rtf 100, 30 s paced): frame p50 4.44 ms, p99 10.7 ms, 0 hitches — smooth, but **view_gather 69.3%**, engine 17.6%, JSON 9.2%, wire 3.8%. Unpaced ceiling ≈ rtf 1,500 on 76 bodies; the gather's share is the same unpaced (69.6%).
- Scaling members 48→400 (the harness caps `--members` at 400): gather p50 0.90→3.56 ms, frame p50 1.44→5.96 ms; **marginal gather cost 7.9 µs/body/frame**, linear. The engine's events per body per game-second stay 0.046–0.054 (scale-free: compute follows change already).
- Probe (`crates/universe/examples/viewdrift.rs`, this run): readouts p50 ≈ one per body per frame (292 at 410 bodies) — the gather re-solves every worldline every frame. But only **28 bodies are even seen** (242 of 270 alive are still beyond first light and cost 1 eval each to rediscover that), and of the seen ones **92.9% change sub-quantum** (1 px @1080p/90° FOV, 1 sRGB step, 1% shift) per frame at rtf 100; 100% at rtf 1 (median sub-quantum streak 162 frames = 2.7 s), 78.6% at rtf 1000.
- At the goal's far scale the readout is also the binding piece: `galaxy --bench --ships 1e9` renders a billion ships at 0.032 ns/ship/frame (aggregation works) but the frame is 32 ms at 960×540 on 4 x86 threads — 2× over the 16.7 ms budget, orders-of-magnitude only (M1 to re-measure).

Expected gain: the gather's Newton load drops by the miss + sub-quantum fraction ⇒ ~10× on the gather at rtf 100 (~160× at rtf 1), frame p50 5.96→~3 ms at 409 bodies. What it deletes: the per-frame per-body solve for everything the display cannot differentiate — the last O(N)-per-frame piece in the frame loop.

## Evidence

All commands ≤ 60 s (Linux/x86, 8 vCPU, load 0.6–3.0; raw JSON in `raw/`):

```
cargo build --release -p xtask                                            # 38 s
target/release/xtask universe --bench --rtf 100 --seconds 30              # 30 s, paced, the player's loop
target/release/xtask universe --bench --rtf 100 --seconds 30 --unpaced    # 2 s
for M in 48 480 4800; do target/release/xtask universe --bench --rtf 100 --seconds 10 --members $M; done
target/release/xtask galaxy --bench --ships 1000000000 --tubes 1000000    # 20 s
cargo build --release -p emergent-universe --example viewdrift            # probe added this run
taskset -c 0-3 target/release/examples/viewdrift 1|100|1000 10 48|400     # ~3 s each
target/release/xtask behave --law plane                                   # 100 s; B13 60/64; see below
```

B14 under the plane law exceeds the 60 s watch and `exit(1)`s the run, so gates after B14 never ran (reproduced once in isolation: 60.0 s wall, 95 s user CPU — computing, not hung; `raw/b14.txt`).

Key numbers in `metrics.json`; probe source saved as `viewdrift.rs` beside this dossier (it is also in the tree patch).

## Predictions

Written before the probe (`predictions.md`). **P1 held** (92.9% ≥ 60% sub-pixel; 100% < 10 px). **P2 held** (readouts ≈ 1/body/frame: 292 at 410 bodies). **P3 failed as written**: the *median* sub-quantum streak at members 400 is 2 frames, not >10 — the population is bimodal (low-orbit leaver ships break every 1–2 frames; the distant majority rides 15+ frames; at members 48 the median is 128). **P4 held** (colour 100% sub-step). Honest refinement: the carry is not one cadence for all bodies; it is per-body, set by drift rate ÷ quantum — which is the point of a quantum-driven readout.

## What would make it wrong

- If the gather's cost is not Newton-dominated: the probe counts evals but does not time the eval separately. The marginal 7.9 µs/body/frame and readouts ≈ bodies/frame make state_rate the only per-body variable work, but a profiler on the M1 could shift the split between crossing evals and per-body bookkeeping (names, `rest()`); the bookkeeping part would not be saved by carrying crossings.
- If the display quantum is judged smaller than 1 px/1 sRGB step/1% (e.g. HDR, zoom, or the player's instruments read raw values, not quantized ones — "your dials are made up", DC), the sub-quantum fraction drops; at rtf 1000 it already drops to 78.6%.
- If the plane's content is not representative (mostly distant heliocentric bodies today): a fleet-engagement scene would lower the fraction — but that scene is exactly where members are already carried without Newton.

Cost of adopting: a change to `gather_with` (carry per-body display state; re-solve on quantum crossing / emitter event / observer velocity change — aberration of a carried direction composes without re-solving the crossing; a first-light skin: one subtraction per not-yet-visible body, their first-arrival envelope is computable at genesis). The digest is untouched: the gather is a pure read ("observation is a pure function of the state"), so a carried readout changes no outcome, only when readouts are computed — same guarantee as the engine's budget.

Fit with PRINCIPLES: "Compute only surprises. Cost follows change and entropy. Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (P3) — the view is named, and today it is the one component that pays per body per frame instead of per change. "The floor is what the player can differentiate" (Julien, 29 September) and "the zoom level is the minimap" (OC#30) are the same law at the readout. P1 ("The cheapest compute is compute not done. Delete before optimizing") says: delete the redundant solve, don't make the solver faster.

## The lens: what it may have made me miss

Goldratt names one constraint and everything else is waste — but the goal has a portfolio (smoothness now, 10⁹ later, GR behaviours always). I measured the frame's constraint (readout) and the scale readout (galaxy render over budget on x86); the *physics* constraint (B12's broken instrument, B13's 4 marginal flybys, E9 phase 2) is not a throughput constraint and this lens under-weights it. Also: this lens measures, it does not build — the exploit here is a design decision plus numbers, not code; the build (the quantum-driven readout) is a next step, and the queue's "readout's cost" item is where it lands. Two harness defects noticed in passing, for the integrator: `behave --law plane` prints unanswered old gates (G1–G11, B7) as `FAIL ... inf`, which reads as catastrophe where it is "not implemented"; and B14 under the plane law exceeds the 60 s watch and `exit(1)`s the run, so gates after B14 never ran (reproduced once; `/tmp/b14.txt` — raw copy in `raw/` only if it finished before the window closed).

## Grade (author's self-assessment)

Silver: the constraint is named on measured whole-plane data, the redundancy quantified with a pre-registered probe, and the exploit is adoptable in one step — but it is a measurement, not a built change, and the 10× is a ceiling, not a measured post-change number. The gold version is the quantum-driven gather built and measured on the same dashboard.
