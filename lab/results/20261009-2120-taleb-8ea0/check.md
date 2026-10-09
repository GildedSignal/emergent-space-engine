Grade: silver

Reproduced bit-for-bit: both key cells' digests (`8ab0b55c40140b35` rtf 10⁴/30 s = 3×10⁵ game-s in 6.9 s; `03e62d9683a30e1c` rtf 10³/55 s/members 400, worst frame 14.1 ms < 16.7, 620 overflow frames, settle 0.82 s) and the control (`41343a14…`, third invocation; seed 2 differs). Engine carries no growing compute liability to 3.5 days: wall 1.6→6.6 s over 10⁴× load, tails bounded, memory slope (13.6→26 MB) reproduced cross-seed, tracking game time not events. Adversarial: the bench **aborts** (no report, nondeterministic tick) past ~3–4×10⁵ game-s — the promised rtf-10⁵ rung "didn't fit in the minute" but fails in 4.3 s; the paced run the dossier omits works and matches the unpaced digest. Gain: unblinds horizon probes; cost: a bench script fix, not engine work.

## Reasons

**Reproduction (clean tree, author's own binary at `/home/glmlab/lab-target-1/release/xtask`, patch empty).** Every number in the dossier's tables matches `ladder.jsonl`. My reruns: R1 = 6.9 s / RSS 26.5 MB / player dead / digest identical; R2 = 26.6 s / worst 14.1 ms / hitches [0,0,0] / digest identical; control digest identical a third time. Cross-process bit-reproducibility under load holds, as the canonical-cut design (mod.rs:99-102, decisions scheduled at canonical ticks) predicts. My paced 55 s cell: digest equals the unpaced A-rtf100-s55 digest — pacing-independence confirmed under real 60 Hz wall.

**Predictions.** Pre-registered: `predictions.md` mtime 21:24:50 precedes the driver (21:25:31) and all runs (jsonl ends 21:29:16); dossier 21:30:02. Six falsifiable predictions with kill criteria and both-side controls; 4 held, 2 misses (settle growth, memory cell, player survival) honestly reported and correctly re-read. This is the pre-registration discipline the lab asks for.

**Adversarial cases of my own (5 new cells).**
1. rtf 10⁵, 30 s (3×10⁶ game-s): the bench errors out at ~2.6×10⁵ game-s ("no view: the player is lost (fault None, doll 2)"), exit non-zero, no report, no digest; the abort tick moves between invocations (5.283e10 vs 5.338e10) — wall-dependent, though completed runs are bit-stable. The dossier's stated reason for skipping this rung ("could not fit in the minute") is wrong: it fits in 4.3 s and fails.
2. rtf 3×10⁴ (9×10⁵ game-s): aborts at ~4.2–4.4×10⁵ game-s. So the harness's measurable horizon tops out at ≈3×10⁵ game-s — exactly where the author's ladder stopped. Past it, a dead player's view eventually fails and the bench crashes instead of reporting (it reports fine with a dead player at shallower depths). This is the real harness defect, one level deeper than the script-death the dossier names.
3. Cliff bracket at low rtf: alive at 5 500 game-s/rtf 100 (burn 33 game-s) → dead at 8 250/rtf 150 (burn 50). The cliff is ≤ ~2.3 h at the low-rtf end, tighter than "1.5–4 h". Burn length and depth still scale together (the author's confound caveat is correct and stands).
4. Seed 2: dead at 15 000 game-s — the cliff is not seed-1-specific.
5. Seed 2 deep run (3×10⁵ game-s): RSS 29.4 MB (seed 1: 25.9–26.5), overflow 598, worst 8.5 ms, settle 1.15 s. The memory slope reproduces; seed 2 carries 3.4× the event rate with the same +17 MB, so the growth tracks game time (or ticks), not events — a mechanism clue the author could have had for one run.

**Novelty.** Digest-canonicality across pacing/budget is known and committed (adba97a: five runs, two paced, one digest) — properly used here as a control, not claimed as new. The horizon-depth measurement itself (hour → days of game time: cost/game-second, tails, settle, memory, player fate) appears nowhere in docs/HISTORY.md or the bench commits; HANDOFF §"Risks to attack first" and line 74 (one-hour budget "open, not dropped") make it an on-plan risk line, now measured.

**Goal fit.** PRINCIPLES #10 "Measure the way the player plays" and #3 "Compute only surprises" are the two lines tested; the engine holds both to 3.5 days. But every decisive cell is unpaced at rtf ≥ 100 with a dead player — the instrument died before the machine did, as the dossier itself concedes.

**Why silver, not gold.** The engine-side result is a solid *negative* (no growing liability to 3.5 days): it closes a risk line but moves no board bottleneck by 10×, deletes no component, and overturns no board premise (the board never claimed liability grows; its live questions — kicks, changeover, encounters — are untouched). The run's actionable finding is a harness fix that is proposed, not built, so nothing is adoptable within one step. The record also carries three dings: the paced run silently timed out in the author's own driver (50 s timeout vs 55 s run) and is absent from the dossier — I ran it, it works and matches; the predictions' promised rtf-10⁵ rung was dropped with an inaccurate excuse that hid the abort; and "16 runs" undercounts the 18 JSONL records. No number contradicts the log; all claimed numbers regenerate.

## The one experiment that would make it gold

Fix the bench so a scripted player *stays alive* and the run *reports* at any depth: station-keeping decisions (or depth-matched decision logs) replacing the ∝rtf burns, plus graceful handling of the dead-player view abort (report `player_alive: false` with the digest, as shallower runs already do). Then re-run the same ladder: a living player's gather/thrust/handoff costs at hour-to-day horizons — the thing every probe of b-readout-cost and b-h-live needs. That is one bench-side change, zero engine risk, and it converts this run's confounded cliff into an instrument.

## What the author missed

- The top promised rung (rtf 10⁵) fails loudly in 4.3 s — the harness's horizon ceiling (~3–4×10⁵ game-s, dead-player view abort, nondeterministic tick) is a stronger and more fixable finding than the script-death cliff, and it was reachable inside the author's own time budget.
- The paced cell — the one closest to "the way the player plays" — was killed by the driver's own timeout and went unreported.
- The headline "compute per game-second falls ~8× per 10× horizon" is partly arithmetic: at fixed wall seconds, game_s = seconds·rtf sits in the denominator, so ms/game-s falls ∝1/rtf even with constant wall. The substantive content is wall growing 1.6→6.6 s over 10⁴× load and ladder A's fixed-rtf fall (1.20→0.58 ms/game-s over 500→5 500 game-s); the dossier blends the two.
- The memory slope's mechanism was left open when one cross-seed comparison (which I ran) already separates event-count from game-time tracking.
- A fat-tail lens should have run ≥3 seeds per rung; single-cell evidence is what left the memory slope "one rung pair".
