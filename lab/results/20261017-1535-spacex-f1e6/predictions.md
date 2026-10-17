# Predictions (written before the decisive runs)

The lever: the `(doll, tick, except)` memo on `Ctx::secondaries` (arm `ES_MEMO=1`), invalidated
per doll when one of its sources rebinds, cleared each frame. Both censuses (5eb2, 6671) measured
64-90% of the stream sharing its key with 0 bit-conflicts; 5ade measured a source memo dead on the
spread belt (hit 0.029). None flew the adoption.

## Cases I have not tuned on, and what I expect

1. **Digest identity (correctness).** All 13 `ladder_digest` cases — coast, burn, key mashing,
   the wave, both belt crossings, at budgets unlimited/events-25/wall-3ms and 1 vs 4 threads —
   print identical digests, kicks, encounters and contacts under `ES_MEMO=1` and without it, and
   the OFF arm matches the frozen record (`artifacts/runs/nladder/ladder_digests_before.txt`).
   *Kill:* any digest, kick, encounter or contact count that differs between arms, or an OFF arm
   that no longer matches the record.
2. **Steady plane (the censused regime).** `nladder 10000 coast 60 600`: hit rate 0.55-0.9
   (the census's 63.9% at rtf 600 pre-crest, 89% at rtf 1800, measured on call keys; my `except`
   normalisation can only add hits). Wall p50/p99 improves by less than the call share: I expect
   the engine-ms p50 to move by at most ~5-10%, because `secondaries` is ~13.5% of the kick's
   calls and the fit owns the kick (5eb2's pricing: ~8-10% of the belt kick at 2.66×).
3. **The crest (rtf 1800).** Hit rate rises toward 0.85-0.9 (more same-tick events per frame).
4. **Burn arm.** Similar to coast or slightly lower hit rate (the player's own items read at
   odd ticks); digests still identical.
5. **The wave / spread belt (5ade's counter-case).** At N=10⁵ through the birth wave the hit
   rate is bimodal: near 1 during the birth frames (one field read per tick, 6671's 29,142×3
   birth reads), then falling to ≤ 0.1 once the belt's kicks sit on distinct ticks (the comb's
   74% distinct ex-birth). *This is the adjudication:* if the hit rate stays high post-wave,
   5ade's 0.029 was an artifact of a different memo key; if it collapses, the memo is a
   plane-steady lever, not a wave lever, and the adoption note must scope it.
6. **Threads (4-thread digest arm).** No deadlock, no digest change; the memo's mutex does not
   serialize enough to matter at these N (secondaries ~6 µs a call vs a hash get under a lock
   ~0.1 µs).

## What would make me wrong

- A stale entry surviving a source rebind: would show as a digest difference in the burn or
  key-mashing cases (the player's items land between same-tick belt events).
- The `except` normalisation being wrong (a body that IS a source reading with `except=self`
  and getting a full-set entry): would show as a digest flip in any case where a source body
  is kicked — the wave and mash cases cover it.
- Wall-time claims: the box is shared; I only claim orders of magnitude and paired same-window
  A/B runs, never cross-window comparisons.
