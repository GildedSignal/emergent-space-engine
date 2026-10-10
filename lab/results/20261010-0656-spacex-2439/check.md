Grade: gold

**Abstract.** Claim: the plane's frame loop pays ≈0.43 µs × N per frame even when nothing is due — `Universe::advance` defers and requeues every non-due entity: a hidden tick (P14). Reproduced on my own build from `work/patch.diff`: engine p50 0.054→2.81 ms (71→6,203 bodies) at constant 453 events/s; walked/frame = N−60…124 at every size; the rekey walk is acquitted (norekey 2.70 vs 2.81 ms, digests bit-identical, including the author's exact 6,203-body digest 3ea75405…); the default-scene digest equals the pristine binary's. Adversarial: at 9,888 quiet bodies engine p50 hits 4.7 ms — the whole 5 ms engine budget. Gain: per-frame cost returns to O(events). Adoption: one step — re-represent the queue by key tick (or a tick calendar), with digest equality as the regression.

**Reproduction** (clean tree at a838a28, patch applied, `cargo build --release -p xtask`, CARGO_TARGET_DIR=/home/glmlab/lab-target-3; every command ≤ 60 s except the 6,203/9,888-body runs at 62/98 s wall, view-bound):

| N | author engine p50 ms | mine | events/s (mine) | walked/frame (mine) |
|---|---|---|---|---|
| 71 | 0.058 | 0.054 | 453.0 | 57.4 |
| 130 | 0.065 | 0.069 | 453.3 | 115.9 |
| 859 | 0.21–0.23 | 0.232 | 453.3 | 838.9 |
| 3,259 | 1.02–1.12 | 1.32 (loaded box) | 453.2 | 3,218.9 |
| 6,203 | 2.45–2.67 | 2.81 | 453.5 | 6,138.3 |
| 9,888 (mine) | — | 4.70 | 453.0 | 9,765.2 |

Slope ≈ 0.45 µs/body/frame (author 0.43). Digests bit-identical where configurations coincide, across the author's runs, my runs, and my pristine build: default 71 a7d089f9… (patched = pristine binary); rekey = `--no-rekey-walk` at 859 (c0a306f1…) and 6,203 (3ea75405…); rtf 30 at 3,259 5b3f34fa… = author's. rtf 30 at 3,259: 0.894 ms (author 1.02–1.47) — the term is per frame, not per game-second. The rekey acquittal reproduces: norekey 2.70 vs rekey 2.81 ms at 6,203.

**Held-out cases.** `predictions.md` (07:08:34) precedes the held-out matrix (07:09+) in file times, after the disclosed 71/6,203 smokes; `run.log` is empty, so mtimes are the only order evidence. Held: linearity, event-rate constancy, rtf independence, digest neutrality at every pair. Failed as pre-registered: the rekey deletion (≥16× predicted, ≈1× measured) — the kill criterion in prediction 5 fired and the author re-attributed with the `walked` counter. That is the lab's ethos working (H0183), disclosed in the dossier's first line of Predictions. Both mid-scale intervals missed low (0.21–0.23 vs 0.34±0.06; 1.02–1.12 vs 1.27±0.15) — called "held" a touch generously, but the numbers are printed next to the claim.

**Adversarial (mine).** (1) 9,888 bodies: engine p50 4.70 ms ≈ the 5 ms budget at 453 events/s, walked/frame 9,765, overflow_frames begins to creep (3→4), p99 8.2 ms — the "budget exhausted by the scan alone at ≈10⁴ quiet bodies" wall is real, and per-band slopes rise with N (≈0.26 µs at mid-N → ≈0.84 µs at 9,888 in my batch), so the affine 0.43 µs extrapolation to 10⁹ is optimistic, not alarmist. (2) Digest neutrality at a pair built and run by me only (859 norekey): bit-identical. (3) Cross-build determinism: my binary reproduces the author's stored digests bit for bit at four configurations.

**Novelty.** No HISTORY entry measures the frame loop's own cost: H0210's limits name the gather share (83%) and kick cost (29 µs); H0213/H0215 own the readout; `b-readout-cost` is queued for the gather. The advance/defer scan is an unowned term; nothing tried it before. The finding kills the implicit premise that the frame budget is spent on events (plane.md foundation 7, "bounded work per presented frame").

**Goal fit.** PRINCIPLES 14: "No work for no reason, so no ticks" — the loop that asks who is due ticks over every body; P22: "the simulation decides, heuristics schedule" — the schedule's cost must follow events too. Precedent: gold 20261006-0737 was a measured kill with nothing to build; this is the same shape, and it redirects the kicks/encounters work: cadence gains are invisible per-frame while the scan owns the budget. Adoptable within one step: order the queue by key tick or bucket by tick (a `Calendar` already exists in `lattice-event`), digest equality as the regression — the method this run used.

**What the author missed.**
- "engine p99 … does not grow with N" is overstated: 1.9→5.5 ms (71→6,203, their own files) and 8.2 ms at 9,888 (mine) — a ~3–4× creep, likely heap/cache on event requeues. The p50 conclusion is unaffected.
- The mid-scale misses are convexity, not noise: the true curve is superlinear in N (log-heap + cache), which the author only concedes for the 10⁹ extrapolation.
- Attribution of the residual slope to the defer path rests on the walked counter, the rekey acquittal and source reading — no semantics-preserving deletion of the defer path exists, so the proposed O(due) fix is a design note, unmeasured. The one gold-making experiment, if built, is the tick-ordered queue itself.
- The larger per-frame O(N) wall is the view gather (≈24 µs/body/frame, 88% of a 6,203-body frame — 149 ms/frame, far past the 16.7 ms frame before the engine term bites); correctly left to `b-readout-cost`, but the plane's real scaling wall today is the gather, not the scan.
