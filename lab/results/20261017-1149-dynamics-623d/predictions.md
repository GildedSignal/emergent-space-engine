# Predictions — 20261017-1149-dynamics-623d

Written before the decisive runs (`lyap belt`, `lyap coorbital`). The control arm
(`lyap control`, μ = 1e-12) is calibration, already launched; its reading gates everything.

Instrument: Benettin twins on the judge's own reference (Dormand–Prince, rtol 1e-12,
`xtask/src/behave/restricted.rs`), d0 = 1e-8·r, renormalized every P/16, horizon 128 local
orbits. Scene: JUPITER (μ = 1e-3 at 5.2 AU) — the plane's Giant (μ = 2^-10) to leading order.

- **P1 (instrument floor, negative control):** the μ = 1e-12 arm reads λ·P < 1e-4 on ≥ 11/12
  ICs. If any reads > 1e-3 the instrument leaks and the run is VOID.
- **P2 (the regular sea):** ≥ 70% of the 164 belt ICs (a ∈ [2,3) AU, e = 0.1, 4 phases) read
  λ·P < 1e-3. The belt between the Giant's resonances is regular at this horizon.
- **P3 (the resonant slivers):** the chaotic fraction (λ·P > 1e-2) of the belt grid is between
  5% and 30%, concentrated within ±0.02 AU of the 4:1 (2.08 AU), 3:1 (2.50 AU), 5:2 (2.86 AU)
  and 7:3 (3.01 AU edge) resonances; the 3:1 sliver reads the largest λ.
- **P4 (the fleet regime):** ≥ 30% of the 70 co-orbital tadpole ICs read λ·P ≥ 5e-2, and λ
  rises with tadpole amplitude (δ ≥ 45° arms the most chaotic) — chaos-shadowing's dead ICs
  (105°-class angles) sit in the chaotic tail this predicts.
- **P5 (the budget composition, the claim):** even at f_chaos = 0.3, the chaos-driven
  re-derivation floor of a 10⁹ belt is < 0.1 events/game-s
  (N_chaos·λ/P_orbit = 3e8 × 0.03 / 1.25e8 s) — two orders below the certificate stream — so
  **chaos never binds the belt's event budget; the certificate cadence does.**
- **P6 (the lookahead inversion, the danger side):** for belt neighbours with Δa/a ≤ 1e-3 the
  encounters tier's Diophantine lookahead (one synodic period ≈ (2/3)·a/Δa ≈ 667 local orbits)
  exceeds the chaos horizon ln(1e7)/λ ≤ 322 orbits of every chaotic-class IC (λ·P ≥ 5e-2):
  conjunction prediction for close pairs in the chaotic class is chaos-limited before one
  synodic period; in the regular sea it is not. If instead the chaotic class keeps a usable
  lookahead (horizon ≥ 667 orbits ⇒ λ·P ≤ 1.5e-2), P6 fails and the Diophantine tier is safe
  everywhere in the belt.

Kill criteria: P1 fails ⇒ VOID. Belt ≥ 90% chaotic (λ·P > 1e-2) ⇒ the "regular sea" premise
dies and the headline inverts (the shipped birth range sits in a resonance-overlap sea).
