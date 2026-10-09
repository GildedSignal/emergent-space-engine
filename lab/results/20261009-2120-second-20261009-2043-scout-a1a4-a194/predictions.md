# Predictions — second-author run on 20261009-2043-scout-a1a4

Written before running `plunge_readout.py` (decisive) and `plunge_record.py`.
The checker's path to gold: honest readout re-measurement (bracket + Newton-in-ψ,
timing AND accuracy, winding sweep |1−L/Lc| ≥ 10⁻³), the missing P3 script, the
two prose numbers, the restated near-critical column. None of the numbers below
were measured by me yet; the tube's edge-vs-oracle errors (the "floor") are taken
from the first run's own record (run-output.txt, verified reproducible).

- **PR1 (readout at the table floor).** Bracket + Newton-in-ψ (3 iterations,
  local GL4) readout error ≤ 5× the tube's own edge error (floor), for r, φ and v
  in every case A–F, photon G, and sweep k=3..7. I.e. the readout mechanism adds
  nothing above the compiled table itself; the floor, not the reader, decides.
- **PR2 (cost, the original P4 prediction).** < 20 µs/sample per readout in every
  case (pure-Python scalar math on this runner), and winding-independent:
  max/min cost over the sweep k=3..7 < 2. Three iterations converge:
  |u(3 iters) − u(5 iters)| < 1e-12 everywhere, including the coalescence-spike
  panels at k=7 (safeguarded Newton, smooth monotone clock integral).
- **PR3 (the shipped readout re-graded).** The shipped linear-interpolation readout
  sits ≥ 100× above the floor at case C (checker measured 6.2e-6 against a ~1e-12
  floor) and degrades with winding: error at k=7 ≥ 3× error at k=3. So the
  original 3.08 µs number buys ~1e-6 accuracy, not table accuracy.
- **PR4 (record fixes).** The P3 pair-precision table regenerates from shipped code
  to the recorded digits (L = Lcrit(1.2)·(1−10⁻ᵏ)). The restated near-critical Δφ
  (60 dps, split points at u = a−20b, a, a+20b) continues +3.256 ± 0.003 per decade
  through k=7, agrees with the checker's 17.329 / 20.585 / 23.842 to < 2e-4
  relative, and the restated 512-panel errors land within 2× of the checker's
  4.2e-7 / 1.8e-4 / 7.4e-3 (k=5/6/7) while matching the shipped column at k ≤ 4.
- **PR5 (prose numbers).** log₁₀(pair b) vs k slope ∈ [−0.52, −0.48] for k = 3..7
  (b ∝ √δ, killing the dossier's "b ∝ δ"); |Lcrit(2000)/(3√3·2000) − 1| ∈
  [2e-8, 6e-8] (the checker's 3.95e-8, killing the dossier's "2×10⁻⁹").

**What would falsify the dossier's readout claim:** Newton-in-ψ accuracy stuck
orders above the floor (like the checker's implementation-limited 1.2e-7), or cost
> 20 µs/sample, or cost growing with winding. Then "exact to 1.3e-10 with O(1)
readout at 3 µs" survives only in part, and I report which half fell.

**Verdict rule (written before the run):** the claim holds if PR1 and PR2 both
pass everywhere; the claim's "3 µs" specifically is expected to fail (PR3) and be
re-stated as the honest mechanism's number.
