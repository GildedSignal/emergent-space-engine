# Predictions — 20261017-1829-spacex-d399

Written after the bench decomposition (fitbench, replayed flown belt inputs, patch
present but inert during the flight whose digest matched pristine `4995f384…`), before
the held-out runs: (a) `FIT_NODECODED=1 ladder_digest N=3000` vs the pristine record,
(b) a wall-time A/B on `nladder 3000 coast 20`.

## P1 (the delete arm is bit-identical on every digest)

The arm skips only `fit.residual = Residual::between(state, fit.decoded_event()?)` in
`Rebinding::from_state` (and nothing else; `bind_in` never reads `fit.residual` — it keeps
its own residual from its own `decode`). Prediction: all 5 `N=3000` ladder_digest cases
print digests, kicks, encounters, contacts identical to the pristine record
(ddd5b1cc…, 69d7abbb…, 253d8aed…, d2632de9…, 4995f384…) and "every case: one digest on
every schedule". Risk I accept: if any corpus case has a state where `decoded_event()`
used to ERROR (Range) and the arm now binds instead, the digest changes — that would show
up as a kick-count change first. I predict no case hits it (the corpus's from_state calls
all succeed today; their decoded_event is on the success path).

## P2 (the wall-time share on a real flight)

The replay measured −3.63 µs/call mean (−13.9% of bind_surface mean 26.16 → 22.52; p50
17.19 → 13.63, −20.7%). Prediction: on `nladder 3000 coast 20` the engine's total ms
drops by the fits' share: the fit stage is 45% of the kick clock item (5eb2) and a kick
is most of the engine's time in the wave; I predict a total-engine-ms drop of 3–8% on
this coast run (the belt's kick stream dominates; the arm removes one of the fit's three
trajectory evaluations). If the drop is < 1%, the replay's share does not transfer to the
flight and I will report that.

## P3 (held-out: the burn arm, never replayed)

The captured corpus is the belt crossing (coast + L10 burn script). Prediction: the
strong-field/handoff-heavy `key mashing` case in P1 exercises other from_state callers
(hand-outs, burns); if the arm is structurally dead, those digests hold too — same
prediction as P1, no separate case.

## P4 (attribution that could still be wrong)

The p99/max spikes (355 µs / 1.6 ms) in the replay are first-touch/FIT2-rebind artifacts
of replay, not the engine's; I predict they shrink or stay in a warm second pass (the
"SHIPPED again" pass already shows mean 26.24 vs 26.16 — stable, so the spikes are
reproducible per-input, and I will NOT claim them as engine costs).
