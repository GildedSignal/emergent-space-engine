# Predictions (written before the members ladder; only the 48-member default has been seen)

The probe: `xtask universe --bench --rtf 100 --seconds 8 --unpaced --members N` for
N = 4 (negative control: minimal battle, readout floor), 48 (baseline, seen), 480, 4800, 48000
(held out), each under `/usr/bin/time -v` for peak RSS. Linux/x86, shared 8-vCPU box: orders of
magnitude only.

The board's premise under test (focus item 1): "kicks dominate the engine's cost". The frame,
not the engine, is what the player pays for: at 48 members the dashboard already reads
engine 25%, gather 63%, json 9%, wire 3.5%, ship items at 73.6 µs each, bytes_per_body 5310.

## Held-out predictions

1. **The readout is the frame's wall at moderate scale.** At N = 480 and 4800 members the
   gather+json+wire share stays ≥ 45% of the frame's measured parts; engine share stays ≤ 40%.
   (Both are O(N) per frame, so shares move slowly; the claim is the readout is not negligible —
   it is the same order or larger than the engine.)

2. **Engine demand crosses the 5 ms/frame budget between 480 and 48000 members**: overflow_frames
   go from ~0 at 480 to > 5% of 480 frames at 48000 (per-item ship cost stays ~50–100 µs, items
   scale with members; 5 ms / 73 µs ≈ 68 items/frame is the budget's ceiling).

3. **Marginal memory per member (peak-RSS slope over the ladder) is ≥ 64 B/member**, ≥ 4× the
   16-byte tube contract, i.e. the plane's containers, not the law, set the memory idiot index
   at scale. Prediction: slope in the 100 B/member class (order 10^2).

4. **bytes_per_body (the tube store's average) stays ≥ 2 kB at every N** — it does not amortize
   down toward the 16-byte tube as the catalogue grows.

5. **Ship us_per_item is flat in N** (within 2×) across the ladder: the per-kick cost is
   per-item constant; scale cost is item count, not item cost.

## What would falsify the probe's headline

- Engine share ≥ 60% at both 480 and 4800 (then kicks really do dominate the frame at scale and
  the readout worry is wrong — premise confirmed, probe still reports it).
- Marginal RSS slope < 16 B/member (then the container is at the tube floor already).
- us_per_item growing ≥ 4× with N (then per-item cost, not count, is the scaling problem).

## Controls

- Positive: the dashboard's engine max (5.39 ms at 48) exceeds its 5 ms budget — the instrument
  sees engine work; events_per_second > 0 at every N.
- Negative: N = 4 (minimal battle) — readout share near its maximum, engine near zero: the
  instrument does not report engine cost where there is none.
