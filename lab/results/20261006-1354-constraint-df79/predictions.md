# Predictions (written after the members-48 baseline, before the 200/400 and rtf-ceiling runs)

The baseline (m48, rtf100, paced, this box): frame p50 3.4 / p99 9.7 ms; shares engine 21.9%,
view_gather 62.4%, view_json 11.0%, wire 4.7%; rtf median 100.0, lowest 1% 9.9, 46/1800 overflow
frames; engine µs per item: ship 283, player 1299, fleet 66; stats leavers 48, lost 26.

1. **The two currencies split.** The engine is wall-budgeted (5 ms) and defers; the view is not.
   As members grow I predict the *engine* (rtf) saturates first: overflow frames and the rtf's
   lowest 1% worsen sharply, while frame p99 stays under 16.7 ms — smoothness survives past the
   point where game time has already slowed. So the constraint order is: engine throughput (rtf)
   before view smoothness, at this scene scale.
2. **What grows with members.** Bodies grow ~linearly (members + a fixed scene). I predict the
   `fleet` kind's items and total ms grow ~linearly with members (it is per-member work, and the
   leavers are never retired — the known forever-stepped bug), while `ship` and `player` stay
   roughly flat. The view gather ms grows ~linearly with bodies (it is per-emitter).
3. **At members 400** (the clamp): overflow frames ≥ 10× the m48 count, rtf lowest 1% below 5,
   frame p99 still < 16.7 ms. If instead frame p99 crosses 16.7 ms first, prediction 1 is wrong
   and the view is the binding constraint for both currencies.
4. **rtf ceiling.** At members 48, rtf 1000: game time per frame is 10× so events per frame 10×;
   I predict the engine cannot hold it (median rtf well under 1000, most frames overflow), i.e.
   the rtf ceiling at this scene is ~a few hundred, set by events/frame × µs/event against the
   5 ms budget — not by the view.
5. **Kick bench.** On this older x86 box, per-kick medians land 2–5× the M1's numbers (kick ~29 µs
   there), with the rebind (fit+compile) around half of a made-body kick, matching the known 15/29
   split in kind.

Kill criterion for the run: if none of 1–4 separates (both currencies saturate together, or
neither does at the clamp), the constraint question is not answerable at the plane's clamped scene
size and the dossier says so — that itself names the next probe (a members-unclamped bench).
