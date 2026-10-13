# Predictions (written before wiring cos4 into `quad`)

Baseline measured on this box (85-key grid, p ∈ 2^2..2^18, e ∈ {0,.2,.5,.8,.9}):
shipped cos 41.9–42.5 ns (serial 13-factor chain); unrolled alone 41.3–41.5 ns (loop
overhead ~nil — the chain is latency-bound); interleaved4 14.09–14.12 ns/cos (2.97–3.01×);
compile best 34.44 µs/key, shape digest b5ef99aabce2f641.

- **P1 (identity):** wiring `cos4` into `quad` keeps every compile bit-identical:
  shape digest stays b5ef99aabce2f641 on the same grid, and the frozen-oracle suite
  passes unchanged. Each chain computes the identical floored products; the sums
  accumulate in the same order; per-node error paths fire in the same order.
- **P2 (gain):** from 7d2b's node split (cos 24% of the ~320 ns node) and ~170
  cos/compile implied by the division census, the serial-cos share of my 34.4 µs
  compile is ~20%; interleaving 4 chains cuts the primitive 3.0×, so I expect the
  compile to drop **−8% to −15%** (to ~29.5–31.7 µs/key). If it drops materially
  less (<4%), the walk's other node work already hides cos latency and the serial
  share was overstated — that would refute the transfer of the primitive ratio.
- **P3 (held-out, not tuned on):** Kerr compiles (kerr.rs is a different walk with
  its own cos sites — untouched by this patch) stay identical; the held-out check is
  `cargo test -p emergent-space` (frozen oracles) plus the universe plane digest,
  neither of which I have measured yet on this box.
- **P4 (what would make it wrong):** any digest or test flip means the interleaved
  chain is not computing the same floors (e.g. an x² overflow path in u64 that the
  shipped i128 square handles) — the fuzz covers [0, π] uniformly at 2M+65k points
  including corners, so a flip would point at operand shapes outside [0, π] Q61.
