# Predictions (written before the decisive run)

Question: the smallest promotion between a compact belt body and a live one
(board focus, ladder break 4). The shipped wave kick = quantize + integer add
(exact, ns) followed by an unconditional rebind that compiles a fresh tube
(~30-76 us, +2.6-2.7 KB standing; eb2d 1.00 compiles/kick, b30b 59-76 us/kick).
The proposed minimal form: kicks carried on the compact row as exact integer
element-drift words (sigma-delta carry, never requantizing the row), Kepler
readout on demand, tube compiled only at consumer contact.

Cases not tuned on (held out until after the measurement):
- a belt drawn per the ladder recipe (a in [2,3] AU, Rayleigh e 0.07, uniform
  angles), 88-day secondary, kick = the secondary's differential pull over one
  step, velocity quantum set so |dv| p01 is ~2.4e3 quanta (a669's shipped p01).

Predictions:
- P1 (cost): the compact-row kick, readout included, lands at 30-150 ns per
  kick per body on this box (x400-2000 vs the shipped in-wave 59-76 us; within
  ~3x of the 42-55 ns kick floor of b063).
- P2 (fired fraction): with the quantum calibrated to a669's p01 |dv|, the
  fired fraction (a whole quantum leaves the carry) is ~1.0, matching the
  shipped 1.00 compiles/kick — the kicks are real at the word, tiny on the
  orbit (dL/L ~ 2e-7).
- P3 (error type, the load-bearing one): after 2,560 kicks (20 waves of 128),
  the carried path's readout error stays <= 2 element quanta (one rounding at
  the end, sigma-delta exactness), while the requantize-each-kick path (the
  refuted memo style) walks to >= ~sqrt(2560) ~ 50x the single-kick rounding.
  If the carried path also walks (error grows like sqrt(K) or faster), the
  design is dead: it is law.md's recorded random-walk objection in another
  place, and the smallest promotion cannot sit on the row.
- P4 (standing bytes): the compact row + drift + carry <= 40 B against the
  shipped 2,407-2,632 B at birth and ~4,900-5,100 B after the first wave
  (78-160x).

Kill criteria: P1 > 300 ns (the readout dominates and the design is only ~10x,
not the board's 10^3) or P3's carried path walking (compounding error type)
kills the row-carried promotion at this form. P2/P4 are calibration checks;
a miss there means my replica is off, not the design.
