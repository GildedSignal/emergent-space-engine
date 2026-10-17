# Predictions — 20261017-1535-taleb-ce22 (written before any flight with the oracle)

Question: does the proposed `(j, t)` state memo (read-stream direction 1, "the cheapest item on
this page") have a reachable ruin mode — a read it would answer stale — and is the hit-rate
collapse on the spread belt (5ade: 0.029) a property of the regime or of the instrument
(6671's censuses measured plane flight only)?

Instrument: `memo_oracle` (print-only, env `ES_MEMO_ORACLE=1`), hashes every `Ctx::state_of(j,t)`
value at its exact key; a repeat with a different hash is a staleness event. Windowed by tick
(2^15) so one flight shows wave and spread phases separately, on one binary.

Held-out cases (not tuned on): the burn arm at N=10^4, N=3×10^4 (5eb2's arm), and the spread-belt
late windows of the long coast (the regime no plane census covered).

## P1 — hit rate by regime (one binary, one flight)

The early windows of `nladder 10000 coast 45 600` reproduce 6671/5eb2's order: ≥ 60% of calls
share their `(j, t)` key through the wave/crest. The late windows (past ~2 belt periods, the
spread belt) fall to ≤ 10% — 5ade's 0.029 order. Prediction: the contradiction is regime, not
instrument; the memo's use is confined to the plane's comb/birth regimes, its safety must hold
everywhere.

## P2 — staleness (the ruin mode)

0 staleness events in every arm, including the burn (rebinding flushes), the opening exodus at
N=0 (promotions rewrite current bindings), and the spread belt. Mechanism: bindings change only
at the source's own events and the scheduler resolves in tick order, so the only theoretical
window is a same-tick read-then-write-then-read, which the shipped flows do not do. If P2 fails
anywhere, the memo as specified (never invalidated) is dead until versioned, and the failure
regime is the result.

## P3 — cost of the oracle itself

Flights with the oracle on stay within 2× wall of oracle-off (it is a measurement instrument,
not a production path); digests (`ladder_digest`) identical with the patch applied and the
oracle both off and on — observation-only by construction.

## Kill criteria for my own claim

If the oracle shows 0 stale everywhere but the windowed hit-rate curve does not separate regimes
(no collapse on the spread belt), then the 5ade-vs-6671 contradiction is NOT regime, my P1 is
wrong, and the dossier says so (the memo's use is broader than 5ade suggested — adoption gets
cheaper, still gated by P2). If STALE > 0 anywhere, P2 is the headline and the adoption is
blocked as specified.
