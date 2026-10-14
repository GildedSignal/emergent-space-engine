# Predictions — 20261014-2130-second-20261014-2012-system-a669-eb2d

Written before the decisive runs (patch built, baselines flown, no dial run yet).
The dial is `ES_KEY_BITS=shape_bits,scale_bits` on the live `OrbitKey`
(`k` = shape, Q48 mantissa of 1/(1+e), quantized as `2k−1`; `periapsis` = scale word,
62-bit Scalar significand). The checker's correction is built in: the L-like word
(periapsis) needs ~2^15–2^16 of coarsening for a run of ~107, not 2^13.

- **P1 (neutrality).** Patched-default (no `ES_KEY_BITS`): the gate compares exact keys,
  so `ladder_digest` (wave, crossing) and `frame_digest` digests are bit-identical to the
  pristine tree's, and the reuse counter stays ≈ 0 (memo.rs: exact keys never recur on
  distinct kicks). If any digest moves, the wiring is not a pure memo — stop.
- **P2 (the flip run).** At `ES_KEY_BITS=48,16` (periapsis kept at 16 significant bits ≈
  2^15–2^16 relative coarsening, shape exact) on N=3000 through the wave: reuse fraction
  of cycle fits ≥ 0.9, compiles/kick ≤ 0.1 (a669's per-kick |ΔL|/L p50 2.1e-7 ≈ 2^-22.4
  predicts a run of ~2^7–2^8 ≈ 100–200 kicks). Shape at 33 bits (`33,16`) adds little:
  reuse within 1.15× of the scale-only dial (the shape word drifts slower than the scale
  word). If reuse < 0.5 at 16 scale bits, the live key's periapsis drifts faster than the
  replica's L and the dial's operating point moves further out.
- **P3 (the map holds).** Dial-on vs default: kicks equal (the kick clock is the doll's,
  not the key's); encounters within ~1%; contacts equal. A moving encounter count is the
  dial leaking into decisions through the readout — report it as the cost.
- **P4 (exactness, the B12-type check).** `jacobi 6 100 6` at `ES_KEY_BITS=48,16`:
  worst per-ship error within ~30× of the baseline's ~5e-6 (the between-events readout
  drift grows by the coarsening and is re-anchored at each flip). Beyond ~100× the dial
  is not free at this grain and the run says so.
- **P5 (the deleted compile stream).** The through-wave flight's wall time drops ≥ 1.2×
  at the dial (compile ≈ 21 µs of the ≈ 38 µs composed kick, b29a), and compiles/kick is
  the measured deletion factor to compose onto the wave's CPU (break 1).
