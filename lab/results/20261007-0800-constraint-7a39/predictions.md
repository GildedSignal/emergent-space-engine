# Predictions (written before the decisive experiment)

State of play, measured first (main, Linux x86, load 0.3–1.1, paced 30 s seed 1):
frame p50 3.31 ms of which **engine 5.1%** (0.149 ms), view_gather 73.6% (2.37 ms), view_json 14.7% (0.536 ms), wire 6.6% (0.241 ms). Zero hitches > 16.7 ms. The board's "kicks dominate the engine" is true *inside* the engine (61 µs per distinct kick, kick-bench) but the engine is 1/20 of the frame: the readout pipeline (gather + json + wire) is 95% of the frame and is the only O(seen)-per-frame part.

## The decisive experiment

`view_json` builds a `serde_json::Value` tree every frame (one allocation per field per emitter per frame), then `to_vec` walks it again. Replace with a `#[derive(Serialize)]` view over the existing `View` (borrowed, no tree), serialised straight to bytes. The wire must be byte-identical (serde_json's `json!` map serialises keys sorted without `preserve_order`; the derived struct declares fields in that same sorted order). A unit test pins old-bytes == new-bytes on a hand-built View.

This is the Goldratt *exploit* step on the measured constraint (the readout), not a representation change: same View, same floats, same key order, same bytes.

## Predictions, held out (not tuned on)

1. **Bytes identical.** The unit test `wire_bytes_unchanged` passes: derived serializer output == `to_vec(view_json(..))` on a View with all field kinds present (ints, u8, bool, Option::None/Some, arrays, strings, negative and subnormal-scale floats).
2. **Paced 30 s seed 1 (the player's run):** view_json + wire together drop ≥ 5× (0.78 ms → ≤ 0.16 ms p50); frame_cpu p50 drops from ~3.3 ms to ~2.5–2.8 ms (view_gather becomes ~90% of what remains); p99 drops from ~5.2 ms to ≤ 4.2 ms.
3. **Unpaced m480 (json-dominated profile):** view_json share falls from 50% to < 10%; frame_cpu p50 falls from ~1.6 ms to ≤ 1.0 ms.
4. **The digest at the canonical cut is unchanged** (the view never writes engine state; determinism untouched) — seed 1 digest equals the pre-patch run's.
5. **The constraint does not disappear:** after the exploit, view_gather's per-emitter crossing readout (~19 µs/emitter unpaced, ~61 µs paced at 39 bodies) is the readout's remaining cost and the frame's next constraint. At that cost a sky with 10⁴ visible emitters (a fleet battle) costs 200–600 ms/frame in gather alone: the readout stays the constraint at goal scale until the crossing readout is ~100× cheaper or incremental.

If 2 or 3 fail (the tree was not the json cost), the constraint reading is wrong and the dossier says so.
