# Predictions — run 20261008-0234-spacex-0083 (spacex lens)

Written **before** the decisive experiment (the jet bench). Held-out cases: the per-kick cost
decomposition has never been measured on the shipped plane; the numbers below are Fermi estimates
from the shipped code's structure (`Work::kick` = readout + forces + quantize + rebind, rebind =
fit + compile + decode + residual), not tuned fits.

Baseline already measured by the shipped bench (not a prediction): kick ≈ 97–100 µs median,
exact-key hit rate 0.0 (663 exact shapes / 682 kicks), quantized shape hit rate 0.93.

- **P1 (compile share).** The fresh cycle/passage compile is ≥ 60% of a kick's median cost.
  Rationale: the compile is a fresh Gauss–Legendre quadrature over all bands (many exact-integer
  Scalar ops); forces read a handful of tubes; decode is a Newton solve in one panel.
- **P2 (rebind share).** The whole rebind (`bind`) is ≥ 70% of the kick.
- **P3 (forces share).** The force eval (parent tide + secondaries) is ≤ 15% of the kick at the
  plane's ~76 bodies. If forces dominate instead, the jet is not the plane's lever and the
  bottleneck re-ranks.
- **P4 (jet ceiling).** Rebinding with the *previous* shape (`from_shape` on the body's own
  compiled shape, the jet's cheap path) costs ≤ 10% of a fresh compile, so a jetted kick
  (forces + readout + from_shape + ~0.05 amortized compiles, the law.md/red-team-df81 cadence)
  lands ≤ 35% of today's kick: **≥ 3× per kick**, order 5–10× if P1 holds strongly.
- **P5 (drift rate).** A body's quantized shape cell (MemoCode) changes on ≤ 20% of its kicks
  (median ≥ 5 kicks per cell): consecutive kicks nudge (E, L) sub-quantum, so a per-body shape is
  stable long enough to jet between re-anchors. If cells flip almost every kick, the drift is
  fast and the re-anchor cadence (hence P4's amortization) worsens.
- **P6 (sanity).** The decomposition sums to the whole: parts within ±20% of the full-kick
  median; two reruns agree in the medians to better than 2×. Otherwise the split is wrong and
  the run reports VOID for the decomposition, whatever the pieces say.

Kill criterion for the premise (written before the run): compile < 30% of the kick, or
from_shape-reuse > 30% of a fresh compile — then "the kick is compile-bound" is dead, the jet
buys < 1.5× on the plane, and the dossier says so with the measured ranking of parts.
