# Predictions (written 2026-10-20 ~10:1x, BEFORE any decisive flight)

Hypothesis (the inversion of ca63's composition): the arrival wave the record prices as
"one wave" (crest floor 1e9 x 47.5 us = 13.2 h) is a **phase-locked comb**: eras recur
every ~13-14k game-s, so the cost recurs per era and the shipped plane re-freezes each
era (cc9d's K-law max_ms ~ 8.1-9.5 us x K). Evidence in the record that motivates it:
seed-2 eras at gs 12-16k AND 26-30k (ca63 checker2); 0659's refutation "wave 1 a birth
transient [wave 2 = wave 1]" (coast); nobody flew the burn plane past ~46k gs / 2 eras.

Arms (shipped bits; my patch is print-only per-frame CSV + Linux footprint stub +
optional seed arg, off = shipped):
- A1 100000 burn 150 400 12 seed1  (rtf 400 play cadence, ~60k gs, ~4 eras)
- A2 150000 burn 120 400 12 seed1  (the freeze rung, 48k gs; 2e5 risks the 2 GB cap)
- A3 100000 coast 150 400 12 seed1 (control: no burn)
- A4 100000 burn 150 400 12 seed2  (seed robustness of era totals)
Anchor (instrument falsity check): 100000 burn 10 2000 12 CSV-off must land in the
record's 2d26 family: max ~780-900 ms, over ~100-120.

Pre-registered predictions on the held-out structure (eras 3-4 never flown by anyone):

- P1 (comb persistence): at 1e5 burn, era 3 (~gs 40k) and era 4 (~gs 53k) each carry
  >= 0.5 arrivals/body (crest-era band from the record ~1.0; total per era incl. tail
  1.2-2.5). KILL of the hypothesis: era-3 arrivals < 0.1/body (the comb shears out in
  <= 2 eras; then the stagger's target is eras 1-2 only and ca63's one-wave price
  stands).
- P2 (the freeze recurs, shipped bits): 1e5 burn max_ms >= 400 ms in EVERY era through
  era 4 (K-law predicts ~810 ms; band 0.4-1.0 s). If era >= 3 max < 100 ms, the freeze
  is birth-only and cc9d's law is a transient, not a per-era event.
- P3 (drainability at play cadence): 1e5 delivered rtf recovers to >= 300 gs/s in each
  inter-era gap (band 300-720). If it stays < 150 gs/s from era 2 on, the wave cost
  saturates play cadence already at 1e5.
- P4 (control both sides): coast 1e5 shows either no eras (player-caused comb) or eras
  with arrivals but max_ms < 100 ms (belt clock comb without the player-item gulp):
  either way it separates the arrivals channel from the freeze channel. If coast shows
  eras WITH >= 400 ms freezes, the freeze is belt-intrinsic, not player-item.
- P5 (composition, derived not flown): if P1 holds, the recurring floor at 1e9 flat
  47.5 us/event is ~13.2 h per 13-14k gs of game time (~3.6 s compute per gs), making
  comb deletion (the stagger's real target) mandatory for 1e9 — amortizing ONE wave
  buys nothing.

Numbers I have NOT tuned on: era period beyond era 2, era-3/4 amplitudes, per-era
max_ms, inter-era delivered rtf, coast era structure at 60k gs.
