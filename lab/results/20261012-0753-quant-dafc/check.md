Grade: silver

**Abstract.** Claim: the plane's first smoothness frontier (wall holds to rtf 1000/417 bodies; delivery floors near 10×; budget knee at 10 ms; readout owns 61–77% of the median frame). Reproduced: readout dominance (share 0.61–0.69 on every rerun), members→gather scaling (p50 0.9→5.9 ms), budget softness (engine max > budget everywhere). Not reproduced at load 1.4–3.0 (author ran at 0.3): 5 ms sufficed at 100× (3 overflow frames, low1 = 100); budget 15 gave 0 hitches (author: 540/hr); m400 broke (31 hitches, engine max 109 ms = 22× budget). Attack: identical commands flip the canonical digest (`6ce6…` ↔ `56f4…`) on byte-identical inputs — schedule independence (claim 5, P6) is falsified, engine-side. Adopt: report the digest flip; the frontier itself is unusable until machine state is pinned.

## Reproduction (clean tree, empty patch.diff, shipped code)

Every table number in the dossier matches its JSON (re-summarised all 11 reports with `summ.py`). Reran four cells (`cargo run --release -p xtask -- universe --bench --rtf R [--members M] [--engine-ms B] --seconds 20`):

| cell | author (load ~0.3) | checker (load 1.4–3.0) |
|---|---|---|
| r100 b5 | 38 ov, low1 9.90, gather p50 3.62 | 3 ov, low1 100, gather 0.95 |
| b10 | 1 ov, low1 100, worst 12.8 | 1 ov, low1 100, worst 11.2 |
| b15 | 3 hitches (540/hr), worst 23.2 | 0 hitches, worst 16.0, engine max 14.3 |
| m400 b5 | 0 hitches, worst 15.0, engine max 7.6 | 31 hitches (5584/hr), worst 115.1, engine max 109.4 (CPU time, threads=1) |

Reproduced robustly: gather share 0.61–0.69 of frame time in all six of my runs; members 400 → gather p50 3.77–5.94 vs 0.7–1.3 at 48 members; engine max exceeds budget in every run; b15's tail ≥ b10's. Not reproduced: "5 ms is 2× too small at 100×", the dip floor ~10× (my b5 paced runs delivered 100× outright), the 540 hitches/hr at b15 (a 3-frame tail), and m400's magnitudes (inverted in severity).

## Attack (adversarial cases)

1. **The canonical digest flips run-to-run.** Same command (seed 1, rtf 100, members 48, b5, 20 s, cut 406050894), byte-identical logged *and* taken decisions at identical canonical ticks, `threads=1`: paced run 1 → `56f49416…`, paced run 2 → `6ce636fa…`, unpaced → `56f49416…`; the author's four same-cut runs all gave `6ce636fa…`. The two attractors differ by ~2,000 events (events/s 227 vs 338). This falsifies the shipped `digest_note` ("one digest, paced or not, on any budget"), H0213's "one digest over five schedules and budgets" as a general property, and the run's claim 5 / P6 ("verified", "right"): four agreeing runs in one machine state were one attractor, not proof. Suspect: `frame_to`'s wall-derived per-frame target (`want = rtf·wall_dt/TICK_SECONDS`) plus the deferred-work path (`universe.rs` advance loop) changing event *content*, not just timing. This is an integrator-level engine bug against PRINCIPLES' first law ("Canonical outcomes are exact and independent of … schedule").
2. **m400 under shared-box load** (the checker prompt's stated reality; "heat and load are part of reality", AGENTS): the frame wall breaks — 31 hitches > 16.7 ms, worst 115 ms, engine max 109 ms against a 5 ms budget. The dossier's own lever ("the budget bounds the number of items, never the cost of one item") is ~10× worse than measured (2.4× → 22×).
3. **b15 repeat**: 0 hitches, worst 16.0 ms — the knee's right edge is within noise of the wall; the "knee at 10 ms" placement is machine-state-dependent, as the dossier itself concedes for the M1 but not for load states of this box.
4. **Load sensitivity**: author load 0.3 vs mine 1.4–3.0 changed overflow 38→3 at the identical cell and digest attractor — the frontier is not a stable function of (rtf, members, budget).

## Novelty

H0210 already measured single points (p99 2.45 ms, no hitch at 100×; "the view gather is 83% of a light frame"); H0211 (p99 2.72, worst 14.5); H0213 recorded a known tail regression (hitches 33–51 ms) and the digest-over-schedules claim; H0214's Next names the plane's readout. New here: the systematic (rtf × members × budget) sweep with pre-registered predictions, the budget-inversion cell, and the dip-floor observation. The digest instability is new and contradicts H0213 — worth an entry regardless of this run's fate.

## Goal fit and errors

Fits board #4 and PRINCIPLES #12 ("minimize spike compute and average compute usage…"). The author's own lens section predicted the trap and the data caught the kill rule; good. Factual slips: P7 graded "right" but b15's engine p99 (6.35) does not exceed its 15 ms budget — only the max (18.65) does; "gather share 61–77% on every run" — r1000's is 0.56. Single seed throughout, against the lab's many-seeds doctrine. b10 post-prediction was disclosed. patch.diff empty and tree clean: every number regenerates from shipped code — the record quality the taste log asks for.

## The one experiment that would make it gold

Pin the machine state (load and frequency recorded and controlled, or both states measured as separate frontiers) and re-derive the frontier on ≥ 3 seeds — after the integrator bisects the digest flip (my case 1), since capacity claims on a plane whose canonical digest is unstable at a fixed cut are built on sand. The digest bisect may itself be the gold.

## What the author missed

The digest control was their strongest-sounding result ("verified end to end") and is the one thing falsified; agreement between four runs that shared one machine state is not independence — the heuristic in their own lens file. Load is part of this box's reality (the window shares it), and the frontier was measured only at load 0.3; the 540/hr and dip-floor headline numbers do not survive it. m400's budget overrun (22×) shows the item-cost lever matters more than reported. No seed variation.
