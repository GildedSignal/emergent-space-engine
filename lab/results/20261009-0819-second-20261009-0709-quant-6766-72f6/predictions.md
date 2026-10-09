# Predictions — second author on 20261009-0709-quant-6766

Written before any n ≥ 10⁴ run (tuning so far: none; the n = 10³ smoke is allowed as tuning).
The checker's acceptance gate, verbatim: "identical digests and lag 0, while the empty-frame
gain stays ≥ 5×" for a cut-preserving break, raced at the same cut over 8- and 16-round
histories, several n.

The fix under test: a second, tick-ordered index (`ticks`, a Calendar keyed by next tick) next to
the deadline queue. `advance` stops at a too-late head only when the tick index's minimum says no
entity's next item is ≤ target. Ticks move only when an item resolves, so `rekey` (the O(N)
deadline pass) never touches it; the index is maintained at resolutions only. Claimed invariant:
while any due item may hide behind the head, the guard defers exactly like mainline, so the
resolved set and order are identical; once nothing is due anywhere, mainline's remaining scan is
pure bookkeeping (deferrals with no resolutions), so stopping changes no outcome.

## P1 — the race (digests and lag)

Held-out cases: n ∈ {10⁴, 10⁵} × rounds ∈ {8, 16} (n = 10³ allowed as tuning), variants
drain/guard/break, cut fixed at the span of 16 quant_events rounds.

- drain vs guard: **identical digests at every (n, rounds), lag 0 for both.** This is the
  prediction that decides gold. If it fails, the fix is wrong and I report the failing case.
- drain 8-round vs drain 16-round digest: equal (schedule independence of the cut; the
  instrument's positive control — if THIS fails the race is broken, not the fix).
- break: digest differs from drain at 10⁴ and 10⁵, lag > 0 at the cut (reproducing the checker's
  finding: 14 lagged at 10⁴, digests 09f67947… vs 79d01861…). This is the negative control: the
  race can see the failure it exists to catch. If break instead matches drain everywhere, the
  checker's race was scenario luck and I report that too.
- guard lag exactly 0 even where break lags: the settle fixed point is restored.

## P2 — the empty-frame gain (the ≥ 5× gate)

At 10⁵ (and 10⁴), empty-frame p50 over 20 empty frames from quant_events:
- drain ≈ 60–80 ms class (author 60.6, checker 77.9 — shared machine, absolutes drift);
- guard within ~1.2× of break (both skip the scan; what remains is the rekey): expect
  guard ≈ break ≈ 11–14 ms, **gain ≥ 5× vs drain**. Guard adds only two peeks per empty frame
  plus one tick-slot set per resolved event.
- If guard's empty frame is materially above break's, the tick index is costing O(N) somewhere it
  should not (a miss in the rekey-split) — that would be a finding against the fix as built.

## P3 — the eventful path is not taxed

ns/event p50 at 10⁵ within ±5% across drain/break/guard (the tick slot set is one indexed-heap
update, ~10² ns, on a ~21 µs event; the deferred pass shrinks). Expect guard ≤ drain if anything,
since guard stops the scan at the last due item instead of the heap's end.

## P4 — guards

`cargo test --release -p emergent-universe` fully green under guard (default), including
`the_same_digest_at_every_budget_and_thread_count` and the threads > 1 wave paths, which exercise
the guard with real interleavings the single-threaded race never sees.

## What would kill it

A digest mismatch drain vs guard at any raced (n, rounds); lag > 0 under guard; empty-frame gain
< 5×; any test failure. Each is reported as found, not patched around in the record.
