Working...
Check complete. `check.md` written; tree restored to clean main and the target binary rebuilt from it; nothing else in the run folder touched; no commits.

**Grade: silver.**

What I did and found:

**Reproduced (exact where determinism allows):** applied `work/patch.diff` to clean main, ran all five dossier commands plus seeds 7/42 and my own per-body instrumentation. All four bench digests bit-identical to the author's JSONs; my stock pre-patch flight digest equals the patched one (the patch measures only). Gather share 57.5–68.3% of frame CPU across seeds and rtf 1/100; 96–97% of the bodies loop is `state_rate` eval; unpaced readouts matched exactly (42137). At 400 members the engine overflows its 5 ms budget on 128/300 frames (author: 126/300). The headline constraint naming — the frame is gather-bound, not engine-bound — survives every adversarial case.

**Killed one headline number:** `readouts_per_body_frame` divides by a hardcoded `27.0`, but the loop iterates all alive doll bodies — 53 at the flight setting, 280 at 400 members. True readouts are ~1.06–1.63 per body per frame, not 2.61/12.0. First-sight bodies (handed-out members) cost exactly 2 readouts once, <1% of the total — so the "measured defect at scale", cut 1's 4.6× ceiling, and cut 2's 2× are phantom, and prediction 2 actually held (5/5, not 4/5). This sharpens the run rather than killing it: the guess machinery is at its design floor, leaving refresh quanta (PRINCIPLES #3, #28) as the only real ≥10× lever — which is unbuilt, hence silver, not gold.

**Novelty (partial):** H0210 already recorded "the view gather is 83% of a light frame"; H0213 tracked 1.2 readouts/emitter. New: the inside-the-gather attribution, per-readout cost, and the flight/400-member frame budgets. Also flagged: several dossier cells don't match the run's own JSONs (rtf1 gather p50 2.36 vs 0.538; kick median 60.3 vs 46.8), and the 4.0× cold inflation didn't reproduce on a quiet machine (1.0×) — load state, not intrinsic.

**Gold path:** build the refresh-quantum gather, measure the ≥10× cut with digests unchanged.
