# Predictions (written before the decisive patched runs)

The question: is the belt's first-kick wave (the through-the-wave wall between ~3×10⁵ and 10⁶
bodies) a manufactured transient (synchronized birth at tick 0 anchoring every root-doll clock
grid, `plan_clock`, step.rs:626) that a per-body phase anchor deletes at ~zero cost?

Already measured pristine (exploration, shipped code, this machine):
- belt_first N=3,000 and N=100,000: belt first items in [13,051, 14,542] game s (width 1,491 s
  ≈ 5.4% of the ~27,400 s step; 99,700 bodies), locals spread 21–5,289 s (the unsynchronized
  control). Matches ladder.txt's 13,051–14,534.

## The decisive experiment (patch: stagger the belt births' first-kick deadline by u·2·half, u = a fresh draw lane of the ladder's own mix64(seed, k); belt loop only)

- **P2 (spike deleted).** At N=10⁵, coast, 200 s at rtf 100: pristine shows the wave as a frame
  event spike (max events/frame ≥ 100) and a worst frame ≥ 8 ms; patched shows first kicks
  uniform over [13,051, ~41,000) game s, max events/frame ≤ 15 (steady 10⁵/27,400 ≈ 3.65
  kicks/game s ≈ 6.1/frame at 1.67 game s/frame, plus locals/player), worst frame ≤ 3 ms
  (coast-level), presented-time lag 0.
- **P3 (bits control).** With `extra = 0` the patched binary is bit-identical to pristine (the
  stagger touches only the ladder belt loop; ladder_digest / frame_digest unchanged).
- **P4 (rate law).** The staggered steady kick rate matches N/(2·half) per game s within ~30%
  (nladder's kicks/game s), and the spike factor (2·half)/width ≈ 18–19.
- **P5 (held-out behaviour).** The patched belt's states at 20,000 game s differ from pristine
  (kick timing moved; the order-boundary lottery re-rolls keys) but the flight completes with
  zero refusals and no lost bodies beyond the pristine run's own.
- **P6 (the leak, named).** The crude delay stagger leaves up to u·2·half of each body's
  secondary drift unfolded before its first kick (≤ one kick's worth, one-off, bounded — the
  fold weight w is not rescaled in the probe). Expectation: no visible breakage at 10⁵; the
  adoption-grade form rescales the first kick's weight by (1+u) (one line in kick_clock) and is
  written up, not built here.

## What would kill the claim

- The wave is not the dominant frame cost at 10⁵ coast (some other term is): then the stagger
  buys nothing and the wall is real work.
- extra=0 digests differ: the patch leaked outside the belt.
- The staggered run refuses/loses bodies at a rate above pristine: the leak is not benign.
