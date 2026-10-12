# Predictions — 20261012-0753-quant-dafc

Written before the decisive sweep. Tuned on nothing but the 5 s smoke run at
(rtf 100, members 48, budget 5 ms, paced): 300 frames, 0 hitches > 16.7 ms,
45/300 overflow frames, rtf lowest-1% = 0.00, engine p50/p99/max = 0.32/6.66/11.96 ms,
gather p50/p99 = 3.95/4.82 ms (61% of frame time).

## The question

Where is the plane's smoothness capacity frontier on this machine class — the rtf at
which game-time delivery (rtf lowest 1%) and the frame tail (p99.9, hitches) first
break — and which stage owns each axis?

## Kill rule (frozen)

Smooth at (R, M, B) iff: hitches/hour above 16.7 ms ≤ 60, worst hitch < 33 ms, and
rtf lowest-1% ≥ 0.9·R. Capacity R* = the largest tested R that is smooth. The design's
claim to falsify: "overflow dips the real-time factor smoothly; nothing hitches" — it
fails if hitches > 16.7 ms appear on any run with overflow > 0.

## The sweep (all seed 1, paced 60 Hz unless said)

rtf {10, 30, 100, 300, 1000(5 s)} at members 48, budget 5 ms; budget 15 ms at rtf 100;
members 400 at rtf 100 and rtf 30; one unpaced run at rtf 100 (throughput ceiling +
digest control).

## Predictions (held out: every cell except the smoke cell)

- **P1** (delivery axis breaks before 100): at rtf 100, 20 s: overflow frames > 10%
  and rtf low1 < 90. The "flies at 100× with no hitch" claim is true on the frame-time
  axis and false on the game-time delivery axis.
- **P2** (first overflow between rtf 10 and 30): rtf 10 has overflow = 0 and low1 ≥ 9;
  rtf 30 has overflow > 0. So R*(48 members, 5 ms) ∈ [10, 30).
- **P3** (frame wall protected everywhere): up to rtf 1000: 0 hitches above 16.7 ms,
  worst < 33 ms. Overload lands on delivery, never on the frame.
- **P4** (the budget, not the machine, binds at 100×): budget 15 ms at rtf 100 brings
  overflow to ~0 and low1 ≥ 90, while the gather keeps frames under 16.7 ms.
- **P5** (members scale the engine linearly): members 400 at rtf 100: ≥ 50% overflow
  frames, low1 = 0; engine share of frame time exceeds the gather's.
- **P6** (control, schedule independence): identical digest at rtf 100 across
  {paced 5 ms, paced 15 ms, unpaced 5 ms}.
- **P7** (the budget has a soft edge): engine p99 exceeds the budget on overflow runs
  (smoke: 6.7 vs 5.0) and still exceeds it at 15 ms — the budget bounds the number of
  items, not the cost of one item; single items (a rebinding burst, a fleet epoch
  batch) overrun the cap.

## What would make this wrong

If P3 fails (hitches appear with overflow), the budget does not protect the frame wall
and the smoothness design is broken, not just capacity-limited. If P6 fails, the
"budget changes when, never what" contract is violated — an integrator-level bug, not
a lab artifact.
