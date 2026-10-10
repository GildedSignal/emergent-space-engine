# Predictions (written before the decisive matrix; smoke runs at N=71 and N=6203 already seen)

Question: does the shipped plane's frame loop do per-frame work proportional to N when no events
fire (a hidden tick, P14), is it the `rekey` deadline walk (`for e in 0..bodies.len() { requeue(e) }`
at the top of every `Universe::advance`), and is deleting it outcome-neutral?

Seen so far (rtf 100, 6 s, unpaced, members 48): N=71 → engine p50 0.058 ms/frame, ev/s 453.0;
N=6203 → engine p50 2.454 ms/frame, ev/s 453.5. The added haulers (circular-ish orbits 0.5–8 AU,
periods of years) fire no events in this window, so the 42× engine rise is not event work.

## Cases not tuned on, and what I expect there

1. **Linearity (fit on 71 and 6203; held out: 800 and 3200, rtf 100):** engine p50 CPU/frame is
   affine in N: slope ≈ 0.39 µs/body/frame, intercept ≈ 0.03 ms. Predicted engine p50:
   N=800 → 0.34 ± 0.06 ms; N=3200 → 1.27 ± 0.15 ms.
2. **rtf independence (held out: rtf 30 at N=3200):** the N-term is per frame, not per event, so
   the slope in N stays ≈ 0.39 µs/body/frame even though the event-proportional part of engine CPU
   (visible in p99) shrinks with rtf. If the slope collapses at low rtf, the term is event-driven
   after all and my reading is wrong.
3. **Deletion (`--no-rekey-walk`, held out at every N):** engine p50 at N=6203 drops to ≤ 0.15 ms
   (≥ 16×), the slope in N falls to ≤ 5% of the with-walk slope, events/s and rtf median unchanged
   (≥ 99.9), no new overflow_frames, player alive, no lost bodies.
4. **Outcome neutrality (held out):** the digest at the canonical cut is bit-identical with and
   without the walk, at every (N, rtf) pair, because resolution is pull-driven and keyed
   (universe.rs doc; ties.rs). Any digest difference kills the deletion outright.
5. **Kill criterion for my own claim:** if the engine slope persists without the walk, the tick
   lives elsewhere (queue rebuild, horizon scan, take_due) — rekey is acquitted and I report the
   residual term's magnitude instead.

Controls: the walk ON is the positive control (the slope exists and the instrument sees it);
digest equality across the flag is the negative control (no outcome moves). The default scene
(N=71) reproduces the pristine binary's digest on the patched binary (already verified).
