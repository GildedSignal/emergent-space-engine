# Dossier — 20261012-0753-quant-dafc (Quant lens)

**Claim.** On the plane's own smoothness dashboard, the frame wall holds everywhere tested
(0 hitches > 16.7 ms up to rtf 1000 and 417 bodies) and game-time delivery dips to an
absolute floor of ~10× real time rather than to zero — but the 5 ms engine budget is
2× too small at 100× (delivery dips) while 15 ms breaks the frame wall (540 hitches/hr),
the knee on this box is 10 ms, and the readout, not the engine, owns the median frame
(61–77% of frame time, growing with members and with rtf).

**Bottleneck.** Board #4 (smoothness and the allocator) and plane.md's "measured on the
whole, from the first flight". Expected gain: not a speedup but the first capacity
frontier of the flying plane — it pins the budget dial (the allocator's only knob exposed
to the frame) to a measured knee, and hands `b-readout-cost` its plane-side numbers.

## Evidence

Machine: GitHub Actions Linux/x86, i7-4790, 8 vCPU, load ~0.3 during every run (recorded
in each report's `uptime_before/after`). Orders of magnitude only; the integrator
re-measures on the M1. All runs seed 1, 20 s paced at 60 Hz unless noted; JSON reports
and `summ.py` are in this folder.

| run | rtf | members | budget ms | overflow | rtf low1% | worst ms | hitch>16.7/hr | engine p99/max | gather p50 | digest |
|---|---|---|---|---|---|---|---|---|---|---|
| r10 | 10 | 48 | 5 | 17 (1.4%) | 9.89 | 13.5 | 0 | 5.1/8.7 | 3.38 | 0c58… |
| r30 | 30 | 48 | 5 | 39 (3.3%) | 9.13 | 15.5 | 0 | 5.3/11.8 | 3.87 | 9f62… |
| r100 | 100 | 48 | 5 | 38 (3.2%) | 9.90 | 11.7 | 0 | 5.2/8.6 | 3.62 | 6ce6… |
| r300 | 300 | 48 | 5 | 54 (4.5%) | 9.98 | 12.7 | 0 | 5.4/8.6 | 3.87 | bd0d… |
| r1000 (5 s) | 1000 | 48 | 5 | 79 (26%) | 2.63 | 13.5 | 0 | 6.5/7.2 | 5.53 | a1ab… |
| b15 | 100 | 48 | 15 | 3 | 100.00 | **23.2** | **540** | 6.4/18.7 | 3.60 | 6ce6… |
| b10 (post-prediction) | 100 | 48 | 10 | 1 | 100.00 | 12.8 | 0 | 2.2/11.2 | 1.27 | 6ce6… |
| m400 | 100 | 400 | 5 | 314 (26%) | **0.00** | 15.0 | 0 | 6.2/7.6 | **5.94** | 45cb… |
| m400r30 | 30 | 400 | 5 | 189 (16%) | 0.00 | 16.6 | 0 | 6.4/10.0 | 4.93 | ee70… |
| unp (unpaced) | 100 | 48 | 5 | 3 | 100.00 | 6.4 | 0 | 1.4/5.7 | 0.72 | 6ce6… |

Reproduce (each ≤ 25 s): `cargo run --release -p xtask -- universe --bench --rtf R
[--members M] [--engine-ms B] [--seconds S] [--unpaced]`, then
`python3 lab/results/20261012-0753-quant-dafc/summ.py <report.json>`.

1. **The frame wall holds; delivery dips to an absolute floor.** Zero hitches above
   16.7 ms on every budget-5 run, worst 15.5 ms, up to rtf 1000 and 400 members. The
   worst 1% of frames deliver ~9–10× real time *regardless of target* (low1 = 9.89,
   9.13, 9.90, 9.98 at rtf 10/30/100/300): the dip floor is ~10× absolute (≈ 160 ms of
   game per 16.7 ms frame), not a fraction of the target. It collapses only under real
   saturation: members 400 → low1 = 0.00 (frames that present nothing), rtf 1000 → 2.6.
   The overflow count grows with rtf (17→54) and members (38→314), so the dips are
   steady-state churn, not just cold start (worst frames sit at frame 36–1018 of 1200).
2. **The budget is a smoothness dial with a knee at 10 ms (this box, 71 bodies, 100×).**
   5 ms: dips (low1 9.9, 3.2% overflow). 10 ms: perfect on both axes (low1 100.00,
   1 overflow frame, 0 hitches, worst 12.8). 15 ms: delivery perfect but the frame wall
   breaks — 3 hitches > 16.7 ms (540/hr), worst 23.2, engine max 18.7. A bigger budget
   lets one expensive item batch overrun the frame deadline: the budget bounds the
   *number* of items, never the *cost* of one item (engine max is up to 2.4× the budget
   even at 5 ms).
3. **The readout owns the median frame; the engine owns its tail.** Gather share
   61–77% of summed frame time on every run; gather p50 3.4→5.9 ms from 71→417 bodies
   and 3.4→5.5 ms from rtf 10→1000 (the view cache's light-cone guesses go stale when
   the player moves fast); engine p50 is 0.13–2.35 ms. Scaling the fleet taxes the
   gather, not the engine (m400: gather share 0.61 vs engine 0.25).
4. **Overflow churn taxes the gather stage.** r100 vs b10: identical digest, but gather
   p50 3.62 vs 1.27 ms (2.8×) and frame p50 4.61 vs 1.78 ms. With the backlog cleared
   (b10) the same bits are produced with a third of the frame time. [INFERENCE:
   cache/frequency duty-cycle effects — the mechanism is not measured; Linux/x86 only.]
   The unpaced control frames the effect: gather p50 0.72 ms, 5× cheaper than paced.
5. **Schedule independence verified on the flying plane.** r100, b10, b15, unp share
   digest `6ce636fa13458efb5f9ab7d6` at cut 406050894: budget and pacing change when
   work is done, never what ("a budget that bites delays work and never moves a
   decision" — the contract holds end to end).

## Predictions (predictions.md, written before the sweep; smoke = rtf100/5 s only)

- P1 (overflow > 10% and low1 < 90 at rtf 100, 20 s): **wrong** — 3.2%, low1 9.90. The
  smoke's low1 = 0.00 was a cold-start artifact of the 5 s window (1% of 300 frames =
  3 frames). Lesson: 1st-percentile service levels need ≥ 20 s windows.
- P2 (first overflow between 10 and 30): **wrong side** — overflow already at rtf 10
  (1.4%). By my frozen rule R* = 10; the rule itself is mis-specified (0.9·R at R = 300
  demands no dip below 270× for even one frame — error size in disguise, the integrator's
  known criterion failure mode in r2/r8). The behavioural invariant is the absolute dip
  floor (~10×) plus the hitch counts.
- P3 (frame wall protected to rtf 1000): **right**, and it also held at 400 members.
- P4 (budget 15 fixes delivery without breaking frames): **inverted** — it breaks the
  frame wall (540 hitches/hr). The post-prediction b10 cell found the knee.
- P5 (members 400: ≥ 50% overflow, engine share > gather): **wrong** (26%; gather 0.61 ≫
  engine 0.25), right that low1 = 0. Members tax the readout, not the engine.
- P6 (digest identical across budgets and pacing): **right** (4 runs, one digest).
- P7 (budget's soft edge persists): **right** (engine p99 > budget at 5 and 15 ms; max
  2.4× budget — the budget bounds item count, not item cost).

## What would make it wrong

The knee (10 ms) and the dip floor (~10×) are scene- and machine-dependent: measured on
one star system (71–417 bodies), one seed, Linux/x86 with its frequency governor. The M1
is fanless and throttles by heat, so the knee moves (probably down under sustained load);
the digest control is machine-independent, the frontier is not. The gather-churn
mechanism (claim 4) is inference, not measurement. b10 was added after predictions
(disclosed); no cell was re-run or tuned away.

## Cost of adoption, and fit

Adoption is a one-line change (`ENGINE_BUDGET_MS`) plus re-measuring on the M1 — but the
real deliverables are the frontier and the two named levers: item-cost bounds (the budget
cannot cap a single rebinding burst or fleet epoch batch) and the readout's members/rtf
scaling (feeds `b-readout-cost`). Fits PRINCIPLES #12 ("minimize spike compute and
average compute usage so that you get a bigger simulation that runs smoothly", OC#36) and
the law of the plane ("bounded work per presented frame", plane.md §7); the dip-floor
result is "errors never compound" translated to service level (dips bottom out, they do
not spiral). The lens's blind spot applied: I priced tails and left the representation
alone; my own kill rule repeated the integrator's error-size-in-disguise habit and my
data caught it.

## The lens

The quant lens prices everything per event and may overweight tail discipline over
representation change: the two biggest levers found (item-cost bound, readout scaling)
are structural, not scheduling, and a lens that only tunes budgets would miss them. It
also nearly reported the smoke's low1 = 0.00 as a finding — the multiple-testing trap
caught by the longer window, not by caution.
