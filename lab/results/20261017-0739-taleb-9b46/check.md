Grade: silver

**Abstract.** Claim: the allocator's wave response is draw-dominated, one finality assert is reachable from shipped driver patterns, and the quiet regime is the family's cost floor. Reproduced: the seed flips the end-state class (s7→1 region, s1→~2,400, s2→~2,500–4,700; my held-out seed 3→1,389); digests bit-identical across replicates, arms and publication cadence; the chunked-`run_to` panic 2/2+2/2 at shipped `alloc.rs:1451` plus 1/1 on my quiet-14k probe; the quiet stall (no 150 chronons in 250 s at 28k). Not reproduced: the headline numbers — 9× wall (→3.4×), 4,715 regions (→2,489), seed-fixed latch (64↔128 within one seed), cap64 1.9× faster (→1.1× slower). Adopt: retire two single-draw page verdicts, install a ≥3-seed protocol, decide the publish/rollback boundary.

## Reasons

**1. Reproduction (regen on the clean tree + `work/patch.diff`, exit 0).** The patch is exactly as described: the new public-API example `ruin.rs` plus the one-line `ES_CAP` min on `escalation *= 2.0` (shipped `alloc.rs:1410`), default `f64::INFINITY` = bit-identical shipped behaviour. The reproducible core came back:

- Seed flips the end-state class, stably across two windows: s7 → 1 region (2/2), s1 → 2,394–2,442 (4 runs), s2 → fragmented (2 draws: 4,715 / 2,489).
- Physics digests are the only reproducible quantity: identical across identical-config replicates (C/C2 in both windows), across shipped vs ES_CAP=64 (`e538163e…`), and across publication cadences (chunk 250 / 500 / single-call at seed 1 all give `a00441e…`).
- The panic reproduced 2/2 at 864/chunk-100 in the regen; chunk-500 wave runs survive with single-call digests.
- The quiet stall reproduced: no tick-150 row in the 250 s cap at 28k, in both windows.

What did **not** regenerate (same args, same seed, same digest): A 14k E 128→64, px 5,770→12,115; C wall 17.9→44.8 s; replicate spread 1.65×→2.4×; G s2 4,715→2,489 regions, E 512→128, wall 160.5→33.1 s; cap64 6.0 s→15.0 s (the "1.9× faster" inverts to 1.1× slower); s7 wasted ops 35k→114k. This *confirms the thesis* (no allocator counter except the digest is a verdict) but refutes the Claim sentence's specifics: the seed alone does **not** pick the latch, the region count or the wall — the same seed latches 64 in one draw and 128 in the next, and s2's own count spread 1.9×.

**2. Predictions.** `predictions.md` predates the matrix (file mtimes: predictions 30 min, first matrix output 28 min) and the scorecard is honest. 4/5 failed ex ante. Note my window *flips* P5 back the other way (wall 28k/14k = 44.8/13.3 = 3.4 > 2, where the author's window gave 1.57): per-window single draws cannot decide these criteria — which is precisely the run's own conclusion.

**3. Attack (my adversarial cases; walls load-confounded, used only for end states/crash/counters).**
- **Held-out seed 3 at 28k:** a third end-state class (1,389 regions, E = 512, rb = 9, 21.3 s). Kills "the most-fragmented draw is the slowest" as a law — a high-latch fragmented draw can be fast.
- **Quiet 14k, chunk 150 (a regime the author never chunked):** tick 150 completes in 88.1 s (E = 1, rb = 0, 1,068 merges, 46.6k promises exceeded, 0 wasted — the first real counters for the quiet regime), then chunk 2 **panics at the finality assert** ("rollback of region 13279 from 112 would revise its published tick 150"), with the main thread cascading at the poisoned lock (`alloc.rs:1940`) and a worker at `1776`. The crash is **not confined to the conflict wave**: loose-gas drift alone produces a post-publication conflict. The trigger is any conflict discovered after a publication whose rollback reaches below it.
- **Cadence, 28k s1, chunk 250:** survives; ends 1,971 regions (vs ~2,400 single-call), all 4 rollbacks inside chunk 1, digest identical. Publication cadence is itself a path knob the dossier missed.
- **Next decade (55,584 bodies, seed 1, single clean run):** finishes in 146.6 s, 4,930
  regions (fragmented class, region count scaling with cells), **E = 128**, rb = 7 — the
  latch is flat in N one decade above the author's range (64–128 at 14k, 64–128 at 28k,
  128 at 56k, same seed family), which buries the page's "latch grows with scene size"
  reading for good. Wall 146.6 s vs 18.4–44.8 s at 28k: superlinear in N, but on single
  draws per size (P5's premise is again window-fragile).

**4. Novelty.** The standing page's own battery had a dead `seed` argument ("every measurement is one world per size") — all prior allocator verdicts, including the gold e704's readings, had zero seed or replicate control. This run is the first controlled seed × replicate experiment on the topic; the finality-assert crash is new (H0196's allocator assert was a different, fixed one); the quiet-regime cost points (14k/28k) are new; the refutation of "E grows with scene size" and of the cap-cost verdict *as controller properties* are new. Draw-fragility was previously an incidental checker caveat, not a measured result.

**5. The page.** Corrected in place: the header sentence ("the seed alone picks…"), the three refuted lines, the crash scope (quiet family included, shipped line 1451), the cadence knob, and the runs entry. The author's fold-in was faithful to the dossier; the dossier itself overstated.

**6. Goal fit.** Board item 4 (smoothness and the allocator). PRINCIPLES: "Measure before claiming, and never strawman" — the page's standing causal readings were single draws; "i care about the p95/99 results i want the game to be smooth" (12) is not decidable on a system whose per-run cost is a draw and which can crash; "Errors never compound" (13) — the assert is the finality police, and today it crashes rather than degrades. Adoption is cheap: retire two readings, require ≥3 seeds + ≥2 replicates per verdict, and take the publish/rollback boundary decision.

**Why silver, not gold.** The reproducible core is real, novel and premise-correcting, but the formal gold bar — "reproduced, and the held-out predictions held" — fails on both edges: 4/5 pre-registered predictions failed, and the Claim paragraph's quantitative specifics (9×, 4,715, seed-fixed E, cap 1.9× faster) are themselves single-draw numbers that did not regenerate — the exact record-sin the taste log grades on ("results that the shipped code could not regenerate"). The corrected claim (class flips, digest-only reproducibility, crash, quiet floor) *is* reproduced, and I have folded it into the page.

## The experiment that would make it gold
**Frames mode.** One `run_frames` run on the wave and quiet scenes (14k–28k): publication
is continuous there, so if the same finality assert can fire, the crash is in the game's
live path and needs an engine-side fix (refuse the advance or hold publication); if it
cannot, it is a batch-driver rule. That is the only load-bearing unknown left, it is the
author's own named miss, and with it decided the run's adoption is one step.

## What the author missed

1. The quiet family itself crashes the assert — the cannon wave is not the trigger (my quiet-14k probe). The crash scope in the dossier is under-drawn.
2. Publication cadence reshapes the allocator path (1,971 vs ~2,400 regions, rb 4 vs 6–7) at identical digest — a knob the battery never varied.
3. "Most fragmented = slowest" is a draw: seed 3 (1,389 regions, E = 512) finishes in 21.3 s.
4. The dossier's Claim sentence commits the sin the run indicts: its headline numbers are one window's draws, stated flat. The two-window truth is direction-only.
5. Minor: the assert's shipped line is 1451 (1456 is the patched tree's numbering); "E = 1, 0 rollbacks at every size tried" for the quiet control had no trace behind it (my 14k probe now supplies one — and then crashes).
