# Predictions (written before the decisive run)

Baseline (this machine, x86-4790, load ~0.8): kick bench seed 1, 55 s replay →
median kick 68.6 µs (dump-polluted run) / ~45 µs (15 s run), p99 ~908 µs; 72 `bind` calls captured.
Attribution from the replay (`prof/`): passages are 14/72 binds but ~86% of total bind µs
(330–1500 µs each, compile ≈ 300–590 µs of it); cycle binds 13–25 µs (compile 3.4–35 µs, ~0.6 µs/knot);
cycle readout 3.2 µs, passage readout 7.3 µs. The bench median is dominated by ~10 secondary
tube readouts per kick plus one bind.

## Change under test
Replace the three unguarded 128-bit divisions per `fast_quad` node (`g`, `g1`, `ratio`) with
`div_word` (exact 128/64 Knuth division, same truncated quotient). Micro-bench: 1.32× per division
(divbench, black_box'd operands).

## Held-out cases (not tuned on)
- Dump replay bit-identity: every `bind` output (tube, residual, turn, orbit state) must hash
  identically before/after on all 72 captured inputs, including the 14 passages.
- Kick bench `replay_digest` must be byte-identical on seeds 1, 2 and 3 (55 s).
- `cargo test -p emergent-space` (quadrature tests incl.) must pass unchanged.

## Predictions
1. Passage-compile inputs in the replay drop by 8–18% (divisions ≈ 30–50% of fast_quad node cost;
   only 3 of 4 divisions swap; `rt` stays).
2. Cycle binds move < 5% (they ride `node()`/Scalar paths already using div_word).
3. Bench median moves < 3% (median is secondary-readout dominated); bench p99 drops 5–15% if the
   p99 kicks are passage rebinds (seed 3 showed p99 908 µs — a passage).
4. Digests: identical everywhere (the swap is value-exact by Knuth's algorithm contract).

If (1) lands < 8% the change is below the lens's 10% bar → revert and report as a lead.
