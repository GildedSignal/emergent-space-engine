# Predictions — written before the decisive run

Run id 20261009-2348-components-42e6. Component: the body store (storage seam, `BodyStore`/`Binding`).
Question: what is the information-theoretic floor of a live body's state on the plane, how far is
today's store above it (idiot index), and what is H_live — the bits of new distinguishing state per
body per game-second — that decide whether 10⁹ bodies fit in 8 GB?

Decisive run (not tuned on): `hlive --seconds 10 --rtf 100 --seed 1` (≈1000 game-seconds of the
plane's own scene, seed 1, 48 fleet members, no player input). Calibration run before this file:
2 game-seconds at rtf 1 (28 kicks, 28 bodies).

1. **Kick rate** stays ~0.5 kicks/body/game-second (28 bodies → ~14k kicks over 1000 s).
2. **Shapes:** ~1 new exact shape per kick (exact memo hit ≈ 0, as H0213 found); the quantized
   12+12 memo hits ≥ 90%. So the catalogue is a per-body cache, not shared structure.
3. **Field widths (order-0, over the population):** periapsis_angle near uniform (31–32 bits);
   residual position < 2^20 quanta and velocity < 2^16 quanta per axis (ships), planets larger;
   turn a,b < 2^35; dv spans > 40 bits across kinds (planets vs ships differ ≥ 2⁴ in magnitude).
4. **Floor of one live body** (packed, derivations shared): 20–40 bytes. Today's store is
   BodyRec 448 B + Arc&lt;Entry&gt; 224 B ≈ 672 B → **idiot index 17–34×**, the catalogue excluded.
5. **What actually grows per kick** is not the live state (a kick replaces the binding; the
   remainder is carried, bounded): it is (a) the kept history Segment (192 B) per kick and (b) one
   catalogue entry per rebind (freed on the next rebind). Prediction: H_live as a *net live-store*
   rate is ≈ 0 in steady state; as a *history/replay-stream* rate it is ~100–300 bits/kick, so a
   stored exact replay at 10⁹ bodies saturates 4 GiB in under one game-minute → replays must be
   recomputed from a decision log, never stored as state.
6. **Fleet members** (leavers) join during the run (kind_ship count > 23); if they never appear
   without player input, the rate claim covers the made bodies only and says so.

Kill criteria for the measurement: if the census (distinct pending kicks resolved) diverges from
the engine's own `stats` events by more than 2× (harness bug), or the 52 s wall guard trips before
the full span (sample too short), rate claims are VOID. A codec that does not round-trip the dumped
integers bit-for-bit is VOID as a floor design.
