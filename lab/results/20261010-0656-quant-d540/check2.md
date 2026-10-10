Grade: gold

Abstract: Claim: the plane's presented frame is Ω(N) at zero events (~0.7 µs/body/frame of deadline bookkeeping), breaking 16.67 ms at ≈3×10⁴ live tubes (0.72 s at 10⁶), and one exact player-neighbourhood find breaks a player item at ≈8–10⁴ (3.0 s at 10⁶); fix the queue before `b-belt-wire`. All commands reproduce in a clean tree: control digest EQUAL/1674 events; 10⁵ frame 63.6 ms sched-only 67.3 (author 55–68); 10⁶ 908 ms, find 3.36 s, RSS 1.93 GB (author 721 ms, 3.0 s, 1.93 GB — load 4 vs 2.2). Adversarial: eccentric ships, rtf=1000, threads=8, fresh strides — none move the wall. Gain: names ≥700× of scheduling fat at 10⁶; adoption is one digest-invariant step.

## Reproduction (clean tree, `git apply work/patch.diff`, load 1.8→4)

- Control: `nwall control` → `events settled 1674, digests 4c390dfb…c70a 4c390dfb…c70a (EQUAL)` — identical to the author's, non-vacuous.
- Main sweep (rtf 100, stride 2654435761): 100 → 27 µs; 10³ → 194; 10⁴ → 3601 (hits 11); 10⁵ → 63 568 (sched-only 67 306, rekey 11 108, hits 90); events 0 at every N. Author's numbers matched within 1.2× (my 10³ is 1.9× faster at lower load).
- Fresh layout (stride 40503): 14/3319/58 972 vs author 14/2236/55 019 — 1.5× under load 3.9; the curve reproduces.
- rtf 1 vs 100 at 10⁴: 3767 vs 3601 µs — per frame, not per game-second ✓.
- Far end (load ~4): 3×10⁵ → 316 584 µs; 10⁶ → 908 234 p50 / 711 043 sched-only / 118 994 rekey, events 0, find 3 358 989 µs (842 hits), peak RSS 1 929 920 KB — the author's 721 515/795 481/117 868/3 010 890/1 930 272, same orders, direction explained by load.
- Break points re-derived from my own numbers: frame crosses 16.67 ms at ≈3×10⁴; one find (16.6 ms at 10⁴, 1.67–3.36 µs/body linear) crosses at ≈10⁴. Both as claimed.

## Held-out predictions

`predictions.md` (21 min before results.md/patch, 36-min-old prompt) freezes P1–P5 with a kill rule. P1: 154× (author), 328× (mine, 10³→10⁵), events 0 ✓. P2: sched-only = frame, −0.5% to −22% across N (the "~100%, ±5%" is slightly optimistic under load; rekey alone 10–17%) ✓. P3: ≈3×10⁴, the low edge, disclosed ✓. P4: 1.6–3.4 µs/body, crossing ≈8–10⁴ ✓. P5: EQUAL + nonzero events + layout within 2× ✓.

## Attack (my cases)

1. Eccentric ships (e up to 0.125, per-ship spread): events still 0, frame 2417 µs at 10⁴ — the zero-event frame is not an artifact of circularity.
2. rtf 1000 (16.7 game-s/frame): frame 2310 µs, events 0 — the cost is the frame, not the horizon.
3. threads = 8 at 10⁵: 55 360 µs vs 58 972–63 568 at 1 thread — multithreading does not touch the wall (rekey and the defer sweep are single-threaded; `resolve_wave` only engages due ship items, line 815), so the bench's `threads = 1` hides nothing.
4. Code audit: `advance` → `rekey` (universe.rs:792) requeues every body (499–505); the loop sets aside each beyond-target entity (807) and requeues all (827–832) — three Calendar touches per body per frame, confirmed; `Budget::events(0)` traverses exactly rekey + defer sweep + requeue. The harness's manual loop equals the shipped `frame_to` (862–874) minus `prune`, which is itself O(N) every 64 frames (967–970) — the bench understates the shipped path.

## Novelty

No prior N-sweep of the frame loop exists: `tail.rs` measures per-item tails and `view_cost.rs` the view gather, both on the plane's default small scene; HISTORY's plane entry (frame p99 2.45 ms) is small-N; the board's item 4 names least-slack scheduling but never measured the queue's own cost. The finding that the allocator's feed is starved by a zero-surprise sweep is new, and it lands before the `b-belt-wire` bet (lab/queue.txt line 13).

## Goal fit

Board item 4 ("least-slack scheduling fed by surprise rates") and B18b's premise. PRINCIPLES #14 "we only care about changes" — the frame re-touches every body three times to learn nothing is due; #1 "the cheapest compute is compute not done"; #12 the p99 — here the whole frame is the tail, at zero events. The proposed fix changes *when*, never *what* (digest-invariant by the control), one builder step.

## What the author missed

- The per-event cost at N remains unmeasured (admitted): the wall is a floor; a belt that does kick at 60 Hz pays resolution on top, and no run here prices one kick under DRAM-distance pressure.
- P2's "±5%" is load-flattering: my sched-only vs frame spread reached −22% at 10⁶ under load 4; the safe statement is "sched-only ≈ frame to first order, rekey 10–17%".
- The restricted scene never fires an event even at rtf 1000 over 2000 game-seconds, so "belt-like cadence ≈ 0 events/frame" is asserted from scene structure, not measured on a real belt birth; b-belt-wire must re-measure the event rate, not just the fixed queue.
- Cloud/x86 constants only (the rule, restated honestly); the M1's cache lines and E-cores could shift the 3×10⁴ break by ×2–3 either way.
