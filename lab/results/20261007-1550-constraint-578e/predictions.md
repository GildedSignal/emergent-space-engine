# Predictions (written before the decisive runs)

Tuned on: rtf 1 and rtf 100 paced benches (default 48 members), kick-bench, the VIEWPHASES
instrumentation at rtf 100. Not tuned on: the cases below.

## P1 — the view does not scale with rtf; the engine does, until its budget binds

At `--rtf 300 --unpaced` (5 s), I predict:
- `view_gather` p50 stays within ±20% of 3.6 ms (it is per presented frame, independent of rtf);
- the engine's p99 sits at its 5 ms budget and `overflow_frames` exceeds 10% of frames;
- the median achieved rtf falls below 250 (the engine budget, not the view, becomes the binding
  constraint somewhere between rtf 100 and 300).

## P2 — the view scales linearly with handed-out bodies and breaks the frame first

At `--rtf 100 --members 400` (paced, 10 s), members are handed out over the run and become root
bodies. I predict:
- `n_bodies` grows from 28 towards a few hundred;
- `view_gather` p50 grows roughly linearly with live bodies at ~60–90 µs per body per frame
  (measured 88 µs at 27 bodies), reaching > 10 ms before the run ends — the frame's 16.7 ms
  deadline is broken by the view, not the engine;
- the engine's cost also grows (leaver kicks at ~366 µs each) but stays under its 5 ms budget
  more often than the view stays under its share.

## P3 — the memo that exists (crossing guesses) underdelivers 3×

The cached gather's own contract is "about one readout per emitter instead of two or three"
(view.rs). Measured at rtf 100: ~3 readouts per emitter per frame (76–85 for 27 bodies). I predict
at rtf 1 the same ratio holds (±1), i.e. the guess memo is rtf-independent and systematically
lands one Newton step away from the bracket.

## What would make the constraint story wrong

If view_gather p50 at --members 400 stays under ~6 ms, the view is not the scale constraint on the
presented path and the board's kick-first order is right as it stands.
