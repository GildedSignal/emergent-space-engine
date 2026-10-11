# Five lessons from Julien's library for the board's top bottleneck (kicks dominate; cadence the lever)

All quotes verbatim from his Readwise export (cached: `readwise.json`), checked against the API text.
Target: board item 1 (fewer kicks per orbit at the same behaviour) and queue top `q-b12-design`.

1. "Delete any part or process you can. You may have to add them back later. In fact, if you do not
   end up adding back at least 10% of them, then you didn't delete enough." — Elon Musk, *Elon Musk* (Walter Isaacson).
   Mechanism: the floor is found by overshooting deletion and calibrating on what bites back, not by analysis.
   Change: the deletion candidate "delete per-body kick evaluations until the field changes by one quantum" was
   pushed past its edge in this run; it bit back 10^3-fold (below). The deletable part is not the event timing.
   Keep deleting elsewhere: the slack skin (12.6x, components-4643), not cadence. Test: this run's probe (done).

2. "By a law of probability called distribution of the maximum of random variables, the maximum of an average is
   necessarily less volatile than the average maximum." — Taleb, *Fooled by Randomness*.
   Mechanism: population means hide per-unit worst cases; budget the average of per-unit maxima.
   Change: the allocator's p99 frame budget must be fed by per-body, per-orbit maxima of wake rates (measured
   here: gated cadence raises p99-rate/mean-rate to 1.35-1.47 vs fixed 1.00; any adaptive scheme does this).
   Test: the `win_max/rate` column in this run's tables (done).

3. "The first mistake rarely proves disastrous, but the downward spiral of the second, third, and fourth error
   creates a devastating chain reaction." — Josh Waitzkin, *The Art of Learning*.
   Mechanism: classify errors by compounding, not size.
   Change: B12's energy register must expose the walk (log-log slope of |ΔJ| vs t), not a magnitude: this run's
   schemes separate by slope 0.03 (bounded) vs 0.75-1.00 (chain reaction) at similar single-event error.
   Test: any candidate cadence through the slope statistic before counting its evaluations (done, table above).

4. "Psychohistory dealt not with man, but man-masses... The reaction of one man could be forecast by no known
   mathematics; the reaction of a billion is something else again." — Asimov, *Foundation and Empire*.
   Mechanism: aggregates admit laws individuals don't; precision lives at the population scale.
   Change: cadence belongs to the aggregate (cell), precomputed from cell constants and inherited by bodies —
   measured safe here (per-body precomputed cadence is bounded, on the fixed curve); only state feedback inside
   the loop walks. Test: next rung — k bodies sharing one precomputed cell cadence (r8/B18 scene).

5. "I have no use whatsoever for projections or forecasts. They create an illusion of apparent precision.
   The more meticulous they are, the more concerned you should be." — Warren Buffett, via Farnam Street.
   Mechanism: meticulous local control is a false signal; rank by the invariant the game observes.
   Change: the significance gate was meticulous (2-50% field change per event, locally optimal) and destroyed
   an exact invariant; gates keep judging registers and behaviours, never local precision. Test: this run (done).
