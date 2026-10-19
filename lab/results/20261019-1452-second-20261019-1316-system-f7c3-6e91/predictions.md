# Predictions — 20261019-1452 (second author on f7c3)

The checker's named gold rung, taken up: (a) gates B12/B13/B17 re-judged with the served
rebind (9eeb's `ES_QMEMO=1` wiring, `Orbit::from_shared`, exact key carried); (b) the
memo.rs 0.9 recurrence guard recalibrated on the served stream; (c) the composed serve
constant (0355's 0.40 µs / 9eeb's 0.85 µs) replaced by a direct measurement on the live
belt rebind stream (timing instrument inside `served()`, identical on both arms; the OFF
arm times the exact compile, so the cited 104 µs compile ceiling is re-measured too).

Nothing below is tuned on: the gates have never been run under ES_QMEMO; the belt has
never been flown under it. The pilot that ran before this file: memo.rs OFF/ON only
(reproduces 9eeb: 796 rebinds, 81 cells, hit 0.898, guard trips; exact hit 0.000).

## P1 — the gates (decisive)

`behave --law plane --gates B12,B13,B17`, arm ES_QMEMO=1 against the OFF control.
- **Prediction: all three PASS.** The serve's orbit differs from the exact compile by
  period ≤ ~7e-4, advance ≤ ~1.4e-4 (9eeb, cell-width-limited), the exact key is carried
  and the binding's residual channel absorbs the difference at the event, so kick times
  shift by ≲ 2⁻¹¹·T — the same order the step grid already quantizes.
- **Band:** each gate's headline error within 3× of the OFF arm's. B12's worst Jacobi
  error ≤ 10³ quanta of 10¹¹; B13 64/64 judged, 0 excluded; B17 within its band.
- **Kill:** any gate FAIL under serving = the 11+11 cell is not adoptable at the plane at
  this width; the honest report is the refutation and the width-ladder step (page od 2).

## P2 — the served belt stream (10⁴ and 10⁵, seed 1, ES_CENSUS=1)

- **Recurrence:** belt stream recurrence under serving ≥ 0.97 (exact arm measured
  0.98–0.99; the ≤ 2⁻¹¹-period fire-time drift can push a body across one cell boundary —
  cells/body p50 stays 1, the tail grows). Kill: < 0.90.
- **Cells:** belt stream cells within ±3% of birth cells (the standing set is
  grid-bounded; serving does not create cells). Kill: > +10%.
- **Fire rate:** belt rebinds per body per ks within 15% of the exact arm (cadence-driven,
  0659's p = 1.0).

## P3 — the measured serve cost (the composition replaced)

- **µs/call ON arm ≤ 2.5 µs** (HashMap hit + from_shared on the true belt key stream).
- **µs/call OFF arm 60–140 µs** (the exact compile; the FIT-cited ceiling is 104 µs).
- **Ratio ≥ 30×.** Kill: ON arm > 10 µs or ratio < 10×.
- **10⁹ row, re-priced on measured constants only:** rate = P2's measured belt
  rebinds/body/ks (not 0659's cited figure) × 10⁹ × µs/call → prediction 0.01–0.1 cores
  served vs 3–8 cores compiled, same arithmetic both arms.

## P4 — the guard

- Served-plane hit 0.898 (measured); served-**belt** hit ≥ 0.97 (P2). The guard's job is
  to catch a write-back regression (exact hit > 0.05), not to pin the stream's cell count;
  recalibrated to 0.85 it keeps 5% margin under the worst measured arm (the plane) and
  still fires on any write-back. **Prediction: memo.rs passes on both arms at 0.85.**

## What I do not fly (scope)

The 10⁹ population itself (2 GB cap; the key-space census extension stands from f7c3),
stirring/burn turnover (the f7c3 successor), 0355's finer class memo, eviction. The gates
half here is B12/B13/B17 only — B1/B2/B9-class statistics were 9eeb's half.
