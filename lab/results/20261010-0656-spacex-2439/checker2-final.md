Working...
Check complete. **Grade: gold** — written to `lab/results/20261010-0656-spacex-2439/check2.md`, tree restored to pristine (`git apply -R` verified).

**What I did (blind to check.md):**
- **Reproduced** from `work/patch.diff` in a clean tree (release build, 28 s): ran the dossier's exact commands at N=130/859/3,259/6,203 plus `--no-rekey-walk` and `--seed 7` pairs.
- **Slope 0.429 µs/body/frame** vs the author's claimed 0.43 (1% match); `walked/frame` = N minus the due few at every size; events/s flat 453–454; engine p99 flat in N (the term is not event work); rekey-walk deletion changes nothing (no 16× drop — the author's pre-registered kill criterion fired and was honestly reported).
- **Determinism cross-check**: my fresh build reproduces the author's stored N=6203 digest `3ea75405…` bit-for-bit; digests identical across the rekey flag at three (N, seed) pairs including my adversarial seed 7; pristine-vs-patched default scene shares digest `a7d089f9…` (patch hygiene holds).
- **Mechanism verified in source**: `advance` breaks only when the queue empties — every entity is peeked/`set(None)`/requeued per frame because the queue orders by light-delayed deadline while deferral compares canonical tick.
- **Novelty**: H0012–H0030 scan kills are the old `emergent-engine` crate; nothing measures the plane's frame loop. plane.md §7's "bounded work per presented frame" is shown broken at ≈1.2×10⁴ quiet bodies (5 ms budget), ~430 s/frame at 10⁹ — a premise correction on the engine's path, with the instrument and three fix directions adoptable in one step.

**Missed by the author (noted in check2.md):** view_gather (146 ms p50 at 6,203 bodies, 88% of frame, 53× the scan) must be fixed with or before the queue or nothing player-visible moves; the sublinear middle points (cache) disclosed but undiagnosed; horizon-vs-outcome neutrality nuance; the 200k-hauler rung unexplored.
