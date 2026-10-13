# Dossier — 20261012-2257-quant-32ab (Quant lens)

## Claim

The flight sweep's L8+ stutter is not the Θ(N)-per-frame fixed tier that `wt/frame`'s lazy
re-keying targets — it is the **burn-input replan waterfall on the player's own item stream**
(up to 1,036 player items resolved in the single frame the burn lands, monotone in burn level)
riding a per-item universe overhead that scales with population (the O(all-bodies) player scan),
so lazy re-keying cannot fix it.

## Bottleneck

`frame-cost`, open direction #1 ("delete the fixed tier") as the assumed fix for the sweep's
finding (HANDOFF item 2: "from L8 up the frame hits its 12 ms budget and the presented time lags
up to 1.6 s"; item 5 hands it to `wt/frame`: "lazy re-keying and the incremental deadline first").
This run measures where those 12 ms actually go in the flight regime — a regime no frame-cost run
had measured (prior runs: zero-event populations, fleet openings, view gather) — and finds the
premise wrong by three orders of magnitude. What it deletes is the wrong lever: the fixed tier
is ≤ ~19 µs/frame here while the player item stream is 87–91% of the flight's CPU.

## Evidence

All from shipped code (main at 7117f6a8, clock fix merged) plus this run's two examples
(`crates/universe/examples/frame_split.rs`, `player_items.rs`; the patch adds them, nothing is
modified inside the engine). Reproduce with `bash lab/results/20261012-2257-quant-32ab/regen.sh`
(~1 min warm). Machine: shared Linux/x86 runner, 8 vCPU, load 0.6–1.5 across passes; orders of
magnitude only. Scene: the sweep's exact flights — `plane(seed 1, Sparse, threads 1, members)`,
forward hold from wall second 1.0, `frame_to(1/60, rtf, …)`, 60 Hz.

1. **The stutter reproduces, and it starts at L8** (paced, the page's 12 ms budget, 20 s): worst
   lag 0.038 s with 1 capped frame at L0–L6, then 1.43/1.53/1.61/1.66 s with 22/34/41/55 capped
   frames at L8/10/12/15.
2. **The fixed tier is unmeasurable in flight.** Demand mode (unlimited budget), L15, 20 s:
   Σframe CPU 1.19 s, of which the engine's own `Stats` attribute 1.09 s to player items, 0.089 s
   to fleet, 0.017 s to ships — remainder −0.4% (measurement noise). At 48 members the
   rekey/drain/queue tier (the thing lazy re-keying deletes) is bounded by the earlier 15 µs/frame
   measurement and is invisible here.
3. **The worst frame is a player-item waterfall at the input frame.** The burst trace fires at
   wall second 1.00 — exactly the frame the burn input lands — and decays over 2–4 frames:
   42 items (L8) → 166 (L10) → 579 (L12) → 1,036 (L15) player items in that one frame
   (deterministic counts, same every run). In the same frame the whole flight's p50 stays
   39–125 µs. `us3_fr_max` (the burst frame's player cost) equals the flight's worst frame
   within 3% at every level ≥ 6.
4. **Per-item cost is flat in speed; the jet is not the flight's problem either.** Micro-probe
   (`player_items.rs`): the pure resolve `step::process` on the player's record costs 22–25 µs at
   coast and 75–80 µs under burn, flat from |v| = 0.12c to 0.55c (median per snapshot; max 473 µs,
   no growth with γ). The universe-side per-item overhead (scan + apply + requeue) is the rest:
   ~340–450 µs/item in flight at 48 members.
5. **The per-item overhead scales with population.** At 400 members the player item averages
   1.8–2.45 ms (4.8–7× the 48-member cost, tracking the O(all-bodies) `PlayerNeighbourhood`
   scan already on the wiki's open list), so the same deterministic waterfall costs 2.4 s in one
   frame (L15, m400) — 200× the page's frame budget.
6. **Capacity, not prologue.** rtf 25→400 at fixed level scales the p99 frame roughly ∝ rtf
   (L8: 3.1→48.6 ms); the burst item counts are rtf-independent. The coast control surprised:
   even unburned, the 48-member plane has p99 ≈ 1.3–1.4 ms and worst ≈ 13–14 ms frames (fleet
   slices + player items), i.e. the sweep's smooth baseline is already one heavy frame in a
   quiet second.

Wall-cost honesty: across processes on this shared box the burst frame's cost moved 0.38 s
(load 0.6) → 2.41 s (load 1.5, after other passes) for the same 1,036 items — per-item 0.37–2.3 ms.
The item counts, shares, and shape are deterministic; absolute times are order-of-magnitude.

## Predictions

Written before the decisive runs (`predictions.md`). Held: P1 (attribution remainder < 5% — the
falsifier for the fixed-tier premise), P2 (event density grows with level), P3's main branch
(throughput ∝ rtf, no flat 12 ms floor). Failed, informatively: P4's ≥2× per-item growth with
level — cost is flat in γ (75–80 µs), the frame is item-count, not item-cost; P5 (<2× growth at
400 members) — the background grows ~9× (ships 0.6 s of a 1.1 s coast flight) and the player item
4.8–7×; P6 (coast p99 ≤ 300 µs) — coast p99 is 1.3 ms.

## What would make it wrong

- If `wt/frame`'s build passes gate F1 and the sweep's stutter disappears with lazy re-keying
  alone, this attribution is wrong (but then the 1,036-item waterfall and the 87–91% player share
  measured here need another explanation — I do not expect it).
- The waterfall's item counts are scene-specific (one seed, one scene, forward holds); a different
  input pattern (key mashing, turns) could distribute the replan differently. The per-level
  monotonicity and the input-frame trigger are the robust parts.
- Linux/x86 shared runner: absolute costs are noisy (see honesty note); the M1 may price the scan
  and the resolve differently. Shares and counts should transfer.

## Cost of adoption, and fit with PRINCIPLES

Adoption cost is a decision, not a build: redirect the flight-stutter fix from the fixed tier to
(a) the player item's O(all-bodies) scan (already open direction #6) and (b) spreading the
burn-input replan waterfall across frames — digest-safe by the schedule-independence gold
(20261007-1234-system-2517), since only *when* the items resolve would change. Fit: "Compute only
surprises" (the burn input is the only surprise in these flights; the frame should pay it at the
input, not amortize it into a hidden per-body tick) and "a fix signals the wrong representation"
(fixing the L8+ stutter with re-keying would be the bandaid). Also relevant: gate F1's "no frame
over 12 ms **after the first second**" excludes exactly the burst frame (the sweep's burns start
at wall second 1.0), so F1 can pass while the burn frame still hitches — the gate should cover
the input frame.

## The lens

The Quant lens priced the frame by its tail and attributed it stage by stage, but it did not look
inside `input()`'s replan (why one input mints ~1,000 due items is one question deeper — the
thrust word's replan semantics, likely the burn re-fitting the tube against every scheduled kick);
and it flew one seed, one scene, forward holds only.
