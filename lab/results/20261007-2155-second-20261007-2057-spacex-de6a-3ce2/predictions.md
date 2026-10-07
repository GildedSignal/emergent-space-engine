# Predictions (written before the decisive runs)

Question (the checker's named experiment for gold): instrument the dense order's contact
carries — the fleet battle's lattice events — and define a horizon-invariant rate, so the
*scene's* H_live exists as a number that does not move with the run's length.

## What is instrumented (read-only; digest must not move)

- **Contacts** (kind 0) at the one funnel every mode calls, `law::respond`: per body per
  response, the integer deltas of the canonical words (k[0], k[1], residual, carry[0],
  carry[1]); pairs counted per call. rev is +1 when k moves (deterministic, 0 bits).
- **Tide epochs** (kind 1) at `Battle::epoch_kick`: each member's kick `dk` (the integer
  velocity quanta applied) and the delta of its tide carry. Anchors and the origin's own
  tube are counted (fleet counters) but not word-instrumented; pcarry accumulation is
  derived state (deterministic from carry and dt), so it is not a distinction.
- **Scar width** per word = bits to write the delta (0 if zero; else 1 + floor(log2|d|)).
  Two rates are reported per kind: the **entropy rate** (the author's protocol: empirical
  conditional entropy given (kind, body, field), fixed horizon 800 game-s) and the
  **scar-width rate** (events/s x mean bits/event), whose per-event width is bounded by
  the registers (|k| < Q = 2^20, so |dk| < 2^21: 22 bits/word) and by the measured
  magnitudes, which do not grow with sample count.

## Fermi first (seed 1, 800 game-s = 1.62e8 ticks)

Fleet budget over the whole run is ~47 ms (JSON, engine_cost_by_kind), so contacts are
bounded by ~1e4-1e5 total even at ~1 us per response; the 48-body scene at ~q/16384
closing speed interpenetrates in ~3 game-s then scatters. Epochs: E = 2^21 ticks at
Home's low orbit (n ~ 2^-27.3 rad/tick), so ~77 epochs x ~48 members ~ 3.7e3 member-kicks
over 800 game-s. Tide dv per epoch ~ 0.2 velocity quanta: most dk = 0, the carry absorbs
the rest. Sparse order at the same horizon: 9.0 bits/s (the author's seed-1 row).

## Held-out predictions (not tuned on)

- P1 (the dense order dominates): at seed 1, 800 game-s, the dense order's scar-width
  rate exceeds the sparse order's entropy rate (8.97 bits/s) by >= 3x. Point guess
  ~300 bits/s.
- P2 (contact rate and width): contacts land in [1, 300] per game-second; mean scar per
  contact (both bodies, all words) in [10, 120] bits; every measured |dk| word stays
  under the 22-bit register bound, mean <= 12 bits.
- P3 (the estimator artifact repeats): at 800 game-s the contact dk deltas are >= 90%
  distinct within (kind, body, field) histograms, so the empirical entropy per word is
  close to log2(samples) — the same saturation the checker measured on the sparse
  carries. The entropy rate therefore *grows with horizon* while the scar-width rate
  stays flat (within 2x from 800 to 1,600 game-s and within 3x to 5,000).
- P4 (tide epochs are quiet): >= 80% of member-epoch events have dk = [0,0] (all of the
  tide goes to the carry below one quantum); non-zero dk are +-1 quanta.
- P5 (the memory verdict survives the better definition): scaling the *measured*
  per-member dense rate to 10^9 battle-like bodies stays over 8 GB per game-hour
  (the author's verdict, now with the dense half measured rather than assumed >= 2
  bits/event); a sparse-only quiet 10^9 stays ~57 GB/hour order of magnitude.
- P6 (anchors are negligible): anchors < 150 in 800 game-s, and their canonical words
  (carries) are already inside the tide registers, so leaving them un-instrumented
  changes the scene number by < 10%.

## Kill criteria for the probe itself

- Any digest differs from the author's recorded digest at the same seed/rtf/cut (their
  clean build was verified equal by the checker): the instrumentation changed an
  outcome -> VOID.
- The h_live sparse numbers (events, bits) do not reproduce the author's stored JSONs
  bit for bit: the record does not regenerate -> fix before reading anything into the
  dense numbers.
- If the scar-width rate moves by > 2x between the 800 and 1,600 game-s horizons, the
  horizon-invariant definition has failed as defined: report it as the finding, do not
  publish a scene number.
