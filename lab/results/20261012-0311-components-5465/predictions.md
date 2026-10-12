# Predictions (written before the census run; not tuned on)

Component: the individual body's store on the plane (`PlainBodies`), against the law's own
16-byte `Tube` packet (`crates/space/src/tube.rs`) and the shared catalogue (`bind.rs`).

Decisive experiment: `cargo test --release -p emergent-universe --test store_census -- --nocapture`
(600 frames of the real plane, same driver as `tests/memo.rs`).

## Predicted (P) vs held-out (H)

- **P1** The plane's `bytes_per_body` is between 300 and 2000 B. (BodyRec is a fat record with a
  `Vec` plan, `Option`s and counters; the trajectory's compiled knots are charged per body.)
- **P2** The compiled entry dominates: knots are ≥ 50% of all per-body bytes.
- **P3** Distinct live `Arc<Entry>` ≈ number of alive bodies (the exact key never recurs, so the
  catalogue shares almost nothing at steady state; `catalogue_live` ≈ alive count).
- **P4** The law's quantized 44-bit cell reproduces `tests/memo.rs`: hit > 0.9, < 250 distinct cells.
- **P5** `Knot` = 88 B, `Scalar` = 16 B, `BodyRec` ≥ 120 B.
- **P6** plan length ≤ 4 for ≥ 90% of live bodies (an inline array would delete the Vec).
- **P7** `carry` (sigma-delta) is nonzero for ≥ half the live ships; `ext` for ≤ 3 bodies (root doll);
  `thrust` for exactly 1 (the player); `proper` nonzero for all alive.
- **P8** Idiot index vs the 16-B tube: ≥ 25×.

## Held-out (no tuning, checked once)

- **H1** The census per-body sum (fat + binding-beyond-tube + plan) differs from the plane's
  `bytes_per_body` by ≤ 15% + history segments (the plane also counts history and counts shared
  knots per body; if the two disagree by more, the plane's own accounting is miscounting sharing).
- **H2** After 600 frames the store reaches steady state: `catalogue_live` stops growing between
  the last 100 frames (rebinds recycle slots). If it still grows, the catalogue is a leak and the
  memory risk is the kick stream, not the packet.

## Kill criterion for my claim

If `bytes_per_body` ≤ 128 B (within 8× of the tube floor), the individual store is already
near-floor: my claim ("the per-body store is a top idiot index on bottleneck 5") is killed, and
the dossier reports the floor side (catalogue/program) instead.
