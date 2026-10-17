# Predictions — 20261017-0238-second-20261016-2138-dynamics-217f-e704

Written before the decisive runs (all calibration so far: 8 cells, one smoke run; 128 cells,
one timing run; no arm comparisons flown yet). The checker's named experiment: a tax that
survives its surface — ≥10⁴-body batch (and frames) comparison, latched vs decayed, enough
interleaved reps to beat run-to-run noise — paired with per-region escalation (ES_LOCAL).

Scene family: the original run's Newtonian battery scaled in cells only (per=8 clusters,
8000-unit spacing, stagger 30): cells=128 → 1,408 bodies / 256 regions; cells=1280 →
14,080 bodies / 2,560 regions. All conflicts are real promise breaks (Fermi-cannon lights
crossing quiet clusters' true boxes).

- **P1 (latch level grows with scale).** The global escalation's frozen level is 2^(number of
  conflicts before the global quench), and more cells means more ignitions before forecasts
  cover the crossings: shipped latches at E ≥ 32 at cells=128 and E ≥ 128 at cells=1280
  (calibration already showed E=32 at 8 cells with 5 rollbacks, against the original's E=4 at
  4 cells). The ratchet is not just permanent — its latch level scales with the conflict wave.
- **P2 (the tax separates at scale).** merges_avoided per 1000 chronons, shipped vs decay, on
  the same scene: at 4 cells the ratio was ~×1.5 (checker's same-scene baseline). At cells=128
  I predict ratio ≥ ×2 and at cells=1280 ≥ ×3, because the over-margin multiplies each hot
  region's forecast reach (E=128 ⇒ reach ~E·margin·vmax_light·horizon ≈ hundreds of cells)
  while the decay arm re-narrows to margin·vmax between waves. wasted_ops goes the other way
  (the decay arm refires conflicts at every ignition: I predict rollbacks_decay ≥ 3×
  rollbacks_shipped at cells=1280, each with replay waste) — the mirror's cost, now priced.
- **P3 (frames).** At 14,080 bodies in the frame harness the latched arm's wider forecasts
  park more regions at merge windows: I predict shipped has more deadline misses / lower
  present rate than decay in ≥ 4 of 5 interleaved reps at equal rate. If no separation
  survives the noise, the honest conclusion is "hygiene-only at this scale" — also a result.
- **P4 (certificate).** Batch outcome digests bit-identical across all three arms at both
  scales (the certificate moves scheduling, never results).
- **P5 (locality).** ES_LOCAL keeps far-from-conflict regions at escalation 1 (escal_max
  ≪ shipped's global level, ~2–8), cuts merges_avoided to near the decay arm's level, and
  still quenches (no runaway rollback growth vs decay); digests identical.
- **P6 (no collapse).** At cells=1280 the shipped arm does NOT collapse to one region forever
  (splits re-fine; the original's 4-cell pattern holds at scale) — but if it does collapse,
  that is the finding: the ratchet's failure mode at scale, and I will report it as such.
