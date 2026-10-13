# Predictions — 20261013-0037-system-174d

Written before the decisive run. Tuned on nothing: the decomposition (item kinds, tide-vs-burn dv in
quanta, recorded steps) has never been measured; the only prior numbers are the published burst totals
(42/166/579/1,036 player items at L8/10/12/15, from 20261012-2257-quant-32ab), which I use as an
external control for the instrument, not as a fit target.

Held-out cases my instrument will measure for the first time:

- **P1 (composition).** In every burn flight, ≥ 90% of the player items in the burst frames are
  `Kick(0)` + `Boundary` pairs on the player itself; `Open` items ≈ 0 (the clock path plans only
  kick+boundary); `decide` items = the number of script inputs.
- **P2 (the tide is silent where the events are many).** During the forward burns at L8–L15, ≥ 90% of
  thrust kicks have the tide's dv below one velocity quantum (`tide_q == 0`): the events exist to
  advance the burn, not the field. If this fails, the "burn belongs in the tube's generator" reading
  dies: the kicks would be carrying real gravity.
- **P3 (the cadence is the law's own formula).** The recorded next-step follows
  `2^⌊log2(β·2⁻⁶/α)⌋` clamped to [128, 2⁵⁰], α = 2^(thrust_log2+level), for ≥ 95% of thrust kicks
  (the held-out content is the actual β range and whether the MIN_STEP clamp binds early in the burn).
- **P4 (the coast control inverts).** In the coast flight the player's items per frame are ≥ 10×
  fewer, and its kicks' tide *fires* (tide_q ≥ 1) at ≥ 50% of kicks: the clock cadence belongs to the
  tide. P2 and P4 together are the system claim: the same tide is silent exactly where the events are
  many and fires where they are few.
- **P5 (a brake is symmetric).** Reverse L8's burst totals are within 2× of forward L8's.
- **P6 (a turn is free).** The turn segment before the burn mints ≈ 0 items beyond coast (turn keys
  set no burn bit, so `decide` only re-heads; the burst arrives with the burn keys).

Kill criterion for the run's claim: P2 or P4 failing. P1/P3 failing means my reading of the item
machinery is wrong and the dossier reports that instead.
