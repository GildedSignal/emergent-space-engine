# Predictions (written before the decisive flight)

## The question, restated

No flight on record has covered one full cadence period of the root doll: the belt's kicks
come every 88 d / 2^7 = 59,400 game-s (the doll's shortest secondary, Cinder, 88 days; shipped
`ext::constants` cadence, ladder.txt break 1), the first wave lands at 13,051-14,534 game-s,
and the deepest flights on record end at 21,900 game-s (f134 checker 2) — before the second
beat. So every smoothness letter on the wiki (the N1 gate's 20 s; the ladder's 200-s flights;
the composed law's checks) is measured inside ONE interval of the law's own cadence.

Inversion: does the wave come back? The ladder letter treats the wave as a one-time event
("the belt's first kicks come as ONE WAVE"), and its steady-state arithmetic ("10^7 bodies =
357 kicks a game-second ... ~1.4 cores") assumes the kicks disperse to a uniform stream.
4c22's finding for planet-doll locals says the opposite tendency: intervals re-anchor to the
absolute power-of-two grid, so "a population born at one tick ... kicks at identical ticks
forever". All belt bodies are one-tick births of ONE doll on ONE grid.

## Held-out predictions (not tuned on; the flight below is the first look past one period)

Flight: `nladder 100000 coast 760 100 12` (budget 12 ms, unlimited events, presented-time CSV
per frame), plus the same flight at N=0 as the floor control. Kill criteria pre-registered:

- **H1 (the train re-herds).** Beat 2 lands at presented ~72,451-73,934 game-s (first-kick
  time + 59,400 per body, the belt_first range shifted by one interval) with a peak
  events/frame in the class of beat 1 (>= 1/3 of beat 1's peak; the letter's beat-1 peak at
  1e5 after the fix is 390). If instead the beat-2 peak is <= 3x the inter-beat steady p99,
  H1 is killed: the wave is a birth transient and the letter's uniform-stream assumption is
  CONFIRMED at one full period (also a result; the horizon hole is then closed, not opened).
- **H2 (interval).** The beat spacing on the presented-time axis is 59,400 +/- 2,000 game-s
  (one interval of 88 d / 2^7). If the spacing differs, the letter's own cadence constant is
  misread and the train's period must be re-derived from the data.
- **H3 (envelope).** If H1 holds: beat 2's peak is within a factor of 2 of beat 1's
  (persistence), not a 10x decay (a dying transient). This separates "standing train" from
  "long tail of one wave".
- **H4 (the frame).** If H1 holds: beat 2's worst frame ms at N=1e5 is within a factor of 2
  of beat 1's worst (the letter's max 12.00 ms after the fix). If the beat-2 frame is 10x
  worse, the backlog interacts (wave-on-wave) and the letter's post-fix claim does not hold
  past one period.
- **H5 (floor).** The N=0 control shows no beat at 72,451-73,934 game-s above its own 12-ms
  frame class (the beat, if present at 1e5, is the belt's, not the plane's).

What I do NOT expect to learn here: the burn seam (taleb-6138/625b own it), memory (b30b's
plateau), the comb's legality (f134 direction 1).

## Amendment (03:2x, after launch, before reading any flight output)

Re-reading the page's Runs list (not just Current best/Refuted) I find the train question is
partly taken: bf21 "the wave is a standing train"; 4af4 "the train shears" (awaiting grade);
7dc6 "25 wave periods flat (700 k game-s, digest-stable)" (awaiting grade); b30b "train
~27-28 k game-s"; cf45 "P_D 77.24 d, interval 2.814e4 s". Two consequences, pre-registered
BEFORE reading the flight data:

- **H2' (corrected interval).** The beats in my flight space at ~28,140 game-s: beat 2 in
  [41,191, 42,674], beat 3 in [69,331, 70,814]. My original H2 (59,400, from ladder.txt's
  "88 days / 2^7") is already contradicted by cf45 on the page; my flight measures the
  spacing directly and adjudicates the letter's constant against cf45's.
- **H1' (narrowed to what the record lacks).** No run on this page prints the per-beat FRAME
  bill (peak events/frame, peak ms, frames over 12 ms, mass, width per beat) on shipped main
  post-fix at rtf 100 with the letter's own instrument; the ladder letter's after-table rows
  are 200-s flights (20,000 game-s), sub-interval. Prediction: on shipped main (no stagger),
  beat 2's peak events/frame is within a factor of 2 of beat 1's (the shear, if present on
  main, is mild: peaks ~390-class at 1e5, not 7da3's staggered-arm decay). If beat 2 decays
  to <= 1/3 of beat 1's peak, the shear is strong on main too and the letter's coast rows
  under-state nothing (the train self-flattens); if beat 2 EXCEEDS beat 1, the sub-interval
  letters under-state the recurring bill.
