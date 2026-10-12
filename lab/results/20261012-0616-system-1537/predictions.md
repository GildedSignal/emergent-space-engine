# Predictions (written before the patch runs)

The shipped `advance` requeues every entity every frame (deadline = tick + light-distance, a sqrt and
an indexed-heap set each) even when no event is due: measured 215 µs/frame at n=1000 quiet bodies,
37.4 ms/frame at n=64,000, with **zero** events (superlinear: 174× cost for 64× bodies).

The patch: the calendar keyed by the canonical tick (t, id) — requeue only at an entity's own events;
deadlines computed only for the frame's due set (priority + overflow horizon); the per-frame `rekey`
pass deleted (only the observer position stays).

## Held-out cases and expectations

1. **Quiet cost collapses.** At n=64,000, per-frame wall drops by ≥ 300× (37,436 µs → ≤ 120 µs), and
   ns/body/frame falls with N instead of rising (≤ 2 ns at n=64k). A mild residual growth with N
   (cache effects on the queue peek) is acceptable if ≤ 2× from 1k to 64k.
2. **Digests identical, bit for bit.** All three schedules (A settle, B threads-4 budgeted frames, C
   starved with overflow) print exactly `645d0367d54b951b4f165ec1ea638a56fb4f650eb4592d7b6b2beac1e8c99204`
   after the patch — the same string the unpatched code prints. The deadline is documented as "a
   scheduling heuristic only"; ordering by the canonical tick instead must not move any outcome.
3. **Schedule C (overflow)** is the case I did not tune on: its digest is the real test that the
   deferred/horizon rewrite keeps the mandatory set identical.
4. **Miss risk I name in advance:** `resolve_wave` (threads > 1) now drains due ships from the
   tick-keyed calendar directly; if its batching composition changes outcomes, digest B will differ
   and the patch is wrong, not the experiment.

If (1) holds but (2) fails on any schedule, the finding stands (the tick is real) and the patch is
killed, not the diagnosis.
