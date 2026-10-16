# Predictions (written before the decisive A/B run)

Context, from the census already run (tuning arm, N=1e5 coast 200 s rtf 100, this box,
`--features prof`): the belt clock-kick is 43.3 µs/call — bind_surface 19.1 (44%),
`Ctx::secondaries` 8.8 (3 planet tube readouts), own `readout` 3.9, rest ~11.5 — plus
`apply`'s `root_state_raw` 4.8 µs/item. The lever built here: a per-`(doll, tick)` cache of
the perturbers' states (a pure function of append-only history at a fixed tick), env-gated
`ES_SEC_CACHE`, default OFF = shipped verbatim.

Cases I have NOT tuned on, and what I expect there:

1. **Digest identity.** `ladder_digest` (13 cases), ON vs OFF: all 13 digests identical.
   Rationale: the cached value is the same pure function at the same `(d, t)`; nothing
   observable changes. If any digest moves, the cache is wrong (a history/prune interaction
   I missed) and the run reports a kill of the configuration, not a caveat.
2. **Hit rate, wave frames.** In the comb's peak frames (hundreds of kicks in one frame),
   the tick-repeat rate of `secondaries` calls is > 90% (the wave fires many bodies at one
   tick; kicks at the same tick read the same three planets).
3. **Hit rate, whole flight.** Aggregate over the 200 s coast at 1e5: ≥ 50% of calls hit.
   The dyadic quantization of kick ticks (`ext.ticks` rounds to powers of two) should make
   tick collisions common even off the wave.
4. **Hit rate, held-out N=3e5 coast 200 s** (not tuned on): also ≥ 50%; the comb is
   N-independent per the nladder page's record.
5. **Cost.** With the cache ON: the SEC stage falls from ~8.8 µs/call to ≤ 2 µs/call
   (misses still pay 3 readouts); `item: kick (clock)` falls 43.3 → ≤ 38 µs/call (−12%);
   `process` whole per frame falls ≥ 10%. If the aggregate hit rate lands < 20%, the cache
   is DEAD as a steady-state lever (the 10⁹ ledger is the steady stream, not the wave) even
   if the wave frames hit — that outcome is a kill, reported as such.
6. **The OFF arm equals shipped.** OFF-arm ladder_digest output identical to a pristine
   build of main (the gate adds a branch, not a behavior).
