Grade: gold

**Abstract (for the integrator).** Claim: the plane's frame loop already is the allocator at plane scale — digest bit-identical across budget/threads/pace through 100 % overflow — but under *sustained* overload the global horizon collapses the player's presented time while events/s stay budget-proportional, so the work worth doing is rule-8 rung 2 (per-region staleness), not a scheduler. Reproduced bit-for-bit (`a0096d59e1`, `bfacdfc5bb`, held-out seed 3 `545df366f5`); cliff reproduced (309→0.098; author 309→0.032); mechanism proven by my differential: members 4/100/400 at one budget → rtf 1000/0.31/0.098. Gain: kills the least-slack/QoS scheduler plan; the missing rung is worth ~10³–10⁴× presented time under sustained load. Cost: one change in `advance`/`frame_to` plus a digest guard; allocator retirement already half-decided.

## Reproduction (clean tree, `main` at a838a28, no patch needed for the JSON runs)

| run (mine) | digest | rtf median | events/s | h16 |
|---|---|---|---|---|
| m48 rtf100 e5 t4 | a0096d59e1 ✓ | 100.0 | — | 0 |
| m48 rtf100 e1 t1 unpaced | a0096d59e1 ✓ (combo not in author's set) | 100.0 | — | 0 |
| m400 rtf1000 e5 t4 | bfacdfc5bb ✓ | 309.6 (author 309.2) | 3071 (2963) | 0 |
| m400 rtf1000 e2 t4 | bfacdfc5bb ✓ | 0.098 (author 0.0319) | 1315 (934) | 0 |

Adversarial, held out (never run by the author): seed 3, m400: e5 vs e1 → same digest `545df366f5`, rtf 1000 → 0.020, events/s 2596 → 587 (budget-proportional). The cliff and the digest invariance hold on an untouched seed. Worst hitch 16.03–16.64 ms, hitch_counts [0,0,0] everywhere, as claimed (the 17.3 ms outlier in the 8 s trace rerun was disclosed).

## Mechanism — verified in code and by differential

`advance` (universe.rs 822–833) takes the horizon as the **global** min over the heap's min and all deferred deadlines; `frame_to` (862–874) clamps `now` to it. Differential at fixed budget/load (rtf 1000, e2, t4, seed 1): members 4 → rtf 1000.0, members 100 → 0.312, members 400 → 0.098; events/s 254/1171/1315 (rise with members — work done is budget-bound, presentation is fleet-bound). This is the cleanest proof the author could have run: the collapse is caused by *another region's* deadlines, exactly the rule-8-rung-2 defect. plane.md foundation 7's "brief, smooth dip" is verified for bursts (p4: lowest 1 % 619×) and falsified for sustained load; engine.md rule 8's fixed sacrifice order is violated (the player waits; nothing goes stale). Both doc references checked and accurate.

Wave (claim 5): reproduced in direction — engine p99 3.75 ms (t4) vs 1.90 ms (t1); author 5.53 vs 2.04. Code line 815 confirms `resolve_wave` fires for every ship whenever threads > 1 (kind-triggered, as stated).

Allocator unused (claim 6): `emergent-universe` deps are space/engine/lattice/lattice-event; `emergent_allocator` appears only in its own examples/tests and `xtask/src/regions.rs`. Verified — but see novelty.

## Predictions

`predictions.md` mtime 12:39:35, first run output 12:40:09 — written before the runs. P1 held everywhere (including my held-out seed). P2 half-held, P3 inverted, P4 wrong — all disclosed in the dossier with their implications, and P3/P4 *are* findings (the wave pessimizes; overload bites at members 48). No tuning; the misses are the falsifications the predictions existed to catch. Precedent (1 Oct red-team) took silver for *concealing* a failed prediction; nothing is concealed here.

## Novelty

- Digest invariance over schedules/budgets: H0213 already had "one digest over five schedules and budgets" — the new part is threads × pace × 100 % overflow.
- The sustained-overload cliff, the bistable presentation, and the wave measurement: not in HISTORY.md, docs, or the taste log. The H0212 tail work is hitch tails, not presentation collapse. Novel.
- Allocator unreachable by the plane: already recorded in HANDOFF (7 Oct deletion-candidates note, 11:15 UTC, before this run). The dossier presents it as a finding without citing that — confirmatory, not a discovery.

## What the author missed

1. **The headline statistic is the wrong column.** "Advance of presented time per frame falls 523 305 → 845 (~600×)" is computed on the trace's `target` column; presented time is the `horizon` column (median advance 524 206 → 59). The collapse is real and *larger* than headlined (rtf median 309 → 0.032 ≈ 10⁴×), and the author's own lens note names the horizon column as the clean one. Understatement, not fabrication; flagging for numbers hygiene.
2. **The horizon is bimodal, not just slow**: 400/479 frames advance ≤ ~100 ticks, then it leaps by exactly 2^19 (79 frames). The player's sky would update in stroboscope steps — hitch-shaped presentation invisible to medians, and a stronger argument for the rung.
3. The members 4/100/400 differential (above) — the author argued the mechanism from code reading only.
4. "Budget-proportional events/s" is only roughly true (2963→934 is 3.2× for a 2.5× cut; mine 2.3×) — superlinearity unexamined.
5. Claim 5's members-48 pair is at rtf 100 (p1a/p1c), unstated; and p99 conflates wave overhead with thread contention — a wave-off control (one line) would separate them.
6. Report JSONs record no `threads`, so the p1/p2 thread combos are unauditable from artifacts alone; `machine_after` therm/batt/swap probes are macOS sysctls and report "unavailable" on Linux (only uptime/loadavg recorded).

## Fit

Board bottleneck 4, register "adopted, not built". Principle 12 ("the algorithm that allocates the work… the most important one") is answered by measurement: at plane scale the queue suffices and the defect is one rung; principle 1 (delete the second allocator); principle 22 (the horizon reads the queue, not a forecast). Scope honestly limited to plane scale, one scene family, Linux orders of magnitude — the author names the region-scale question as open, and the unification claim licenses nothing beyond the plane.

**Why gold:** every number reproduced (digests bit-for-bit, timings same orders on a shared machine); the mechanism independently confirmed by code and a differential the author didn't run; a premise on the board's focus list is falsified with the fix scoped to one rung; the prediction record is honest and pre-registered. Adoptable now: stop planning a scheduler for the plane, build rule-8 rung 2 with a digest guard, re-measure the wave on the M1 before deleting it.
