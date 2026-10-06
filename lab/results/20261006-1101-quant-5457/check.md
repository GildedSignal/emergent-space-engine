Grade: silver

**Abstract.** Claim: one player burn is priced in deferred game time, not hitches — at 11,560 g player items grow 13× (289→3807) with zero frames over 16.7 ms and repeat-identical digests. Reproduced: all five digests byte-identical on a quieter box, encounters exact (132/238/178), items within ±1. My probes hold stronger than tested: unpaced and 1 ms-budget L15 give the same digest with zero hitches; seed-3 L15 repeats byte-identical (cross-seed determinism, untested by the author). Gain: the measurement the burst policy lacked; nothing to build. Cost: the dossier's L8 `opens` cell (404) contradicts its own stored JSON (86) and the "wall-dependent" inference is backwards — `opens` tracks dose. Silver: real and reproduced, but one log-contradicted number and no 10× lever.

## Reproduction

Applied `work/patch.diff` to a clean tree (`git apply`), built `xtask --release` (38 s), ran all five commands (`xtask universe --bench --seed 7 --rtf 100 --seconds 30 [--coast|--level L]`, paced, 30 s each):

- **Digests byte-identical to the author's stored runs on all five** (4bff5f86…, 74651968…, 8fe4d5d5… twice, 86891074…), on a quieter box (my load ≈ 0.2 vs their 0.8–1.3).
- Exact counters: encounters 132/132/238/238/178 identical; player items 290/297/1352/1352/3808 vs 289/293/1352/1352/3807 (near-canonical, as the dossier says); kicks within 0.1–3%; L8/L8b digest-identical.
- Service layer: 0/0/0 hitches (wall and CPU) in every run of mine too; my worst frame 12.3 ms < 16.7. Overflow (wall-derived) 2/2/52/65/124 vs author 5/41/60/65/348 — monotone in dose on both boxes, as claimed. p99.9 7.9→12.0 ms ✓. rtf worst-1% 0.2 at L15 ✓. Shares engine 24→42%, gather 59→45% ✓ (from `where_the_time_goes_ms`).
- Decay: recomputed from the stored L15 series with the author's lag logic — first non-positive excess at lag 4, consistent with "≤ 41" (their analysis.json: 25/41 on L8/L8b, 4 on L15).

## Adversarial cases (mine)

1. **`--unpaced --level 15`**: same digest `868910746819a8fe`, wall 2.4 s, 0 hitches. The digest's pacing-independence promise holds at max dose.
2. **`--engine-ms 1 --level 15`** (5× tighter budget): same digest again, overflow 688, worst 2.8 ms, 0 hitches — the deferral claim ("budget governs the frame, bits unchanged") in its strongest form, which the author did not test.
3. **`--seed 3 --level 15`** (twice): alive, 0 hitches, 3808 player items (dose reproduces on a fresh trajectory; author's own lens note flags single-seed), digest `002db048fce53261` distinct from seed 7 and **byte-identical across the repeat** — cross-seed determinism.
4. **The author's L15 anomaly resolved**: my L15 run counts `decisions: 16` (theirs: 14) with the same digest — a transient coalesced count under lag, exactly their "possibly coalesced flushes" guess; not a lost input.

## What fails (why not gold)

- **A number the stored log contradicts.** The table's L8 `opens` cell says 404; `bench-L8.json` says 86, and my reproduction says 86. The inference built on it — "`opens` is outright wall-dependent: 404 vs 86 on identical physics, so it measures re-opened windows under deferral, not dose" — is **backwards**: both L8 runs sit at 86 under different overflow (60/65), while L15 is 404 (author) and 406 (mine, quieter box). `opens` tracks dose, not wall. By the lab's own rule ("a headline the log contradicts … the run loses its grade") this bars gold.
- **Predictions:** #2, #4, #5 (and survival) held; #1 (≥2× per-frame CPU at L15; measured 1.23) and #3 (gather ≥50%; 45% at L15) and #6's rtf clause (0.2×) failed — all honestly reported, but two clean holds is not "the held-out predictions held".
- **Not a 10×, deletion, or premise kill by the board's letter:** it confirms the budget premise survives a 33,000× throttle range; a confirmation, however useful, is not gold.

## Novelty

H0211 introduced the bench and measured smoothness (p99 2.72 ms, worst 14.5 ms) and the throttle levels (HANDOFF: 0.35 g–11,560 g, merged 2dc53c); H0213's A/B bench concerned mass mantissas. No HISTORY entry or doc measures the dose-response of a player action on the plane. First of its kind; the patch is minimal (`--coast` control + per-frame series dump) and regenerates every stored number except the one `opens` cell.

## Goal fit

Board #4 (smoothness/allocator) and PRINCIPLES #12 — "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36): measured, the spike becomes a rate. #5 — "Priority is slack, not proximity": the slack queue held 16.7 ms under max dose with identical bits, and my 1 ms-budget run shows the same digest at 5× the pressure. Honest about wall-derived numbers and the M1 re-measure.

## The one experiment that would make it gold

Cut the 13× where it lands: extend the already-queued window-setup deferral (components-4643's slack skin) to the player-decision path and show ≥10× fewer player items at L15 with the digest unchanged, across ≥3 seeds. Failing that, the named artifact risk — four cycled headings — must be killed with a randomized-heading burn script before the dose claim is load-bearing.

## What the author missed

- The `opens` transcription error and its inverted inference (above).
- The strongest form of their own claim was one flag away: `--unpaced` and `--engine-ms` digest-invariance, both untested.
- Single seed for the determinism claim (their own lens note admits it); seed 3 fills the gap.
- The encounter seam's non-monotone dose (132→238→178) is flagged but unprobed; worth its own run, as they say.
