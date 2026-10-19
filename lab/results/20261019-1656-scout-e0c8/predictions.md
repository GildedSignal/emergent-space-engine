# Predictions (written before the decisive run)

Question: the ledger's open-2 successor (budget-1e9, 0659): the shipped cadence fires one
clock-kick per belt body per doll step (~27.4k game-s, p = 1.0 measured). Can the compact
row (shipmem's grids: p 25-bit over [2048,2560), e on a Rayleigh-quantile u32, kind 6-bit,
omega 32-bit, t_p 44-bit) absorb that kick **in place** (departure bits vs the birth program
stay near the smooth level), or does the first kick already re-drive the row toward the
driven-worst 126 bits, forcing the live round-trip the ledger now budgets?

Instrument: float64 first-order 3-body replica (star + one circular perturber, scenario.rs's
`restricted` μ = 1/999 at sep, two arms: inside sep=1 and outside sep=4 of the [2, 2.5) belt;
belt drawn per shipmem's birth law: p uniform, e Rayleigh 0.07 redrawn above 0.4, uniform
angles), one doll step Δt = 27.4k game-s = 8.68e-4 yr (0659's wave spacing 14.3k/41.7k/69k gs),
vectorized leapfrog, step-halving control on the element deltas. Bits = empirical entropy of
the grid-quantized departures (uv-length universal code, codec.rs's own measure) per column,
per body, on held-out members. Orders of magnitude; the grids, distributions, μ and Δt are
the shipped record's constants.

Held-out predictions (not tuned on):

- P1 (magnitude): the per-body departure of the p column over one doll step is a few
  grid quanta, not sub-quantum and not thousands: |δp|/q_p p50 in [0.5, 40] on both arms.
- P2 (which column dominates): the clock columns (t_p, omega) carry more departure bits
  than the shape columns (p, e); specifically t_p alone ≥ 15 bits/body on the inside arm.
- P3 (the absorbable half — the scout's mechanism): one shared per-block rate predictor
  (a single global slope fit per column on a training half, the codec's DFOR/CHORD shape)
  recovers ≥ 60% of the raw departure entropy on the held-out half (the departure is
  structured in the birth keys, not scattered).
- P4 (the failure minority): ≥ 0.3% of bodies sit within one half-width of a J:K
  mean-motion resonance with the perturber (the resonance census; these cannot ride rates).
- P5 (control, must hold): scrambling the departures across bodies at identical per-body
  magnitudes costs ≥ 3× the bits of the structured tide arm (the instrument can see
  structure, so P3's pass/fail is meaningful).

Kill criteria: P3 failing (rates recover < 60% on both arms) kills in-place absorbability
on the shipped tide — the fix must then fold the kick at the law level (rates in the
compiled orbit), not in the row. P5 failing voids the instrument. P1 outside its band on
either arm re-opens the magnitude question before any bits are read.
