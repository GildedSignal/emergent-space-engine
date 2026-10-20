# Predictions — 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second author)

The prior run (20261020-1326-inversion-3b88, silver) attributed B13's step-9 `inf`
to the i64 tick wall in `next_periapsis` (`step.rs:275`), and the checker's named
gold experiment is: fly the fix class (overflow reads as `Ok(None)`, "no periapsis
within the tick horizon") and show the lost ships complete with B13's other rows
unchanged. The fix is one branch in `work/wall-fix.diff` (crate edit for this
demonstration only, never merged); the prior run's two print-only tests come along
byte-identical (`work/tests.diff`). Baseline re-anchored on this tree before the
flight: gate 9 FAIL 63/64 `worst ΔE inf` with the `lost=1` trace at kicks=926;
walk draw 27 fault #0 at tick 910984136830, doll 0, period 3.195e19 ticks;
scan 9 = 2/229 (draws 27, 104) — all bit-for-bit the prior record.

Held-out cases (not tuned on; the fix branch was written before any fixed run):

- **P1 (survival, the deletion):** with the wall fix, the full-draw scan loses
  **0/229 at every octave flown** — 8 (baseline 1/229, draw 104), 9 (baseline
  2/229, draws 27+104) and 10 (baseline 0/229), plus step 7 (checker's adversarial
  octave, baseline 0/229): no draw dies to any fault.
- **P2 (the gate flips, and only by losing the anomaly):** B13 at step 9 goes from
  FAIL 63/64 `inf` to **PASS 64/64 with finite worst ΔE**, and that worst lands
  within the brackets' range (step 8: 5.30e-3, step 10: 3.32e-4), i.e. between
  ~1e-4 and ~1e-2. Draw 27's own dE err at 9 becomes unremarkable (baseline
  brackets: 4.49e-3 at 8, 2.00e-4 at 10).
- **P3 (other rows unchanged, bit-for-bit):** B13's verdicts and worst ΔE/ΔL at
  steps 8 and 10 are **identical** to the baseline record (PASS 5.30e-3 / 3.32e-4):
  the fix touches only orbits whose next periapsis is beyond i64::MAX ticks, which
  no healthy row has, so no other row's plan changes at all.
- **P4 (the mechanism dissolves, not mutates):** the instrumented walk of draw 27
  with the fix shows **no fault, alive at exit**, min kick E ≈ the baseline swing
  (−1.17e-9 doll-units — the orbit is physically the same), and a kick count within
  ~2× of 926 (the saturated MAX_STEP kick replaces the refused one; later planning
  may differ slightly).

Kill criterion for the fix-class claim: if with the fix any draw of the stream is
still lost to `Refused("periapsis")` (a second refuser downstream of the same
orbit), or the step-8/10 gate rows shift by more than round-off (a print digit),
then the one-line deletion is wrong — the refusal class has another source, and
the dossier reports that instead of the deletion.
