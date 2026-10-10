# Dossier — 20261010-0352-quant-3435 (Quant lens)

## Claim

On the shipped plane the frame is paid by the readout, not the physics: view gather + JSON +
wire are 90–97 % of frame CPU at every time factor, the gather is unbudgeted Θ(live bodies +
active fleet members) per frame (Newton per emitter, `view.rs`'s loop over `0..n_bodies()`),
and at 10× real time with a drained fleet (~380 emitters) the frame contract breaks — p99
16.9 ms, worst 21 ms, ~3,240 hitches > 16.7 ms per hour — while the engine idles at 5–10 %
under its working 5 ms clamp. The player's burn is priced diffusely in the event queue
(player items ×531, encounters 2 → 442, events/s 61 → 141) with no tail spike.

## Bottleneck

Board #4 (smoothness and the allocator) and the queued `b-readout-cost` build. The measured
10× lever is in the readout path (cull, budget, or re-represent the gather and the JSON),
not in the law: the engine's worst frame is its own budget clamp (~5.5–5.8 ms), i.e. the
bounded-work mechanism works where it is applied, and the gather/view/wire path has no such
clamp despite plane.md foundation 7 naming it ("nothing takes an unbounded synchronous claim
on the frame, whether a cycle compile, a rebinding burst, a decompression or a gather").

## Evidence

All runs on this box (Linux x86, 8 vCPU, shared, load 1.2–1.4; orders of magnitude only —
CPU-time metrics wobble ±2× between identical runs, see a2 vs a2b). Build:
`cargo build --release -p xtask` (44 s); binary at `$CARGO_TARGET_DIR/release/xtask`.
Raw reports: `work/*.json` in this folder. Each command ≤ 60 s.

```
X=/home/glmlab/lab-target-1/release/xtask   # cargo build --release -p xtask
$X universe --bench --seed 1 --rtf 1  --seconds 20 --members 48          # a1
$X universe --bench --seed 1 --rtf 1  --seconds 20 --members 480         # a2, repeated as a2b
$X universe --bench --seed 1 --rtf 1  --seconds 20 --members 480 --unpaced  # d
$X universe --bench --seed 1 --rtf 1  --seconds 20 --members 480 --level 12  # c1
$X universe --bench --seed 1 --rtf 10 --seconds 20 --members 480         # b1
$X universe --bench --seed 1 --rtf 10 --seconds 20 --members 48          # f1
$X universe --bench --seed 1 --rtf 50 --seconds 20 --members 400         # e1
$X universe --describe --members 4800                                    # the clamp
```

| run | live | gather p50 | frame p50/p99/p99.9 | engine p99 / max | hitches>16.7 /h | ev/s | bpb | digest |
|---|---|---|---|---|---|---|---|---|
| a1 m48 rtf1 | 39 | 0.54 ms | 0.79 / 4.5 / 6.4 | 0.21 / 5.6 | 0 | 61 | 2266 | c1c28574… |
| a2b m480 rtf1 | 33 | 0.82 ms | 2.9 / 3.1 / 7.0 | 0.17 / 5.8 | 0 | 61 | 1770 | c4307bb5… |
| d = a2 unpaced | 33 | 0.98 ms | 3.8 / 9.1 / 10.1 | 0.49 / 5.2 | 0 | 61 | 1770 | c4307bb5… ✓ |
| c1 = a2 level 12 | 33 | 1.04 ms | 4.1 / 8.9 / 9.5 | 2.46 / 5.7 | 0 | 141 | 3673 | f546d996… |
| b1 m480 rtf10 | 389 | 6.83 ms | 10.3 / **16.9** / 20.7 | 5.9 / 6.7 | **3240** | 347 | 6873 | cbac1322… |
| f1 m48 rtf10 | 71 | 1.04 ms | 1.3 / 3.6 / 6.8 | 1.8 / 5.8 | 0 | 93 | 5065 | — |
| e1 m400 rtf50 | 415 | 3.43 ms | 5.0 / 11.2 / 11.6 | 5.5 / 6.6 | 0 | 1045 | 6467 | — |

Stage shares at rtf 1 (a2b): gather 29 %, JSON 53 %, wire 6 %, engine 3 % — JSON alone
(~47 µs/body) costs about twice the physics gather (~25 µs/body). The engine's per-frame max
sits at ≈ the 5 ms budget in every run: the clamp binds exactly where designed.

1. **Content, not time factor, breaks the frame.** f1 (rtf 10, 71 live) is smooth; b1
   (rtf 10, ~380 emitters after 361 members drained into the doll) breaks p99 and racks up
   3,240 hitches/hour with rtf lowest-1 % = 0. The gather iterates every live body plus every
   active member each frame (`crates/universe/src/view.rs`, `for i in 0..u.n_bodies()` + the
   members loop), one Newton solve each, memo only seeds the guess — nothing is skipped, and
   the stage has no budget.
2. **The player's order is diffuse.** c1 vs a2b (level 12 = 1,433 g for ⅓ s every 4 s):
   player event items 1 → 531, kicks 2 → 269, boundaries 0 → 263, encounters 2 → 442,
   events/s 61 → 141; frame p99.9 +36 %, worst hitch at frame 825 — mid-coast, not within 10
   frames of any burn window (240k..240k+19). The budget absorbs the wake; its price is ~80
   extra doll events/s of engine work that was idle anyway.
3. **Determinism holds under wall noise.** a2 = a2b = d give the identical digest c4307bb5…
   (paced repeat and unpaced), through p99 swings of 3.1 ↔ 9.1 ms from box contention.
4. **Instrument notes.** `--members` is clamped to [4, 400] (`xtask/src/universe/mod.rs`),
   so 480 and 4800 are the same scene (identical digests resolved by `--describe`: "1
   fleet(s) of 400 members"); the members axis saturates and cannot probe capacity — live
   bodies grow only as the fleet drains (~1.8 leavers/game-second, capped ≈ 428 here).
   `bytes_per_body` grows 1770 → 5065–6873 as the scene ages (leaver records accumulate):
   at ~7 KB/body, 10⁶ bodies ≈ 7 GB — the memory question `b-h-live` owns, now with a
   measured shadow.

## Predictions

`predictions.md` was written before any run. Scored: (1) HELD — readout majority, engine
inside budget; (2) HALF — p99 within 2× across members at rtf 1 held, but I predicted
overflow at 4800 members (dead axis: the clamp) and "degrades by throughput, not hitches":
FALSE at ~380 emitters, where hitches appear; (3) HALF — the <2× p99.9 bound held (+36 %),
the burn-aligned worst hitch FAILED (frame 825, mid-coast); (4) HELD — both digest controls;
(5) FAILED as stated — events/s 61–1045, not >10⁵: ev/s measures this scene's demand
(3–21 events per game-second), not the engine's ceiling (the engine never exceeded ~10 %
busy); a ceiling probe needs a doll-event-dense scene, which the plane cannot make today.

## What would make it wrong

M1 constants differ (integrator-re-measured); the JSON share is a debug-view artefact the
real visual layer deletes; leaver-driven emitter growth may be unrepresentative if real
fleets dissolve once and forever; single-session, shared-box, single-seed measurement —
the 3,240 hitches/hour is one 20 s run (≈18 hitched frames), and CPU metrics wobble ±2×
between identical runs. The structural reading (unbudgeted Θ(emitters) readout vs a
clamped engine) is code-visible and seed-independent; the exact break point is not.

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt — a measurement that re-ranks work: the readout, not the law, is where the
frame's 10× lives, and the gather must join the budget (or cull by what the player can
differentiate) before any engine optimisation pays. Fits "minimize spike compute and
average compute usage so that you get a bigger simulation that runs smoothly" (OC#36) and
"i care about the p95/99 results" (CL 09-25); the gather recomputing every emitter every
frame is compute done on what has not changed, against "Compute only surprises". The fix
direction is already queued (`b-readout-cost`); this run hands it numbers and a falsifier:
after any readout fix, b1's configuration must show p99 < 16.7 ms with zero hitches.

## The lens

The Quant lens priced tails and stages, and read the queue's priority as confirmed; it may
have missed that the deeper answer is representational, not schedulable — what the player
can differentiate (the view's information floor, "the floor is what the player can
differentiate") should decide which emitters are gathered at all, and a budgeted gather
that skips nothing only postpones the same wall. It also nearly mistook the members clamp
for a digest hole; `--describe` settled it.
