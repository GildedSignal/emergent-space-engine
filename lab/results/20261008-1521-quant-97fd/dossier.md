# Dossier — 20261008-1521-quant-97fd (Quant lens)

## Claim

On the flown plane (rtf 100, paced 60 Hz), the frame is owned by the **view gather** (62–69% of summed frame time; 74% at real time), not the engine (19–26%); and a paced frame costs **4.5–6× its hot-loop cost** in CPU time (cpu≈wall, so compute, not stalls) — so hot-loop measurements, including the repo's own benches, overstate the player's capacity by ~5×, while the engine's 5 ms budget holds everywhere except single items that overshoot it up to 2.2×, and a player order costs nothing at p99 (ratio 1.01).

## Bottleneck

The board's live question #1 ("fewer kicks per orbit — kicks dominate the engine's cost") prices the wrong share of the frame: all of physics together is 19–26% of the flown frame; the readout (the view gather: Newton crossings of the past light cone, 71 bodies) is 62–74%. The next marginal hour buys ≤26% on kick cadence but 62%+ on the readout — `b-readout-cost` (already queued) is the frame's owner, and it should sit above cadence in the queue order. Second pricing: every hot-loop ns/event in this repo needs a paced control, or its number is ~5× optimistic for the player.

## Evidence

Machine: shared Linux x86, 8 vCPU, load 0.68–1.25 during runs (recorded in each JSON: `uptime_before/after`, `machine_before/after`). Orders of magnitude only; the integrator re-measures on the M1. Every number regenerates with `python3 analyze.py` in this folder.

1. **The flown point, fresh seeds** (`xtask universe --bench --rtf 100 --seconds 30 --seed 7|20261008`, 30 s each):
   frame p50 4.2/4.6 ms, p99 10.4/10.5, p99.9 12.3/11.2; **zero hitches >16.7 ms**; overflow 49/1800 and 41/1800 frames (RTF dips, as designed). Shares of summed frame time: view gather 65.6%/68.8%, engine 21.2%/19.2%, JSON 9.3%/8.4%, wire 3.9%/3.6%.
2. **The paced tax** (same rtf 100, `--unpaced --seconds 20` vs paced): view p50 0.72 → 3.25 ms (**4.5×**), engine p50 0.05 → 0.28 ms (**6.0×**); thread CPU ≈ wall frame time in both, so this is compute on cold caches/low clocks after each ~15 ms sleep, not descheduling. The player's machine pays this tax by construction ("measure the way the player plays, heat included").
3. **Capacity is not the binding constraint on this box**: unpaced, frame p50 stays ≤1.65 ms up to rtf 1000 (events/s 163→552); the engine's 5 ms budget caps its tail (max 5.65–5.74 ms) and defers (3–4 overflow frames per 1200).
4. **The budget's leak — single items**: 7 frames per 30 s run exceed 6 ms of engine time (max **10.8 ms vs the 5 ms budget, 2.2×**), carrying a p50 of 3 counted *events* each — one queue item (a fleet slice or a v2 rebind; not attributable from outside without per-item timing) is a synchronous claim the between-item budget check cannot split. Engine time is only mildly concentrated: top 10% of frames carry 53–55% of it (predicted >60% — a miss).
5. **Engine time by kind** (paced rtf 100, 30 s): ship 537 ms (43%, 239 µs/item, 2251 items), fleet 395 ms (31%, 56 µs/item, 7050 items), **player 327 ms (26%, 1125 µs/item — 20× the fleet's per item**; the motion law v2's rebind path). As more bodies move to the v2 law this per-item cost is a scaling risk the cadence work does not touch.
6. **A player order is free** (`--rtf 1 --seconds 30`, paced; burns every 240 frames for 20): cpu p99 burn 5.01 vs coast 4.94 ms (**ratio 1.01**), engine p99 ratio 0.98; no wake visible after the burn. plane.md foundation 7's bounded-impact claim holds at plane level.
7. **At real time (rtf 1)** the frame is 74% view, 4.7% engine, worst frame 11.6 ms — the view floor follows the player everywhere.

## Predictions

`predictions.md` was written after one 5 s smoke run and before all runs above. Held: P1 (view >50% on fresh seeds, p50 within ±30%), P4 (order impact ≤3×; measured 1.01×), P2's side claim (view flat-ish in rtf: 0.72→1.19 ms p50, +65% over 33× rtf — engine grows faster, as predicted). Missed: P3 (burst concentration 53–55% vs >60% predicted), P5 (per-item leader is the player, not the fleet), P2's crossing point (p50 never crosses 16.7 ms even at rtf 1000 unpaced — the paced tax, not capacity, is what binds). The kill criterion (paced/unpaced shares disagreeing >2×) did not fire on shares, but the *levels* differ 4.5–6×, which is the finding, not noise.

## What would make it wrong, cost, fit

- **Wrong if**: the M1's paced tax is ~1× (its governor and unified memory differ — then only the view-share finding survives); or the shipped view changes to an incremental gather that is cheap per frame (`ViewCache` exists and the gather is still 3.3 ms paced — I did not profile inside it); or the real browser view amortises the gather across frames. The browser/HTTP send is *not* in these numbers, so the view's true share is if anything larger.
- **Cost of adopting**: none in code; a paced control beside every hot-loop bench (the bench already supports `--bench` vs `--unpaced`), and a queue flip (readout above cadence). Per-item timing inside `Universe::advance` would close finding 4's attribution.
- **PRINCIPLES**: "Measure the way the player will run it: heat and load are part of reality, not noise to sidestep" (the 4.5× tax is that sentence, measured); "the goal, never a proxy" (hot-loop ns/event is a proxy for the player's frame); Simons, from the lens: "You have to know what your costs are when you trade."

## The lens

The Quant lens priced the tail and the capacity and nearly missed the representation point: the cheapest frame is the one not rendered, and "cache lines per event" says nothing about a gather that runs 60×/s over the whole catalogue regardless of change (principle 3: compute only surprises — does the view?). I also did not touch the GPU order, where the same gather may already be a non-issue.

## Reproduce

```
cd <repo>; cargo build --release -p xtask   # FRAME_CSV patch from this run's diff applied
X=target/release/xtask  # here: /home/glmlab/lab-target-2/release/xtask
for s in 7 20261008; do FRAME_CSV=a-rtf100-s$s.csv $X universe --bench --rtf 100 --seconds 30 --seed $s > a-rtf100-s$s.json; done
for r in 30 100 300 1000; do FRAME_CSV=b-unpaced-rtf$r.csv $X universe --bench --rtf $r --seconds 20 --unpaced > b-unpaced-rtf$r.json; done
FRAME_CSV=c-rtf1.csv $X universe --bench --rtf 1 --seconds 30 > c-rtf1.json
python3 analyze.py
```
Each command ≤ 45 s. CSVs, JSONs and `analyze.py` live here; the diff (Dash per-frame ticks/events + the FRAME_CSV dump) is saved by `run.sh`.
