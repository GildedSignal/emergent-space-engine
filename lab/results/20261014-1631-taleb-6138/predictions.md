# Predictions (written before any wave flight ran)

Held-out cases: the M1 record (ladder.txt, `after 32e9e986`) fixes only the endpoints
10^5 burn (max 45.0 ms, 9 frames over, events/frame max 1,339) and 3x10^5 burn
(max 1,280 ms, 28 over, events/frame max 37,938). Everything below is measured on
this Linux box, shipped main (db0f3e74), 200 s flights at rtf 100, budget 12 ms,
unless said. Kill criteria are stated per prediction.

- **P1 (convexity of the worst frame in N).** worst(2x10^5 burn) > 4 x worst(10^5 burn)
  (superlinear; point estimate 150-450 ms). Linear drain would give ~2x (<= 120 ms).
  Kill: worst(2x10^5) <= 2.2 x worst(10^5).
- **P2 (the shock is batched into single unbudgeted items, not spread).** events/frame
  max at 2x10^5 burn > 5,000 (the M1 ratio at 3x10^5 was 37,938 against a ~337/frame
  uniform-wave mean, so the frame content, not the event cost, carries the spike).
  Kill: events/frame max < 1,000 while max ms is still > 10x the 10^5 arm.
- **P3 (control: the wave alone is harmless; the player's doll is the difference).**
  2x10^5 coast, same seed, same wave: max < 13 ms, zero frames over. Kill: coast fails
  too (then the seam is the drain, not the player's item).
- **P4 (structural, not schedule luck).** seed 2 at 2x10^5 burn: worst frame within
  0.5x-2x of seed 1's. Kill: seed 2 passes F1 (max < 12 ms) or exceeds 5x (then the
  pass/fail of the same physics is decided by the draw, which is worse news).
- **P5 (the wave is not intrinsically spiky).** belt_first at 2x10^5: the belt's first
  items inside a ~13,000-15,000 game-s window with no single game-second holding > 2%
  of the belt (uniform-ish); so the single-frame event spikes are backlog accumulation
  at the player's item, not lumps the birth drew. Kill: some 1.67 game-s slice holds
  > 10% of the belt.
- **P6 (recovery, not ratchet).** after the wave (past ~146 s of wall), frames return
  under 12 ms by flight end and the presented time never lags > 0.1 s (a freeze, not a
  falling-behind spiral). Kill: frames still over budget at 190-200 s.
