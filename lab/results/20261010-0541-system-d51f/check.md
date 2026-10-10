Grade: silver

Abstract: Claim: light-arrival bookkeeping (scheduler deadlines, view gather, coming news gravity) re-derives the same doll-chain readout. All headline numbers reproduce (gather 775–858 µs vs engine 56–62 µs median, 13–18× across seeds; sched walk 7.1–7.9 µs/call, 1123 calls, ≈47% of the *median* engine frame; memo redundancy 2.9%). Checks: the shipped stream control was vacuous (counters reset after the last gather — my corrected control confirms its 0% conclusion); "~6.4–7.2 µs per level" conflates per-call with per-level (avg depth 2.04 ⇒ ~3.9 µs/level; news-gravity arithmetic halves to ~60–90 µs/kick, conclusion stands); the bit-identity assert is wall-sensitive (`Budget::wall(5.0)` is 5 ms; seed 13 diverges via overflow bites, not memo impurity). Gain: ~1.9× on the median engine frame, not 10×. Cost: one owner unifies three paths.

## Reproduction

`cargo test --release -p emergent-universe --test lab_arrival -- --nocapture` after `git apply work/patch.diff`: events 2827, levels 36594, hit share 2.9%, gather median 775.1 µs, engine median 56.7 µs, sched 1123 calls @ 7.09 µs — every number matches the dossier. Across seeds (7/3/99, rtf 100): gather/engine 13.9×/18.0×/13.3×; sched 7.84–7.96 µs/call. Source-verified mechanism: `apply`'s `root_state_raw` exists solely to keep `pos[e]` for `light_distance`→`deadline_of` (universe.rs:531, 473, 481); `ViewCache::put` already stores the arrival rate `(1+n·β_obs)/(1+n·β_em)` every frame (view.rs:130–148); law.md's news gravity is a queued build (HANDOFF, motion law v2). All predictions' outcomes (held and falsified) match what the dossier reports.

## Adversarial cases and defects found

1. **Broken control.** The stream control calls `lab::reset()` *after* each gather, then takes the counters: `levels 0` for any scene, so "0 hits" there measures nothing. My corrected control (reset before gather): 7680 levels, 0 hits, 0.00% — the author's *conclusion* (prediction 2) is right; the instrument was not.
2. **Unit conflation.** Sched 7.1–7.9 µs is per *call* (a whole chain walk; avg plane depth 2.04 ⇒ ~3.9 µs/level); 6.4–7.0 µs/level from the gather attributes *all* gather wall (Newton loop, per-emitter work, fleet section) to readouts. "Two independent paths land on the same ~6.4–7.2 µs" is coincidence of mixed units. The derived news-gravity cost halves to ~60–90 µs/kick — still ≥1 median engine frame per kick, so the structural warning survives.
3. **Bit-identity is load-sensitive, not a purity proof.** On seed 13 the author's assert fails on this shared runner: `Budget::wall(5.0)` is 5 **ms** (ms/1e3), heavy frames overflow, and at frame 68 both flights bite the wall with 19 vs 20 events resolved — divergence from flight timing, not memo impurity (within a frame the memo provably returns `ramped`'s own output under an immutable ctx; allocation churn alone also flips bites). The seed-7 pass was quiet-machine luck; the right instrument is a settle-cut digest. Prediction 3's "held" is overclaimed as evidence, though the memo's within-frame purity itself is sound. Also, prediction 5's "≥1 call per kick" measured 0.397/event and is not reported as falsified.
4. **Median vs mean.** Sched tax is 47% of the median engine frame but ~7% of mean engine compute (438 µs mean, tail frames capped at 5 ms) and 9% at rtf 10/1000. Stated against the median it is honest (smoothness framing, "median" said explicitly) but reads larger than the total-cost share.

## Novelty

Gather dominance is known (H0210 limitations: "the view gather is 83% of a light frame; kicks cost 29 µs"; the ViewCache crossing cache was already built). Memo-of-a-pure-read cannot change bits was established at the `field_at` layer (G3, same-law memo). New here: the scheduler's per-event walk tax measured for the first time; the 2.9% within-frame redundancy *killing* the naive per-frame sharing idea (retarded ticks differ per emitter — a real negative result); the per-level cost atom; the pre-build cost warning for news gravity.

## Goal fit

Moves board #1 (kicks dominate) at the measurement layer and feeds the queued news-gravity build; fits "Compute only surprises" (3) and "the best part is no part" (17). The deletion is designed, not measured: no running code deletes the 26.7 µs/frame.

## The one experiment for gold

Build the incremental deadline (`deadline' = deadline + Δt·(1+n·β)` from the rate the view already stores) behind the same lab flag, and show: median engine frame drops by the predicted ~26 µs; digests equal *at a settle cut* (not raw flight cuts, which bite the 5 ms wall); across seeds and rtf including a β→1 flight (the regime the lens itself flags). That is one afternoon on this same harness.

## What the author missed

The shipped control measured nothing (reset-after-read); the per-call/per-level conflation inflated the derived news-gravity cost ~2× and manufactured the "internally consistent" argument; the bit-identity assert cannot distinguish memo purity from budget bites (5 ms, not 5 s — `Budget::wall` takes ms); the mean-frame and rtf-10/1000 shares of the sched tax go unreported; and prediction 5's failed call-rate half is silently dropped from the "held" list.
