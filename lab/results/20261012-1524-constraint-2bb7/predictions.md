# Predictions (written before the decisive runs)

Baseline measured (exploratory, unpaced, seed 1, rtf 1, 28 bodies, 48 members):
frame p50 0.63 ms; engine share 3.9%, view_gather 72.5%, view_json 16.5%, wire 7.1%;
stats: 0 kicks, 600 slices, 34 opens. Engine budget 5 ms never approached.

## D1: rtf sweep (unpaced, seed 1, 10 s, members 48): rtf = 100 and 1000

- Engine share rises roughly linearly with rtf until the 5 ms budget bites
  (budgeted work is deferred, overflow_frames > 0 above some rtf).
- Prediction: at rtf = 100 (Julien's flight pace) engine share is 40-80% of the
  frame but the frame stays under 16.7 ms; at rtf = 1000 the engine budget is
  the binding constraint and overflow frames appear (rtf median < target).
- View gather cost per frame stays ~constant with rtf (it is per-emitter work,
  not per-game-time work), so the view is the constraint at low rtf and the
  engine (kicks/slices) at high rtf.

## D2: members sweep (unpaced, seed 1, rtf 100, 10 s): members = 480, 4800

- Gather, json and wire grow linearly in presented emitters (no culling: every
  live body gets a Newton light-cone solve and serialised floats every frame).
- Prediction: view pipeline crosses the 16.7 ms frame between ~1,000 and ~2,000
  presented emitters (0.46 ms gather / 27 emitters ≈ 17 µs each), long before
  the engine budget (5 ms) is spent. The constraint for presented scale is the
  view's gather, not the engine.
- The engine's own cost at rtf 100 grows slower than the view's (kicks are
  amortised per orbit, not per frame per emitter).

## D3: gates

- `behave --law plane` matches the handoff (B13 60/64, B17 pass, G/E mostly
  pass, E9 fails phase 1 as designed); no new failures on this machine.

Kill criterion for the run: if none of D1/D2 scalings hold (view flat in
members, or engine flat in rtf), the constraint analysis is void and the run
reports the raw numbers only.
