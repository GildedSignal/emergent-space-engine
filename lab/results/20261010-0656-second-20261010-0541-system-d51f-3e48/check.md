Grade: gold

Abstract: Claim: the incremental deadline (last doll-chain readout carried by its velocity — the arrival rate `1+n·β` in position form — re-anchored only past ⅛ of the light distance) deletes the scheduler's per-event walk with digest and view bit-identical at settle cuts. Reproduced exactly: walks 1123→42 (rtf 1000: 4224→42), all eight configs' equality asserts pass, deadline err med 2.06e3 / max 2.07e6 ticks, carry 5.49e-8. My five adversarial cases hold too: seeds 13 (the first checker's wall-divergent seed) and 42, a 0.5 ms wall budget, 600 frames (walks pinned at exactly 42). The saving is −26.6 µs on the **mean** engine frame — the walk tax to the arithmetic — flat on the rtf-100 median: the silver's "46% of the median" was a mean/median conflation, here corrected. Adoptable by flag-flip plus constant re-derivation.

## Reproduction

`git apply work/patch.diff` clean; `cargo test --release -p emergent-universe --test lab_arrival -- --nocapture --test-threads=1` (13 s). Every deterministic number regenerates exactly: events 2827, walks 1123→42, 94→38 (rtf 10), 4224→42 (rtf 1000), floor sweep 42/147/438, stream control 7680 levels / 0 hits / 0.0%, memo hit share 2.9%, deadline err med 2.061e3 max 2.070e6 ticks, carry-vs-walk 5.49e-8, all digest/view equality asserts pass. Timings run ~1.7× the author's (my load 2.9 at start vs their ~1.0; 13 GB free) — inside their stated noise band; the walk-count arithmetic closes on my run too (seed 7: −45 µs measured vs −38 predicted; rtf 1000: −130 vs −148). Full crate suite: 57 passed, 0 failed (the author's 56 + my adversarial test) — the default path is untouched, verified. The original record's corrected control (reset-before-gather, 7680/0/0.0%) and the per-call µs distinction are both fixed in the shipped test as claimed.

## Predictions

`predictions.md` precedes the decisive run (file times: predictions 21 min before run-log.txt, which precedes the dossier). Held: 1 (≤150 walks: 42), 3 (digests, all 8), 4 (views, all 8), 6 (presented time ≥ 90%; identical to 4 digits on seeds 7/3, 99.6–100.6% on my rerun), 7 (rtf dilution). Falsified and reported, not hidden: 2 (median drop — flat at rtf 100, −86.7 µs at rtf 1000 where the median frame carries 39 events) and 5 (the relative error form; the provable bound is the anchor-distance form). Both falsifications are instrument errors, not mechanism errors: the mean drop equals the walk tax exactly (1081 deleted walks × per-call µs ÷ 300 frames), and the max absolute deadline error is 0.36% of the worst body's light distance. This is H0183 done right — the first checker's gold criterion ("median drops ~26 µs") inherited the silver's mean/median conflation, and the run corrects both with closing arithmetic. A falsified *presentation unit* with the mechanism intact does not block gold; a silently passed one would.

## Adversarial cases (mine)

1. **Seed 13** (diverges on raw flight cuts under the 5 ms wall, per the first checker) and **seed 42**: digest and view equal at the settle cuts; walks 846→37, 890→44 — the same amortization on unseen seeds.
2. **0.5 ms wall budget** (heavy bites, forced different resolution order between modes): digests and views still equal at the settle cuts; presented-time ratios 1.03–1.04 (no rtf collapse — the lagging deadline did not starve the flight). The settle-cut equality is not an artifact of a never-biting budget.
3. **600 frames** (2× flight): incremental walks pinned at exactly 42 while the walked mode grows 1123→1712 — the anchor count is O(bodies), not O(events); amortization does not decay with flight length.
4. **Full suite** on the default path (above).
Not run by me either: relativistic *kicks* (below).

## Novelty

The parent silver (20261010-0541) measured the tax and designed the deletion; this run builds and measures it — exactly the named gold experiment. No H entry or doc specs an arrival-rate deadline carry before it (H0215's "readout as a partial step" is the motion-law readout, a different mechanism; `20261006-1931-b-readout-cost-43c6` — the queued readout-cost build — died VOID at a 429 and targeted the partial step's force, not the scheduler walk). Secondary novelty that should be adopted as a claim: the digest's schedule-independence, previously a design assertion, is now *tested* under a real scheduling perturbation (different resolution order, different bite patterns, 13 configurations counting mine).

## Goal fit

Board #1 at the scheduling layer; the deleted component is `apply`'s per-event `root_state_raw` walk (26.7× fewer walks at rtf 100, 100× at rtf 1000, bounded at 42 across flight length). PRINCIPLES 17 ("the best part is no part" — the walk is deleted, not optimized) and 19 ("a fix signals the wrong representation" — the walk repaired the queue's lack of the arrival rate; the carry is the representation that needs no repair). Honest scope: the saving is ~7% of the mean engine frame at rtf 100 and −86.7 µs of the 1094 µs median at rtf 1000 — modest against the gather (13–18×), but it caps the readout pattern news gravity would otherwise multiply per (source, kick), and the mean/median correction tells the integrator exactly what to expect on the M1's p95/p99 metric (nothing at rtf 100, ~8% at rtf 1000).

## What the author missed

- **Bookkeeping:** the dossier's engine timings (399.0→372.4 µs, 54.8→57.8 µs, 7.18 µs/call) come from an earlier execution than the run-log.txt it cites as "the full log" (426.5→398.8, 62.3→62.6, 7.57 µs). Same structure, within noise, but the dossier should quote its own log.
- **One loose arithmetic:** "the median frame carries ~2 events ≈ 14 µs of walk" overstates ~2.5× (2 events × 0.397 walks/event × 7.2 µs ≈ 5.7 µs). The flat median is measured directly, so nothing rests on it.
- **The floor's meaning:** prediction 5's 250× failure on near bodies shows the re-anchor bound is relative to anchor distance + floor, not the body's own distance; near-body deadlines carry ~2e3-tick error (harmless here — digests equal — but `REL_DEADLINE`/`FLOOR_DEADLINE` must be re-derived from the scheduler's actual tolerance before the flag flips, as the author only gestures at).
- **The stated β→1 gap cuts deeper than "no shipped scene":** the carry's error grows with worldline curvature, and the plane's bodies are slow; nothing in this record exercises a fast *curved* worldline. The inertial-0.99c check (5.49e-8, flat in t) is necessary but not sufficient — re-measure the re-anchor cadence when motion law v2 brings β→1 kicks, as the author says.
- The 42 anchor walks' own deletability (anchor at handouts/rekeys only) is proposed, not measured.

Machine: Linux 6.8, 8 vCPU, load 2.9→0.4 across the runs, 13 GB available; every process under 2 GB.
