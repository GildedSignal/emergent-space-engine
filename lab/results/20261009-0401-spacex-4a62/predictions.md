# Predictions (written before the decisive run)

Question: what is the plane's H_live — distinctions created per game-second and the
retention they force — and does it let 10⁹ bodies fit in 8 GB?

Cases I have NOT tuned on (the plane scenario's defaults, members=64, seed=1):

- P1 Event mix and spread: kicks are > 60% of all events, and per-ship event rates span
  at least 3 orders of magnitude between dolls (AU orbiters ≈ 0 events per game-second;
  the inner doll's bodies and the fleet carry the load).
- P2 Reabsorption works: prune() reclaims ≥ 90% of the bytes settle() created in a
  100-game-second interval, so steady bytes/body is flat in time. (If it reclaims ~0,
  retention is unbounded and that is the finding.)
- P3 The multiplier: steady bytes/body ≥ 500 (≥ 30× the law's 16-byte tube), because
  each retained segment pins an Arc<Entry> with a compiled OrbitShape (knots), not a
  16-byte word.
- P4 The decision: at the measured steady bytes/body, 10⁹ bodies exceed the 8 GB budget
  by ≥ 10×. I predict this holds — the 16-byte tube is not the memory law of the plane;
  retention of compiled trajectories is.
- P5 Creation floor: distinct new tubes (rebounds) per ship per game-second is < 1 for
  every AU-orbit ship (their kicks are rarer than one per second at 1/64-period cadence),
  so per-game-second *creation* is not what kills scale; retention is.

Instrument controls (both sides): the allocator counter must rise during settle and
fall after prune (else the counter is broken); dropping the universe must return live
bytes to within 5% of the pre-build baseline (else the counter leaks).
