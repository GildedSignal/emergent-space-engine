# Predictions (written before the decisive runs)

The run I am second author on (20261012-2257-spacex-5eb6) was graded silver for one reason: under
sustained starvation (3-event budget, rtf 5e6, 200/200 overflow) the plane gate
`work_per_frame_is_bounded_and_overflow_is_a_dip_not_a_hitch` fails — the budgeted fleet's battle
committed to tick 54,525,951 while the cut is 54,525,823, so budgeted-then-settled ≠ freshly-settled.

## Diagnosis (mechanism, predicted before the fix is tried)

The lazy horizon subtracts the staleness slack (`wander`) from the smallest stored deadline, but the
fleet's commit cap `second_dl − dist` does not subtract it. A stored deadline can be stale-high by
up to `wander` (the observer moved since it was stamped), so the fleet can commit up to ~slack past
any time the frame may present. A second residue: when the fleet is within `slack` light-ticks of
the player, its own requeued deadline `to + 1 + dist` enters the horizon's min, and the blanket
`− slack` puts the presented time below its own commit regardless of the cap (needs `dist ≥ slack`).
The player's neighbourhood pull (`resolve_fleet(f, key.0 − 1)` in `resolve_body`) can also commit
past the presented time when the player's next event is closer than `slack`; I predict it does not
bind in this scenario (player event gaps ~10⁵ ticks against slack ≤ want/64 ≈ 4.3×10³).

## The fix

`cap = second_dl − dist − slack` (the same staleness subtraction the horizon makes), and a fleet
within `slack` light-ticks of the player parks instead of committing (its own deadline cannot be
made safe under the blanket subtraction; the next rekey zeroes the slack and it proceeds).

## Predictions, in the cases I have not tuned on

1. **The gate passes and `lazy_probe starve` prints one digest for budgeted and settled**: with the
   slack-subtracted cap, the fleet's committed tick never passes the frame's presented time, so the
   final `settle(h)` lands it exactly at the cut, as the settled arm does. If the pull path also
   commits past, the gate still fails and I report which path did it (the instrumentation prints
   every commit past `now` with its caller).
2. **The stepped-settle arm still differs** from the single settle (both arms on base too: the
   fleet's stop point below the cut is chunk-dependent, a shipped property of the battle's slice
   end, not of this change). This is not the gate's comparison and I do not touch it.
3. **Digest identity across arms and schedules is unchanged** (deadlines are a schedule, never an
   outcome; the quiet and fly probes print the same digests as the author's record: per-seed one
   digest, arms agree).
4. **The quiet-frame medians are unchanged** (lazy 1.3–1.5 µs flat to 2×10⁵ bodies): the fix touches
   only the fleet branch of `resolve_entity`, which quiet frames never take.
5. **The rekey counts do not move** (fly 1–219, quiet 2): the fix does not touch the wander gate.
6. **Red team (the author's trap, revisited): a parked fleet must not stall the presented time.**
   The author's first slack-subtracted cap deadlocked by spinning no-op resolutions inside one
   frame; the park-and-retry in the final patch makes a parked fleet cost one try per advance, and
   the player's pull keeps handouts flowing. I predict no freeze: the starve probe's presented time
   reaches the same cut 200 frames in (± a few percent of ticks), and the fly suite's starved
   schedule (wall 0.05 ms) still reaches the cut within its 40,000-frame bound.
