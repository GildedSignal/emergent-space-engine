topic: flyable-frame
status: open
closed-by:
valid-while:
updated: 20261018-1237-system-4875

# The flyable frame: engine + view + wire in one loop, and which half binds

## Current best

**The flyable frame (the loop `xtask universe` serves: engine advance + view gather + view
JSON + wire, all inside the frame, engine budget 5 ms of 16.7) is view-owned from ~8×10²
bodies, and the ladder's "10⁶ smooth" is an engine-only instrument reading a plane the
player cannot fly past that point (20261018-1237-system-4875, system; `xtask universe
--bench --unpaced` on `scenario::plane_extra` — a 20-line `--extra` knob, this run's patch —
seed 1 + held-out seed 2 + rtf 1, rtf 100, the bench's burn script).** At 10,071 ladder
bodies: frame p50 261.8 ms with engine 0.11 / 4.6 ms p50/p99 (inside its 5 ms budget; the
ladder's own flat-in-N record reproduced on the same flights) and 99.7% of the frame in the
view's three Θ(N) channels: gather 232 ms (19–23 µs/body — real tube readouts up the doll
chain, ~3× the fleet-member constant the view page had), json build 24 ms (2.4 µs/row),
wire 4.7 ms (~2 MB/frame, ~120 MB/s at 60 Hz). At 1,071 bodies: 22.0 ms (593/600 frames
over 16.7); the shipped 71-body plane: 0.98 ms, 0 hitches (the control). Slopes 21 and
26.6 µs/body over the two decades; crossing 16.7 ms at ≈ 794 bodies. rtf 1 identical (257
ms): the wall is per-frame, not per-event. Consequence (the ranking): the view's row-set
deletion (62c1/2df1, built, unwired, 1–3 ms at 10³–10⁶ map-class) is the first adoption for
the furthest-behind scoreboard gap — no engine cure (the composed law, the scan tier) can
reach the player past ~800 bodies until it lands; then the engine's cures bind again past
~10⁶. Before the patch the flyable binary could not load the ladder's scene at all
(`--members` clamps at 400).

## Refuted

- **"10⁶ keep smooth flight" as a statement about the flyable engine (the HANDOFF
  scoreboard line, nladder's instrument):** engine-only — the flyable frame crosses 16.7 ms
  at ≈ 8×10² bodies with the engine at 0.1 ms; the instrument gap is ~3 orders
  (20261018-1237-system-4875).
- **"The gather is ~7 µs/body" extended from fleet members to belt bodies:** belt bodies
  are full tube readouts up the doll chain — 19–23 µs/body warm (20261018-1237-system-4875;
  0d46's 6.9 and e401's 7.3 were the bench crowd's handed-out members).

## Open directions

1. **Wire the row-set deletion (2df1) into `Session::step`** and re-fly this exact matrix:
   the prediction is frame p50 ≤ ~3 ms at 10⁴ and the crossing moving past 10⁶ (then the
   engine's scan channel and comb are the bind again — nladder's cures, in their order).
2. The served half: HTTP + page parse of ~2 MB/frame at 10⁴ is unmeasured; the true served
   crossing is earlier than 794. One flight with the browser driven (not just the bench).
3. The formation scene in the flyable frame (needs the formation knob beside `--extra`):
   there the scan channel joins the view in one frame; the ranking's second step.
4. Belt zoom (62c1's checker: ~N rows on canvas): if the row set is Θ(N) there, the view
   cure is zoom-scoped — price it before calling 10⁶ flyable.

## Contradictions

None open. This page's engine numbers (flat, inside budget) and nladder's agree; the
difference is the instrument, not the law.

## Runs

- 20261018-1237-system-4875 (system, awaiting grade): the flyable frame is view-owned from
  ~8×10² bodies; 262 ms at 10⁴ with the engine inside budget; adoption order inverts
  (view's row set first).
