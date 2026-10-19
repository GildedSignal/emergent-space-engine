# Predictions (written before the decisive census runs)

Instrument: `cargo run --release -p emergent-universe --example belt_cells -- <seed> <extra>`
(shipped `ladder_ship` population, shipped `MemoCode` cell function, shipped `Orbit::compile`;
weak-branch shape id `(1<<44) | low 17 bits` replicated from `orbit.rs::shape_bits`).

Cases not tuned on: seed 7, extra = 10^6, and every band below.

- **P1 (saturation):** distinct belt cells at extra = 10^5 seed 1 < 3,000 (Fermi: the belt's
  shape identity on the weak branch is the quantized gap = f(e) only; e is Rayleigh(0.07) on
  [0, 0.4], an 11-bit fraction cell is ~2^-12 of the gap significand ~ 1.2e-4 in e, so the
  support holds ~600 cells plus tail).
- **P2 (sub-linear):** cells(10^6) / cells(10^5) < 1.5 at seed 1.
- **P3 (error):** max served period error over all belt members <= 2^-10, and advance <= 2^-10
  (the plane's 11+11 numbers were 6.8e-4 / 1.3e-4; the belt is weaker and its e-band narrower,
  so I expect the same order or better).
- **P4 (no exact sharing):** exact distinct ShapeKeys ~= extra (within 1%): sharing exists only
  through quantization, never exactly.
- **P5 (locals contrast):** the ~300 locals (strong branch) land ~1 cell per body: the belt is
  the sharing population, the plane's is not.
- **P6 (deletion):** standing table bytes cells x knots x 88 B against per-body knots x 88 B
  (share_delete) >= 100x at 10^5.
- **P7 (no comb):** max_share / mean_share < 8 (occupancy tracks the smooth Rayleigh density of
  e; no concentration class).
- **P8 (knots):** knot_mismatch = 0 (B9-class: one cell, one knot count).

Kill criteria: P1 or P6 failing kills the "the belt's standing shape wall deletes under the
shipped 11+11 cell" claim; P3 failing above 2^-9 kills the serve as B1/B2-legal without a width
ladder step.
