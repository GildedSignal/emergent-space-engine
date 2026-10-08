# Predictions (frozen before the decisive experiment)

Bottleneck: B12 cannot separate a bounded error from a compounding one (board, 6 Oct: "the recurrence ratio does not separate a slow leak from a bounded error"). Proposed statistic: **decade-local growth exponent** of the running max |dE/E0|, α(h→10h) = [log m(10h) − log m(h)] / log 10, reported per decade, never as one window-fitted slope.

Data: the frozen probe-1 evidence (`artifacts/evidence/gravity-v1-freeze-20260929/probe-scripts/`), code untouched, verdicts already on record and generated for another purpose (held out): fixed-Δ control = bounded (1.8e−8), mandated variable-Δ rule = walks then saturates (~8.65e−4, the hard case). Plus two synthetic calibrations and one adversarial case.

| # | Case | Prediction |
|---|---|---|
| P1 | fixed-Δ control (η=1/32, o2, 10^4 orbits, e=0.2) | top-decade α(10^3→10^4) < 0.10; every decade < 0.15 |
| P2 | variable-Δ rule (η=1/16, o2, 10^4 orbits, e=0.2) | early decades α ≥ 0.30 (leak-like), bending below 0.10 only at the decade where saturation (~8.6e−4) is reached |
| P3 | synthetic random walk (10^5 samples) | α ≈ 0.45–0.55 at every decade ≥ 1 |
| P4 | synthetic bounded-with-transient (amplitude a·(1−e^(−k/50)) + sine, saturates by k≈300) | a single-window slope over [1,10^3] (B12's current style) reads > 0.2 (misclassifies as compounding); the top-decade local exponent reads < 0.10. If local exponents ALSO misclassify, the statistic dies |
| P5 | held-out orbit: repeat P1/P2 at e=0.5 | same classification (fixed < 0.15 everywhere; variable-Δ leak-like early, bending late) |

Kill criterion for this run: if P4's local exponents misclassify the transient case, or if P1/P2 exponents overlap (no separating threshold), the horizon-exponent statistic is rejected for B12 and the dossier says so.

Secondary (lesson 4, Musk order): on current main, `shipmem` and `encounters` have no live caller (handoff says measured 7 Oct); check is a one-command import-graph fact, expected to confirm.
