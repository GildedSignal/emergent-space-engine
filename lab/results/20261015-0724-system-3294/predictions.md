# Predictions (written before the decisive flights)

Run 20261015-0724-system-3294. Instrument: digest-neutral census at both kick sites
(`kick_clock`, `kick`) in `crates/universe/src/step.rs` + `census.rs`; flights are
`nladder <N> coast|burn <s> <rtf>` at rtf 600 (≈ 33,000 game-s at 55 s wall, past the
first kick wave at ≈ 14,000 game-s and through one train period ≈ 27–28 k game-s).
Smoke (not decisive, run before these predictions): N=1000, rtf 300, 2,400 game-s —
all kicks so far are `ship/child` (near-Home, hot doll), fire rate 1.00, dv ≥ 5 units;
the belt's first kicks had not arrived yet.

The question: what does the root doll's metronome actually carry at the belt? The wave
(H0218: "the root doll kicks every body on one 88-day grid, ~250× the kicks behaviour
needs") is a synchronized kick stream; each kick quantizes its impulse against the
velocity word and fires (rebinds) only when a unit flips, else carries (sigma-delta).

## Held-out predictions (cases not tuned on)

1. **Belt fire rate is low: `ship/root` fire rate < 0.10 over the flight** (the belt
   tide at 2–3 AU is below the velocity word's quantum most intervals; the carries
   accumulate and fire rarely), against `ship/child`'s measured 1.00.
2. **Fires are single-unit sigma-delta steps: dv1 fraction ≥ 0.9 of `ship/root` fires.**
3. **The fired stream is a standing train: ≥ 0.9 of `ship/root` fires fall within a
   ±128-tick window around multiples of one grid interval** (measured from the train
   dump; the clocks were all planned at genesis on one doll-wide Δs, so fires stay
   phase-locked), i.e. bursty at the grid, not spread.
4. **Composition:** belt kick *events* per body per game-s ≈ the grid rate
   (1/Δs ≈ 3.5e-5), while *fires* per body per game-s are ≤ 1/10 of that — the event
   stream is ≥ 10× emptier in content than in count.

## Kill criteria (pre-registered)

- If `ship/root` fire rate > 0.5 with dv1 ≥ 0.9: the metronome delivers a genuine
  one-quantum walk every interval; "the wave is empty events" dies in its strong form
  (the rate story stands on cf45/effb alone).
- If fires are spread across the grid (no ≥ 0.9 concentration): the standing-train
  claim dies (the clocks shear more than the flat-in-a interval suggests).
- Controls both sides: `ship/child` (near-Home, hot) must stay fire rate ≈ 1.0
  (an always-fire population — if it does not, the instrument is broken); the
  ladder's own `kicks` counter must equal the census total (if not, the census
  misses a path).

Held-out cases for the checker: N = 3×10⁴ (between my rungs), burn at 10⁴
(the player's flight crosses the wave), and rtf 1000 at 10⁴ (two train periods).
