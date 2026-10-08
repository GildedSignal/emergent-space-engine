# Predictions (written before the decisive runs)

The component: the storage layer's commit path (retired segments + BodyRec rewrites), the plane as
shipped. The floor: the live distinguishing information of a committed kick is its `dv` pair (the
new binding is re-derived by `rebind`; the kind/window come from the schedule). The decisive runs:
`xtask universe --h-live --rtf {1e4,1e5} --seed {1,7} --members 400 --seconds ≤ 40`, entropy
measured off-line on the `dv` streams.

Cases not tuned on, and what I expect there:

- **P1 (bits per kick).** Order-0 joint entropy H(dv0,dv1) of ship kicks ≤ 24 bits, and conditioned
  on the body ≤ 18 bits. Rationale: orbit-averaged kicks in quanta of the velocity exponent are
  small integers; most of the pair's range is never used.
- **P2 (bytes per kick vs floor).** The persistent write per kick (one `Segment` + the `BodyRec`
  rewrite) is ≥ 120 B, i.e. ≥ 40× the floor at H ≈ 20 bits (2.5 B).
- **P3 (no reabsorption).** The flight loop never prunes: history segments accumulate ~1:1 with
  kicks, so live store bytes grow linearly in game time at the measured kick rate × `Segment` size.
- **P4 (mix).** Kicks and boundaries together ≥ 85% of committed events; kicks stay below 60% (the
  smoke at rtf 30 showed 46% kicks / 41% boundaries; at 1e4–1e5 the mix moves by ≤ 15 points).
- **P5 (pace and seed independence, held out).** Bits per kick at rtf 1e5 within ±25% of rtf 1e4,
  and seed 7 within ±25% of seed 1: the kick's content is set by the law's quantization, not the
  pace or the seed.
- **P6 (the law's model).** docs/law.md's allocator model "+62 bits per kick" is ≥ 2× the measured
  order-0 H per kick (i.e. the model over-provisions the scar budget).

Instrument checks (not predictions): the recorder leaves every digest untouched (kick-bench
digests bit-identical pristine vs patched; `--h-live` repeats bit-identical); the entropy tool
gives ~0 bits on a constant stream and loses the order-1 structure of a shuffled stream while
keeping order-0.
