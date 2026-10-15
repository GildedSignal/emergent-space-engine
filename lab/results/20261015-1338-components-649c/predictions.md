# Predictions (written before the decisive grid)

Cases not tuned on: the grid below extends the smoked instrument (N=10³ coast, 300 and 1000 frames; one rtf 10⁴ probe) to N=10⁴/10⁵ and burn levels 8 and 15. Tuned on: N=10³ coast only.

The instrument: `view_floor`, one flight per arm, the page's own loop order (`gather_cached`, then keys, then `frame_to`), rtf 100, 12 ms engine budget. Price = per-frame gather wall, readouts/emitter; floor = the free-run error of a row whose emission geometry is frozen at one frame while the observer's state is taken fresh (aberration and shift recomputed observer-side, `view.rs`'s own closed form).

1. **Scaling of the price (N=10⁴, 10⁵, coast):** gather is linear in N, 17–21 µs/body on this box at every N; readouts/emitter 1.4–1.8.
2. **The crawl:** at 10⁵ the gather owns ≥ 97% of the flown frame (engine p50 ≤ 0.5 ms) and the achieved rtf is ≤ 1.5 — this is the rtf-0.7/~2 s-frame crawl the nladder page found, priced.
3. **Burn 8 does not stale the crossings:** readouts/emitter ≤ 2.2 and µs/body ≤ 1.3× coast (the observer's per-frame displacement at L8 stays inside Newton's bracket); the far rows remain bit-frozen (≤ 1e-12 rad) for ≥ 100 frames of the burn — a burn changes only the observer side, which the closed form takes fresh.
4. **Burn 15:** readouts/emitter ≤ 3.0; far rows still bit-frozen ≥ 60 frames (the emission quantum is the emitter's, not the observer's). If far rows depart the map half-pixel within < 100 frames under either burn, the observer-side claim is wrong and the burn really is an O(visible) re-read (view open direction 3 stands as a cost).
5. **Near rows are the per-frame set:** near-ship and local rows (≤ 250 light-s) depart within ≤ 2 frames at every burn level (drift ~1e-2 rad/frame), and their count stays ~300–340 at every N (the belt adds only far rows).
6. **Far-row horizon:** p99 horizon at the map half-pixel ≥ 5,000 frames at 10⁴ and 10⁵ (the drift rate is set by belt distance and orbital speed, both N-independent).

Kill criteria: (a) far rows departing under burn (< 100 frames) kills the observer-side deletion and bounds the row-set deletion by the burn; (b) µs/body at 10⁵ < 5 would mean the crawl is not the gather — the dossier would then report the crawl unpriced by this instrument.
