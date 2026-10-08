Working...
**Grade: silver** — written to `lab/results/20261008-0458-second-20261008-0338-library-f045-0102/check.md` (only file touched in the run folder; `patch.diff` is empty, nothing to apply).

**What reproduced** (clean tree, /tmp/check):
- All three defects, independently re-derived, not just re-run: vr-flip control 3.141 rad broken vs 9.602e-7 fixed; mirror-state corruption exactly 2|vr| = 1.521e-2 with a/e/position preserved; flip rate 71.7–75.2%; mislabel arithmetic 6.28 / 100.53 kicks per "orbit", 47.75 true orbits for "300"; teleport 0°→183.6° at step 1.
- Original published row digit-for-digit (`shock_probe.py`, 28 s; harness byte-identical to the original branch).
- Decisive v2 sweep bit-identical on 4 of 7 rows inside the window (τ=0.05–0.17, every column); τ=0.20–0.30 recorded as not finished.

**My four attacks**: v2's Kepler validated to 1e-12 vs a 2M-step RK4 at e≤0.2; 24 interleaved phases confirm the τ=0.25 "boundary" is phase/horizon noise (0.83→1.07→1.84); μ=1e-2 shows no τ-crossing either (kill generalizes); teleport-reach map corrects the record.

**Two findings the author missed** (why silver, not gold — the physics is done):
1. The teleport fires at **only τ=0.25** (μ=1e-3), not "every run" — but that is exactly the sole A>1 cell (1.68) of the published row, and the checker's μ=1e-2 crossing cells (1.52, 5.87) are also teleported: every pro-crossing cell ever published sits on a teleported cell. The dossier's reach claim is false; the kill is sharper than claimed.
2. "The toy never supported a convexity measurement" is μ=1e-3-specific — at μ=1e-2 the corrected toy measures it cleanly (A16 = 23–67, 12/12 phases).

Plus: P3' point prediction failed (disclosed honestly; failure direction strengthens the kill). Gold path: a 60-second correction pass on those two lines — no new physics needed. The kill itself (don't freeze A(τ) into q-cadence — queued at `lab/queue.txt` line 31, no rung file) is adoptable at zero cost regardless of grade.
