# Predictions — run 20261008-0338-second-20261008-0234-spacex-0083-492f (second author)

The named gold experiment from the silver check: build the minimal jet (stored exact shape +
derivative-offset tables + re-anchor at the accumulated-drift bound) and measure the jetted kick
end-to-end against the exact rebind; the cheaper prelude is the offset-error growth on this scene.
Built additively (`crates/space/src/orbit/jet.rs` + `Rebinding::from_state_with`, xtask `--jet2`);
the shipped paths are untouched and the parity control asserts `from_state_with(Orbit::compile)`
≡ `from_state` bit for bit every 16th kick. Debug smoke runs (2 s) fixed a zip misalignment and a
factor-2 in the correction; the numbers below are Fermi estimates from the corrected smoke, not
fits to it. Held-out: the 10 s/30 s windows, seeds 3 and 7, and the timing ratios have not been
recorded.

Baseline (not a prediction): the shipped kick ≈ 97 µs median, exact rebind ≈ 76 µs, compile 61 µs
(run 0234, checker-reproduced). My smoke (2 s): anchor pricing ≈ 28 µs (one extra quadrature
sweep, ~46% of a compile), C ≈ 4.4, median per-kick drift step ≈ 2.2×10⁻⁸.

- **P1 (rebind speedup).** The jetted rebind (`from_state_with` + correction + `from_shape` +
  decode/residual, anchors priced inside) has median ≤ 35 µs against the exact rebind's ~76 µs:
  ≥ 2× on the rebind, the part the previous run priced at 78% of the kick.
- **P2 (end-to-end resolver).** readout + forces + jetted rebind ≤ 45 µs median against the
  shipped full kick's ~97 µs: ≥ 2.1× on the whole resolver scope, without touching cadence,
  forces or the readout.
- **P3 (the error law, on scene).** The jetted trajectory's period error against the exact
  rebind follows error ≈ C·(Δgap/gap)² with C in [1, 50] (median over jetted reads), and at the
  largest drift any body reaches in a 30 s window (≥ 10⁻⁷) the period, proper-period and
  radius errors all stay below the law's 10⁻⁶ floor — i.e. no re-anchor fires in-window and
  none is needed. If the error at 30 s crosses 10⁻⁶, the re-anchor cadence implied by the
  measured C must be reported and the jet's price re-rated accordingly.
- **P4 (controls).** Parity control mismatches = 0; refused = 0; the universe digest at cut
  equals the shipped bench's (13cfe88b… at 10 s, seed 1), proving nothing fed the universe;
  `--kick-bench` on the patched tree reproduces its shipped record (digest and kick median).
- **P5 (jet population).** All 45 sampled bodies anchor at their record's compiled shape
  (weak-branch cycles; 0 fresh-compile anchors, 0 strong-field fallbacks); passages stay ≈ 3%
  of kicks (compiled, as the law keeps them); anchor pricing ≈ 20–40 µs each; with the re-anchor
  bound at 1.5×10⁻⁴ (from C's p90 ≈ 40: error ≤ 40·(1.5×10⁻⁴)² ≈ 9×10⁻⁷ < 10⁻⁶) no re-anchor
  fires in any ≤ 55 s window, because the scene's correlated drift (~2.2×10⁻⁸ per kick, median)
  needs ~7×10³ kicks to reach the bound — the amortized re-anchor price is then ~0.01 µs/kick
  (compile 61 µs + pricing 28 µs over ~6800 kicks), reported as arithmetic, not as a fired event.
- **P6 (B8 determinism).** Two identical 10 s runs give identical counters (kicks, jetted,
  anchors, passages) and error medians equal to < 10⁻¹² relative difference (all-integer
  arithmetic; f64 only in the report).
- **Adversarial (held out).** Seeds 3 and 7: same structure — C within one order of magnitude
  of seed 1's, rebind speedup ≥ 2×, errors below the floor throughout.

Kill criteria (written before the runs): jetted rebind ≥ 0.6× the exact rebind (the jet buys
< 1.7× on the dominant part and the 22 µs ceiling is dead as a price); or any parity-control
mismatch (the harness, not the jet, is then broken); or the 30 s error crossing 10⁻⁶ with a
re-anchor cadence under ~100 kicks (the jet degenerates to compile-per-few-kicks); or the digest
differing from the shipped bench's (the universe was fed — VOID).
