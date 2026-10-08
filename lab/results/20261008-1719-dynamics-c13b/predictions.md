# Predictions (written before the decisive analysis; the dump is only data collection)

The run's question: can a derived statistic pair separate a bounded, state-only Jacobi error from a
compounding one on B12's chaotic ships, where the growth exponent ranks them backwards (law.md B12,
miscalibration of 6 October) and the recurrence ratio fails on slow leaks (red-team b12-stat)?

Statistics (all computed on the law's own signed series X(t) = (C_J(t) − C_J(0))/C_J(0), never on a
comparison with the reference, so nothing depends on the reference's machine-dependent convergence):

- **S1 trend blade**: per ship, the OLS slope of X against t, standardized by a circular-shift
  permutation of the increment series (the null preserves the series' own diffusion and
  autocorrelation; only the net drift is destroyed). Leak ⇒ every ship's slope has the same sign and
  a permutation p far below 0.05. Aggregate across 16 ships: a sign-consistency count (≥14 of 16
  same-signed at p<0.05 has false-alarm ≈ 0.4%, derived, not fitted).
- **S2 memory blade**: pairs of samples of one ship whose slow state (heliocentric E, L) falls in the
  same decile cell; Spearman rank correlation of |ΔX| with the time gap Δt, null by permuting the gap
  labels. An error that is a function of the state gives the same X at the same (E, L) — bounded
  |ΔX| at any gap; an error with memory has |ΔX| growing with Δt. Cells on (E, L), never on the
  law's own drifting elements alone (the recurrence ratio's blind spot for secular leaks).
- Derived detection floor for a secular leak at horizon T with the series' own detrended spread σ̂:
  ℓ_min ≈ z*·σ̂/sqrt(Σ(t−t̄)²) = z*·σ̂·sqrt(12/n)/T, z* = 2.5.

## Held-out predictions

1. **Miscalibration reproduced on this machine (Linux)**: median growth exponent of `planted-bounded`
   above `planted-compound` (inversion), bounded in 0.4–0.55, compound in 0.25–0.35; leaks 0.85–1.0;
   echo and scaled(3e-13) under the 1e-12 floor (0 judged).
2. **S1 passes the clean controls**: echo, scaled(3e-13), scaled(1e-11), planted-bounded — no more
   than 5 of 16 ships spuriously at p<0.05, and signs mixed (sign count ≤ 13/16).
3. **S1 flags every secular leak**: leak1e-12 on ≥15/16 ships same-signed; leak1e-13 on ≥12/16;
   leak3e-14 on ≥10/16 (its trend is clean against echo-scale noise ~1e-15, so even 6e-12 of travel
   is far above the floor). `planted-drift`: honest uncertainty — I predict flagged by S1 or S2 on
   at least 10/16 ships combined, but would not bet on S1 alone.
4. **S2 flags memory, passes state-only**: `planted-compound` flagged on ≥12/16 ships; `bounded` and
   both scalings pass, with the median matched-pair |ΔX| of `bounded` below 1e-3 of that law's own
   spread of X (a is a function of E alone, so matched (E, L) ⇒ the same error). `scaled(1e-11)`
   shows bounded |ΔX| at matched states (phase-dependent but not growing with Δt).
5. **S2 may miss the secular leaks** (their own (E, L) drift, so far-gap matched pairs are rare) —
   that is S1's job; the pair is disjunctive (fail if either blade flags).
6. **Floor calibration**: on synthetic mixtures (bounded series + leak at rate ℓ), the empirical
   detection boundary tracks the derived ℓ_min within a factor of 3 in ℓ at fixed T, and the derived
   horizon T*(ℓ) ≈ z*·σ̂·sqrt(12/n)/ℓ inverts correctly.

## Kill criteria

S1 flagging `bounded` at ≥14/16 same-signed, or S2 flagging `bounded`/`scaled(1e-11)`, or
`compound` passing S2, kills the pair. If the exponent does NOT rank bounded above compound on this
machine, the miscalibration claim itself is machine-dependent and must be reported as not reproduced.
