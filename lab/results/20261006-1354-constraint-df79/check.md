Grade: silver

**Abstract.** Claim: at the 400-member clamp the plane's felt constraint is game-time fidelity, not the frame; the largest spike is the player's O(doll-population) encounter scan (27% of engine time from ~1% of items, one item = 68% of the frame budget), and 4 threads worsen overflow. Reproduced bit-for-bit: bench and kickbench digests identical, every table number recomputed from `data/` matches; my fresh runs confirm the ordering (m400: player 2336 µs vs ship 83; overflow 301→507 with 4 threads; seed 2 and m100 hold). Gain: measured payoffs for the already-queued cone and skin; threads killed as a lever. Cost: nothing to build. Not gold: no gate moved, and predictions 1–3 were written after the m200/m400 runs had finished.

## Reproduction

Clean tree (`work/patch.diff` is empty — a measurement-only run; `run.sh`'s restore is consistent). Built, then re-ran the commands:

- **m400 paced**: digest `24208b…` and `cut_tick` **identical**; engine p50/p99 0.41/5.7 ms (author 0.43/6.1), share 25% vs 23%, rtf median 100 / worst-1% 0.0, overflow 301/1800 vs 389 (shared box, quieter now); µs/item player 2336 / ship 83 / fleet 37 vs 3405/104/40 — same ordering, player ≈ 28× ship.
- **kick-bench**: digest `a6792e…` **identical**; memo identical (exact 0%, quantized 95.47%, 1125/51 shapes); resolver median 34.9 µs (author 35.3), all-kicks 76.3 (76.4), leaver 92.5 (92.1), 793/1158 leaver samples.
- Every number in the dossier table recomputed from the stored JSONs: all six rows match exactly (frame percentiles, engine/view p50/p99 and shares, rtf, overflow, and each µs/item from `cost_ns`/`items`). The m200/m400 hitch counts `[1,0,0]` match "one frame above 16.7 ms, zero above 33".
- Source claims verified in code: `encounter.rs:53` is a literal `for j in 0..ctx.bodies.len()` with a tube eval per body; `universe.rs:564–586` runs the fleets to the tick before the player inside the player's item; `universe.rs:819–830` is the horizon clamp (it only clamps *down*, so catch-up frames cannot inflate the worst-1% — the author's worry (a) was answerable from this and the tail is genuine); `xtask/src/universe/mod.rs:32` confirms the 400-member clamp; line 812 confirms the wave path parallelises ships only.

## Held-out check — the record's flaw

File times: `predictions.md` 13:59:31; `bench-m200` finished 13:58:30, `bench-m400` 13:59:00 (their `uptime_before/after` bracket the runs). Predictions 1–3 — the constraint-order and m400 predictions the dossier scores as "held" — were written **after** the m200 and m400 runs had finished, contradicting both the predictions header ("before the 200/400 and rtf-ceiling runs") and the dossier ("before all other runs"). Genuinely held out: unpaced, rtf-1000, kick-bench, threads-4 (predictions 4–5; 4 half-wrong, 5 held — honestly reported). The measurements themselves are real and regenerate exactly; the hold-out claim does not.

## Attacks (mine)

1. **m100 (128 bodies)**: worst-1% rtf 81.4, overflow 19/1800, player 909 µs vs ship 87 — the transition band claim holds and refines to 128–221 on today's box (the author said the band would move).
2. **Threads**: overflow 301→**507** (author 389→505), ship µs/item 83→154 (104→156), player still serial — direction and mechanism independently confirmed.
3. **Seed 2**: overflow 313, worst-1% 0.0, player 2044 µs = 23× ship — the finding is seed-robust despite the single-seed record.
4. **Schedule independence**: paced, unpaced and threads-4 at m400 share one digest at one cut — the canonical outcome is immune to budget and schedule, a stronger statement than the dossier makes, sitting unclaimed in the author's own data.
5. Overflow at 21% of frames is not 64-periodic — the author's prune worry (e) is unfounded.

## Novelty

The skin payoff (92% window setup) is components-4643's finding, reproduced; the cone is already queued (board focus, H0212 context); the memo numbers match H0212's 95–98%. New here: the player scan quantified as the single largest item and O(doll population) with the serial fleet pull attached to it; threads-4 worsening overflow; the two-currency ordering (game time breaks between 76 and 221 bodies while frame p99.9 stays ≤ 15.7 ms); the unpaced intrinsic tail; and two real defects reported (machine_state macOS-only on Linux; `catalogue_live` 428 vs 213 lost).

## Fit

Board bottleneck 4 and focus line 1; PRINCIPLES #12 ("minimize spike compute and average compute usage… the algorithm that allocates the work to prevent those heavy tails, it's the most important one") — the 3.6–10 spike/mean ratio at 34% mean load is that principle as a number — and #17 ("Use idle time to compute ahead" — the 66% idle is measured). Respects #10: paced, scripted decisions at canonical ticks, state recorded (as far as the macOS-only probes allow, which the author flagged).

## Why silver, and the one experiment for gold

Real, reproduced bit-for-bit, attacked on seed, band and threads, and it re-orders the queue with numbers while killing the threads lever. But it builds nothing (no gate moved, no 10×), and the hold-out protocol was breached on the record's central predictions. **The experiment:** replace the O(N) `PlayerNeighbourhood::find` scan with a constant-work neighbourhood (the cone's payoff, in situ) and re-measure the m400 tail — predictions written before the run this time. A members-unclamped bench with a seed ensemble and honest hold-outs is the alternative route.

## What the author missed

The predictions-timing breach itself; the digest identity across paced/unpaced/threads in their own data; the player item conflates scan + forced fleet pull + own kick (admission (c) — a one-line instrumentation split would have pinned it); "1.5% of items" is 0.79% of all items (1.5% only of ship+player items); worry (a) was decidable from the clamp's code; `bytes_per_body` 5825 goes unremarked beside a memory-floor board.
