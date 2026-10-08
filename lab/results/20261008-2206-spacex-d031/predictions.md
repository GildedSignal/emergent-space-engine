# Predictions (written before the decisive runs)

The decisive runs are the rtf ladder (1, 10, 100) of `xtask universe --bench --seconds 10 --unpaced`
with the H_live probe, default seed and scene. Tuned on: one run at rtf 100 (counts and digest only).
Held out: rtf 1 and 10, all derived rates, the entropy numbers, and the byte-level history cost.

1. **Digest identity holds at every rtf**: the probe is write-only counters; a run with and without
   it gives the same digest (already verified at rtf 100; predicted to hold at 1 and 10).
2. **Per-game-second rates are rtf-invariant**: distinct resolved events per game-second (by kind),
   recompile fraction, and emitted-quanta distribution change only with the scene, not the schedule
   (outcomes are schedule-independent by construction). A rate that moves with rtf would falsify the
   probe's distinctness (the 5 Oct memo artifact) or the engine's schedule independence.
3. **Recompile fraction on distinct kicks > 90%** at every rtf (board claims ~99%; I measured 93.5%
   at rtf 100 before writing this).
4. **Bits per kick-component (entropy of emitted quanta) is 8–20 bits**, i.e. the sigma-delta emits
   real work every kick, not sparse zero-emissions (if it were <2 bits, most kicks would write
   nothing and the kick cadence lever would be weaker than the board thinks).
5. **The catalogue is at churn equilibrium** (inserts ≈ releases, net ≈ 0) and **history
   (retired segments) grows monotonically** — the only unbounded live-memory term the probe sees.
6. Extrapolated to 10⁹ bodies at the plane's scene rates, the per-game-second distinction *count*
   stays ≤ ~10 events/body/game-second; whether the *bytes* (5,189/body today) dwarf the
   distinctions is the idiot index I set out to measure — prediction: the ratio exceeds 100×.
