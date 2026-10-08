# Predictions (written before the decisive/held-out runs)

Tuning set: seed 1, members 8, sparse (the plane's cost_split ship 14). Machine load is shared and recorded per measurement; the digest is load-independent and is the behaviour gate.

Baseline (this run's branch, shared-load numbers): pure kick 33.7–57 µs; phase split stable: rebind ≈ 66% (compile ≈ 35%, decodes+bookkeeping ≈ 31%), readout/secondaries/tide ≈ 10% each. Baseline digests (canonical cut 3e10 ticks):
- seed 1 m8 sparse: e317b2680d65325981d67a5e5d9e67288e624e6ae6ce0c1ec04c2de3c595a5be
- seed 7 m8 sparse: 74a3a79fcbd75170ea6b67c2803c08998b8b316179ffb461fd217ba40780706e
- seed 23 m32 sparse: 366c42e8547589010ad347be149432bbd217787d5369fe6739c60b7acb858967
- seed 3 m16 dense: d9da1adf53f9eeca4847abfdbb95081ca5e7fde53b3db8e9db39874b22ff6ac8

## Held-out cases (not tuned on): seeds 7, 23/m32 sparse and 3/m16 dense, plus the crate's own test suite

1. **Digests stay bit-identical** on all four configs after every kept change: the changes only replace a recomputation of a pure function of immutable binding fields by its cached first computation (same inputs, same integer path). If any digest moves, the bit-identity claim is wrong and everything is reverted.
2. **The absolute µs saved per kick is roughly seed-independent** (the removed work is a fixed number of decodes per kick, not a seed-dependent amount): seed 7 and seed 23 see about the same absolute gain as seed 1; the *relative* gain on m32 is smaller (more secondaries per kick).
3. **Phase split after round 1+2**: rebind loses ~2 decodes (uncontended ≈ 6–7 µs, shared-load ≈ 10–11 µs); readout/secondaries/tide unchanged in round 1–2.
4. **Whole-universe settle per-item improves less than the pure kick** (universe-side overhead: apply, queue, root-position cache, fleet battle are untouched), so expect roughly the kick fraction of the item cost: a few tens of percent at most, not a 10× on the settle.
5. If a round gains < 10% on the pure-kick metric three rounds in a row, the loop stops (lens rule).

Kill criterion per change: any digest difference, or a slower measurement. A control: the unmodified build's binary (kick_bench_base) is re-run back-to-back with each candidate to cancel load drift.
