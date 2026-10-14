# Predictions (written before the decisive experiment)

Scene: the shipped plane's ladder belt (scenario.rs `ladder_ship`: a uniform in [2,3) AU,
Rayleigh e 0.07 re-drawn above 0.4, periapsis > 1.2 AU), kicked at the root doll's cadence
(`step_log2 = 7` per the shortest secondary Cinder, interval ≈ 2.8e4 s), perturbers = the
shipped roster (Cinder 2^-21 at 0.39 AU, Home 2^-18 at 1 AU, Giant 2^-10 at 5.2 AU; the
Moon and the star's tide do not reach the belt). Key quanta: E Q48 on scale 1
(= c²·2^-48 = 319.3 m²/s², f0a2's SI anchor), L Q32 on the doll's scale with the shipped
documented range 1/4 ≤ L ≤ 4096 — so the L quantum is between 5.6e-14 and 2.3e-9 of L,
whatever the doll convention. Held out (not tuned on):

- **P1 (the load-bearing one):** |ΔL| per kick ≥ 100 L-quanta at EVERY scaling the
  shipped range allows — the key's L flips on ~100% of kicks. If the per-kick ΔL/L ever
  falls below 2.3e-9 (the coarsest legal L quantum), the "compile-per-kick is forced by
  the key's own fineness" claim dies.
- **P2:** the E axis flips on 25–60% of kicks (|ΔE| ~ 0.3–0.6 Q48 quanta, alternating
  sign with the synodic geometry). If E flips ~100% too, coarsening only L buys nothing
  (the key is the pair).
- **P3 (the deletion's physics):** over one Giant–belt synodic period the impulse series
  nearly cancels: net |ΔE| per synod ≤ 5% of Σ|ΔE| per synod, and the E word stays
  within ~±12 quanta of its birth value over 100 synods (slow secular drift). Then a
  2^5-coarser E quantum absorbs the oscillation and the E-flip run length is ≥ 8. If the
  drift is linear-fast, coarsening buys ~nothing on E.
- **P4 (direction, falsifiable):** the kick size DECREASES toward the inner belt (the
  Giant at 5.2 AU dominates over Home/Cinder at ≤ 1 AU at every belt radius). If Home or
  Cinder dominated, it would invert at the inner edge.
- **P5:** the fraction of kicks whose quantized velocity step is zero (the shipped carry
  gate, step.rs:424) is ~0% on this belt — the carry gate never blocks, the rebind always
  runs. (Sanity anchor: the engine's own record — the plane recompiles ~99% of kicks,
  the wave costs ~30 µs a kick, memory doubles per first kick.)

What each outcome would mean:
- P1+P2+P3 hold → the ladder's breaks 1 (wave CPU), 2 (memory doubling) and 4 (birth
  build) are one dial: the key's fineness. Price the deletion by the run length.
- P1 fails → the no-flip rebind is already common; the lever is a key-equality gate, and
  the dossier says so instead.
- P3 fails → coarsening deletes little; the compile stream is honest secular work; lead.
