# Predictions — 20261017-1829-library-2fe9 (library lens, the kick)

Written before the decisive composition and quote verification. All constants are
published on `lab/wiki/kick-jet.md`, `frame-cost.md`, `nladder.md`, `library-directions.md`
(cf2a) and `docs/HANDOFF.md`; no engine flight in this run.

- **P1 (regime split, no overlap band wider than ~2×).** Using c4d3's shipped compile
  at true belt keys (3.4–8.3 µs across the belt's e band, redraw cap e = 0.4) and
  cd6e's composed closed-form kick (8–19 µs lean-cold, flat in e): the shipped compile
  wins everywhere in the belt band, and the closed form wins everywhere the strong-field
  grid reads 29–192 µs (e ≥ 0.5, c4d3/21ba). Prediction: a single dimensionless
  predicate (e ≳ 0.4–0.5, equivalently the panel count above its crossover) separates
  the two regimes with both sides measured on both sides, and wiring Carlson globally
  (belt included) regresses the belt ~2.9× (c4d3's kill of 262f). Falsifier: any
  published belt-band point where shipped > composed, or any e ≥ 0.5 point where
  shipped < composed.
- **P2 (memory is the wiring's largest consequence).** The compiled orbit the closed
  form deletes is ~43 knots × 88 B ≈ 3.78 KB of the 4.85–5.06 kB/B live plateau (b30b,
  HANDOFF): prediction: the live-per-body plateau drops to ~1.1–1.3 kB/B and the
  flyable memory wall (1.2–1.65×10⁶ bodies, nladder) rises by ≥ 3× (predicted
  3.8–4.7×, i.e. 4.6–7.4×10⁶). Falsifier: if the deletion factor computes below 3×.
- **P3 (the kick row cannot move the worst-mix 10⁹ ledger).** Composed at cf2a's
  constants, the kick row is 10.3 cores of 4,510 (F = 10⁵ worst mix), share ≤ 0.23%;
  a 10× cheaper kick moves the composed total by ≤ 0.23%. Prediction: no kick-cost
  lever (including open 1 and open 5) moves the worst-mix 10⁹ CPU ledger by more than
  0.3%; the kick's honest scoreboard is the flyable frame and the bytes.
- **P4 (quotes verify 5/5).** An independent script re-fetches the Readwise export and
  checks each of the five quotes byte-identical by highlight id. Falsifier: any quote
  not byte-identical (then it is dropped or marked, never paraphrased as verbatim).
- **P5 (post-wiring wall, pre-registered).** With the compile deleted, the plane rebind
  lands at ~8–15 µs (a765's floor stack: key 2.3 + closed compile ≤ 2.9 + tail
  5.3–5.6 + read overheads) and the belt wave kick becomes reads-dominated (5ade:
  sources 23% + readout 8% + bind decode 8% of the post-tau-carry 41.3 µs item).
  Falsifier: a wired arm measuring a plane-population rebind mean > 20 µs, or a belt
  wave kick still compile-dominated after wiring.
