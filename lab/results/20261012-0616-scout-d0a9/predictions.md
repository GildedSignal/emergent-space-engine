# Predictions (held out before the decisive 40-orbit run)

Calibration only: seed 1, 10 orbits (kick rms A=1.28e-3, D=1.63e-3, max/rms≈5,
frac scarred at Q=4σ by orbit 10 = 0.75). The decisive runs are 40 orbits,
seeds 1 and 2; every quantitative claim below about seed 2 and about the
scaling sweep is a genuine prediction, not a fit.

Theory under test (the H_live identity): a body's live distinction from its
birth program is a random walk driven by per-orbit kicks of rms σ_s; a scar is
stored only when the sigma-delta carry crosses one quantum Q.

- **P1 (diffusive scaling).** For qfac = Q/σ_s ∈ {32, 16, 8}: rate · qfac² ∈
  [0.5, 2.0] per dimension, both seeds (theory: rate = σ_s²/Q², so the product
  is 1 for a pure Gaussian diffusive walk; real kick streams are heavy-tailed
  and mildly correlated, so a factor 2 either way is the tolerance).
- **P2 (ballistic floor).** For qfac ≤ 0.5: rate ≥ 0.7 per orbit per dimension
  (every kick then jumps at least one cell).
- **P3 (crossover).** rate · qfac² rises above 2 somewhere in qfac ∈ [1, 8]
  (walk becomes ballistic).
- **P4 (scar payload bits).** At qfac ≥ 8: deltas are ≥ 90% single-quantum
  (|d| = 1) and the delta entropy ≤ 1.2 bits per dimension. At qfac ≤ 0.5:
  delta entropy ∈ [2, 4] bits.
- **P5 (control, must pass).** Gravity off: max |ΔA| per orbit < 1e-12 and
  zero scars at Q = 1e-14 (drift conserves invariants exactly; only float
  roundoff remains).
- **P6 (seed transfer).** Seed 2's kick rms within [0.8, 1.25] × seed 1's;
  fraction of bodies scarred at qfac = 4 by orbit 10 ∈ [0.6, 0.85]; final
  offset entropy at qfac ∈ {16, 4} within 0.7 bits of the Gaussian formula
  0.5·log2(2πe σ_off²/Q²) per dimension.
- **P7 (heavy-tail effect, the calibration's surprise).** First-scar surfacing
  is faster than a Gaussian random walk predicts: measured fraction scarred at
  qfac = 4 by orbit 10 ≥ 1.3 × the Gaussian first-passage estimate
  2·(1 − Φ(qfac/2)) accumulated over 10 orbits. Mechanism: the kick
  distribution's tail (max/rms ≈ 5) lets rare strong encounters surface in one
  step, while the steady rate still follows σ_s²/Q².
- **P8 (D behaves like A).** All of P1–P4 hold in both dimensions (D is the
  more aggregate of the two invariants; if anything its kicks are slightly
  larger, from the calibration ratio 1.63/1.28 ≈ 1.27).
