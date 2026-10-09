# Predictions — run 20261009-1556-redteam-18fc

Written before the decisive experiment, from analysis only (no tuning runs).

**Target premise** (representation.md §2, "Observables are emergent" / "Light is gathered at the
observer"): *"Each visible tube crosses the observer's past light cone once; Newton's method finds
the crossing, starting from the previous frame's."* The implementation
(`crates/universe/src/view.rs::crossing`) is a bracketed Newton with an extrapolated guess whose
slope is clamped to `[1e-3, 1e4]`, a 64-readout cap, and a tick-0 fallback before first light.
`view_rel` covers β ≤ 0.99 toward; the design's stated worst case (bottleneck 5: "a near-c 50 cm
missile"; queue item "γ to 10⁶") is β → 1 and the mutual-speed case, never measured.

**Setup.** `scenario::stream`, Toward, dist = 1e6 ticks, start = 1.2e9, 24 emitters, rtf = 100 and
rtf = 1, 200 frames. Cases: β = 0 (static, control), 0.9 across (control), 0.9 toward (reproduction
of view_rel's grid), 0.999, 0.9999, 0.99995, 0.99999 toward, and observer 0.9c × emitter 0.9999
toward (closing speed 0.999994, arrival rate ≈ 1.7e6).

**Held-out predictions:**

- **P1 (controls pass).** Static and Across cases: mean ≤ 3 readouts per emitter per frame, zero
  dropped emitters, cold and memo gathers agree on every emitter and frame.
- **P2 (reproduction).** β = 0.9 toward reproduces view_rel's shape: memo reads per emitter in the
  2–5 range, no drops.
- **P3 (the attack).** At β = 0.9999 toward the true arrival rate (1e4) sits exactly at the slope
  clamp; at 0.99995 (2e4) and 0.99999 (1e5) the clamp lags the truth by 2–10×. The guess then lags
  the root by (rate_true − 1e4)·frame ticks ≈ 10⁹ ticks per frame at rtf = 100. Prediction: the
  bracketed walk still recovers the crossing at 0.9999 and 0.99995 (correct cold = memo, reads ≤
  10), but at 0.99999 at least one frame drops an emitter (64-read cap hit, or the lagged guess
  evaluates outside the tube and returns None), i.e. the emitter flickers exactly during its
  relativistic approach.
- **P4 (mutual speed).** Observer 0.9c × emitter 0.9999 (rate 1.7e6, 170× the clamp) behaves like
  the 0.99999 case: memo reads ≥ 5× the 0.9-toward baseline, drops if P3 drops.
- **P5 (compression is visible, not a bug).** In every Toward case the crossing tick advances by
  ≈ frame/(1−β) per frame (e.g. ≈ 3.4e9 ticks per frame at β = 0.9999, rtf = 100): the whole
  approach compresses into ≤ 1 frame of observer time at rtf = 100. If the gather survives, this is
  the premise holding in its hardest regime — worth reporting as a survivor with numbers.

**What would make the premise wrong:** drops (P3/P4) or cold ≠ memo disagreements at any β the
game supports (the plane currently refuses past γ ≈ 2,000, i.e. β ≈ 0.99999988 — well above the
cases here), or apparent positions disagreeing between the budgeted (memo) and true (cold) paths.

**Instrument controls:** static case must converge in ≤ 2 reads (instrument can pass); the 0.99999
case is the negative control (where failure is expected).
