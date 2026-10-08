# Predictions — 20261008-2031-second (r6, the view at gamma)

Written before the decisive run. Tuned on: the pilot (γ ∈ {1, 22.4, 70.7, 125, 250, 2×10⁶} at
β_o = 0.3; 2×10⁶ at β_o = 0.05) fixed the thresholds and the criterion set. Held out: γ ∈ {2.24,
255} in full, the whole β_o = 0.05 ladder, and every pooled percentile.

- P1: `kavg` passes all four criteria; pooled bright_p99 ≤ 0.08 (the residual is the intra-window
  arrival wobble at β_o = 0.3, inherent to any sprite keyed by k alone).
- P2 (held out): pooled bright_p99 for β_o = 0.05 alone ≤ 0.02 (the wobble scales with β_o).
- P3: `instant` fails `bright` with p99 ≥ 1.0 (≥ 10× tolerance) and passes the solver criteria;
  its below-Nyquist rotation is honest per emitter (phase_below_p99 ≤ 10⁻⁶) — the failure is
  temporal, not positional.
- P4: `raw-obs` fails `solve-fail` (order 0.1–3%) and `wrong-roots` (≥ 6000 of 6336 per 2×10⁶
  case) but passes `bright` within kavg's margin: at thousands of orbits per window a wrong root
  is invisible to the fluence criterion (both render ≈ the time-average). The two criteria catch
  different failures; that is why both are frozen.
- P5: `exact-exposure` (positive) passes everything; its bright differs from kavg's by < 10⁻⁶
  (doll root errors ≤ 1.6×10⁻⁸ s).
- P6 (held out): at γ = 255, β_o = 0.3 (≈ 2.03 orbits/frame, near-integer ratio) the instant
  law's frozen fraction ≥ 0.8 (the wagon wheel, per-emitter statistic on a flyby-free record);
  at γ = 125 (0.94 orbits/frame) it is ≈ 0.3: above the boundary the apparent rotation is
  arbitrary — frozen only near integer ratios, wrong speed or direction elsewhere.
- P7 (diagnostic): `kavg-global` (global approaching k as the memo key) also satisfies the fluence
  criterion (≤ 0.05): for whole-orbit windows the orbit-averaged arrival compression equals
  √((1+β)/(1−β)). Local geometry is required for the crossing itself and any sub-orbit structure,
  not for the memo key. If this fails, the rung still stands (it is not a configuration).
- P8: doll-solver iters ≤ 12 at every case, fail 0, wrong 0 (flyby-free removes the only stress
  the original record had; staleness is absorbed because the doll-frame arrival equation is
  globally near-linear in the emission time).

Kill criteria for my own claim: if kavg's pooled bright_p99 > 0.1 the sprite law does not render
the received history within its own wobble margin and the rung KILLs it (the premise failure would
then have no cheap fix in the design's own vocabulary). If instant's pooled bright_p99 < 0.1 the
premise failure itself evaporates on the corrected instrument and the original claim is refuted.
