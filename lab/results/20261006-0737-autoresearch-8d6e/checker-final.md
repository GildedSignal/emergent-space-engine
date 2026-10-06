Working...
Check written. Final state verified: tree restored to clean at f51ddd2 (patch reverse-applied, 0 modified files), only `check.md` added to the run folder, nothing committed.

## Verdict: silver

**Reproduced** (clean tree, patch applied per instructions):
- `replay_digest 50b705f1…` exact and stable over 4 runs; seed-1 55 s dump **byte-identical** to the author's (`cmp`)
- Replay `output_hash 95fafd8590f8f8ee` exact; 14/72 passages = 19% of calls, 87% of bind µs (claimed 86%); compile/readout/µs-per-knot numbers all within noise
- p99 tail: `kick_us_all` 504.6 µs (seed 1) / 1010.7 µs (seed 3) vs claimed 908 — my initial "miss" was reading the made-only `kick_us` key
- `div_word` 1.29×; adversarially strengthened with a 200k-case randomized differential test — 0 mismatches
- Held-out seed 2 (author never reached): digest stable, memo 0%

**Killed by adversarial probe:** the dossier's headline "expected 10× on the p99 tail" from a trajectory-relative compile-out radius. Interleaved edge-scaling on their own harness (±1% spread): compile is linear at ~44 µs/octave, and the deepest passage still costs 636 of 985 µs at the largest valid shrink — −10 octaves refuses at `outer_radius ≤ periapsis`. Ceiling is **1.55×**, not 10×; the residual ~636 µs is near-periapsis quadrature no radius removes. The attribution and scaling law stand; the promised magnitude is ~6× optimistic, which the integrator needs before spending a law decision on it.

Not gold because nothing is adopted and the one magnitude claim doesn't survive; not lead because every measured claim reproduces bit-for-bit and the decomposition (plus the regenerable dump/replay harness) is new against H0210 and the taste log. The gold-making experiment is named in `check.md`: measure the `k·periapsis` / tiered-panel counterfactual on the replay harness.
