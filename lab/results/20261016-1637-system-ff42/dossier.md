# Dossier — 20261016-1637-system-ff42 (system lens)

## Claim

The plane's crash search (`step::next_impact`) and the compiled trajectory's inverse
(`Trajectory::at_radius`) are one mechanism shipped as two: the inverse is exact, already
compiled into every tube, and already wired as `next_exit`'s verified guess for passages —
but the crash search, half of every flying kick's cost (frame-cost's census: 45%), bisects
blind over ~2^30 ticks with full Cartesian readouts. Wiring the same verified guess into
`next_impact` gives tick-identical answers (36/36) at a mean 2.0× (best rows 3.2–4.9×) on
shipped code, in 11 lines.

## Bottleneck

Not the memory wall, not the belt's stream: the per-kick cost on crash-course bindings —
the player's, the battle's, every leaver's first plan (birth-stagger: 485–686 µs a leaver;
frame-cost: the flying leaver kick 199 µs, 45% of it this search). Expected gain: the
search's term collapses from the probe class's floor (mean 10.9, worst 18 full readouts)
to one inverse solve plus two verifications where it verifies. It also deletes the future
need for the probe-policy layer (ES_FP/AB-IQI): a structural answer beats any probe policy
— the frame-cost page itself says the black-box class is "at its policy class's floor",
which is the signature of the wrong representation, not of a finished component.

## Evidence

Bench: `crates/universe/examples/levelbench.rs` (new, in the patch), 36 crash-course
bindings (bound cycles at periapsis fractions 0.05–0.99 × both senses × clock_exp 0 and 6,
unbound flybys e 1.05–3 at three impact parameters), each answered by (a) an inline
verbatim copy of the shipped bisection loop and (b) the shipped `next_impact` with the
patch. Full table in `bench.txt`. Machine: shared Linux x86 (orders of magnitude only).

- **Answers: 36/36 bit-identical** (the guess is verified against the shipped predicate and
  falls back to the shipped bisection; equality additionally rests on the same
  monotone-on-branch premise the shipped bisection already requires — its own doc comment).
- **Cost: mean 55.9 → 27.9 µs (2.0×); probes mean 10.9 readouts → 2.9.** Timing splits the
  paths: ~22/36 rows collapse to ~18–21 µs (one `at_radius` + two verifications: 3.2–4.9×
  vs their 59–91 µs references); ~11 rows fall back (cost = shipped + one wasted inverse);
  3 rows are the untouched O(1) paths (plunge terminal, periapsis above surface).
- Untouched paths measured unchanged: plunge (23–24 µs both arms), no-course (4.7 µs both).

Patch (11 lines of logic + 2 visibility words): `crates/space/src/binding.rs`
`Trajectory::at_radius` made `pub`; `crates/universe/src/step.rs` gains the verified-guess
block in `next_impact` (the identical pattern `next_exit` already uses for passages) and
`next_periapsis` made `pub` for the bench. Nothing else; no behaviour change on any path
the guess declines.

## Predictions (predictions.md, written before the bench)

- Held: tick-exactness (100%, by construction — the risk was a units bug, none found);
  probes ≤ 3 where verified; O(1) paths untouched.
- **Missed, honestly: the fallback rate.** Predicted < 2% at mid periapsis fractions;
  measured ~40% overall (11/36 fall back). Mechanism, from the diag (`levelbench diag`):
  the guess tick is the pure-tube crossing rounded by `fixed_ceil`, while the predicate
  reads the tube **plus its turn and integer offset** (the residual), and near a slow fall
  a sub-quantum offset moves the crossing by more than the ±1-tick verification window.
  The cure is mechanical and named: verify a ±k window with k from the local fall speed
  (or read the readout at the guess and Newton-step once), then fall back. Prediction 5's
  kill (fallback > 50% at mid fractions) did not fire — this is a rounding-window
  artifact, not a wrong representation; but it caps today's gain at 2× mean instead of 4–5×.

## What would make it wrong

- Any flight digest changing. Not flown today (the per-call battery is exact-tick equal on
  36/36, and the function is pure in `(binding, surface, after)`, but the flight-level
  `--replay-all` digest check is the adoption gate and is unflown — that is the first thing
  the adopter runs).
- The monotonicity premise: if the readout radius is not monotone on the fall branch for
  some binding (eccentric plunge-adjacent courses), the shipped bisection is already wrong
  there, and the guess would agree with a wrong answer — no new exposure.
- The residual offset reaching further than a few ticks on grazing courses: then the
  verified window must widen and the win shrinks toward 1× for those courses only.

## Cost of adopting, and fit

Eleven lines in one function, one `pub`, plus the bench. It composes with (and eventually
deprecates) the probe-policy work: `ES_FP`/`ES_IMP_WARM` optimize the fallback path this
patch keeps as the safety net. PRINCIPLES, 19: "a fix signals the wrong representation" —
the bisection over ticks was the fix; the compiled cycle was the right representation all
along ("we just need to have the right representation so that math is trivial", 18). Also
32: the symmetry (Darwin phase makes the radius crossing a closed form) was found in the
representation, not paid for in search.

## The lens (what it may have made me miss)

The system lens looked for two-mechanisms-one and found it half-wired; what it did not do
is price the SAME unification for `next_exit`'s **Cycle** branch (still bisection, rarer)
and the view's emission search (a different level function: `t + |x(t)−X| = T`, not a
radius crossing — the inverse does not apply directly). A red-team should check whether the
battle's scan predicate (`encounter.rs`) is a third radius-level consumer in disguise.
And the 40% fallback is exactly the kind of hard special case the lens brief warns about:
the residual offset is not noise the structure can ignore — it is part of the crossing law.
