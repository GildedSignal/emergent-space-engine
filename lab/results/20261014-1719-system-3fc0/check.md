Grade: lead

**Abstract.** The author claims that bounding the player-item `pull_ships` (6138's named fix, built as `ES_PULL_MAX` + held scan) freezes the frame horizon at 2×10⁴ belt members, killing the fix. Not reproduced: the runner's regen and two independent checker re-runs (ES_PULL_MAX=256 and 64) show the bounded arm advancing on pristine's own trajectory (now = 1,048,715 by frame 1,200; 50×10⁶ ticks by frame ~15,000) with the worst frame cut ~12× (294.8 vs 3,439.9 ms, regen pair). At 5×10⁴ and 10⁵ both arms stall identically (now=111 / now=30): no dissociation in any configuration measured. The dossier's headline numbers (tick-55 freeze, 2,893.1 ms, over-12=656) are absent from its own regenerated evidence file. Mechanism reading verified against shipped code; patch builds, digest-neutral when unset. Cost to adopt the kill: it would discard a fix that works at 2×10⁴ on this box.

## Reproduction — the claim dies here

`git apply work/patch.diff`, build, `regen.sh` (already run by the runner; log in `regen.log`) plus my own battery (this box, 1 thread/arm, <1 GB each):

| Dossier claim (author's flights) | Runner's regen (`wave_runs.txt`) | Checker re-run |
|---|---|---|
| m20k bounded: horizon **frozen at tick 55** within 1,200 frames (stall exit, ~15 s) | advances: 55 → 1,048,721 @f1200 → **809,526,205 ticks** @f21,600; no stall; full 200 s timeout | a1 (256): 55 → 1,048,715 @f1200 → 50,332,333 @f14,400; a2 (64): same, no stall; a3 (256+forced scan): same, no stall |
| m20k bounded: worst 200.8 ms, over-12 = 7 | worst 294.8 ms; over-12 = 444 @f21,600 (7 only at the f600 line) | worst 318.7 (a1) / 330.8–396.4 (a2) ms — concurrent arms, contention noise; over-12 climbing equally in all arms |
| m20k pristine: worst **2,893.1 ms**, over-12 = 656 by 23,400 frames | worst 3,439.9 ms, over-12 = 475 @f24,000; own near-stall window @f21,000–22,800 (+267 ticks/1,800 frames) | — |
| m100k: "neither arm reaches the cut in 150–260 s, > 10× behind" | **both arms hard-stall at now=30** ≤f1200 (stall exit; worst 678.5/703.6) | a4/a5: both stall at now=30 (worst 756.6/788.8) |
| — (not tested by author) | — | a6/a7 (5×10⁴): **both arms stall at now=111** (worst 385.0/371.3) |

The bounded-vs-pristine dissociation the kill rests on appears **nowhere**: at 2×10⁴ both advance (bounded tracking pristine to the tick pre-burn, then ahead: regen f21,600 has bounded at 809M vs pristine at 336M ticks); at 5×10⁴ and 10⁵ both stall together. The only number that regenerates is the m100k worst-frame magnitude (author 678.9; regen 678.5/703.6). The dossier's own description of `regen.sh` ("the bounded arm exits on its stall in ~15 s, pristine needs the 200 s timeout") is contradicted by `regen.log`: at m20k the bounded arm ran to the 200 s timeout; the ~15 s stall exits belong to the **m100k arms, both of them**.

This is the lab's most-recorded failure mode (5 October: "results that the shipped code could not regenerate"), and here the regenerated log doesn't merely fail to confirm the headline — it inverts it.

## Why the "freeze" is an artifact, not structure

1. **The pre-burn unlock sits at the stall threshold.** Every arm — pristine included — sits at now=55 at frame 600 and unlocks to ~1,048,7xx by frame 1,200 (regen, a1, a2, a3). The author's dissociation is which arm crossed 600 consecutive non-advancing frames first: a marginal, load-dependent boundary, not a property of the bound.
2. **Shipped code answers the author's liveness hypothesis.** The dossier's candidates were "ships reaching the queue only via `requeue` after resolution; or the player's item blocked behind loops that assume the sweep". `rekey` (`universe.rs:623-628`) promotes every due ship from `waiting` into the frame's budgeted queue each frame, with no pull involved — the budgeted drain inherits a truncated pull's backlog by construction. a1/a2 advancing to 50M ticks confirm it empirically.
3. **The stall onset is machine-conditional in N.** The regen (~18:05) had both arms stalling at 10⁵; my battery (~18:19, busier box) had both stalling already at 5×10⁴. This matches 6138's checker note ("the onset N moves with the drain rate: machine-conditional as much as schedule-conditional") and undermines any freeze-based verdict measured on this box at all.

## Predictions

- Registered before the flights as far as mtimes show (`predictions.md` 42 min before dossier/patch; the author's own flight logs were overwritten by the runner's regen, so log-order proof is gone — keep author logs beside `regen.sh` output to fix this).
- **P1 (bit-identity): untested**, correctly disclosed by the author (no arm reached a cut). I attempted it at a reachable cut (230 game-s, past the burn at 200, where the arms' trajectories diverge so the bound demonstrably fires): under this window's load no arm reached the cut in 210 s (pristine peaked at 211.7 game-s; the 3.8–8.6 s "worst frames" in those runs are box contention, not the sim). P1 remains open — it is the certificate the fix still owes.
- **P3 (worst ≤ ~30 ms): failed in every telling** — author's own numbers (2,893 → 201 ms), regen (294.8), my re-runs (318.7–396.4). The pre-registered criterion says "P3 failing kills 'the pull is the monster'": that kill fired; the dossier's fallback ("the pull carries the monsters, but it also carries liveness") is exactly the half that did not reproduce.
- Scene drift, undisclosed: predictions say m100k / cut 16,000; the flights ran cut 5,000 (immaterial — no cut was ever reached).

## Novelty

Had it reproduced, the kill would be new (6138 named the fix, "not built"; nothing in `lab/wiki/nladder.md` or the board tests it). What the evidence supports is the opposite sign at 2×10⁴ on this box: the bound cuts the worst frame ~12× while the horizon advances ahead of pristine. Adopting this dossier's kill would discard that.

## The page

Corrected in place (`wiki/nladder.md` in this folder): the Current-best paragraph, the Refuted bullet, open direction 1 and the Runs line stated the freeze and the kill as measured facts; they now carry the regen/re-run numbers, the `rekey` waiting→queue fact, the both-arm stalls at 5×10⁴/10⁵, and P1's status. The author's methodological point (report the box's effective-rtf with cross-box frame costs) is kept.

## Goal fit

The board's focus list says "**not here:** the burn's stutter above L8 (GPT's `burst` job tonight, gate T1)… no lens re-measures them." This run re-measures exactly that seam (reverse-L8 burn monster frames). The liveness question it raises touches the nladder focus (the queue term), but the measured territory is the excluded one. PRINCIPLES #10 ("measure before claiming") is respected in form; the claim fails the record bar, and #9 ("a failed experiment kills that configuration, never the method") is quoted correctly — but the experiment did not fail as described.

## What the author missed

1. The evidence-file mismatch: the dossier's headline numbers are not in the `wave_runs.txt` that its own `regen.sh` produced — check the regenerated file against the dossier before writing the claim.
2. Their own m100k arms stall-exit (both) in the regen they cite — read as ">10× behind" slowness instead of the hard stall it is.
3. The `rekey`/`waiting` promotion path (`universe.rs:623-628`), in the very file they read, which answers their structural-liveness hypothesis before it needed a flight.
4. Instrument resolution: printing `now` every ~100 frames through frames 500–1,300 would have shown the pre-burn unlock directly and killed the freeze reading before it reached the dossier; likewise, a stall window that distinguishes "slow" from "dead" at m≥5×10⁴.
5. P1 was testable in ~3 minutes at cut ~230 game-s on a quiet box; the probe's cut parameter exists for exactly that.

The run's durable residue: the env-gated instrument (`work/patch.diff`), the probe with progress/stall discipline, a fully accurate mechanism reading (every code citation checks: `universe.rs:690-700/770`, the 762-768 invariant comment, `1163-1165`; `encounter.rs:162-198`; `body.rs:152-161`), and one inverted-but-real observation now on the record — at 2×10⁴ on this box the bound helps. The next run should take P1 at a reached cut and a quiet-box worst-frame pair past the wave; that run, not this one, decides 6138's fix.
