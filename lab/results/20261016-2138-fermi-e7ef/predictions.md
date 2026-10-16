# Predictions (written before the decisive experiment)

The run: assemble the 10⁹ closing ledger (CPU + memory) from page-cited measured
constants, anchored on shipped code. The decisive experiment is (a) the shipped
`belt_first` example (my own box, independent of 4093's flights) and (b) the
ledger script `ledger.py`. Cases I have not tuned on:

- **P1 (the interval, from shipped code, untuned):** `belt_first` (default
  N=3000) prints the belt's first-item p50 at **14,100 ± 700 game-s**
  (= interval/2, with interval 28,141.5 s; 4093's anchor, never reproduced by
  me). The locals' p50 is ≤ 300 game-s (Home's doll is far faster).
- **P2 (the clock factor, my own derivation, untuned):** the interval × 128
  implies P_D = 3.60e6 game-s at Cinder's a = 0.3905 AU, which is
  **0.468 ± 0.02 of Cinder's SI Kepler period 7.70e6 s** — i.e. the law's
  `f'(c)` doll-clock factor at Cinder's distance is ≈ 2, not 1. If the ratio is
  not within [0.40, 0.54], my reading of "P_D = the shortest secondary's
  period" is wrong and I report which constant instead reproduces 28,141.5 s.
- **P3 (the redundancy, arithmetic):** at 10⁹ bodies, rtf 100, kick cost
  50 µs, the belt stream costs 165–190 cores (4093's 120–190 with the rate
  spread 3.3–3.6e-5); with the measured 8× cadence split (7f97) alone it is
  21–24 cores, and the kick cost REQUIRED to fit 4 cores is then
  **9–12 µs — at least 160× above the 42–55 ns floor**. With the 8× split AND
  the measured belt delete (38.5–61%), required cost is 15–29 µs.
- **P4 (the inversion):** at the 42–55 ns floor, even the SHIPPED cadence fits:
  0.15–0.25 cores. So the kick-cost row and the cadence row of the scoreboard
  are alternative sufficiencies for the 10⁹ stream, not two independent gaps
  both of which must be paid.
- **P5 (the crest cross-check):** 4093's "69 s of clamped delivery per 281-s
  interval at 10⁶ rtf 100" regenerates as N·C/0.72 = 1e6 × 50e-6/0.72 = 69.4 s;
  on the M1 anchor (29.3 µs/event, 1051) the same crest is 40.7 s.
- **P6 (the two terms that do not close):** (i) the encounter tier's graded
  levers leave 62–571 cores at 10⁹ (only f0a2's ungraded routing closes it);
  (ii) memory: every generic floor busts the ~6 GB budget at 10⁹ (62 bits →
  7.75 GB; 126 → 15.7 GB); only the measured phase-locked program class
  (21–40 bits) fits. Prediction: these two, not the kick, are the 10⁹ blockers.

What would make me wrong: belt_first printing a p50 outside P1 (then the
interval anchor or my doll reading is wrong); the ledger showing a
configuration where even 42 ns does not close the stream (then the kick row is
load-bearing after all); an arithmetic error in the cores table vs 4093's own
120–190 (then my rate or rtf frame is off).
